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
    cursor = connection.cursor()
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

    cursor.close()

    return jsonify(retobj)

@app.route('/addRoutine',methods=['GET', 'POST'])
def addRoutine():
    content = request.json
    cursor = connection.cursor()
    t_id = "'" + content["teacher_id"] + "',"
    t_id1 ="'" + content["teacher_id"] + "'"
    t_id2 = content["teacher_id"]
    sub = "'" + content["subject_code"] + "',"
    clas = "'" + content["class_code"] + "',"
    clas1 = content["class_code"] 
    day = "'" +  content["day"] + "',"
    time_begin = "'" + content["time_begin"] +"',"
    time_end = "'" + content["time_end"] + "')"

    # find whether the teacher exists
    q = "select id from teacher where id=" + t_id1
    cursor.execute(q)
    data = cursor.fetchall()
    if(len(data)==0):
        retobj = {"status": "Teacher does not exist"}
        return jsonify(retobj)

    cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
    data = cursor.fetchall()
    f=0
    res_list = [x[0] for x in data]
    for row in res_list:
        print(row,(clas1+"_"+t_id2).lower())
        if(row == (clas1+"_"+t_id2).lower()):
            f=1
            break
    if f == 0:
        q2 = "select * INTO " + clas1 + "_" +  t_id2 + "  from  " + clas1
        cursor.execute(q2)
    
        
    query = "insert into routine values(" + t_id + sub + clas + day + time_begin + time_end 
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}
    
    cursor.close()


    return jsonify(retobj)

@app.route('/addsubject',methods=['GET', 'POST'])
def addsubject():
    content = request.json
    cursor = connection.cursor()
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
    
    cursor.close()
        
    return jsonify(retobj)

@app.route('/addClass',methods=['GET', 'POST'])
def addClass():
    content = request.json
    cursor = connection.cursor()
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
        
    cursor.close()
    return jsonify(retobj)

@app.route('/addTeacher',methods=['GET', 'POST'])
def addTeacher():
    content = request.json
    cursor = connection.cursor()
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

    cursor.close()
        
    return jsonify(retobj)

@app.route('/addStudent',methods=['GET', 'POST'])
def addStudent():
    content = request.json
    cursor = connection.cursor()
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

    
    cursor.close()
        
    return jsonify(retobj)

@app.route('/createClass',methods=['GET', 'POST'])
def createClass():
    content = request.json
    cursor = connection.cursor()
    code = content["code"] 
    query = "create table " + code + " (id varchar(20), name varchar(20), total integer default(0))"
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}

    cursor.close()
        
    return jsonify(retobj)

@app.route('/addAttendancedate',methods=['GET', 'POST'])
def addAttendancedate():
    content = request.json
    cursor = connection.cursor()
    date = "dt_" + str(content['date'])
    clas = content['class_code'].lower()
    t_id = content['teacher_id'].lower()
    table = clas + "_" + t_id

    query = "Alter table " + table + " add column " + date  + " int " + "Default(0)"
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}

    cursor.close()

    return jsonify(retobj)

@app.route('/addAttendance',methods=['GET', 'POST'])
def addAttendance():
    content = request.json
    cursor = connection.cursor()
    date = "dt_" + str(content['date'])
    clas = content['class_code'].lower()
    t_id = content['teacher_id'].lower()
    table = clas + "_" + t_id
    s_id = "'" + content['student_id'] + "'"


    query = "update " + table + " set " + date + "=1, total=total+1 " + " where id=" +  s_id
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        retobj = {"status": "done"}
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting PostgreSQL table", error)
        retobj = {"status": "Error"}

    cursor.close()

    return jsonify(retobj)

@app.route('/returnattendance',methods=['GET', 'POST'])
def returnAttendance():
    content = request.json
    cursor = connection.cursor()
    clas = content['class_code'].lower()
    t_id = content['teacher_id']
    s_id = "'" + content['student_id'] + "'"
    
    table = clas + "_" + t_id
    q1 = "select total from " + table + " where id=" +  s_id 
    cursor.execute(q1)
    data = cursor.fetchall()
    print(data[0][0])
    tot = data[0][0]

    q2 = "SELECT count(*) FROM information_schema.columns WHERE table_name = " + "'" + table + "'"
    cursor.execute(q2)
    d2 = cursor.fetchall()
    print(d2[0][0])
    col = d2[0][0] - 3
    ans = (tot/col)*100

    connection.commit()
    retobj = {"percent": ans}
    
    cursor.close()

    return jsonify(retobj)

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345



    app.run(port=port)
