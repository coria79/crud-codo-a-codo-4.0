
#from importlib.metadata import requires
#from turtle import update
from flask import Flask
from flask import render_template, request, redirect, send_from_directory, url_for,flash
from flaskext.mysql import MySQL

from datetime import datetime

import os

app=Flask(__name__)
app.secret_key="SecretKey"

mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='EmployeeSystem'

mysql.init_app(app)

FOLDER=os.path.join('uploads')
app.config['FOLDER']=FOLDER

@app.route('/uploads/<namePhoto>')
def uploads(namePhoto):
    return send_from_directory(app.config['FOLDER'],namePhoto)

@app.route('/')
def index():

    sql="SELECT * FROM `employee`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    _employees=cursor.fetchall()
    print(_employees)
    conn.commit()

    return render_template('employees/index.html', employees=_employees)


@app.route('/create')
def create():
    return render_template('employees/create.html')

@app.route('/store', methods=['POST'])
def store():

    _name=request.form['txtname']
    _email=request.form['txtemail']
    _photo=request.files['txtphoto']

    if _name=='' or _email=='' or _photo=='':
        flash('All fields must me completed')
        return redirect(url_for('create'))


    now=datetime.now()
    tempo=now.strftime("%Y%H%M%S")
    
    if _photo.filename != '':
        newNamePhoto=tempo + _photo.filename
        _photo.save("uploads/"+newNamePhoto)

    #datos=(_name, _email, _photo.filename)
    datos=(_name, _email, newNamePhoto)

    sql="INSERT INTO employee(name, email, photo)VALUES(%s,%s,%s);"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #return render_template('employees/index.html')
    return redirect('/')    


@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("SELECT photo FROM EmployeeSystem.employee WHERE id=%s;",(id))
    _row=cursor.fetchall()
    os.remove(os.path.join(app.config['FOLDER'],_row[0][0]))    

    cursor.execute("DELETE FROM EmployeeSystem.employee WHERE id=%s;",(id))
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM EmployeeSystem.employee WHERE id=%s;",(id))
    _employees=cursor.fetchall()
    conn.commit()

    return render_template('employees/edit.html', employees=_employees)

@app.route('/update', methods=['POST'])
def update():
    _name=request.form['txtname']
    _email=request.form['txtemail']
    _photo=request.files['txtphoto']
    id=request.form['txtid']

    #sql="UPDATE EmployeeSystem.employee SET name=%s, email=%s, photo=%s WHERE id=%s;"
    sql="UPDATE EmployeeSystem.employee SET name=%s, email=%s WHERE id=%s;"

    #datos=(_name, _email, _photo.filename)
    #datos=(_name, _email, newNamePhoto, id)
    datos=(_name, _email, id)

    conn=mysql.connect()
    cursor=conn.cursor()

    now=datetime.now()
    tempo=now.strftime("%Y%H%M%S")
    
    if _photo.filename != '':
        newNamePhoto=tempo + _photo.filename
        _photo.save("uploads/"+newNamePhoto)
    else:
        newNamePhoto=_photo.filename


    cursor.execute("SELECT photo FROM EmployeeSystem.employee WHERE id=%s;",(id))
    _row=cursor.fetchall()
    os.remove(os.path.join(app.config['FOLDER'],_row[0][0]))
    cursor.execute("UPDATE EmployeeSystem.employee SET photo=%s WHERE id=%s;",(newNamePhoto, id))

    datos=(_name, _email, newNamePhoto)

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')





if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='127.0.0.1',port=5001,debug=True)