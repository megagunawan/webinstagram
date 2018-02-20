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

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps
from PIL import GifImagePlugin

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
                    <a href="index.py"><h3>web instagram</h3></a>"""

footer = """</body></html>"""

flag = 1
if (cookie_set == 0):
    body = "Please <a href="login.py">login</a> first"
    flag = 0
else:
    form = cgi.FieldStorage()
    if not form.has_key('file'):
        body = "<h1>File not found, return to <a href="index.py">index page</a></h1>"
        flag = 0

    form_file = form['file']
    if not form_file.file:
        body = "<h1>File not found, return to <a href="index.py">index page</a></h1>"
        flag = 0

    if not form_file.filename:
        body = "<h1>File not found, return to <a href="index.py">index page</a></h1>"
        flag = 0

    while True:
        image_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        cursor.execute("select count(*) from image where imageid='"+image_id+"';")
        result = cursor.fetchone()
        if(result[0] == 0):
            break

    filename, filetype = os.path.splitext(form_file.filename)
    filepath = os.path.join('./images', os.path.basename(image_id + filetype))
    with file(filepath, 'wb') as fout:
        while True:
            chunk = form_file.file.read(100000)
            if not chunk:
                break
            fout.write (chunk)

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    PREV_FOLDER = os.path.abspath(os.path.join(THIS_FOLDER, os.pardir))
    TARGET = PREV_FOLDER + '/images/'
    image_file = os.path.join(TARGET + image_id + filetype)
    check_mime = magic.from_file(my_file, mime=True)
    if(check_mime != 'image/jpeg' and check_mime != 'image/png' and check_mime != 'image/gif'):
        flag_err = 1
        body = "image type is wrong, has to be jpeg, png or gif, return to <a href="index.py">index page</a>"
    elif(check_mime == 'image/jpeg'):
        img_type = 'jpg'
    elif(check_mime == 'image/png'):
        img_type = 'png'
    elif(check_mime == 'image/gif'):
        img_type = 'gif'

    if(form['mode'].value == 'private'):
        private = 1
    else:
        private = 0

    cursor.execute("select userid from users where username='"+username+"';")
    result = cursor.fetchone()
    user_id = str(result[0])

    cursor.execute("insert into images(imageid, userid, imgtype, private, disable) values('"+str(image_id)+"', "+user_id+", '"+img_type+"', "+ str(private)+", 1);")
    conn.commit()
    body += "<p>file successfully uploaded</p>"
    body += "<img src='../images/" + image_id + "." + imgtype + "'>"

if (flag == 1):
    try:
        body += "<p>submitted: " + filename + filetype + "</p>"
        body += "<p>mode: " + form['mode'].value + "</p>"
    except:
        body += "<p>no submitted file.</p>"

    try:
        body += "<button href='edit.py?id=" + image_id + "'>Edit or discard this image</button>
        body += "Return to <a href="index.py">index page</a>"
    except:
        body += "<p>upload failed.</p>"

print header
print body
print footer