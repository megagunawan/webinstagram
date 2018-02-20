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

db = conn.connect(user='root', password='', host='localhost', port='8080', database='webinstagram')
cursor = db.cursor()
cgitb.enable()
form = cgi.FieldStorage()

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
		<form method="post" action="changepassword.py">
			<div class="form-group">
	     			<input name="oldpassword" type="password" class="form-control" placeholder="old password" required>
	     			<input name="password" type="password" class="form-control" placeholder="password">
	     			<input name="password2" type="password" class="form-control" placeholder="Retype password">
	 		<button type="submit">Change Password</button>
	 	</form>"""

if(cookie_flag == 0):
	body = """You need to <a href="login.py">login</a> first."""
else:
	if "oldpassword" not in form or "password" not in form or "password2" not in form:
		body += "Please fill in all the information."
	else:
		old_pw = form["oldpassword"].value
		new_pw = form["password"].value
		new_pw2 = form["password2"].value
		if (old_pw == new_pw):
			body += "Old and new password are the same"
		elif (new_pw != new_pw2):
			body += "New passwords do not match"
		else:
			cursor.execute("select password from users where username='"+username+"';")
			result = cursor.fetchone()
			if(str(result[0]) != old_pw):
				body += "Old password is wrong"
			else:
				cursor.execute("update users set password='" + new_pw + "' where username='" + username + "';")
				conn.commit()
				body = """Success updating password, return to <a href="index.py">index</a> page"""

print header
print body
print footer