import socket
import sys


def main():
    local_table = {}
    with open("PROJI-DNSRS.txt", "r") as f:
        for line in f:
            entry = line.split()
            local_table[entry[0]] = entry
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Unable to create socket\n")
        exit()
    server_binding = ('', sys.argv[1])
    s.bind(server_binding)
    s.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    while True:
        csockid, addr = s.accppt()
        print("[S]: Got a connection request from a client at {}".format(addr))
        from_client = ''
        while True:
            data = csockid.recv(8)
            if not data:
                break
            from_client += data
            print(from_client)
            csockid.send(lookup(from_client.decode('utf-8'), local_table))
    s.close()
    f.close()

def lookup(msg, local_table):
    key = msg.split()[0]
    if key in local_table:
        msg = str(key + ' ' + msg[key][1] + ' ' + msg[key][2])
    else:
        msg = (key + " - NS")
    return msg

