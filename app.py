from flask import Flask,render_template,request,jsonify,session,redirect
from data import data
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy 
import requests,json
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
	userId= db.Column(db.Integer, db.ForeignKey('user_tb.id'), comment='使用者訂購編號') 

	
	def __init__ (self,attractionId,date,time,price,userId):
		self.attractionId = attractionId
		self.date = date
		self.time = time
		self.price = price
		self.userId = userId

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
	if 'email' not in session:
		return redirect("/")
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

	if "email" in session:
			return jsonify({"data":{
				"id":session["id"],
				"name":session["name"],
				"email":session["email"]
				}
			})
	else:
		return jsonify({"data":None}) 

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
			sql = f"select * from user_tb where email='{email}' and password='{password}'"
			result = db.engine.execute(sql)
			for row in result:
				# print(i)
				session["id"]=row[0]
				session["email"]=row[1]
				session["name"]=row[2]
				return jsonify({"ok":True})
		else:
			return jsonify({"error":True})					
	except:
			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500
		
@app.route("/api/user", methods = ["DELETE"])
def signout_user():
	if 'email' in session:
		session.pop("id")
		session.pop("name")
		session.pop("email")
		return jsonify({"ok":True})


@app.route("/api/booking", methods=["GET","POST","DELETE"])
def get_booking_data():
	if 'email' not in session:
		return jsonify({"error":True, "message":"未登入系統"}),403
	
	if request.method == "POST":
		try:
			data=request.get_json()
			attractionId=data.get("attractionId")
			date = data.get("date")
			time = data.get("time")
			price = data.get("price")
			userId=session['id']

			if date and time and price:
				new_booking=booking_tb(attractionId=attractionId,date=date,time=time,price=price,userId=userId)
				db.session.add(new_booking)
				db.session.commit()
				return jsonify({"ok":True})
			else:
				return jsonify({"error":True,"message":"訂單失敗,有資料未輸入"}),400
		except:
			return jsonify({"error":True, "message":"伺服器內部錯誤"}),500
	
	if request.method == "GET":
		userId=session["id"]
		
		booking=f'''
		SELECT booking_tb.date,booking_tb.time,booking_tb.price,
		attraction_tb.id as attId,attraction_tb.name,attraction_tb.address,attraction_tb.images,booking_tb.id 
		FROM booking_tb
		INNER JOIN attraction_tb ON booking_tb.attractionId = attraction_tb.id 
		WHERE booking_tb.userId='{userId}' ORDER BY booking_tb.id DESC 
		'''	
		booking_data = db.engine.execute(booking)
		for row in booking_data:
			data = {
					"attraction":{
						"id":row[3],
						"name":row[4],
						"address":row[5],
						"image":row[6].split(";")[0]
						},
				"date":row[0],
				"time":row[1],
				"price":row[2]
				}
			return jsonify({"data":data})
		return jsonify({"data":None})
	
	if request.method=="DELETE":
		db.session.query(booking_tb).filter_by(userId=session['id']).delete()
		db.session.commit()
		return jsonify({"ok":True})
	return jsonify({"error":True})


@app.route("/api/orders",methods=["POST"])
def post_order():
	try:
		if 'email' not in session:
			return jsonify({"error":True, "message":"未登入系統"}),403
		if request.get_json()["order"]["contact"]["phone"]=="":
			return jsonify({"error":True, "message":"請填入您的聯絡資訊"}),400

		primeAPI_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
		tappayRequest = {
			"partner_key":"partner_aBZwbMw78X7wUNpCYfa9veTp57IU2my09X32HvHOhR8BJCvHLpg4Fohg",
			"prime": request.get_json()["prime"],
			"amount": request.get_json()["order"]["price"],
			"merchant_id": "phoebepao_TAISHIN",
			"details":f'''
			{request.get_json()["order"]["trip"]["attraction"]["id"]};
			{request.get_json()["order"]["trip"]["attraction"]["name"]};
			{request.get_json()["order"]["trip"]["date"]};
			{request.get_json()["order"]["trip"]["time"]}
			''',
			"cardholder": {
				"phone_number": request.get_json()["order"]["contact"]["phone"],
				"name": request.get_json()["order"]["contact"]["name"],
				"email": request.get_json()["order"]["contact"]["email"]
				}
		}
		headers = {
			'content-type': 'application/json',
			'x-api-key': 'partner_aBZwbMw78X7wUNpCYfa9veTp57IU2my09X32HvHOhR8BJCvHLpg4Fohg'
		}
		r = requests.post(primeAPI_url,data=json.dumps(tappayRequest),headers=headers,timeout = 30)
		data = json.loads(r.text)

		
		if data["status"]==0:
			return jsonify({
				"data":{
					"number":data["bank_transaction_id"],
					"payment":{
						"status":"0",
						"message":"付款成功",
					}
				}
			})
		else:
			return jsonify({
				"data":{
					"number":data["bank_transaction_id"],
					"payment":{
						"status":"交易失敗",
						"message":"付款失敗",
					}
				}
			})
	except:
		return jsonify({"error":True, "message":"伺服器內部錯誤"}),500

@app.route("/api/order/<orderNumber>",methods=["GET"])
def get_order(orderNumber):
	if 'email' not in session:
			return jsonify({"error":True, "message":"未登入系統"}),403
	if orderNumber:
		recordAPI_url="https://sandbox.tappaysdk.com/tpc/transaction/query"
		tappayRecord={
			"partner_key":"partner_aBZwbMw78X7wUNpCYfa9veTp57IU2my09X32HvHOhR8BJCvHLpg4Fohg",
			"filters":{
			"bank_transaction_id":orderNumber
			}
		}
		headers = {
			'content-type': 'application/json',
			'x-api-key': 'partner_aBZwbMw78X7wUNpCYfa9veTp57IU2my09X32HvHOhR8BJCvHLpg4Fohg'
		}
		r = requests.post(recordAPI_url,data=json.dumps(tappayRecord),headers=headers)
		data = json.loads(r.text)
		# print(data)
		if not data["trade_records"]: 
			return jsonify({"data":None})
		trip = data["trade_records"][0]["details"].split(";")
		info=db.session.query(attraction_tb.id,attraction_tb.name,attraction_tb.address,attraction_tb.images).filter_by(id={trip[0]}).first()
		db.session.commit()
		# print(info)
		attr = {
			"id":info[0],
			"name":info[1],
			"address":info[2],
			"image":info[3].split(";")[0]
		}

		if data["trade_records"][0]["record_status"]==0:
			return jsonify({
				"data":{
					"number":data["trade_records"][0]["bank_transaction_id"],
					"trip":{
						"attraction":attr,
						"date":trip[2],
						"time":trip[3]
					},
					"price":data["trade_records"][0]["original_amount"],
					"contact":{
						"name":data["trade_records"][0]["cardholder"]["name"],
						"email":data["trade_records"][0]["cardholder"]["email"],
						"phone":data["trade_records"][0]["cardholder"]["phone_number"],
					},
					"status":0
				}
			})
		else:
			return jsonify({
			"data":{
				"number":data["trade_records"][0]["bank_transaction_id"],
					"trip":{
						"attraction":attr,
						"date":trip[2],
						"time":trip[3]
					},
				"price":data["trade_records"][0]["original_amount"],
				"contact":{
					"name":data["trade_records"][0]["cardholder"]["name"],
					"email":data["trade_records"][0]["cardholder"]["email"],
					"phone":data["trade_records"][0]["cardholder"]["phone_number"],
				},
				"status":1
			}
		})
		

if __name__=='__main__':
	db.create_all()
	app.run(port=3000,debug=True)


