#coding: utf-8
#[From] http://www.pjbj.com/%E7%94%A8python%E5%86%99%E4%B8%80%E4%B8%AA%E6%9C%89%E9%81%93%E5%BE%B7%E6%84%9F%E7%9A%84dht%E7%88%AC%E8%99%AB/
#[DHT Protocol] http://www.bittorrent.org/beps/bep_0005.html
#[Extension Protocol] http://www.bittorrent.org/beps/bep_0010.html

import socket
import random
import hashlib
import bencode
from struct import unpack, pack
import time
from threading import Thread
import Queue
import cPickle

class DHTServer(Thread):
    def __init__(self, debug=True):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.bind(("0.0.0.0", 65111))
        self.s.settimeout(10)
        self.table = set()
        self.nodes_queue = Queue.Queue(4096)
        self.debug = debug
        self.nid = "4e4ee047ef070d2633f00c3e908f018c0c10f0f0".decode("hex")
#         self.nid= self.random_id()
        self.tar = "60603BB64B43A0318B98817AC8CC1C6A64D17D7D".decode("hex")
#         self.tar = self.random_id()

    def run(self):  # 接收DHT数据包线程
        while 1:
            try:
                data = self.s.recvfrom(2048)
                self.process_data(data)
            except Exception, e:
                print e
                pass
                del e

    def process_data(self, data):
        addr = data[1]
        data = bencode.bdecode(data[0])

        if self.debug:
            print data
            print "TABLE LEN ", len(self.table)

        if data['y'] == 'q':
            self.process_q(data, addr)
        if data['y'] == 'r':
            self.process_r(data)

    @staticmethod
    def decode_nodes(nodes):
        n = []
        length = len(nodes)
        if (length % 26) != 0:
            return n
        for k in xrange(0, length, 26):
            nid = nodes[k:k + 20]
            ip = socket.inet_ntoa(nodes[k + 20:k + 24])
            port = unpack("!H", nodes[k + 24:k + 26])[0]
            n.append((nid, ip, port))
            n = list(set(n))
        return n

    def process_q(self, data, addr):

        try:  # 把请求节点加入路由表
            nid = data['a']['id']
            ip = addr[0]
            port = addr[1]
            node = (nid, ip, port)
            self.table.add(node)
        except:
            pass

        if data["q"] == 'get_peers':
            print "GP"
            print data['a']['info_hash'].encode("hex")

        elif data['q'] == 'ping':
            t = data['t']
            self.send_msg(self.pack_ping_respond_msg(t), addr)
            time.sleep(0.0025)
            self.send_msg(self.pack_ping_respond_msg(t), addr)
            print "responded_ping from", addr

        elif data['q'] == 'find_node':
            t = data['t']
            target = data['a']['target']
            self.send_msg(self.pack_find_node_respond_msg(t, target), addr)
            time.sleep(0.0025)
            self.send_msg(self.pack_find_node_respond_msg(t, target), addr)
            # print bencode.bdecode(self.pack_find_node_respond_msg(t, target))
            print "responded_find_node from", addr

    @staticmethod
    def decode_ip(ip):
        ip_ = "0.0.0.0"
        port = 65535
        if len(ip) == 4:
            return socket.inet_ntoa(ip)
        elif len(ip) == 6:
            ip_ = socket.inet_ntoa(ip[0:4])
            port = unpack("!H", ip[4:6])[0]
        return ip_, port


    @staticmethod
    def encode_nodes(nodes):
        strings = []
        for node in nodes:
            s = "%s%s%s" % (node[0], socket.inet_aton(node[1]), pack("!H", node[2]))
            strings.append(s)
        return "".join(strings)

    def process_r(self, data):
        nodes = data['r']['nodes']
        for node in self.decode_nodes(nodes):
            if node not in self.table:
                self.nodes_queue.put(node)

    def send_msg(self, msg, addr):
        try:
            self.s.sendto(msg, addr)
        except Exception, e:
            print e

    def pack_find_nodes_query_msg(self):
        msg = {
            "t": self.entropy(2),
            "y": "q",
            "q": "find_node",
            "a": {
                "id": self.nid, 
                "target": self.tar
            }
        }
        return bencode.bencode(msg)

    def pack_ping_node_query_msg(self):
        msg = {
            "t": self.entropy(2),
            "y": "q",
            "q": "ping",
            "a": {"id": self.nid}
        }
        return bencode.bencode(msg)

    def pack_get_peers_query_msg(self):
        msg = {
            "t": self.entropy(2),
            "q": "get_peers",
            "y": "q",
            "a": {
                "id": self.nid,
                "info_hash": self.tar

            }
        }
        return bencode.bencode(msg)

    def pack_ping_respond_msg(self, t):
        msg = {
            "t": t,
            "y": "r",
            "r": {"id": self.nid}
        }
        return bencode.bencode(msg)

    def pack_find_node_respond_msg(self, t, target):
        msg = {
            "t": t,
            "y": "r",
            "r": {"id": self.nid,
                  "nodes": self.search_node_from_table(target)
                  }
        }
        return bencode.bencode(msg)

    def find_nodes(self):
        msg = self.pack_find_nodes_query_msg()
        node = self.nodes_queue.get()
        addr = (node[1], node[2])
        self.send_msg(msg, addr)
        self.table.add(node)
        return node

    def get_peers(self):
        msg = self.pack_get_peers_query_msg()
        node = self.nodes_queue.get()
        addr = (node[1], node[2])
        self.send_msg(msg, addr)
        self.table.add(node)
        return node

    def random_id(self):
        h = hashlib.sha1()
        h.update(self.entropy(20))
        return h.digest()

    @staticmethod
    def entropy(length):
        return "".join(chr(random.randint(0, 255)) for _ in xrange(length))

    @staticmethod
    def intify(hstr):
        return long(hstr.encode('hex'), 16)

    def search_node_from_table(self, target):
        table = list(self.table)
        nodes = []
        tmp = []
        min_list = []
        min_id = []
        for k in table:
            tmp.append(self.intify(k[0]) ^ self.intify(target))
        tmp1 = tmp[:]
        for k in xrange(8):
            mi = min(tmp)
            min_list.append(mi)
            tmp.pop(tmp.index(mi))
        for k in min_list:
            min_id.append(tmp1.index(k))
        for k in min_id:
            nodes.append(table[k])
        return self.encode_nodes(nodes)

BOOTSTRAP_NODES = (
    ("67.215.246.10", 6881),    #router.bittorrent.com
    ("82.221.103.244", 6881),   #router.utorrent.com
    ("212.129.33.59", 6881)     #dht.transmissionbt.com
)
    
if __name__ == "__main__":
    dht = DHTServer(debug=True)
    for address in BOOTSTRAP_NODES:
        msg = dht.pack_find_nodes_query_msg()
        dht.send_msg(msg, address)
        
    time.sleep(1)    
    dht.start()
    
    #
    # f = open("nodes.txt", "r")
    # dht.table = cPickle.load(f)
    # f.close()

    
    while True:
        dht.find_nodes()
        print '\r' + str(len(dht.table)),
    
        if len(dht.table) == 10000:
            f = open("nodes.txt", "a")
            cPickle.dump(dht.table, f)
            f.close()
            break
        time.sleep(0.004)
        dht.get_peers()
        time.sleep(0.004)
        