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

UPLOAD_DIR = './images'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
PREV_FOLDER = os.path.abspath(os.path.join(THIS_FOLDER, os.pardir))
file_name = ''
file_ext = ''
TARGET = PREV_FOLDER + '/images/'

displayRedirect = False
redirectMessage = ''
flag_err = 0
err_msg = ""

if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ.get('HTTP_COOKIE')
    cookie = Cookie.SimpleCookie()
    cookie.load(cookie_string)
    try:
        username = cookie['user'].value
        cookie_flag = 1
    except KeyError:
        cookie_flag = 0

db = conn.connect(user='root', password='', host='localhost', port='3000', database='webinstagram')
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

try:
	if(qs_dict['id']):
		haveId = True
except:
	pass

try:
	if(qs_dict['filter'] and int(qs_dict['filter']) >= 1 and int(qs_dict['filter']) <= 4):
		haveFilter = True
		filter_set = int(qs_dict['filter'])
except:
	pass

try:
	if(qs_dict['remove'] and int(qs_dict['remove']) == 1):
		haveRemove = True
except:
	pass

try:
	if(qs_dict['submit'] and int(qs_dict['submit']) == 1):
		haveSubmit = True
except:
	pass

if(cookie_flag != 1):
	displayRedirect = True
	redirectMessage = """You need to <a href="login.py">login</a> first."""
elif(not haveId):
	flag_err = 1
	err_msg = "image id missing."
else:
	query = ("select count(*) from image where iid='" + qs_dict['id'] + "';")
	cursor.execute(query)
	result = cursor.fetchone()
	rows = result[0]
	if(rows != 1):
		flag_err = 1
		err_msg = "image not found."
	else:
		file_name = qs_dict['id']
		query = ("select ext from image where iid='" + qs_dict['id'] + "';")
		cursor.execute(query)
		result = cursor.fetchone()
		file_ext = str(result[0])
		query = ("select count(*) from image where iid='" + qs_dict['id'] + "' and disable=1;")
		cursor.execute(query)
		result = cursor.fetchone()
		rows = result[0]
		if(rows != 1):
			html += "Image on server already, return to <a href='index.py'>Homepage</a>."
		else:
			# image id is valid and is disable=1 (valid to do actions)
			if(haveRemove):
				try:
					os.remove(TARGET + file_name + '.' + file_ext)
					os.remove(TARGET + file_name + '1.' + file_ext)
					os.remove(TARGET + file_name + '2.' + file_ext)
					os.remove(TARGET + file_name + '3.' + file_ext)
					os.remove(TARGET + file_name + '4.' + file_ext)
				except:
					pass
				query = "delete from image where iid='" + qs_dict['id'] + "';"
				cursor.execute(query)
				conn.commit()
				html += "Image removed, return to <a href='index.py'>Homepage</a>."
			elif(haveSubmit):
				if(haveFilter):
					# replace the original file in upload folder
					try:
						os.remove(TARGET + file_name + '.' + file_ext)
						if(filter_set != 1):
							os.remove(TARGET + file_name + '1.' + file_ext)
						if(filter_set != 2):
							os.remove(TARGET + file_name + '2.' + file_ext)
						if(filter_set != 3):
							os.remove(TARGET + file_name + '3.' + file_ext)
						if(filter_set != 4):
							os.remove(TARGET + file_name + '4.' + file_ext)
						os.rename(TARGET + file_name + str(filter_set) + '.' + file_ext, TARGET + file_name + '.' + file_ext)
					except:
						pass
				else:
					try:
						os.remove(TARGET + file_name + '1.' + file_ext)
						os.remove(TARGET + file_name + '2.' + file_ext)
						os.remove(TARGET + file_name + '3.' + file_ext)
						os.remove(TARGET + file_name + '4.' + file_ext)
					except OSError:
						pass
				query = "update image set disable=0 where iid='" + qs_dict['id'] + "';"
				cursor.execute(query)
				conn.commit()
				html += "Image published, return to <a href='index.py'>Homepage</a>.<br><br>"
				html += "<div class='uploaded-image'><img src='../upload/{0}.{1}'></div>".format(qs_dict['id'], file_ext)
				html += "<br>permalink(relative): <a href='../upload/{0}.{1}'>../upload/{0}.{1}</a>".format(qs_dict['id'], file_ext)
			else:
				html += "Preview Image:"
				html += "<div class='uploaded-image'><img src='../upload/" + qs_dict['id']
				if(haveFilter):
					html += qs_dict['filter']
				html += '.' + file_ext + "'></div><br>"
				html += "<a href='edit.py?id=" + qs_dict['id'] + "'><button type='button' class='btn btn-primary'>No Filter</button></a> "
				html += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=1'><button type='button' class='btn btn-primary'>Border</button></a> "
				html += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=2'><button type='button' class='btn btn-primary'>Lomo</button></a> "
				html += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=3'><button type='button' class='btn btn-primary'>B & W</button></a> "
				html += "<a href='edit.py?id=" + qs_dict['id'] + "&filter=4'><button type='button' class='btn btn-primary'>Blur</button></a>"
				html += "<br><br><br>"
				html += "<a href='edit.py?id=" + qs_dict['id'] + "&remove=1'><button type='button' class='btn btn-danger'>Discard</button></a> "
				html += "<a href='edit.py?id=" + qs_dict['id'] + "'><button type='button' class='btn btn-warning'"
				if(not haveFilter):
					html += " disabled"
				html += ">Undo</button></a> "
				html += "<a href='edit.py?id=" + qs_dict['id'] + "&submit=1"
				if(haveFilter):
					html += "&filter=" + qs_dict['filter']
				html += "'><button type='button' class='btn btn-success'>Publish</button></a>"

cgitb.enable()

header = "Content-type: text/html\n\n"

if flag_err:
    html += "<h5>" + err_msg + "</h5>"

if displayRedirect:
    html += redirectMessage

html += """</div></body></html>"""

print header
print html