# coding: utf-8
import hashlib
from bencode import bencode, bdecode
# pip install demjson
import demjson

def write():
    print "write"
#     file_object = open('F:\\torrent\\data.txt', 'wb')
    file_object = open('F:/torrent/data.txt', 'wb')
#     all_the_text = "testtttttttt";
    metadata = [1,2,3]
    print "".join(metadata)
    metadata = "".join(metadata)
    file_object.write(metadata)
    file_object.close( )

def decode( s):
    if type(s) is list:
        s = ';'.join(s)
    u = s
    for x in ('utf8', 'utf8', 'gbk', 'big5'):
        try:
            u = s.decode(x)
            return u
        except:
            pass
    return s.decode('utf8', 'ignore')
    
def decode_utf8( d, i):
    if i+'.utf-8' in d:
        return d[i+'.utf-8'].decode('utf8')
    return decode(d[i])

def parse_metadata( data): #解析种子
    info = {}
    encoding = 'utf8'
    try:
        torrent = bdecode(data) #编码后解析
        if not torrent.get('name'):
            return None
    except:
        return None
    detail = torrent
    info['name'] = decode_utf8(detail, 'name')
    if 'files' in detail:
        info['files'] = []
        for x in detail['files']:
            if 'path.utf-8' in x:
                v = {'path': decode('/'.join(x['path.utf-8'])), 'length': x['length']}
            else:
                v = {'path': decode('/'.join(x['path'])), 'length': x['length']}
            if 'filehash' in x:
                v['filehash'] = x['filehash'].encode('hex')
            info['files'].append(v)
        info['length'] = sum([x['length'] for x in info['files']])
    else:
        info['length'] = detail['length']
    info['data_hash'] = hashlib.md5(detail['pieces']).hexdigest()
    return info


def metadata():
    file_object = open("18270c973085f6a41ac3a1f1f6e2ac8f73064d3c.metadata", 'rb')
    data = file_object.read()
    print data
    info = parse_metadata(data)
    print info
    json_str = demjson.encode(info, "utf-8")
    print json_str

if __name__ == "__main__":
    print "test"
#     write()
    metadata()