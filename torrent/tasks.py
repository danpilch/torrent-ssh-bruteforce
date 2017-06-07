from celery import Celery
import sh


app = Celery('tasks', backend='rpc://', broker='amqp://guest@172.17.0.2//')

def ssh_interact(line, stdin, stdout):
    pass

@app.task()
def check_open_port(ip, port=22):
    try:
        check = sh.grep(sh.nmap("-p{0}".format(port), ip, _piped=True), "open", _timeout=3)
        if "open" in check.stdout:
            return ip
        else:
            return None
    except Exception as e:
        return None

@app.task()
def check_available_auth_methods(ip):
    try:
        check = sh.ssh("-o", "PreferredAuthentications=none", "-o", "StrictHostKeyChecking=no", "root@{0}".format(ip), _out=ssh_interact, _out_bufsize=0, _tty_in=True, _ok_code=[255], _timeout=3)
        if "password" in check.stderr:
            return ip
        else:
            return None
    except sh.TimeoutException:
        return None

@app.task()
def bruteforce_ssh(ip, password):
    try:
        check = sh.ssh()
    except Exception as e:
        return None


