#!/usr/bin/env python
import os,sys
#######################################
sys.dont_write_bytecode = True
# scriptbindir=os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(scriptbindir))
#######################################

from FsQueue import FsQueue

testq = FsQueue("testq",10)
ba = bytearray("a_string".encode())
msg =[]
msg.append({"key":True, "blobs":{"a.bin":ba ,"b.bin":ba} })
msg.append({"key":False})
msg.append({"key":True, "blobs":{"b.bin":ba } })

testq.send(msg)


