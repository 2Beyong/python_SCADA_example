'''
本模块用来初始化config
'''

import json
# for socket
import time
import asyncore
import socket
import threading
import protocol.protocol

import web.webTest as ApiProfessor#导入我的网站
# 预定义的函数
def DBG(msg,level="verbose"):
    print("[Debug][{1}]:{0}".format(msg,level))

#用于动态引用Protocol库中的协议
def createInstance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


#定义的节点
class Node:
    def __init__(self,
        name="default",
        type="unknown",
        describe="unknown device",
        proto="default",
        port=20000):
        
        # from config
        self.name=name
        self.type=type
        self.describe=describe
        self.proto=proto
        self.port=port
        # running status
        self.state={}
        self.rate={}
        self.data={}
        # comm socket
        self.protoObj=None # like a list
        self.socket=None

    # methods
    def bindprotocol(self,x):
        self.protoObj=x
    def bindSocket(self,x):
        self.socket=x
    def updateData(self):
        self.rst = self.protoObj.getRunningDataCommand()
        self.socket.send(bytes(self.rst,"UTF-8"))
       
    def onReceive(self,rst): #供socket调用的回调函数
        rsd = self.protoObj.handleReceiveData(rst)
        self.data=rsd.copy()
        print("[{2}][{0}]get:{1}".format(   self.name,
                                            self.data,
                                            time.asctime(time.localtime(time.time()))
                                            )
            )

#定义的DataClinet
class DataClient(asyncore.dispatcher): #socket
    '''该类暂时没有重连功能'''
    '''目前该类有重连功能了，尝试的周期相当长
       而且还有BUG。每次断开会接收到一个空白，然后触发一个重连，显示的是连接成功，
       再然后断掉。
    '''
    count=0
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host =host
        self.port = port
        DataClient.count=DataClient.count+1
        self.order=DataClient.count
        self.linkNode=None
    def bindNode(self,node):
        self.linkNode=node
    def startConnect(self):
        self.connect((self.host, self.port))
    def handle_connect(self):
        print("Connect Success,{0},port = {1}".format(self.host,self.port))
    def handle_error(self):
        DBG("[{0}:{1}]:Socket Error occupied.".format(self.host ,self.port),"Error")
        #尝试重连
        self.close()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.startConnect()    

    def handle_close(self):
        DBG("[{0}:{1}]:Socket Remote close.".format(self.host ,self.port))
        DataClient.count=DataClient.count-1 #总量减一
        self.close()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.startConnect() 

    def handle_read(self): #透传
        rst = self.recv(1024)
        
        self.linkNode.onReceive(rst)
            
class DataClientsThread(threading.Thread):
    def __init__(self,SocketList):
        
        threading.Thread.__init__(self)
        self.sslist=SocketList
        print("thread init")
    def run(self):
        print("thread run")
        for i in self.sslist:
            i.startConnect()
        
        asyncore.loop()


#Main
fo = open('config.json','r+')
obj_config = json.loads(fo.read())

#DBG(obj_config)

#初始化
#global variable
NodeList =[]
SocketList=[]
hostName="127.0.0.1"
print("Hello,here is ",obj_config['systemName'])
for i in obj_config['nodeList']:
    
    #
    if(i['type']=="INV"): #随着Node类的扩展，初始化的类会有所不同
        print("Init Inverter",i['name'])
        tNode = Node(i['name'],
                     i['type'],
                     describe=i['describe'],
                     port=i['port'],
                     proto=i['proto']
                     )
        #绑定Socket
        tDataClient =DataClient(hostName,tNode.port)
        tNode.bindSocket(tDataClient)
        #绑定协议
        obj = createInstance("protocol.protocol", tNode.proto)
        tNode.bindprotocol(obj)
        tDataClient.bindNode(tNode)
        #添加到列表
        NodeList.append(tNode)
        SocketList.append(tDataClient)
    
    if(i['type']=="LOAD"): #随着Node类的扩展，初始化的类会有所不同
        print("Init Load")
        tNode = Node(i['name'],
                     i['type'],
                     describe=i['describe'],
                     port=i['port'],
                     proto=i['proto']
                     )
        #未绑定Socket
        NodeList.append(tNode)
    
print("Initialize finish.")



DBG("STARTing SocketListening")
t1 = DataClientsThread(SocketList)
t1.start()

DBG("Socket Listening Start.")

input("Press any Key to Start WebApi.\n")

ApiProfessor.setSource(NodeList)
ApiProfessor.testRun()

