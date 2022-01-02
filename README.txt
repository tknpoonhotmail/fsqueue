# fsqueue
Simple Queue System using local file system

Class file:
    FsQueue.py 
Methods:
    send(listOfDict)    : Send List of Dict with blob . return MsgID
                       e.g. [
                                {"age":30, "name":"Adam", "blobs": {"pictureA": b'0x0a', "pictureB": b'0x0b' }},
                                {"age":20, "name":"Barry" }
                            ]
    read([msgid])       : Read Message optionally specify the MsgID; wait until timeout
                            Return     msgid, listOfDict     ; if no message, msgid=None & listOfDict=[]
    ack(msgid)          : Acknowledge the message; either delete or move to success -- depending on initialization
    nack(msgid)         : Nack the message; and the message will be moved to failed
    getlist()           : Return {"input":[msgid...],"success":[msgid...],"processing":[msgid...],"failed":[msgid...]}
    retry_failed()      : Move failed messages to input
    requeue_success()   : Move succeed messages (if any) to input
    ageout()            : Fail the messages stuck in processing
    purge()             : Purge all messages of all stages in the queue 


