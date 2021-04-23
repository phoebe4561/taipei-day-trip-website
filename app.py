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
			# print(attraction_list)
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

app.run(port=3000,debug=True)

