"""Server that will hold our data structure"""
import socket
import sys


def main():
    """This part just create the data structure that I'm going to use for our lookups"""
    lookup = {}
    File = open(r"PROJ1-DNSTS.txt", "Access_Mode")
    lines = File.readlines()
    for line in lines:
        key = line.split()
        lookup[key[0]] = key
    server()


"""Here we just establish the server code"""


def server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server socket created\n")

    except socket.error as e:
        print("Unable to create socket\n")
    bind = ('', sys.argv[1])
    s.bind(bind)
    s.listen(3)
    host = socket.gethostname()
    localhost_ip = socket.gethostbyname(host)
    print("Server host name is {}".format(host))
    print("Server IP address is {}".format(localhost_ip))

