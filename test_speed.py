#!/usr/bin/env python 
import time
import dns_pb2

import sys
sys.path.append("gen-py/passivedns")

import PassiveDns
import simplejson
import cjson
import yaml
import zlib

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

#import psyco
#psyco.full()

import string
import random

chars = string.ascii_letters + string.digits

def get_random_string(s):
    return ''.join(random.sample(chars, s))

def get_random_records(num=5000):
    data = []
    for x in xrange(num):
        data.append({
            'key':    get_random_string(15),
            'value':  get_random_string(20),
            'first':  get_random_string(15),
            'last':   get_random_string(15),
            'type':   random.choice(["A", "CNAME"]),
            'ttl':    random.choice([86400,3600,60]),
        })
    return data

def get_pb():
    ret = dns_pb2.DnsResponse()
    for x in raw:
        r = ret.records.add()
        for k,v in x.items():
            setattr(r, k,v)
    return ret

def get_thrift():
    ret = []
    for x in raw:
        ret.append(PassiveDns.dns_record(x))
    return PassiveDns.dns_response(dict(records=ret))

def thrift_to_bytes(var):
    transportOut = TTransport.TMemoryBuffer()
    protocolOut = TBinaryProtocol.TBinaryProtocol(transportOut)
    var.write(protocolOut)
    bytes = transportOut.getvalue()
    return bytes

def thrift_from_bytes(bytes, clas):
    transportIn = TTransport.TMemoryBuffer(bytes)
    protocolIn = TBinaryProtocol.TBinaryProtocol(transportIn)
    
    n = clas()
    n.read(protocolIn)
    return n

def _ser_thrift():
    ret = get_thrift()
    return thrift_to_bytes(ret)

def ser_thrift():
    return len(_ser_thrift())

def ser_thrift_compressed():
    return len(zlib.compress(_ser_thrift()))

def _ser_pb():
    ret = get_pb()
    return ret.SerializeToString()

def ser_pb():
    return len(_ser_pb())

def ser_pb_compressed():
    return len(zlib.compress(_ser_pb()))

def ser_json():
    j = simplejson.dumps(raw)
    return len(j)

def ser_json_compressed():
    j = simplejson.dumps(raw)
    return len(zlib.compress(j))

def ser_yaml():
    y = yaml.dump(raw)
    return len(y)

def ser_yaml_compressed():
    y = yaml.dump(raw)
    return len(zlib.compress(y))

def serde_thrift():
    s = _ser_thrift()
    thrift_from_bytes(s, PassiveDns.dns_response)

def serde_json():
    j = simplejson.dumps(raw)
    simplejson.loads(j)

def serde_yaml():
    j = yaml.dump(raw)
    yaml.load(j)

def serde_pb():
    s = _ser_pb()
    n=dns_pb2.DnsResponse()
    n.ParseFromString(s)

def ser_cjson():
    j = cjson.encode(raw)
    return len(j)
 
def ser_cjson_compressed():
    j = cjson.encode(raw)
    return len(zlib.compress(j))
 
def serde_cjson():
    j = cjson.encode(raw)
    cjson.decode(j)

def t(f):
    s = time.clock()
    ret = f()
    e = time.clock()
    return e-s, ret

if __name__ == "__main__":
    x, raw = t(get_random_records)
    print len(raw), 'total records (%0.3fs)' % x

    print

    print 'get_thrift          (%0.3fs)' % t(get_thrift)[0]
    print 'get_pb              (%0.3fs)' % t(get_pb)[0]

    print

    print 'ser_thrift          (%0.3fs) %s bytes' % t(ser_thrift)
    print 'ser_pb              (%0.3fs) %s bytes' % t(ser_pb)
    print 'ser_json            (%0.3fs) %s bytes' % t(ser_json)
    print 'ser_cjson           (%0.3fs) %s bytes' % t(ser_cjson)
    print 'ser_yaml            (%0.3fs) %s bytes' % t(ser_yaml)

    print

    print 'ser_thrift_compressed (%0.3fs) %s bytes' % t(ser_thrift_compressed)
    print 'ser_pb_compressed     (%0.3fs) %s bytes' % t(ser_pb_compressed)
    print 'ser_json_compressed   (%0.3fs) %s bytes' % t(ser_json_compressed)
    print 'ser_cjson_compressed  (%0.3fs) %s bytes' % t(ser_cjson_compressed)
    print 'ser_yaml_compressed   (%0.3fs) %s bytes' % t(ser_yaml_compressed)

    print

    print 'serde_thrift        (%0.3fs)' % t(serde_thrift)[0]
    print 'serde_pb            (%0.3fs)' % t(serde_pb)[0]
    print 'serde_json          (%0.3fs)' % t(serde_json)[0]
    print 'serde_cjson         (%0.3fs)' % t(serde_cjson)[0]
    print 'serde_yaml          (%0.3fs)' % t(serde_yaml)[0]
