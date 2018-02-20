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

try:
  query_string = os.environ['QUERY_STRING']
  array = query_string.split('&')
  user_input = {}
  for s in array:
    temp = s.split('=')
    user_input[temp[0]] = temp[1].replace('+', ' ')
  qs_dict = user_input
except:
  pass

if(cookie_flag == 1):
  cursor.execute("select userid from users where username='"+username+"';")
  result = cursor.fetchone()
  command = ("select count(*) from image where (disable=0 and private = 0) or (private=1 and disable=0 and userid="+str(result[0])+");")
else:
  command = ("select count(*) from image where (disable=0 and private=0);")
cursor.execute(command)
result = cursor.fetchone()
max_page = int(math.ceil((result[0])/8))
if (max_page < 1):
  max_page = 1

try:
  if(qs_dict['page'] and int(qs_dict['page']) >= 1 and int(qs_dict['page']) <= max_page):
    page_set = int(qs_dict['page'])
  else:
    page_set = 1
except:
  page_set = 1

if(not page_set):
  page_set = 1

page_offset = (page_set-1)*8
if(cookie_flag == 1):
  command = ("select username, imageid, imgtype, timestamp from users, images where (users.userid=image.userid) and ((disable=0 and private=0) or (private=1 and disable=0 and image.userid=" + str(result[0]) + ")) order by timestamp desc limit 8 offset " + str(page_offset) + ";")
else:
  command = ("select username, imageid, imgtype, timestamp from users, images where (users.userid=image.userid) and (disable=0 and private=0) order by timestamp desc limit 8 offset " + str(page_offset) + ";")
cursor.execute(command)

if(cookie_flag == 1):
  body += "<button href="login.py">Logout</button>"
  body += "<button href="changepassword.py">Change Password</button>"
  body += "<p>Welcome " + username + "</p>"
else:
  body += "<button href="login.py">Login</button>"

for (username, imageid, imgtype, timestamp) in cursor:
  body += ("""
      <div class="polaroid"><img src='../images/{0}.{1}'>
      <div class="container">
        User: {2}
        <br>
        Link: <a href='../images/{0}.{1}'>../images/{0}.{1}</a></p>
      </div>
    </div>""".format(imageid, imgtype, username))

body += "<br><br>"
body += "<div class='pagination'>"
for i in range(1, max_page+1):
  body += "<a href='index.py?page=" + str(i) + "'>" + str(i) + "</a>"
body += "</div>"

if (cookie_set == 1):
  body += """
          <form action="upload.py" method="POST" enctype="multipart/form-data" style="display: inline;">
            <input name="file" type="file" style="margin-right: 30px;">
            <input type="radio" checked="checked" name="mode" value="public"><span class="checkmark" style="margin-right: 5px;"></span>Public
            <input type="radio" name="mode" value="private"><span class="checkmark" style="margin-right: 5px;"></span>Private
            <button class="button" type="submit>Upload</button>
          </form>"""

print header
print body
print footer