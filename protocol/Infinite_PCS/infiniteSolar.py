'''
基于日月元串口通信协议 2016版本的基础上
进行的协议解析尝试，属于其协议的子集，
主要是针对运行信息的提取，
以及功率设置信息的方法。
'''



# 
def sendCommand(keyWord):
    rst = "^P"+str((len(keyWord))+1).zfill(3)+keyWord +'\r'
    return rst



# --- --- --

def judgeType(recvMsg):
    if recvMsg[0]!= '^':
        return
    
    if recvMsg[1]=='1' :
        pass
    elif recvMsg[1]=='0':
        pass
    elif recvMsg[1]=='D':
        pass
    
    return 
    

# 从 
def splitDatagram():
    pass

#  AAA,BBB,,CC  --> [AAA,BBB,'',CC]
def transToList(data):
    rst=[]
    if type(data) is str:
        rst = data.split(',')
    elif type(data) is bytes:
        rst = bytes.decode(data).split(',')
    return rst

# 'AAAA' -> AAA.A factor = 0.1
def ToFloat_d1(string):
    
    if string == '':
        return None
    return round(ToFloat(string,0.1),1)
def ToFloat(string,factor =1):
    
    
    if string == '':
        return None
    if factor <0:
        return 
    
    return (float(string)*factor)



'''
    命名模式 就苦逼一点
    查询的命令，就直接关键词加_GS,表示是返回的处理
    sheet : datasheet 已经经过list化的源数据
    在以下的函数中,给他们附上名字，最后输出到一个新的rst上
    key直接使用description中的名字 大小大
    value转成对应有向数字
'''
def _GS(sheet):
    rst={}
    try:
        rst['SolarInputVoltage1']=float(sheet[0])/10
        rst['SolarInputVoltage2']=float(sheet[1])/10
        rst['SolarInputCurrent1']=float(sheet[2])/10
        rst['SolarInputCurrent2']=float(sheet[3])/10
        rst['BatteryVoltage']=float(sheet[4])/10
        rst['BatteryCapacity']=int(sheet[5])
        rst['BatteryCurrent']=float(sheet[6])/10
        rst['ACInputVoltageR']=float(sheet[7])/10
        rst['ACInputVoltageS']=None if sheet[8] == '' else float(sheet[8])/10
        rst['ACInputVoltageT']=None if sheet[9] == '' else float(sheet[9])/10
        rst['ACInputFrequency']=float(sheet[10])/100
        rst['ACInputCurrentR']=float(sheet[11])/10
        rst['ACInputCurrentS']=None if sheet[12] == '' else float(sheet[12])/10 
        rst['ACInputCurrentT']=None if sheet[13] == '' else float(sheet[13])/10
        rst['ACOutputVoltageR']=float(sheet[14])/10
        rst['ACOutputVoltageS']=ToFloat_d1(sheet[15])
        rst['ACOutputVoltageT']=ToFloat_d1(sheet[16])
        rst['ACOutputFrequency']=float(sheet[17])/100
        rst['ACOutputCurrentR']=ToFloat_d1(sheet[18])
        rst['ACOutputCurrentS']=ToFloat_d1(sheet[19])
        rst['ACOutputCurrentT']=ToFloat_d1(sheet[20])
        rst['InnerTemperature']=float(sheet[21])
        rst['ComponetMaxTemperature']=float(sheet[22])
        rst['ExternalBatteryTemperature']=float(sheet[23])
        rst['SettingChangeBit']= False if sheet[24] == '0' else True
    except IndexError:
        
        print('_GS: IndexError')

        return 

    

    return rst

# 
def _PI(sheet):
    rst={}
    rst['ProtocolID'] = sheet[0]
    return rst  

# 写完  
def _ID(sheet):
    rst={}
    length = int(sheet[0][0:2])
   
    number = sheet[0][2:2+length]
    
    rst['SeriesNumber'] = number
    return rst

def _VFW(sheet):
    rst={}
    rst['CPUVersion']=sheet[0][6:6+8]
    return rst

def _VFW2(sheet):
    rst={}
    rst['CPUVersion2']=sheet[0][7:7+8]
    return rst

def _MD(sheet):
    rst={}
    rst['MachineNumber']=int(sheet[0])
    rst['OutputRatedVA']=ToFloat(sheet[1])
    rst['OutputPowerFactor']=ToFloat(sheet[2],1)
    rst['ACInputPhaseNumber']=int(sheet[3])
    rst['ACOutputPhaseNumber']=int(sheet[4])
    rst['NorminalACOutputVoltage']=ToFloat_d1(sheet[5])
    rst['NorminalACInputVoltage']=ToFloat_d1(sheet[6])
    rst['BatteryPieceNumber']=int(sheet[7])
    rst['BatteryStandardVoltagePerUnit']=ToFloat_d1(sheet[8])
    return rst

