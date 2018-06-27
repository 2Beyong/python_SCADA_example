
from . import goodwe 
import queue
import threading
import time
import socket

def DBG(msg,level="Notice"):
    print("[{0}]:{1}".format(level,msg))

class Goodwe_v1:
    def __init__(self):
        self.c_queue = queue.Queue()
        self.thread =None
        self.raw_data={}
        
    def startThread(self):
        if self.thread ==None:
            self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def updateData(self,rst):
        self.raw_data.update(rst)
    
    def handleResponse(self,resp):
        if resp[4] == 0X01 and resp[5] == 0x81 :
            self.updateData(
                goodwe.TransRunningData(
                    goodwe.getDataContent(resp)
                ))
            

    def run(self):
        '''给线程用的函数，建议不要'''
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.settimeout(5) #设置延时
        self.socket.connect((self.remote_ip,self.remote_port))
        DBG("connect to Remote ip")
        while True:
            
            try:
            
                # 查看队列里有无任务
                if self.c_queue.qsize()>0:
                    
                        t_command = self.c_queue.get()
                        if (type(t_command) == bytes) or (type(t_command) == bytearray) :
                            self.socket.send(t_command)
                        elif type(t_command) is str:    
                            self.socket.send(bytes(t_command,"utf-8"))
                        t_response = self.socket.recv(1024)
                        
                        # handle recv
                        self.handleResponse(t_response)

                        
                else:
                    time.sleep(0.5)
                
            # 出现错误则重新run
            except Exception as e:
                DBG(e,"Socket Error")
                self.socket.close()
                time.sleep(3) 
                self.run()
                return      
    
    def timeStamp(self):
        return time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time()))

    def bindRemote(self,remote_ip,remote_port):

        self.remote_ip = remote_ip
        self.remote_port = remote_port
    
    def readCommandSet(self):
        self.c_queue.put(bytes.fromhex('AA 55 B0 7F 01 01 00 02 30'))

    def setMaxOutputPower(self,power):
        if power<0:
            return
        l_byte = power&0xff
        h_byte = (power>>8)&0xff
        
        t_command = bytearray.fromhex('AA 55 C0 7F 03 35 02')
        t_command.append(h_byte)
        t_command.append(l_byte)
        goodwe.checkSum(t_command)
        DBG(t_command)
        self.c_queue.put(t_command)
    
    #
    def getPQ(self):
        rst={}
        try:
            rst['P']= self.raw_data['ACPower']
            rst['Q']= 0
        except KeyError as e:
            DBG(e,'getPQerror')
            return {'P':None,'Q':None}  
        return rst 