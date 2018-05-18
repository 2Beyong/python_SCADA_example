import time
import asyncore
import socket
import threading

class Node:
    def __init__(self,name=" a device",type="unknown",describe="unknown device"):
        
        self.name=name
        self.type=type
        self.describe=describe
        self.proto=None
        self.data=None # like a list
        self.socket=None
    def bindprotocol(self,x):
        self.proto=x
    def bindSocket(self,x):
        self.socket=x
    def updateData(self):
        self.rst = self.proto.getRunningDataCommand()
        self.socket.send(bytes(self.rst,"UTF-8"))
       
    def onReceive(self,rst): #供socket调用的回调函数
        rsd = self.proto.handleReceiveData(rst)
        print("from [{0}]get:{1}".format(self.name,rsd))
        
        
    
class INVProtocol:
    def __init__(self):
        
        pass
    def getRunningDataCommand(self):
        pass
    def getswitchONCommand(self):
        pass
    def getswitchOFFCommand(self):
        pass
    def handleReceiveData(self):
        pass
class InfiniteSolarPro_v3(INVProtocol):
    def __init__(self):
        INVProtocol.__init__(self)
        self.lastCommend=""
        pass
    def getRunningDataCommand(self):
        self.lastCommend = InfiniteSolarPro_v3.RunningDataCommand
        return InfiniteSolarPro_v3.RunningDataCommand
    def handleReceiveData(self,recv):
        if self.lastCommend== InfiniteSolarPro_v3.RunningDataCommand :
            rst =str(recv)
            print("Last Command {0}".format(self.lastCommend))
            return rst
        else:
            rst ="Unknown:"+str(recv)
            return rst
    '''以下是该类的辅助方法'''
    RunningDataCommand="^P003PI\r"


class DataClient(asyncore.dispatcher): #socket
    '''该类暂时没有重连功能'''
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
        
    
    def handle_close(self):
        DataClient.count=DataClient.count-1 #总量减一
        self.close()

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

'''以下是test程序
'''
NodeList=[]
SocketList=[]

hostName="localhost" #串口服务器的地址
# 初始化Node
'''数据库的数据是 name port protocol，假设条目数为3'''
testPairs=[
    (3001, 'a', 'INV', 'InfiniteSolarPro_v3'),
    (3002, 'GoodWe 5kw ES', 'INV', 'InfiniteSolarPro_v3')
    ]
for i in testPairs:
    m_node = (Node(i[1],i[2],describe="device"))
    m_socket= DataClient(hostName,i[0])
    #绑定
    m_node.bindprotocol(eval(i[3]+"()"))
    m_node.bindSocket(m_socket)
    m_socket.bindNode(m_node)
    #添加一下索引
    NodeList.append(m_node)
    SocketList.append(m_socket)

#启动线程，传入SocketList



t1 = DataClientsThread(SocketList)
t1.start()
input("Press any Key to Exit.\n")

