import cv2
import sys
import os
import numpy as np
from face_recognition import face_encodings, face_locations, compare_faces, face_distance
from datetime import datetime, date
from keyboard import is_pressed
from flask import Flask, render_template, request, flash, redirect
from flask_mysqldb import MySQL
from pandas import DataFrame

app = Flask(__name__)

app.config["Secret_Key"] = "6a79852e71abd3dc5e4d#"
app.debug = True
app.secret_key = "AsdHahD12@!#@3@#@#554"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSORD'] = ''
app.config["MYSQL_DB"] = 'face pay'
app.config["SQLALCHEMY_DATABASE_URL"] = "http://localhost/phpmyadmin/db_structure.php?server=1&db=face+pay"
app.config["MYSQL CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route("/")
def index():    #login page open here
    return render_template("index.html")    #redirecting to index.html


@app.route("/register", methods=["GET", "POST"])
def register():     # to register the new user
    try:
        con = mysql.connection.cursor()
        print("Connected to database")
    except Exception as e:
        sys.exit(e)
    con.execute("SELECT * FROM register")
    data = DataFrame(data=con.fetchall())

    if request.method == "POST":
        Name = request.form.get("name")
        Password = request.form.get("password")
        cur = mysql.connection.cursor()
        if Name in list(data[0]):
            if Password not in list(data[1]):
                flash("You need to log in")
                return render_template("index.html")
            if Password in list(data[1]):
                flash('User already exist')
                return render_template('index.html')
            else:
                cur.execute("INSERT INTO register(Name,Password) VALUES (%s,%s)", (Name, Password))
                mysql.connection.commit()
                cur.close()
                flash("Submission-Successful")
                return render_template("image.html")
        else:
            flash("Submission-Successful")
            return render_template("image.html")
    return render_template("index.html")


def findEncodings(images):      #find the encodings for images of user
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markEntry(name):    #to insert the user who have boarded from one station to another
    try:
        con = mysql.connection.cursor()
        print("Connected to database")
    except Exception as e:
        sys.exit(e)
    con.execute("SELECT * FROM register")
    data = DataFrame(data=con.fetchall())

    if request.method == "POST":
        Name = request.form.get("name")
        Password = request.form.get("password")
        cur = mysql.connection.cursor()
        if Name in list(data[0]):
            if Password not in list(data[1]):
                flash("You need to log in")
                return render_template("index.html")
            if Password in list(data[1]):
                flash('User already exist')
                return render_template('index.html')
            else:
                cur.execute("INSERT INTO register(Name,Password) VALUES (%s,%s)", (Name, Password))
                mysql.connection.commit()
                cur.close()
                flash("Submission-Successful")
                return render_template("image.html")
        else:
            flash("Submission-Successful")
            return render_template("image.html")
    return render_template("index.html")


def detect_faces():     # comparing the face on the webcam to the images given by the user
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_locations(imgS)
        encodesCurFrame = face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = compare_faces(encodeListKnown, encodeFace)
            faceDis = face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markEntry(name)

        cv2.imshow('Webcam', img)
        if is_pressed("esc"):
            return
        cv2.waitKey(1)


# Uploading of images will be started here
UPLOAD_FOLDER = "C:/Users/asus/Desktop/Practice/Face Detection"
ALLOWED_EXTENSIONS = {'jpg', 'png'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/start', methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No Flash Apart")
            return redirect(request.url)
        file = request.files["fileToUpload"]
        if file.filename == '':
            flash("No File Selected")
            return redirect(request.url)
        else:
            file.filename = f"{id}.png"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO register(image_path) VALUES(%s)", (file.filename,))
            cur.connection.commit()
            cur.close()
            id += 1
            detect_faces()
            return render_template("journey.html")
    detect_faces()
    return render_template("journey.html")


@app.route("/exit")
def ex():
    start = request.form.get("start")
    end = request.form.get("end")
    ac_no = request.form.get("Account No")
    return render_template("ex.html", acc_no = acc_no, start=start, end=end, money ="50", balance="940")


if __name__ == '__main__':
    print("Encoding has been started please wait a few minutes :)")
    images = []
    path = 'database_images'
    classNames = []
    id = 2
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    app.run(debug=True)
    HARNEET
