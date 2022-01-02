#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
#######################################
usagetext="""
Usage: %s qname {display | ageout | requeue}
    qname   - Queue Name

    display - Display the queue count
    ageout  - Check the stuck processing items; fail them if too old.
    requeue - Requeue the failed items; i.e. put back to input
"""
#######################################
import os,json,pprint
from FsQueue import FsQueue

#######################################
def usage():
    print(usagetext % (sys.argv[0]))
#######################################
def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    [_qname , _command] = sys.argv[1:]
    if _command not in ['display', 'ageout','requeue']:
        usage()
        sys.exit(2)
    ###
    q = FsQueue(_qname,timeout=10)
    if _command == "ageout":
        aged = q.ageout()
        print("Requeued aged msg:")
        pprint.pprint(aged)
    elif _command == "requeue":
        requeued = q.requeue_failed()
        print("Requeued failed msg:")
        pprint.pprint(requeued)
    else: # display
        pprint.pprint(q.getlist())

    
#######################################
if __name__ == "__main__":
    main()
