import socket
import sys
import traceback

if __name__=="__main__":
    address=('127.0.0.1', 5555)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            msg = raw_input()
            if not msg:
                break
            client.sendto(msg, address)
            print "[client] send :" + msg + ", to :" + str(address)
            (response, server) = client.recvfrom(65535)
            print "[client]receive:" + response + ", from:" + str(server) 
    except:
        info = sys.exc_info()
        print info[0],":",info[1]
        traceback.print_exc()
        
    client.close()