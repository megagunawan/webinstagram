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
import insta

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps
from PIL import GifImagePlugin

UPLOAD_DIR = './images'

if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ.get('HTTP_COOKIE')
    c = Cookie.SimpleCookie()
    c.load(cookie_string)
    try:
        username = c['insta_login'].value
        cookie_set = 1
    except KeyError:
        cookie_set = 0

insta_conf = insta.Insta()
conn = insta_conf.connect()
cursor = conn.cursor()

cgitb.enable()

header = 'Content-Type: text/html; charset=UTF-8'

displayRedirect = False
displayFailed = False
flag_err = 0
err_msg = ""
flag_success = 0

if(cookie_set != 1):
    displayRedirect = True
else:
    form = cgi.FieldStorage()
    if not form.has_key('file'):
        displayFailed = True
        flag_err = 1
        err_msg = "Cant process file."
    
    form_file = form['file']
    if not form_file.file:
        displayFailed = True
        flag_err = 1
        err_msg = "Cant process file."

    if not form_file.filename:
        displayFailed = True
        flag_err = 1
        err_msg = "Cant process file."

    while True:
        sIid = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(10))
        query = ("select count(*) from image where iid='" + sIid + "';")
        cursor.execute(query)
        result = cursor.fetchone()
        rows = result[0]
        if(rows == 0):
            break

    oriFilename, oriFile_extension = os.path.splitext(form_file.filename)

    try:
        uploaded_file_path = os.path.join(UPLOAD_DIR, os.path.basename(sIid + oriFile_extension))
        with file(uploaded_file_path, 'wb') as fout:
            while True:
                chunk = form_file.file.read(100000)
                if not chunk:
                    break
                fout.write (chunk)
    except:
        displayFailed = True
        flag_err = 1
        err_msg = "Upload failed."

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        PREV_FOLDER = os.path.abspath(os.path.join(THIS_FOLDER, os.pardir))
        TARGET = PREV_FOLDER + '/upload/'
        my_file = os.path.join(TARGET + sIid + oriFile_extension)
        checked_mime = magic.from_file(my_file, mime=True)
        if(checked_mime != 'image/jpeg' and checked_mime != 'image/png' and checked_mime != 'image/gif'):
            displayFailed = True
            flag_err = 1
            err_msg = "Mime type not in jpeg/png/gif."
        elif(checked_mime == 'image/jpeg'):
            sExt = 'jpg'
        elif(checked_mime == 'image/png'):
            sExt = 'png'
        elif(checked_mime == 'image/gif'):
            sExt = 'gif'
    except:
        displayFailed = True
        flag_err = 1
        err_msg = "Not able to locate the uploaded file."

    sUid = ""
    if(flag_err == 0):
        if(form['mode'].value == 'private'):
            sPrivate = 1
        else:
            sPrivate = 0

        sIid = str(sIid)
        im = Image.open(TARGET + sIid + '.' + sExt)
        if(sExt == 'gif'):
            im.seek(0)
            im = im.convert('RGB')

        out_f1 = ImageOps.expand(im,border=30,fill='black')
        overlay = Image.new(im.mode, im.size, "#0000CC")
        bw_src = ImageEnhance.Color(im).enhance(0.0)
        out_f2 = Image.blend(bw_src, overlay, 0.3)
        out_f3 = im.convert('L')
        out_f4 = im.filter(ImageFilter.BLUR)
        
        out_f1.save(TARGET + sIid + '1' + '.' + sExt)
        out_f2.save(TARGET + sIid + '2' + '.' + sExt)
        out_f3.save(TARGET + sIid + '3' + '.' + sExt)
        out_f4.save(TARGET + sIid + '4' + '.' + sExt)

        query = ("select uid from user where username='" + username + "';")
        cursor.execute(query)
        result = cursor.fetchone()
        sUid = str(result[0])

        add_image = ("insert into image (iid, uid, ext, private, disable) values('" + str(sIid) + "', " + sUid + ", '" + sExt + "', " + str(sPrivate) + ", 1);")
        cursor.execute(add_image)
        conn.commit()
        flag_err = 0
        flag_success = True

html = """
<html>
    <head>
        <title>insta</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="../style.css">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="heading"><a href="index.py"><h3>Insta</h3></a></div>
            </div>
"""

if flag_err:
    html += "<h5>" + err_msg + "</h5>"

if flag_success:
    html += "<h5>upload success.</h5>"
    html += "<div class='uploaded-image'><img src='../upload/" + sIid + "." + sExt + "'></div><br>"

if displayFailed:
    html += "We cant process your file or the file is missing or broken, return to <a href='index.py'>Homepage</a>.<br><br>"
if displayRedirect:
    html += """You need to sign in first, <a href='login.py'>Login</a> now."""
else:
    html += '<br>'
    html += 'Log<br><br>'
    try:
        html += 'submitted file: ' + form_file.filename + '<br>'
        html += "submitted file's name: " + oriFilename + '<br>'
        html += "submitted file's extension: " + oriFile_extension + '<br>'
        html += 'mode selected: ' + form['mode'].value + '<br>'
    except:
        html += 'no submitted file.'
    html += '<br>'
    try:
        html += 'assigned image id: ' + sIid + '<br>'
        html += 'uploaded file: ' + sIid + oriFile_extension + '<br>'
        html += 'verified mime type: ' + checked_mime + '<br>'
        html += '<br>'
        html += 'owner id: ' + sUid + '<br>'
        html += '<br>'
        html += "Continue to <b><a href='edit.py?id=" + sIid + "'>edit</a></b>, or your image wont be publish."
    except:
        html += 'upload failed.'

html += """</div></body></html>"""

print header
print html
