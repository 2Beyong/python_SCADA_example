'''
本模块用来实现日月元逆变器的操作框架
核心是使用队列与优先队列，来缓存命令。

'''

'''* Node -> Protocol -> Socket'''

from . import infiniteSolar as proto
import queue
import threading
import time
import socket
def DBG(msg,level="Notice"):
    print("[{0}]:{1}".format(level,msg))

#合并两个DICT
def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
class Infinite_PCS:
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
    
                        self.socket.send(bytes(t_command,"utf-8"))
                        t_response = self.socket.recv(1024)
                        
                       
    
                        #如果是消息报文则执行
                        if t_command[1] == 'P':
                            DBG(self.timeStamp(),"Time")
                            t_cmdContent = t_command[5:-1]
                           
                            # 规约转换成dict
                           
                            t_dataList = proto.transToList(t_response[5:-3])
                            DBG(t_dataList)
                            rst = eval('proto._{0}({1})'.format(t_cmdContent,t_dataList))
                            #DBG(rst,"Rst Dict")
                            #self.raw_data = merge_two_dicts(self.raw_data,rst)
                            self.updateData(rst)
                            DBG(self.raw_data)
                        #对于设置报文，只看 1 ，0 来决定是否成功
                        else:
                            rst_flag = True if t_response[1]>0x30  else False
                            DBG(self.timeStamp(),"Time")
                            DBG(t_command[5:-1],"Socket send:")
                            DBG(rst_flag,"Socket receive")

                        
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
    def setPower(self,power):
        print("in setPower")
        #power<0 input,power>0 output
        
        #对于日月元设备 , 设置放电需要两步
        # 1 修改 充放电时间 
        #如需充电，改成全部 00:00 -> 00:00
        #如需放电，改成 00:01 ->00:02
        if power <0:
            self.c_queue.put("^S024ACCT0000,0000,0000,0000\r")
            
            # 这边需要获取当前电池电压 ,如果raw_data里没有这个数据,则使用默认的50V.
            try:
                m_Volt = self.raw_data['BatteryVoltage']
                ta = str(abs(int(power*10/m_Volt))).zfill(4)
                self.c_queue.put("^S011MUCHGC"+ta+"\r") 
            except KeyError:
                m_Volt =50
                ta = str(abs(int(power*10/m_Volt))).zfill(4)
                DBG(ta)
                self.c_queue.put("^S011MUCHGC"+ta+"\r") 
        else:
            
            self.c_queue.put("^S024ACCT0001,0002,0001,0002\r")
            tb = str(abs(power)).zfill(6)
            self.c_queue.put("^S011GPMP"+tb+'\r')
           
        # 2 修改 并网功率限制

    def readCommandSet(self):
        self.c_queue.put("^P003ID\r")
        self.c_queue.put("^P003GS\r")    
        self.c_queue.put("^P004MOD\r")
       
