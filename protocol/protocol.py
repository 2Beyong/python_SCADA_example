import random

#模拟的类
class INV_virtual:
    def __init__(self):
        pass

    # 从这里提取出对应的命令，所以用的手法是get.    
    def getRunningDataCommand(self):
        return "^PRD"
    def getswitchONCommand(self):
        pass
    def getswitchOFFCommand(self):
        pass

    '''
        解析socket接收到的信息，
        一般而言，要根据报文中的type类型，来确定是记录的运行信息，或是其它的内容.
        recv:报文
    '''    
    def handleReceiveData(self,recv):

        #对定长报文,确定其首尾长度

        #提取类型字段

        #根据类型，调用处理函数

        #返回值封装成dict

        #返回

        #对于Default ,返回随机的结果.
        data={  'power':round(random.random()*5000,2),
                'vgrid':round(220+(random.random()-0.5)*10,2),
                'vpv':round((100+random.random()*500),2),
                'tmp':round(20+random.random()*10,2)
        }
        return data
        