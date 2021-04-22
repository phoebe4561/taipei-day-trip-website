from flask import Flask,render_template,request,jsonify
from data import data
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zaq11403@localhost:3306/taipeiprojectdb'

db = SQLAlchemy(app)

# Pages
@app.route("/load")
def load():
	data.load_data(db)
	return "ok"

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(port=3000)

