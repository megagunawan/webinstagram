#! /usr/bin/env python

import cgi
import cgitb
import time
import os
import random
import Cookie
import shutil
import mysql.connector as conn
from mysql.connector import errorcode

cgitb.enable()
form = cgi.FieldStorage()
db = conn.connect(user='root', password='', host='localhost', port='3306', database='webinstagram')
cursor = db.cursor()

header = """Content-type:text/html\n\n
            <!DOCTYPE html>
            <html lang='en'>
                <head>
                    <meta charset='utf-8'/>
                    <title>web instagram</title>
                    <link rel="stylesheet" href="../style.css">
                </head>
                <body>
                    <div class="heading"><a href="index.py"><h3>web instagram</h3></a></div>"""

footer = """</body></html>"""
body = ""

flag = 0
if "password" not in form:
	flag = 1
	body += "Please fill in the password."
else:
	pw = form["password"].value

if flag == 0:
    cursor.execute("create database if not exists webinstagram")
    cursor.execute("create table if not exists admin(password varchar(32) not null unique);")
    conn.commit()
    cursor.execute("select count(*) from admin;")
    result = cursor.fetchone()
	if(result[0] == 0):
		cursor.execute("insert into admin values('"+pw+"');")
		conn.commit()
	else:
		try:
			cursor.execute("select password from admin")
			result = cursor.fetchone()
			if(str(result[0]) != pw):
				flag = 1
				body += "Password incorrect."
		except:
			flag = 1
			body += "Fail to authenticate admin."

if flag != 1:
	cookie = Cookie.SimpleCookie()
    cookie["user"] = ''
    cookie["user"]["expires"] = \
        expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    
	cursor.execute("drop table if exists images;")
	conn.commit()
	cursor.execute("drop table if exists users;")
	conn.commit()
	cursor.execute("create table if not exists users(userid int not null AUTO_INCREMENT, username varchar(10) not null unique, password varchar(32) not null, PRIMARY KEY (userid));")
	conn.commit()
	cursor.execute("create table images(imageid varchar(5) not null unique, userid int not null, imgtype varchar(3) not null, timestamp timestamp not null default CURRENT_TIMESTAMP, private boolean not null default 0, disable boolean not null default 1, PRIMARY KEY (imageid), FOREIGN KEY (userid) REFERENCES users(userid));")
	conn.commit()

	THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
	PREV_FOLDER = os.path.abspath(os.path.join(THIS_FOLDER, os.pardir))
	TARGET = PREV_FOLDER + '/images'
	for f in os.listdir(TARGET):
		path = os.path.join(TARGET, f)
		try:
			if os.path.isfile(path):
				os.unlink(path)
		except Exception as e:
			print(e)

if flag != 1:
	body += "System initialization done, return to <a href='index.py'>index page</a><br>"

print header
print body
print footer