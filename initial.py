'''
本模块用来初始化config
运行这个模块
'''

import json
# for socket
import time
import asyncore
import socket
import threading
import protocol

import web.webTest as ApiProfessor#导入我的网站

from memsNode import Node #导入子节点
from memsNode import INV
from memsNode import PCS

# 预定义的函数
def DBG(msg,level="Notice"):
    print("[{1}]:{0}".format(msg,level))




#定义的节点


#Main

# 第一步 打开配置文件 ,读取项目架构
fo = open('config.json','r+',encoding='UTF-8')
obj_Config = json.loads(fo.read())
fo.close()
#Topo
g_NodeList =[]
# 兼容 flask
NodeList = g_NodeList
g_HostName=obj_Config['remoteHost']
DBG("Configuration Start.","Notice")

# 创建节点
# 为每个节点，按照规约绑定一个设备
# 为每个设备，给予一个通信地址（ip,port）
# 最终将所有节点加入列表中集中管理

for i in obj_Config['nodeList']:
    
    #
    if i['type']=="INV": #随着Node类的扩展，初始化的类会有所不同
        
        t_Node = INV(   name = i['name'],
                     
                        describe=i['describe'],   
                        port=i['remote_port'],
                        proto=i['proto']
                     )
        exec('import protocol.{0}'.format(i['proto']))
        m_protoObj = eval('protocol.{0}.createInstance()'.format(i['proto']))

        m_protoObj.bindRemote(i['remote_ip'],i['remote_port'])

        t_Node.bindprotocol(m_protoObj)

        #添加到列表
        g_NodeList.append(t_Node)
        
    
    if i['type']=='PCS':
        t_Node = PCS(   name = i['name'],
                     
                        describe=i['describe'],   
                        port=i['remote_port'],
                        proto=i['proto']
                     )
        exec('import protocol.{0}'.format(i['proto']))
        m_protoObj = eval('protocol.{0}.createInstance()'.format(i['proto']))

        m_protoObj.bindRemote(i['remote_ip'],i['remote_port'])
        t_Node.bindprotocol(m_protoObj)
        

        #添加到列表
        g_NodeList.append(t_Node)
    

DBG("Initialize finish.")

# 下一步是为每个

# 启动每个node
for i in g_NodeList:
    i.protoObj.startThread()

def readCircle():
    while True:
        try:
            for i in g_NodeList:
                i.protoObj.readCommandSet()
                
            #DBG('reading','readCircle')
            time.sleep(1)
        except:
            DBG("Error",'readCircle')
            break
th1 = threading.Thread(target = readCircle)
th1.start()

def test_readPQ():
    while True:
        try:
            for i in g_NodeList:
                i.data = i.protoObj.getPQ()
            time.sleep(3)
        except:
            break
th2 = threading.Thread(target = test_readPQ)
th2.start()

input("Press any Key to Start WebApi.\n")

ApiProfessor.setSource(g_NodeList)
ApiProfessor.testRun()

#
input("[for debug]Press any Key to Leave.")



