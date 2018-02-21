#! /usr/bin/env python

import cgi
import cgitb
import os
import sys
import random
import string
import Cookie
import magic
import mysql.connector
from mysql.connector import errorcode

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

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
PREV_FOLDER = os.path.abspath(os.path.join(THIS_FOLDER, os.pardir))
filename = ''
filetype = ''
TARGET = PREV_FOLDER + '/images/'

if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ.get('HTTP_COOKIE')
    cookie = Cookie.SimpleCookie()
    cookie.load(cookie_string)
    try:
        username = cookie['user'].value
        cookie_flag = 1
    except KeyError:
        cookie_flag = 0

db = conn.connect(user='root', password='', host='localhost', port='3306', database='webinstagram')
cursor = db.cursor()

query_string = os.environ['QUERY_STRING']
array = query_string.split('&')
user_input = {}
for s in array:
	tmp = s.split('=')
	user_input[tmp[0]] = tmp[1].replace('+', ' ')
query = user_input

if(cookie_flag != 1):
	body = """You need to <a href="login.py">login</a> first."""
elif(not haveId):
	body = """image id missing. Return to <a href="index.py">index page</a>"""
else:
	cursor.execute("select count(*) from images where imageid='" + query['id'] + "';")
	result = cursor.fetchone()
	if(result[0] != 1):
		body += "image not found"
	else:
		filename = query['id']
		cursor.execute("select imgtype from images where imageid='" + query['id'] + "';")
		result = cursor.fetchone()
		filetype = str(result[0])
		cursor.execute("select count(*) from images where imageid='" + query['id'] + "' and disable=1;")
		result = cursor.fetchone()
		if(result[0] != 1):
			body += "Image on server already, return to <a href='index.py'>Homepage</a>."
		else:
			if(int(query['remove']) == 1):
				try:
					os.remove(TARGET + filename + '.' + filetype)
					os.remove(TARGET + filename + '1.' + filetype)
					os.remove(TARGET + filename + '2.' + filetype)
					os.remove(TARGET + filename + '3.' + filetype)
					os.remove(TARGET + filename + '4.' + filetype)
					os.remove(TARGET + filename + '5.' + filetype)
				except:
					pass
				cursor.execute("delete from images where imageid'" + query['id'] + "';")
				conn.commit()
				body += "Image removed, return to <a href='index.py'>index page</a>."
			elif(int(query['submit']) == 1):
				if(int(query['filter']) >= 1 and int(query['filter']) <= 5):
					os.remove(TARGET + filename + '.' + filetype)
					if(img_filter != 1):
						os.remove(TARGET + filename + '1.' + filetype)
					if(img_filter != 2):
						os.remove(TARGET + filename + '2.' + filetype)
					if(img_filter != 3):
						os.remove(TARGET + filename + '3.' + filetype)
					if(img_filter != 4):
						os.remove(TARGET + filename + '4.' + filetype)
					if(img_filter != 5):
						os.remove(TARGET + filename + '5.' + filetype)
					os.rename(TARGET + filename + str(img_filter) + '.' + filetype, TARGET + filename + '.' + filetype)
				else:
					os.remove(TARGET + filename + '1.' + filetype)
					os.remove(TARGET + filename + '2.' + filetype)
					os.remove(TARGET + filename + '3.' + filetype)
					os.remove(TARGET + filename + '4.' + filetype)
					os.remove(TARGET + filename + '5.' + filetype)

				cursor.execute("update images set disable=0 where imageid='" + query['id'] + "';")
				conn.commit()
				body += "Image published, return to <a href='index.py'>index page</a><br>"
				body += "<img src='../images/{0}.{1}'>".format(query['id'], filetype)
				body += "<br>permalink: <a href='../images/{0}.{1}'>../images/{0}.{1}</a>".format(query['id'], filetype)
			else:
				body += "Preview:"
				body += "<img src='../upload/" + query['id']
				if(int(query['filter']) >= 1 and int(query['filter']) <= 5):
					body += query['filter']
				body += '.' + filetype + "'></div><br>"
				body += "<a href='edit.py?id=" + query['id'] + "'><button>No Filter</button></a> "
				body += "<a href='edit.py?id=" + query['id'] + "&filter=1'><button>Border</button></a> "
				body += "<a href='edit.py?id=" + query['id'] + "&filter=2'><button>Lomo</button></a> "
				body += "<a href='edit.py?id=" + query['id'] + "&filter=3'><button>B & W</button></a> "
				body += "<a href='edit.py?id=" + query['id'] + "&filter=4'><button>Blur</button></a>"
				body += "<a href='edit.py?id=" + query['id'] + "&filter=5'><button>Lens Flare</button></a>"
				body += "<br><br><br>"
				body += "<a href='edit.py?id=" + query['id'] + "&remove=1'><button>Discard</button></a> "
				body += "<a href='edit.py?id=" + query['id'] + "'><button type='button'"
				if(not (int(query['filter']) >= 1 and int(query['filter']) <= 5)):
					body += " disabled"
				body += ">Undo</button></a> "
				body += "<a href='edit.py?id=" + query['id'] + "&submit=1"
				if(int(query['filter']) >= 1 and int(query['filter']) <= 5):
					body += "&filter=" + query['filter']
				body += "'><button>Save</button></a>"

cgitb.enable()

print header
print body
print footer