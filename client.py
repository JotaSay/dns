import socket
import sys


def main():
    if(len(sys.argv)!=4):
        print("Error too many or little arguments entered in the command line")
        exit()
    print("Welcome to our DNS look up project")
    """This is where we read all the lines and perform each lookup accordingly"""
    File = open(r"PROJI-HNS.txt", "Access_Mode")
    lines = File.readlines()
    client(lines)
    File.close()


def client(lines):
    rshost = sys.argv[1]
    rsport = sys.argv[2]
    tsport = sys.argv[3]
    created = False
    #attempt to make both client sockets to connect to our two DNS
    try:
        csrs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        csts = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Both client sockets succesfully created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

  # Define the port on which you want to connect to the server

    # connect to the server on local machine
    server_bindingrs = (rshost, int(rsport))

    csrs.connect(server_bindingrs)

    f = open("RESOLVED.txt", 'a')
    """connected to the rs server now we can begin to send our queries"""
    for query in lines:
        """send the query to rs"""
        csrs.sendall(query.encode('utf-8'))
        # Receive data from the server
        rsdata =csrs.recv(100)
        """Now that we received the data we must decide if we need to print it or contact the ts server"""
        print("[C]: Data received from server: {}".format(rsdata.decode('utf-8')))
        readable = rsdata.decode('utf-8').split()
        if str(readable[2]) == "NS":
            """creating connection to ts now that we are given the host name of ts"""
            if not created:
                server_bindingts = (readable[0], int(tsport))
                csts.connect(server_bindingts)
                created = True
            """send the same query to ts server now"""
            csts.sendall(query.encode('utf-8'))
            tsdata = csts.recv(100)
            print("[C]: Data received from server: {}".format(tsdata.decode('utf-8')))
            readable2 = tsdata.decode('utf-8').split()
            if str(readable2[2]) == "NS":
                f.write("{} - Error:HOST NOT FOUND\n".format(str(readable[0])))
            else:
                f.write("{} {} {}\n".format(str(readable2[0]), str(readable2[1]), str(readable2[2])))
        else:
            """It successfully got the lookup and we just have to print the string out"""
            f.write("{} {} {}\n".format(str(readable[0]), str(readable[1]), str(readable[2])))

    # close the client socket
    csrs.close()
    csts.close()
    f.close()
    exit()
