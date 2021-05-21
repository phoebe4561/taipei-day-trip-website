from flask import Flask,render_template,request,jsonify,session
from data import data
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy 
import os

app=Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hello:password@localhost:3306/taipeiprojectdb'

db = SQLAlchemy(app)

class attraction_tb(db.Model):
	__table_args__ = {
		'comment': 'Notice table',
		'extend_existing': True}
	id = db.Column(db.Integer, primary_key = True, comment='編號')
	name = db.Column(db.String(50), nullable = False, comment = '景點名稱') 
	category = db.Column(db.String(50), nullable = False, comment = '景點分類') 
	description = db.Column(db.Text, nullable = False, comment = '景點介紹') 
	address = db.Column(db.String(255), nullable = False, comment = '地址') 
	transport = db.Column(db.Text, comment = '交通資訊') 
	mrt = db.Column(db.String(50), comment = '捷運') 
	latitude = db.Column(db.Numeric(9,6), nullable = False, comment = '經度') 
	longitude = db.Column(db.Numeric(9,6), nullable = False, comment = '緯度') 
	images = db.Column(db.Text, nullable=False , comment = '景點照片')
	
	def __init__ (self,id,name,category,description,address,transport,mrt,latitude,longitude,images):
		self.id = id
		self.name = name
		self.category = category
		self.description = description
		self.address = address
		self.transport = transport
		self.mrt = mrt
		self.latitude = latitude
		self.longitude = longitude
		self.images = images
	
class user_tb(db.Model):
	__table_args__ = {
		'comment': 'Notice user_table'
		}
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, comment='編號') 
	email = db.Column(db.String(50), nullable = False, comment = '帳號') 
	name = db.Column(db.String(50), nullable = False, comment = '姓名') 
	password = db.Column(db.String(255), nullable = False, comment = '密碼') 
	time = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True),nullable = False, server_default = sqlalchemy.sql.func.now(), comment = '註冊時間')

	def __init__ (self,email,name,password):
		self.email = email
		self.name = name
		self.password = password

class booking_tb(db.Model):
	__table_args__ = {
		'comment': 'Notice booking_table'
		}
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, comment='景點編號') 
	attractionId = db.Column(db.Integer, db.ForeignKey('attraction_tb.id'), comment='訂單景點編號')
	date = db.Column(db.String(50), nullable = False, comment = '預約日期')
	time = db.Column(db.String(50), nullable = False, comment = '預約時間') 
	price = db.Column(db.String(50), nullable = False, comment = '景點價格')
	
	def __init__ (self,attractionId,date,time,price):
		self.attractionId = attractionId
		self.date = date
		self.time = time
		self.price = price

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

@app.route("/api/attraction/<id>", methods = ["GET"])
def get_one_attraction(id):

	place = attraction_tb.query.filter_by(id=id).first()

	try:
		if not place:
			return jsonify({"error":True, "message":"景點編號錯誤"}),400
		else:
			attraction_data = {}
			attraction_data['id'] = place.id
			attraction_data['name'] = place.name
			attraction_data['category'] = place.category
			attraction_data['description'] = place.description
			attraction_data['address'] = place.address
			attraction_data['transport'] = place.transport
			attraction_data['mrt'] = place.mrt
			attraction_data['latitude'] = place.latitude
			attraction_data['longitude'] = place.longitude
			attraction_data['images'] =place.images.split(";")[:-1]

			return jsonify({"data":attraction_data})
	
	except:
		return jsonify({"error":True, "message":"伺服器內部錯誤"}),500


