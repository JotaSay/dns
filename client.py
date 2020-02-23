import socket
import sys

def main():
    if(len(sys.argv)!=4):
        print("Error too many or little arguments entered in the command line")
        exit()
    print("Welcome to our DNS look up project")
    """This is where we read all the lines and perform each lookup accordingly"""
    File = open(r"PROJ1-HNS.txt", "Access_Mode")
    lines = File.readlines()
    client(lines)

def client(lines):
    rshost = sys.argv[1]
    rsport = sys.argv[2]
    tsport = sys.argv[3]
    #attempt to make both client sockets to connect to our two DNS
    try:
        csrs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        csts = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Both client sockets succesfully created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

  # Define the port on which you want to connect to the server
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_bindingrs = (localhost_addr, int(rsport))
    server_bindingts = (localhost_addr,int(tsport))

    csrs.connect(server_bindingrs)
    csts.connect(server_bindingts)

    # Receive data from the server
    data_from_server=csrs.recv(100)
    """Now that we received the data we must decide if we need to print it or contact the ts server"""
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
    cs.close()
    exit()
