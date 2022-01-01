#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
#######################################
"""
Usage:
fsqueue_send.py qname json_dict_text [blob_files ...]
"""
#######################################
import os,json,pprint
from FsQueue import FsQueue

#######################################
def usage():
    usagetext="""
Usage: %s qname json_dict_text [blob_files ...]
""" % (sys.argv[0])
    print(usagetext)

#######################################
def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    [_qname , _json_text] = sys.argv[1:3]
    _bloblist = sys.argv[3:]

    data = json.loads(_json_text)

    blobdict={}
    for fname in _bloblist:
        with open(fname,'rb') as f:
            blobdict[ os.path.basename(fname) ] = f.read()
    if blobdict:
        data["blobs"] = blobdict

    FsQueue(_qname).send( [data] )


#######################################
if __name__ == "__main__":
    main()
