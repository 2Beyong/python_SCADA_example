
import sqlite3
print("hello")

'''
这个类的作用是提供对内置数据库Sqlite的增删改查的一层封装，
对于以下几个表的操作的简化:
    端口-设备绑定表:port_device_pair
        |__ port: int prime
        |__ device: text
        |__ type: text
        |__ protocol: text
    历史记录表:hitstory_record
        |__ time: text
        |__ port: int
        |__ power: float

'''
'''
    test.db参考
    CREATE TABLE hitstory_record (
    time  DATETIME,
    port  INTEGER  REFERENCES port_device_pair (port),
    power REAL
);
'''
'''
    基本的操作，首先是打开本地数据库，假设连接叫conn
    然后弄出一个游标，
    游标执行sql语句，
    conn要执行commit(关键!)
    不然修改只对内存中的cursor有效。

    SQLite允许多方同时读取，但是只有单方可以写入，所以未来需要以事务的形式，拓展DBOperation的功能，

    目前的记录，最快每秒插入16条数据
'''
class DBOperation:
    '数据库操作'
    def __init__(self):
        self.conn =[]
        self.cursor=[]
    def OpenDB(self,dbpath):
        self.conn = sqlite3.connect(dbpath)
    
    def Close(self):
        self.conn.close()
    
    def addPair(self,port,device,_type,protocol):
        self.cursor = self.conn.cursor()
        try:
            sql = ''' insert into port_device_pair
                  (port, device, type,protocol)
                  values
                  (:m_port, :m_device,:m_type, :m_protocol)'''

            self.cursor.execute(sql,{'m_port':port,'m_device':device,"m_type":_type,"m_protocol":protocol})
            self.conn.commit()
        except:
            print("Error - addPair")
        else:
            self.cursor.close()


    def getPairs(self): #返回全部结果
        self.cursor = self.conn.cursor()

        sql='''select * from port_device_pair'''
        result = self.cursor.execute(sql)
        rst = result.fetchall()
        self.cursor.close()
        return rst
    def delPair(self,port):
        self.cursor = self.conn.cursor()
        sql =''' delete from port_device_pair where port=(:m_port)'''
        self.cursor.execute(sql,{'m_port':port})
        self.conn.commit()
        self.cursor.close()
    def updatePair(self,port,device,_type,protocol):    
        self.delPair(port)
        self.addPair(port,device,_type,protocol)


