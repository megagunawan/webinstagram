#! /usr/bin/env python

import os
import cgi
import cgitb
import sys
import mysql.connector
import Cookie
from datetime import datetime, date

if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ.get('HTTP_COOKIE')
    cookie = Cookie.SimpleCookie()
    cookie.load(cookie_string)
    try:
        username = cookie['user'].value
        cookie_flag = 1
    except KeyError:
        cookie_flag = 0

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

body = """
        <form method="post" action="signup.py">
            <div class="registerform">
                <input type="text" placeholder="Enter username" name="username" required>
                <input type="password" placeholder="Enter password" name="password" required>
                <input type="password" placeholder="Retype password" name="password2" required>
                <button type="submit">Create</button>
            </div>
        </form>"""

if(cookie_flag == 1):
    body = """You have logged in, return to <a href="index.py">index page</a>."""
else:
    if "username" not in form or "password" not in form or "password2" not in form:
        body += "Please fill in the information"
    else:
        user_name = form["username"].value
        pw = form["password"].value
        pw2 = form["password2"].value
        if (pw != pw2):
            body += "Password does not match"
        else:
            cursor.execute("select count(*) from users where username='"user_name+"';")
            result = cursor.fetchone()
            if (result[0] != 0):
                body += "Username is already taken"
            else:
                cursor.execute("insert into users(username, password) values ('"+user_name+"','"+pw+"');")
                conn.commit()
                body = """Registration success, <a href="login.py">Login</a> or return to <a href="index.py">index page</a>."""

print header
print body
print footer