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

db = conn.connect(user='root', password='', host='localhost', port='3306', database='webinstagram')
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
    body = """Please <a href="login.py">login</a> first"""
    flag = 0
else:
    form = cgi.FieldStorage()
    if not form.has_key('file'):
        body = """<h1>File not found, return to <a href="index.py">index page</a></h1>"""
        flag = 0

    form_file = form['file']
    if not form_file.file:
        body = """<h1>File not found, return to <a href="index.py">index page</a></h1>"""
        flag = 0

    if not form_file.filename:
        body = """<h1>File not found, return to <a href="index.py">index page</a></h1>"""
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
    type_check = magic.from_file(image_file, mime=True)
    if(type_check != 'image/jpeg' and type_check != 'image/png' and type_check != 'image/gif'):
        flag = 0
        body = """image type is wrong, has to be jpeg, png or gif, return to <a href="index.py">index page</a>"""
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

    image_id = str(image_id)
    img = Image.open(TARGET + image_id + '.' + img_type)
    if(img_type == 'gif'):
        img.seek(0)
        img = img.convert('RGB')

    width, height = img.size
    filter1 = ImageOps.expand(img,border=30,fill='black')
    overlay = Image.new(img.mode, img.size, "#0000CC")
    bw_src = ImageEnhance.Color(img).enhance(0.0)
    filter2 = Image.blend(bw_src, overlay, 0.3)
    filter3 = img.convert('L')
    filter4 = img.filter(ImageFilter.BLUR)
    lensflare = Image.open("../lensflare.png")
    lensflare = lensflare.convert("RGB")
    lensflare = lensflare.crop((0,0,width,height))
    filter5 = Image.blend(img, lensflare, 0.4)
    
    filter1.save(TARGET + image_id + '1' + '.' + img_type)
    filter2.save(TARGET + image_id + '2' + '.' + img_type)
    filter3.save(TARGET + image_id + '3' + '.' + img_type)
    filter4.save(TARGET + image_id + '4' + '.' + img_type)
    filter5.save(TARGET + image_id + '5' + '.' + img_type)

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
        body += "<button href='edit.py?id=" + image_id + "'>Continue</button>"
    except:
        body += "<p>upload failed.</p>"

print header
print body
print footer