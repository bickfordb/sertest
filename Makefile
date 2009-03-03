
all: PassiveDns.py dns_pb2.py

PassiveDns.py:
	thrift --gen py passivedns.thrift
	cp gen-py/passivedns/PassiveDns.py .

dns_pb2.py:
	protoc --python_out=. dns.proto
