# 2018.6.8
# 张弘
# 逆变器协议转换

'''
    固德威逆变器协议较为简单。

    以BYTES数组的形式呈现.

    首部固定为
    request:    AA 55 B0 7F
    response:   AA FF 7F B0

    之后是控制码
    control code 代表注册,读取,写入,执行四个方面
    再之后是功能码,指示对应的内容。
    
    在之后就是数据。

    最后是一个和校验。
'''

'''
    主要是读取运行信息，还有设置输出功率的操作。
'''
response = "AA 55 7F B0 01 81 82 0C F9 0D AF 00 0B 00 0D 08 C5 00 26 13 87 02 1A 00 01 01 AF 00 00 00 00 00 00 62 C2 00 00 0F 4D 28 3F 00 00 0F F5 23 00 01 45 00 09 00 A8 02 12 00 00 00 64 FF FB 6A 0F 00 00 01 13 00 3A 00 00 48 DB 03 2C 08 99 00 1A 00 02 00 00 00 00 00 64 01 45 00 1E 00 4B 00 03 02 1A 00 00 12 06 08 10 25 00 00 96 09 C4 00 01 00 01 13 86 00 00 00 01 00 30 00 01 00 01 00 00 00 00 00 00 08 00 00 00 00 02 14 74 "

# 这两个报文用来查询WIFI地址
WiFiRead='WIFIKIT-214028-READ' 
WiFiPort = 48899

'   point 保留一位小数 '
def trans(src,index,length,unit='',point=1):
    result = 0
    # length没用上
    result =src[index]*256+src[index+1]
    for i in range(0,point,1):
        result =result/10
    
    return round(result,point)

    if(unit ==''):
        return round(result,point)
    else:
        return str(round(result,point)) +unit

def transSigned(src,index,length,unit='',point=1):
    result = 0
    # length没用上
    result =src[index]*256+src[index+1]
    if(result > 0x8000):
        result = result -65536

    for i in range(0,point,1):
        result =result/10
    
    return round(result,point)
    
    if(unit ==''):
        return round(result,point)
    else:
        return str(round(result,point)) +unit
# 运行数据获取 0x01 <-> 0x81
def TransRunningData(data):
    result = {
    'vpv1' : trans(data,0,2,'v'),
    'vpv2' : trans(data,2,2,'v'),
    'ipv1' : trans(data,4,2,'a'),
    'ipv2' : trans(data,6,2,'a'),
    'vac1' : trans(data,8,2,'v'),
    'iac1' : transSigned(data,10,2,'a'),
    'fac1' : trans(data,12,2,'hz',point =2),
    'pac' : str(trans(data,14,2) + trans(data,74,2)*65536) +'w',
    #workMode = workModeTable(data[16]),
    'tmp' : trans(data,18,2,'℃'),
    #errorMessage= errorMessageTable(data[22],data[20]]),
    'eTotal' : str(trans(data,26,2) + trans(data,24,2)*65536) +'kwh',
    'hTotal' : str(trans(data,30,2,point=0) + trans(data,28,2,point=0)*256) +'h',
    #'tmpFaultValue' : trans(data,32,2,'℃'),
    #'pv1FaultValue' : trans(data,34,2,'v'),
    #'pv2FaultValue' : trans(data,36,2,'v'),
    #functionValue = functionValueTable(data[38]),
    'eDayToGrid' :  trans(data,44,2,'kwh'),

    'vBat' : trans(data,46,2,'v'),

    'eDayPV' : str(trans(data,54,2) + trans(data,48,2)*65536) +'kwh',

    'cBat' : trans(data,50,2,'%',0),
    'iBat' : transSigned(data,52,2,'a'),

    'loadPower' : trans(data,58,2,'va'),
    'eLoadDay' : trans(data,60,2,'kwh'),
    'eTotalLoad' :   str(trans(data,64,2) + trans(data,62,2)*65536) +'kwh',
    'totalPower' : trans(data,66,2,'w'),
    'vLoad' :trans(data,68,2,'v'),
    'iLoad' :trans(data,70,2,'a')
    #operationMode=data[70],

    }
    return result

def getDataContent(response):
    
    data =response[7:len(response)-7]
    return data
# 
def checkSum(x):
    m_sum =0
    length=len(x)
    for i in x:
        m_sum=m_sum+int(i)
        m_sum=m_sum%65536
    high = (m_sum>>8)&0xff
    low =  m_sum&0xff
    x.append(high)
    x.append(low)


#Setting命令
# 发送命令格式

def setPower(powerRate):
    msg=bytearray.fromhex("aa 55 b0 7f 03 0a 05 ")
    msg.append(powerRate)
    msg.append(0x00)
    msg.append(0x02)
    msg.append(0x03)
    msg.append(0x04)
    checkSum(msg)
    return msg
    
def getACPower(data):
    x = transSigned(data,10,2,)
    y = trans(data,8,2)

    p=round( x*y,2)
    return p
# 回复报文格式

