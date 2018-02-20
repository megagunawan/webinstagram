#! /usr/bin/env python

import cgi
import cgitb
import time
import os
import Cookie
import mysql.connector
from mysql.connector import errorcode

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

body = """<h5><a href="register.py">Register</a> an account</h5>
            	<form method="post" action="login.py">
                	<div class="loginform">
                	    <input type="text" placeholder="Enter username" name="username" required>
                	    <input type="password" placeholder="Enter password" name="password" required>
                	    <button type="submit">Login</button>
                	</div>
            	</form>"""

if(cookie_flag == 1):
	cookie = Cookie.SimpleCookie()
    cookie["user"] = ""
    cookie["user"]["expires"] = \
        expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
	body = """Logout success, return to <a href="index.py">index page</a>."""
else:
	if "username" not in form or "password" not in form:
		body += "Please fill in all the information."
	else:
		user_name = form["username"].value
		pw = form["password"].value
		cursor.execute("select count(*) from users where username'"+user_name+"';")
		result = cursor.fetchone()
		if(result[0] == 0):
			body += """There is no user with such username. <a href="register.py">Sign up</a>?"""
		else:
			cursor.execute("select password from users where username='"+user_name+"';")
			result = cursor.fetchone()
			if(str(result[0]) != pw):
				body += "Wrong Password"
			else:
				cookie = Cookie.SimpleCookie()
				cookie['user'] = user_name
    			cookie["user"]["expires"] = 3600
				body = """Login success, return to <a href="index.py">index page</a>."""

print header
print body
print footer