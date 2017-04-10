#coding=utf-8

import socket
from random import randint
from hashlib import sha1 #进行hash加密
from bencode import bencode, bdecode

BOOTSTRAP_NODES = (
    ("67.215.246.10", 6881),
    ("82.221.103.244", 6881),
    ("23.21.224.150", 6881)
)

def entropy(length):
    return "".join(chr(randint(0, 255)) for _ in xrange(length))

def get_neighbor(target, nid, end=10):
    return target[:end]+nid[end:]

def random_id():
    h = sha1()
    h.update(entropy(20))
    return h.digest()

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    bind_ip='0.0.0.0'
    bind_port=6881
    server.bind((bind_ip, bind_port))
    
    tid = entropy(2)
    nid = random_id()
    targetid = random_id()
    print tid, nid, targetid
    msg = {
        "t": tid,
        "y": "q",
        "q": "find_node",
        "a": {
            "id": nid,
            "target": targetid
        }
    }
    
    sendmsg = bencode(msg)
    print sendmsg
    
    for address in BOOTSTRAP_NODES:
        print address
        server.sendto(sendmsg, address)
        # 阻塞了, 估计是dht协议被公司内部禁止了
        (response, server) = server.recvfrom(65536)

        print response, server
        
        