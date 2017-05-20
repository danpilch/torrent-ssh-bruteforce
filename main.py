#!/usr/bin/env python

from torrent.torrentscanner import TorrentScanner
import argparse



def main():
    parser = argparse.ArgumentParser(
        description="Torrent peer analysis"
    )

    parser.add_argument(
       '--torrent', 
        '-t', 
        help="Torrent file to grab peers from", 
        required=True, 
    )
    
    parser.add_argument(
       '--attempts', 
        '-a', 
        type=int,
        help="Number of attempts to collect peers", 
        default=5
    )
    
    parser.add_argument(
       '--duration', 
        '-d',
        type=int,
        help="Duration in seconds to collect peers", 
        default=5
    )

    args = parser.parse_args()


    torrent = TorrentScanner(
        torrent_file=args.torrent,
        collection_attempts=args.attempts,
        collection_duration=args.duration
    )

    torrent.get_peers_from_swarm()
    torrent.find_open_ports()
    torrent.check_for_weak_auth()


if __name__ == "__main__":
    main()
