#!/bin/bash
DIR=`dirname $0`
echo === Send message
$DIR/fsqueue_send.py testq {} /etc/group
echo === Fail the message
$DIR/fsqueue_consume.py testq -f
echo === Move back to retry
$DIR/fsqueue_manage.py testq retry
echo === Consume the message
$DIR/fsqueue_consume.py testq 
echo === Display
$DIR/fsqueue_manage.py testq display
echo === Purge
$DIR/fsqueue_manage.py testq purge
