# flask测试
FLASK_DEBUG =1
from flask import Flask,Response
from flask import render_template
import json
import random
import math
app = Flask(__name__,static_folder='build', static_url_path='/')

g_nodeList=[]


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/CommonStatus')
def CommonStatus():
    dick ={
        'todayProduct':round( 5+ random.random()*3,2),
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

@app.route('/Nodes/')
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
        
    T =Response(json.dumps(rst), mimetype='application/json')
    T.headers['Access-Control-Allow-Origin'] = '*'
    return T;


@app.route('/Nodes/RunningData')
def sendNodeRunningData():
    rst=[]
    global g_nodeList
    for i in g_nodeList:
        k=i.data
        
        rst.append(k)
    
    T =Response(json.dumps(rst), mimetype='application/json')
    T.headers['Access-Control-Allow-Origin'] = '*'
    return T;
if __name__ == '__main__':
    app.run()

def setSource(ndL):
    print(ndL)
    global g_nodeList
    g_nodeList=ndL
    

def testRun():
    app.run(host="0.0.0.0", port=5000)