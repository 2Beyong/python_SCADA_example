import time

class Node:
    def __init__(self,
        name="default",
        type="unknown",
        describe="unknown device",
        proto="default",
        port=20000 # 以后可能要改.
        ):
        
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
    
   
       
    
'''
    Inverter的基类，继承Node节点,采用通用的大写.
'''
class INV(Node):
    def __init__(
        self,
        name="default INV",
        describe="default Inverter",
        proto="INV_Virtual",
        port=20000 # 以后可能要改.
    ):
        super().__init__(name = name,describe =describe,type="INV",proto=proto,port=port)
    
    
       
    def setMaxOutputPower(self): # 调用配套协议中的setpower函数,发送命令
        pass
    def getData(self): # 注意是直接从self.data里拿旧的数据
        pass
    
    

'''
    风扇的基类
    设置最高输出功率，读取数据

'''
class FAN(Node):
    def __init__(
        self,
        name="default FAN",
        describe="default Fan",
        proto="FAN_Virtual",
        port=20000 # 以后可能要改.
    ):
        super().__init__(name = name,describe =describe,type="FAN",proto=proto,port=port)
    
    def setPower(self): # 调用配套协议中的setpower函数,发送命令
        pass
    
    '''
        {
        power
        apparent
        }
    '''
    def getData(self): # 注意是直接从self.data里拿旧的数据
        return self.data
    
class GEN(Node):
    def __init__(
        self,
        name="default GEN",
        describe="default Gen",
        proto="GEN_Virtual",
        port=20000 # 以后可能要改.
    ):
        super().__init__(name = name,describe =describe,type="GEN",proto=proto,port=port)
    
    def setPower(self,power): # 调用配套协议中的setpower函数,发送命令
        self.protoObj.setPower(power)
    def getData(self): # 注意是直接从self.data里拿旧的数据
        return self.data

'''
    储能变流器
'''
class PCS(Node):
    def __init__(
        self,
        name="default PCS",
        describe="default Power Control System",
        proto="PCS_Virtual",
        port=20000 # 以后可能要改.
    ):
        super().__init__(name = name,describe =describe,type="PCS",proto=proto,port=port)
    
    def setPower(self): # 调用配套协议中的setpower函数,发送命令
        pass
    def setFrequency(self):
        pass
    
    
    
    '''
        获取数据应包含(皆为float)
        workmode 1:vf control 2:pq control 
        power    功率 +-A (正为流出, -为流入, 下同)
        frequeny 频率 hz   
        current  电流 +-A
        capacity 电量 %
    '''
    def getData(self): # 注意是直接从self.data里拿旧的数据
        return self.data

'''
    负载(AC)
'''
class LOAD(Node):
    def __init__(
        self,
        name="default LOAD",
        describe="default LOAD",
        proto="LOAD_Virtual",
        port=20000 # 以后可能要改.
    ):
        super().__init__(name = name,describe =describe,type="LOAD",proto=proto,port=port)
    
    def cutOFF(self):
        pass

    def startON(self):
        pass

    def getData(self):
        return self.data



