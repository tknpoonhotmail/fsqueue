#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
#######################################
usagetext="""
Usage: %s qname {display | ageout | requeue} [-t sec]
    qname   - Queue Name

    display - Display the queue count
    ageout  - Check the stuck processing items; fail them if too old.
    requeue - Requeue the failed items; i.e. put back to input

    -t sec  - Valid for "ageout"; how old the stuck items in processing should be aged out
"""
