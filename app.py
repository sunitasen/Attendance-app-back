import flask
from markdown import markdown
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
import time
from datetime import datetime
import psycopg2

try:
    DATABASE_URL = os.environ['DATABASE_URL']

    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while connecting PostgreSQL", error)

app = Flask(__name__)
CORS(app)

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

@app.route('/getTeacherRoutine',methods=['GET', 'POST'])
def getTeacherRoutine():
    content = request.json
    id = content["id"]
    query = "select * from routine where teacher_id=" + "'" + id + "'"
    print(query)
    cursor.execute(query)
    data = cursor.fetchall()
    sub = ""
    clas = ""
    day = ""
    dat = {}
    i = 0
    for row in data:
        sub = row[3]
        clas = row[4]
        day = row[5]
        dict = {"sub":sub, "class":clas, "day":day}
        arg = str(i)
        dat[i] = dict
        i+=1
    
    retobj = {"data": dat}

    return jsonify(retobj)

@app.route('/addRoutine',methods=['GET', 'POST'])
def addRoutine():
    content = request.json
    t_id = "'" + content["teacher_id"] + "',"
    sub = "'" + content["subject_code"] + "',"
    clas = "'" + content["class_code"] + "',"
    day = "'" +  content["day"] + "',"
    time_begin = "'" + content["time_begin"] +"',"
    time_end = "'" + content["time_end"] + "')"
    query = "insert into routine values(" + t_id + sub + clas + day + time_begin + time_end 
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}

    return jsonify(retobj)

@app.route('/addsubject',methods=['GET', 'POST'])
def addsubject():
    content = request.json
    a = 9
    code = "'" + content["code"] + "',"
    name = "'" + content["name"] + "')"
    query = "insert into subject values(" + code + name 
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}
        
    return jsonify(retobj)

@app.route('/addClass',methods=['GET', 'POST'])
def addClass():
    content = request.json
    code = "'" + content["code"] + "',"
    name = "'" + content["name"] + "')"
    query = "insert into class values(" + code + name  
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}
        
    return jsonify(retobj)

@app.route('/addTeacher',methods=['GET', 'POST'])
def addTeacher():
    content = request.json
    code = "'" + content["id"] + "',"
    name = "'" + content["name"] + "',"
    department = "'" + content["department"] + "')"
    query = "insert into teacher values(" + code + name + department
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}
        
    return jsonify(retobj)

@app.route('/addStudent',methods=['GET', 'POST'])
def addStudent():
    content = request.json
    code = content["code"] 
    id = "'" + content["id"] + "',"
    name = "'" + content["name"] + "')"
    query = "insert into " + code +" values(" + id + name
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}
        
    return jsonify(retobj)

@app.route('/createClass',methods=['GET', 'POST'])
def createClass():
    content = request.json
    code = content["code"] 
    query = "create table " + code + " (id varchar(20), name varchar(20))"
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}
        
    return jsonify(retobj)

@app.route('/addAttendance',methods=['GET', 'POST'])
def addAttendance():
    content = request.json
    date = "dt_" + str(content['date'])
    code = content['code']
    query = "Alter table " + code + " add column " + date  + " int " + "Default(0)"
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}

    return jsonify(retobj)

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345



    app.run(port=port)
