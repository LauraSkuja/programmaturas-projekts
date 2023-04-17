from flask import Flask, render_template, request, json
from cryptography.fernet import Fernet
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def ediens():
    return render_template("spele.html")

@app.route('/database', methods=['POST', 'GET'])
def database():
    mydb = mysql.connector.connect(
        host="lauraskuja.mysql.pythonanywhere-services.com",
        user="lauraskuja",
        passwd="datubazesparole123",
        database="lauraskuja$default"
    )
    mycursor = mydb.cursor()
    f = open("/home/lauraskuja/mysite/images/key.txt", "r")
    key= f.read()
    fernet = Fernet(key)
    if request.method == "POST":
        sql = "INSERT INTO Rezultati (Vards, Rezultats, Izmers) VALUES (%s, %s, %s)"
        vards= request.json["vards"]
        encvards= fernet.encrypt(vards.encode())
        values = (encvards, request.json["sekunde"], request.json["izmers"])
        mycursor.execute(sql, values)
        mydb.commit()

    mycursor.execute("SELECT Vards, Rezultats, Izmers FROM Rezultati order by Rezultats")
    atbilde1= mycursor.fetchall()
    rezultati = []
    for v in atbilde1:
        rezultati.append({"sekunde": v[0], "vards": v[1], "izmers": v[2]})
    return json.dumps(rezultati);