def _PIRI(sheet):
    rst={}
    rst['ACInputRatedVoltage']=ToFloat_d1(sheet[0])
    rst['ACInputRatedFrequency']=ToFloat_d1(sheet[1])
    rst['ACInputRatedCureent']=ToFloat_d1(sheet[2])
    rst['ACOutputRatedVoltage']=ToFloat_d1(sheet[3])
    rst['ACOutputRatedCurrent']=ToFloat_d1(sheet[4])
    rst['MPPTRatedCurrentPerString']=ToFloat_d1(sheet[5])
    rst['BatteryRatedVoltage']=ToFloat_d1(sheet[6])
    rst['MPPTTrackNumber']=int(sheet[7])
    rst['MachineType']=sheet[8]
    rst['Topology']=sheet[9]
    rst['Enable/DisableParallelForOutPut'] = False if sheet[10] == '0' else True
    return rst

def _PS(s):
    rst ={}
    rst['SolarInputPower1'] = ToFloat(s[0])
    rst['SolarInputPower2'] = ToFloat(s[1])
    rst['BatteryPower'] = ToFloat(s[2])
    rst['ACInputActivePowerR'] = ToFloat(s[3])
    rst['ACInputActivePowerS'] = ToFloat(s[4])
    rst['ACInputActivePowerT'] = ToFloat(s[5])
    rst['ACInputTotalActivePower'] = ToFloat(s[6])

    rst['ACOutputActivePowerR'] = ToFloat(s[7])
    rst['ACOutputActivePowerS'] = ToFloat(s[8])
    rst['ACOutputActivePowerT'] = ToFloat(s[9])
    rst['ACOutputTotalActivePower'] = ToFloat(s[10])

    rst['ACInputApparentPowerR'] = ToFloat(s[11])
    rst['ACInputApparentPowerS'] = ToFloat(s[12])
    rst['ACInputApparentPowerT'] = ToFloat(s[13])
    rst['ACInputTotalApparentPower'] = ToFloat(s[14])

    rst['ACOutputApparentPowerR'] = ToFloat(s[15])
    rst['ACOutputApparentPowerS'] = ToFloat(s[16])
    rst['ACOutputApparentPowerT'] = ToFloat(s[17])
    rst['ACOutputTotalApparentPower'] = ToFloat(s[18])
    rst['ACOutputPowerPercentage'] = ToFloat(s[19])
    rst['ACOutputConnectStatus'] = False if s[20] == None else True
    rst['SolarInput1WorkStatus'] = False if s[21] == None else True
    rst['SolarInput2WorkStatus'] = False if s[22] == None else True
    rst['BatteryPowerDirection'] = s[23]
    rst['DC/ACPowerDirection'] = s[24]
    rst['LinePowerDirection'] = s[25]

    return rst

Table_Mode = ('Power On Mode','Stand By Mode','ByPass Mode','Battery Mode','Fault Mode','Hybird Mode','Charge Mode')

def _MOD(s):
    rst={}
    global Table_Mode
    code = int(s[0])
    rst['WorkingMode'] = Table_Mode[code]
    return rst

def _WS(s):
    rst ={}
    rst['SolarInput1Loss']= True if s[0]=='1' else False
    rst['SolarInput2Loss']= True if s[1]=='1' else False
    rst['SolarInput1VoltageTooHigher']= True if s[2]=='1' else False
    rst['SolarInput2VoltageTooHigher']= True if s[3]=='1' else False
    rst['BatteryUnder']= True if s[4]=='1' else False
    rst['BatteryLow']= True if s[5]=='1' else False
    rst['BatteryOpen']= True if s[6]=='1' else False
    rst['BatteryVoltageTooHigher']= True if s[7]=='1' else False
    rst['BatteryLowInHybirdMode']= True if s[8]=='1' else False
    rst['GridVoltageHighLoss']= True if s[9]=='1' else False
    rst['GridVoltageLowLoss']= True if s[10]=='1' else False
    rst['GridFrequenceHighLoss']= True if s[11]=='1' else False
    rst['GridFrequenceLowLoss']= True if s[12]=='1' else False
    rst['ACInputLong-TimeAverageVoltageOver']= True if s[13]=='1' else False
    rst['ACInputVoltageLoss']= True if s[14]=='1' else False
    rst['ACInputFrequencyLoss']= True if s[15]=='1' else False
    rst['ACInputIsland']= True if s[16]=='1' else False
    rst['ACInputPhaseDislocation']= True if s[17]=='1' else False
    rst['OverTemperature']= True if s[18]=='1' else False
    rst['OverLoad']= True if s[19]=='1' else False
    rst['EPOActive']= True if s[20]=='1' else False
    rst['ACInputWaveLoss']= True if s[21]=='1' else False

    return rst    
    
def _FLAG(s):
    rst={}
    rst['MuteBuzzerBeep']= True if s[0]=='1' else False
    rst['MuteBuzzerBeepInStandbyMode']= True if s[1]=='1' else False
    rst['MuteBuzzerBeepOnlyOnBatteryDischargedStatus']= True if s[2]=='1' else False
    rst['GeneratorAsACInput']= True if s[3]=='1' else False
    rst['WideACInputRange']= True if s[4]=='1' else False
    rst['N/G relay Function']= True if s[5]=='1' else False
    return rst
def _T(s):
    rst={}
    
    rst['Year'] =s[0]
    rst['Month'] =s[1]
    rst['Day']=s[2]
    rst['Hour']=s[3]
    rst['Minute']=s[4]
    rst['Second']=s[5]
    
    return rst

