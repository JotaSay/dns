"""Server that will hold our data structure"""
import socket
import sys


def main():
    """This part just create the data structure that I'm going to use for our lookups"""
    lookupt = {}
    File = open(r"PROJI-DNSTS.txt", 'r')
    lines = File.readlines()
    for line in lines:
        key = line.split()
        lookupt[str(key[0]).lower()] = key
    server(lookupt)
    File.close()


"""Here we just establish the server code"""


def server(lookupt):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server socket created\n")

    except socket.error as e:
        print("Unable to create socket\n")
    bind = ('', int(sys.argv[1]))
    s.bind(bind)
    host = socket.gethostname()
    localhost_ip = socket.gethostbyname(host)
    print("Server host name is {}".format(host))
    print("Server IP address is {}".format(localhost_ip))
    s.listen(3)
    try:
        while True:
            conn, addr = s.accept()
            from_client = ''
            while True:
                data = conn.recv(200)
                if not data: break
                from_client += data.decode('utf-8').strip()
                print from_client
                """This is what where we look into our code and see what we can do"""
                conn.send(lookup(from_client.decode('utf-8'), lookupt))
                from_client=''
    except KeyboardInterrupt:
        s.close()
        return



def lookup(message, table):
    key = str(message).lower()
    if key in table:
        message = str(key+' '+table[key][1]+' '+table[key][2])
    else:
        message = (str(message)+' '+"- Error:HOST NOT FOUND")
    return message

if __name__ == "__main__":
    main()