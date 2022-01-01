#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
#######################################
usagetext="""
Usage: %s qname json_dict_text [blob_files ...]
    qname           - Queue Name
    json_dict_text  - one liner of json dict text e.g. '{"id":1}'
    blob_files      - list of file path on the server. the basename will be the key in the dict.
"""
#######################################
import os,json,pprint
from FsQueue import FsQueue

#######################################
def usage():
    print(usagetext % (sys.argv[0]))

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
