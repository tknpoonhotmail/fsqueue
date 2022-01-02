import os, sys, pprint, json, shutil, glob
import time
import datetime as dt

#########################################################
class FsQueue():
    def __init__(self,qname,timeout=60):
        # default
        self.queues_parent_dir=os.path.join( os.environ['HOME'], "tmp", "_queues")
        self.polling_interval = 5
        self.timeout = 60
        self.max_processing_age=86400
        self.keep_success = False
        # 
        self.qname = qname 
        self.timeout = timeout
        #
        self.queue_dir = os.path.join(self.queues_parent_dir, self.qname)
        self.q_input = os.path.join(self.queue_dir, 'input')
        self.q_processing = os.path.join(self.queue_dir, 'processing')
        self.q_failed = os.path.join(self.queue_dir, 'failed')
        self.q_success = os.path.join(self.queue_dir, 'success')

        #ensure dirs exist
        for d in [self.q_input, self.q_processing, self.q_failed, self.q_success] :
            if not os.path.isdir(d):
                os.makedirs(d)

    #################################################
    def del_msg(self, msgid, fromdir):
        try:
            os.remove(os.path.join(fromdir, msgid +'.json'))
            msgblobdir=os.path.join(fromdir, msgid)
            if os.path.isdir(msgblobdir):   shutil.rmtree(msgblobdir)
            return True
        # except FileNotFoundError as e:
        except IOError as e:
            return False
    #################################################
    def move_msg(self, msgid, srcdir, destdir):
        try:
            os.rename(os.path.join(srcdir, msgid +'.json')  , os.path.join(destdir, msgid +'.json'))
            shutil.move(os.path.join(srcdir, msgid),  os.path.join(destdir, msgid))
            for p in glob.glob(os.path.join(destdir, msgid+"*")):
                os.utime(p)
            return True
        # except FileNotFoundError as e:
        except IOError as e:
            return False

    #################################################
    def newID(self):
        """ New msg ID """
        curtime=dt.datetime.now()
        return "%s-%s" % (self.qname ,curtime.strftime("%Y%m%d-%H%M%S-%f"))

    #################################################
    def send(self, list_of_dict):
        """
        list_of_dict in the following format:
            [   {"fieldA":dataA, "fieldB":dataB, "blobs":{<name>:<bytearray>,...} }            ]
        JSON file will become:
            [   {"fieldA":dataA, "fieldB":dataB, "blobs":[<name>,...] } ]
        blob will be saved as:
            <id>/<seq_from_0>/<name>
        """
        count =0
        realmsg=[]
        id = self.newID()
        for d in list_of_dict:
            blobs = d.pop("blobs",None)
            if blobs is not None:
                blobnames=[]
                for k in blobs.keys() :
                    data=blobs[k]
                    blobdir=os.path.join(self.q_input, id, str(count))
                    if not os.path.isdir(blobdir):  os.makedirs(blobdir)
                    blobnames.append(k)
                    with open(os.path.join(blobdir,k), 'wb') as bfile:
                        bfile.write(data)
                d["blobs"]=blobnames
            realmsg.append(d)
            count += 1

        # write json file
        with open(os.path.join(self.q_input, id + '.json'),'w') as jfile:
            jfile.write(json.dumps(realmsg,indent=2))
        # pprint.pprint(realmsg)

    #################################################
    def read_msg(self, msgid):
        """
        JSON file is:
            [   {"fieldA":dataA, "fieldB":dataB, "blobs":[<name>,...] } ]
        blob will be saved as:
            <id>/<seq_from_0>/<name>
        Return list_of_dict
        """
        msg=[]
        # move to processing
        if self.move_msg(msgid, self.q_input, self.q_processing) : #process message
            with open(os.path.join(self.q_processing, msgid+'.json'), 'rb') as infile:
                list_of_dict = json.load(infile)
            count =0
            for d in list_of_dict:
                blobnames = d.pop("blobs",None)
                if blobnames is not None:
                    blobdict={}
                    for k in blobnames:
                        blobdir=os.path.join(self.q_processing, msgid, str(count))
                        with open(os.path.join(blobdir,k), 'rb') as bfile:
                            data=bfile.read()
                        blobdict[k] = data
                    d["blobs"]=blobdict
                msg.append(d)
                count += 1

        return msg

    #################################################
    def read(self, getmsgid=''):
        countdown = self.timeout / self.polling_interval
        while True:
            if getmsgid:
                jfile = os.path.join(self.q_input, "%s.json"%(getmsgid))
                filelist = [jfile] if os.path.isfile(jfile) else []
                countdown=0
            else:
                filelist = sorted( glob.glob(os.path.join(self.q_input, "*.json")), key=os.path.getmtime)

            if filelist:
                _msgid= os.path.basename(filelist[0]).replace('.json', '')
                return _msgid, self.read_msg(_msgid)

            countdown -= 1
            if countdown <=0:   
                return None,[]
            time.sleep(self.polling_interval)
        
    #################################################
    def ack(self,msgid):
        if self.keep_success:
            self.move_msg(msgid, self.q_processing, self.q_success)
        else:
            self.del_msg(msgid, self.q_processing)

    #################################################
    def nack(self,msgid):
        self.move_msg(msgid, self.q_processing, self.q_failed)

#########################################################
#########################################################
#########################################################
def msgsend(fsq):
    ba = bytearray("a_string".encode())
    msg =[]
    msg.append({"key":True, "blobs":{"a.bin":ba ,"b.bin":ba} })
    msg.append({"key":False})
    msg.append({"key":True, "blobs":{"b.bin":ba } })
    fsq.send(msg)

def msgread(fsq):
    while True:
        id,msg=fsq.read()
        if id:
            pprint.pprint(msg)
            fsq.ack(id)
        else:
            print("no msg to process")
            return 
    
if __name__ == "__main__":
    testq = FsQueue("testq",10)
    msgsend(testq)
    msgread(testq)
    # testq.move_msg("testq-20220101-163343-002423", testq.q_failed, testq.q_input)

