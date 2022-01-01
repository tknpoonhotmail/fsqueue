#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
#######################################
"""
Usage:
fsqueue_consume.py qname [-f]
"""
#######################################
import os,json,pprint
from FsQueue import FsQueue

#######################################
def usage():
    usagetext="""
Usage: %s qname [-f]
    -f : fail 
""" % (sys.argv[0])
    print(usagetext)

#######################################
def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    _qname  = sys.argv[1]
    _restlist = sys.argv[2:]

    # print(_qname)
    # print(_restlist)

    q = FsQueue(_qname,timeout=10)

    id,msg = q.read()
    if id:
        pprint.pprint(msg)
        if "-f" in _restlist:
            q.nack(id)
        else:
            q.ack(id)
    else:
        print("No message")

#######################################
if __name__ == "__main__":
    main()
