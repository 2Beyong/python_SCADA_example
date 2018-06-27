import protocol
import protocol.Infinite_PCS
print(protocol.Infinite_PCS)
#bbr = protocol.Infinite_PCS.createInstance()
exec('import protocol.{0}'.format('Infinite_PCS'))
#aar = protocol.Infinite_PCS.createInstance()
aar = eval('protocol.{0}.createInstance()'.format("Infinite_PCS"))

print(aar.timeStamp())