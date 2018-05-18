# flask测试
FLASK_DEBUG =1
from flask import Flask,Response

import json

app = Flask(__name__)

g_nodeList=[]

@app.route('/')
def hello_world():
    return 'Hello Flask!'

@app.route('/CommonStatus')
def CommonStatus():
    dick ={
        'todayProduct':5,
        'linePower':1345,
        'batteryCap':97.75,
        'isOnline':1, # 0 = off 1= on 并网
    }
    resp = Response(json.dumps(dick), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
@app.route('/Config')
def Config():
    fo = open("config.json",'r')
    rst = fo.read()
    fo.close()
    return Response(rst, mimetype='application/json')

@app.route('/test1')
def printNode():
    rst=[]
    global g_nodeList
    for i in g_nodeList:
        k={
            "name": i.name, 
            "type": i.type, 
            "describe": i.describe, 
            "port": i.port, 
            "proto":i.proto,
            "data":i.data
        }
        rst.append(k)
    
    return Response(json.dumps(rst), mimetype='application/json')

if __name__ == '__main__':
    app.run()

def setSource(ndL):
    print(ndL)
    global g_nodeList
    g_nodeList=ndL
    

def testRun():
    app.run()