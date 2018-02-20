#! /usr/bin/env python

import cgi
import cgitb
import time
import os
import Cookie

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

try:
	queryString = os.environ['QUERY_STRING']
	array = queryString.split('&')
	user_input = {}
	for s in array:
		tmp = s.split('=')
		user_input[tmp[0]] = tmp[1].replace('+', ' ')
	qs_dict = user_input
except:
	pass

haveId = False
haveFilter = False
haveRemove = False
haveSubmit = False

if(qs_dict['id']):
	haveId = True

if(qs_dict['filter'] and int(qs_dict['filter']) >= 1 and int(qs_dict['filter']) <= 4):
	haveFilter = True
	filter_set = int(qs_dict['filter'])

if(qs_dict['remove'] and int(qs_dict['remove']) == 1):
	haveRemove = True

if(qs_dict['submit'] and int(qs_dict['submit']) == 1):
	haveSubmit = True

if(cookie_flag != 1):
	body = """You need to <a href="login.py">login</a> first."""
elif(not haveId):
	body = """image id missing. Return to <a href="index.py">index page</a>"""
else:
	cursor.execute("select count(*) from images where imageid='" + qs_dict['id'] + "';")
	result = cursor.fetchone()
	if(result[0] != 1):
		body += "image not found"
	else:
		filename = qs_dict['id']
		cursor.execute("select ext from images where imageid='" + qs_dict['id'] + "';")
		result = cursor.fetchone()
		filetype = str(result[0])
		cursor.execute("select count(*) from images where imageid='" + qs_dict['id'] + "' and disable=1;")
		result = cursor.fetchone()
		if(result[0] != 1):
			body += "Image on server already, return to <a href='index.py'>Homepage</a>."
		else:
			if(haveRemove):
				try:
					os.remove(TARGET + filename + '.' + filetype)
					os.remove(TARGET + filename + '1.' + filetype)
					os.remove(TARGET + filename + '2.' + filetype)
					os.remove(TARGET + filename + '3.' + filetype)
					os.remove(TARGET + filename + '4.' + filetype)
				except:
					pass
				cursor.execute("delete from images where imageid'" + qs_dict['id'] + "';")
				conn.commit()
				body += "Image removed, return to <a href='index.py'>index page</a>."
			elif(haveSubmit):
				if(haveFilter):
					try:
						os.remove(TARGET + filename + '.' + filetype)
						if(filter_set != 1):
							os.remove(TARGET + filename + '1.' + filetype)
						if(filter_set != 2):
							os.remove(TARGET + filename + '2.' + filetype)
						if(filter_set != 3):
							os.remove(TARGET + filename + '3.' + filetype)
						if(filter_set != 4):
							os.remove(TARGET + filename + '4.' + filetype)
						os.rename(TARGET + filename + str(filter_set) + '.' + filetype, TARGET + filename + '.' + filetype)
					except:
						pass
				else:
					try:
						os.remove(TARGET + filename + '1.' + filetype)
						os.remove(TARGET + filename + '2.' + filetype)
						os.remove(TARGET + filename + '3.' + filetype)
						os.remove(TARGET + filename + '4.' + filetype)
					except OSError:
						pass
				cursor.execute("update images set disable=0 where imageid='" + qs_dict['id'] + "';")
				conn.commit()
				body += "Image published, return to <a href='index.py'>index page</a><br>"
				body += "<img src='../images/{0}.{1}'>".format(qs_dict['id'], filetype)
				body += "<br>permalink: <a href='../images/{0}.{1}'>../images/{0}.{1}</a>".format(qs_dict['id'], filetype)
			else:
				body += "Preview:"
				body += "<div class='uploaded-image'><img src='../upload/" + qs_dict['id']
				if(haveFilter):
					body += qs_dict['filter']
				body += '.' + filetype + "'></div><br>"
				body += "<a href='edit.py?id=" + qs_dict['id'] + "'><button>No Filter</button></a> "
				body += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=1'><button>Border</button></a> "
				body += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=2'><button>Lomo</button></a> "
				body += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=3'><button>B & W</button></a> "
				body += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=4'><button>Blur</button></a>"
				body += "<br><br><br>"
				body += "<a href='edit.py?id=" + qs_dict['id'] + "&remove=1'><button>Discard</button></a> "
				body += "<a href='edit.py?id=" + qs_dict['id'] + "'><button type='button' class='btn btn-warning'"
				if(not haveFilter):
					body += " disabled"
				body += ">Undo</button></a> "
				body += "<a href='edit.py?id=" + qs_dict['id'] + "&submit=1"
				if(haveFilter):
					body += "&filter=" + qs_dict['filter']
				body += "'><button>Publish</button></a>"

cgitb.enable()

print header
print body
print footer