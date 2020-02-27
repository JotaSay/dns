"""Server that will hold our data structure"""
import socket
import sys


def main():
    """This part just create the data structure that I'm going to use for our lookups"""
    lookupt = {}
    File = open(r"PROJ1-DNSTS.txt", "Access_Mode")
    lines = File.readlines()
    for line in lines:
        key = line.split()
        lookup[key[0]] = key
    server(lookupt)
    File.close()


"""Here we just establish the server code"""


def server(lookupt):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server socket created\n")

    except socket.error as e:
        print("Unable to create socket\n")
    bind = ('', sys.argv[1])
    s.bind(bind)
    host = socket.gethostname()
    localhost_ip = socket.gethostbyname(host)
    print("Server host name is {}".format(host))
    print("Server IP address is {}".format(localhost_ip))
    s.listen(3)
    host = socket.gethostname()
    localhost_ip = socket.gethostbyname()
    while True:
        conn, addr = s.accept()
        from_client = ''
        while True:
            data = conn.recv(8)
            if not data: break
            from_client += data
            print(from_client)
            """This is what where we look into our code and see what we can do"""
            conn.send(lookup(from_client.decode('utf-8'), lookupt).encode('utf-8'))
        s.close()


def lookup(message, table):
    key = message.split()[0]
    if key in table:
        message = str(key+''+message[key][1]+''+message[key[2]])
    else:
        message = (key+''+"- Error:HOST NOT FOUND")
    return message
