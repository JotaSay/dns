import socket
import sys


def main():
    if (len(sys.argv) != 4):
        print("Error too many or little arguments entered in the command line")
        exit()
    print("Welcome to our DNS look up project")
    """This is where we read all the lines and perform each lookup accordingly"""
    File = open(r"PROJI-HNS.txt", "r")
    lines = File.readlines()
    client(lines)
    File.close()


def client(lines):
    rshost = str(sys.argv[1])
    rsport = int(sys.argv[2])
    tsport = int(sys.argv[3])
    created = False
    # attempt to make both client sockets to connect to our two DNS
    try:
        csrs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        csts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Both client sockets successfully created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server

    # connect to the server on local machine
    server_bindingrs = (rshost, rsport)

    csrs.connect(server_bindingrs)
    f = open("RESOLVED.txt",'w')
    """connected to the rs server now we can begin to send our queries"""
    for query in lines:
        """send the query to rs"""
        csrs.sendall(query.encode('utf-8'))
        # Receive data from the server
        rsdata = csrs.recv(205)
        """Now that we received the data we must decide if we need to print it or contact the ts server"""
        print("[C]: Data received from server: {}".format(rsdata.decode('utf-8')))
        readable = rsdata.decode('utf-8').split()
        if str(readable[2]) == "NS":
            """creating connection to ts now that we are given the host name of ts"""
            if not created:
                hostts = str(readable[0]);
                """got ip below in case we need if for the socket.connect instead"""
                ipts = socket.gethostbyname(hostts)
                server_bindingts = (hostts, tsport)
                csts.connect(server_bindingts)
                created = True
            """send the same query to ts server now"""
            csts.sendall(query)
            """write what we receive into the server"""
            tsdata = csts.recv(200)
            readablets = str(tsdata.decode('utf-8'))
            f.write(str(readablets+'\n'))

        else:
            """It successfully got the lookup and we just have to print the string out"""
            f.write(str(readable[0]+' '+readable[1]+' '+readable[2]+'\n'))

    # close the client socket
    csts.close()
    csrs.close()
    exit()


if __name__ == "__main__":
    main()
