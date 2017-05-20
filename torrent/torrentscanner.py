from celery import group
from sh import ssh
from tasks import check_available_auth_methods, check_open_port
import libtorrent
import time
import sys


class TorrentScanner(object):
    def __init__(self, torrent_file, collection_attempts, collection_duration):
        self.torrent_file = torrent_file
        self.max_peer_collection_attempts = collection_attempts
        self.peer_collection_seconds = collection_duration
        self.torrent_ip_list = []
        self.open_ip_list = []

    def get_peers_from_swarm(self): 
        session = libtorrent.session()
        session.listen_on(6881, 6891)

        info = libtorrent.torrent_info(self.torrent_file)
        handler = session.add_torrent({'ti': info, 'save_path': './poc', 'connections_limit': '1000', 'num_want': '2000'})
        handler.set_download_limit(2)
        handler.set_upload_limit(2)

        print 'starting: ', handler.name()

        for i in xrange(0, self.max_peer_collection_attempts):
           status = handler.status()
        
           time.sleep(self.peer_collection_seconds)
           for i in handler.get_peer_info():
               if i.ip[0] not in self.torrent_ip_list:
                   self.torrent_ip_list.append(i.ip[0])
        
        print "\npeers collected: ", len(self.torrent_ip_list)

    def cleanup_list(self, l):
        return [x for x in l if x is not None]

    def find_open_ports(self):
        job_list = []
        if len(self.torrent_ip_list) > 0:
            for ip in self.torrent_ip_list:
                job_list.append(check_open_port.s(ip))

            jobs = group(job_list)
            results = jobs.apply_async()
            self.open_ip_list = self.cleanup_list(results.join())

    def check_for_weak_auth(self):
        job_list = []
        for ip in self.open_ip_list:
            job_list.append(check_available_auth_methods.s(ip))

        jobs = group(job_list)
        results = jobs.apply_async()
        test = self.cleanup_list(results.join())

    def password_bruteforce(self):
        pass
