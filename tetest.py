import protocol.Infinite_PCS as proto
import protocol.GoodWe_ES as goodwe
aar = proto.createInstance()
bbr = goodwe.createInstance()
bbr.setMaxOutputPower(1000)
aar.bindRemote("192.168.0.100",20001)
print(aar.timeStamp())