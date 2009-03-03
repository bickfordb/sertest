#!/bin/sh -e
export PYTHONPATH=~/src/protobuf-2.0.3/python
~/src/protobuf-2.0.3/src/protoc --python_out . dns.proto

./passivedns.thrift

./test_speed.py