@app.route("/api/attractions", methods = ["GET"]) 
def get_attraction_list():

	try:
		page = request.args.get("page", 0, type = int)
		k = request.args.get("keyword")		

		if k:
			attraction_list = attraction_tb.query.filter(attraction_tb.name.like(f"%{k}%")).paginate(page=page+1, per_page=12,error_out=False)
			if attraction_list.has_next:
			   nextPage = attraction_list.next_num-1
			else:
			   nextPage = None			
		else:
			attraction_list = attraction_tb.query.paginate(page=page+1, per_page=12,error_out=False)
			if attraction_list.has_next:
			   nextPage = attraction_list.next_num-1
			else:
			   nextPage = None 		
		# page=page+1 因為page=0實際上並不存在 所以用page+1來符合實際情況

		output=[]
		for place in attraction_list.items:
				attraction_data = {}
				attraction_data['id'] = place.id
				attraction_data['name'] = place.name
				attraction_data['category'] = place.category
				attraction_data['description'] = place.description
				attraction_data['address'] = place.address
				attraction_data['transport'] = place.transport
				attraction_data['mrt'] = place.mrt
				attraction_data['latitude'] = place.latitude
				attraction_data['longitude'] = place.longitude
				attraction_data['images'] =place.images.split(";")[:-1]
				output.append(attraction_data)
		
		return jsonify({"nextpage":nextPage, "data":output})

	except:
		return jsonify({"error":True, "message":"伺服器內部錯誤"}),500

@app.route("/api/user", methods = ["GET"])
def get_user_data():
	email=session.get('email')

	if email:
		user=user_tb.query.filter_by(email=email).first()
		
		user_data = {}
		user_data['id'] = user.id
		user_data['name'] = user.name
		user_data['email'] = user.email
		db.session.commit()
		return jsonify({'data':user_data})
	else:
		return jsonify({'data':None})

@app.route("/api/user", methods = ["POST"])
def create_new_user():
	data=request.get_json()
	name=data['name']
	email=data['email']
	password=data['password']
	
	try:
		if name and email and password:
			user = user_tb.query.filter_by(email=email).first()
			if user:
				return jsonify({"error":True, "message":"此信箱已被註冊,註冊失敗"}),400
			else:
				new_user=user_tb(name=data['name'],email=data['email'],password=data['password'])
				db.session.add(new_user)
				db.session.commit()
				return jsonify({"ok":True})
		else:
			return jsonify({"error":True})
	except:
			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500

@app.route("/api/user", methods = ["PATCH"])
def signin_user():
	data=request.get_json()
	email=data['email']
	password=data['password']

	try:
		if email and password:
			user=user_tb.query.filter_by(email=email,password=password).first()
			if not user:
				return jsonify({"error":True, "message":"帳號或密碼錯誤,註冊失敗"}),400
			else:
				signin_email=data['email']
				signin_password=data['password']
				session['email']=signin_email
				return jsonify({"ok":True})
		else:
			return jsonify({"error":True})
	except:
			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500
		
@app.route("/api/user", methods = ["DELETE"])
def signout_user():
	if 'email' in session:
		session.pop("email")
		return jsonify({"ok":True})


@app.route("/api/booking", methods=["GET","POST","DELETE"])
def get_booking_data():
	if 'email' not in session:
		return jsonify({"error":True, "message":"未登入系統"}),403
	if request.method == "POST":
		try:
			data=request.get_json()
			print(data)	
			attractionId=data.get("attractionId")
			date = data.get("date")
			time = data.get("time")
			price = data.get("price")
			if date and time and price:
				new_booking=booking_tb(attractionId=attractionId,date=date,time=time,price=price)
				print(new_booking)
				db.session.add(new_booking)
				db.session.commit()
				return jsonify({"ok":True})
			else:
				return jsonify({"error":True,"message":"訂單失敗,有資料未輸入"}),400
		except:
			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500
	
	if request.method == "GET":
		
		booking="SELECT booking_tb.*,attraction_tb.name,attraction_tb.address,attraction_tb.images FROM booking_tb INNER JOIN attraction_tb ON booking_tb.attractionId = attraction_tb.id"		
		
		booking_data = db.engine.execute(booking)
		res = {"data":None}
		for row in booking_data:	
			res = {
				"data":{
					"attraction":{
						"id":row[1],
						"name":row[5],
						"address":row[6],
						"image":row[7].split(";")[0]
						},
				"date":row[2],
				"time":row[3],
				"price":row[4]
				}
			}
		return jsonify(res)

	
	if request.method=="DELETE":
		db.session.query(booking_tb).delete()
		db.session.commit()
		return jsonify({"ok":True})
	return jsonify({"error":True})

if __name__=='__main__':
	db.create_all()
	app.run(port=3000,debug=True)


