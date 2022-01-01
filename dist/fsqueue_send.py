#!/usr/bin/env python
import os,sys
#######################################
sys.dont_write_bytecode = True
scriptbindir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptbindir,'..','lib'))
#######################################

from fsqueue import FsQueue

testq = FsQueue("testq",10)

