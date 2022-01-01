#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
#######################################
usagetext="""
Usage: %s qname [msgid] [-f]
"""
#######################################
import os,json,pprint
from FsQueue import FsQueue

#######################################
def usage():
    print(usagetext %(sys.argv[0]))

#######################################
def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    _qname  = sys.argv[1]
    _restlist = sys.argv[2:]
    
    if "-f" in _restlist:
        _to_fail = True
        _restlist.remove('-f')
    else: 
        _to_fail = False

    q = FsQueue(_qname,timeout=10)

    id,msg = q.read(_restlist[0]) if _restlist  else q.read()
    
    if id:
        pprint.pprint(msg)
        q.nack(id) if _to_fail else q.ack(id)
    else:
        print("No message")

#######################################
if __name__ == "__main__":
    main()
