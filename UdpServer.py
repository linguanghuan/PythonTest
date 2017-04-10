#coding=utf-8

import socket
from socket import inet_ntoa
import traceback

if __name__=="__main__":
    bind_ip='127.0.0.1'
    bind_port=5555
    try:
        ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ufd.bind((bind_ip, bind_port))
        while True:
            (data, address) = ufd.recvfrom(65536)
            print "[server] received :" + data + ", from :" + str(address)
            ufd.sendto("response", address)
    except:
        traceback.print_exc()
