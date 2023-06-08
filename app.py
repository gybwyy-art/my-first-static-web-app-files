from multiprocessing import connection
from flask import Flask, render_template, request
import sqlite3
import os
import json
app = Flask(__name__)
fileRootPath = 'static'
db = {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update',methods=['POST','GET'])
def updatek():
    if (request.method=='POST'):
        form = request.form

        file = request.files['file']
        file.save(os.path.join(fileRootPath,form["username"]+"_"+file.filename))
        print(file)
        print(form)
        db[form['username']] = {
            "username": form['username'],
            "type" : form['type'],
            "desc" : form['desc'],
            "fileName":form["username"]+"_"+file.filename,
        }
       
        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4) # 缩进4个空格
    return render_template('index.html')
@app.route('/getlist',methods=['POST','GET'])
def getList():
    itemList = []
    for item in db:
        itemList.append(db[item])
    return {
        "code":0,
        "data":itemList,
    }
@app.route('/getText',methods=['POST','GET'])
def getText():
    fileName = request.args['fileName']
    textContent = []
    with open('static/'+fileName,'r') as f:
        textContent = f.readlines()
    return {
        "code":0,
        "data":{
            'content':textContent,
        },
    }
@app.route('/delete',methods=['POST','GET'])
def delete():
    username = request.args['username']
    os.remove(os.path.join(fileRootPath,db[username]["fileName"]))
    del db[username]
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4) # 缩进4个空格
    return {
        "code":0,
        "data":{},
    }


if __name__ =="__main__":
    with open('db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
        app.run(debug=True)
