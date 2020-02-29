import socket
import sys


def main():
    tshostname = ''
    local_table = {}
    with open("PROJI-DNSRS.txt", "r") as f:
        lines = f.readlines()
        print(lines)
        for line in lines:
            entry = line.split()
            if(entry[2]=='NS'):
                tshostname=str(entry[0])
            local_table[str(entry[0]).lower()] = entry
    f.close()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Unable to create socket\n")
        exit()
    server_binding = ('', int(sys.argv[1]))
    s.bind(server_binding)
    s.listen(5)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    try:
        while True:
            c, addr = s.accept()
            print("[S]: Got a connection request from a client at {}".format(addr))
            from_client = ''
            while True:
                data = c.recv(200)
                if not data:
                    break
                from_client += data.decode('utf-8').strip()
                print("String created from receiving " + from_client)
                c.send(lookup(from_client, local_table,tshostname).encode('utf-8'))
                print('This is what lookup is sending back to the client ' +lookup(from_client,local_table,tshostname))
                from_client = ''
    except KeyboardInterrupt:
        s.close();
        return


def lookup(msg, local_table,tshostname):
    key = str(msg).lower()
    if key in local_table:
        print("got a hit")
        message = str(key + ' ' + local_table[key][1] + ' ' + local_table[key][2])
    else:
        message = str(tshostname + ' ' +local_table[tshostname][1] + ' ' + local_table[tshostname][2])
    return message

if __name__ == "__main__":
    main()