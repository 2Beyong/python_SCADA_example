import DBOperation

db =DBOperation.DBOperation()

db.OpenDB("./test.db") #测试数据库
print(db.getPairs())
db.addPair(1,"a","b","c")
db.addPair(2,"a","bsd","csd")
print(db.getPairs())
db.delPair(1)
db.updatePair(2,"GoodWe 5kw ES","INV","GoodWe_es_v3")
print(db.getPairs())

