# -*- coding:utf-8 -*- 
'''
    这个类代表了MEMS中的每个节点，
    这个节点是个基类，可以拓展为INV,LOAD,PCS,GEN,MotherLine等

'''
import json

class PowerNode:
    

    def __init__(self,name=" a device",port=-1,type="unknown",protocol="unknown",describe="unknown device"):
        
        self.name=name
        self.port=port
        self.type=type
        self.protocol=protocol
        self.describe=describe

    def makeOnline(self):
        pass
    def makeOffline(self):
        pass
    def __str__(self):
        selfDict = self.__dict__
        return json.dumps(selfDict,ensure_ascii=False)

