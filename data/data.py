def load_data(db):

    import json

    class attraction_tb(db.Model):
        __table_args__ = {
            'comment': 'Notice table',
            'extend_existing': True
        }
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

    with open("data/taipei-attractions.json", mode = "r", encoding = "utf-8") as file:
        data = json.load(file)

    target = data["result"]["results"]
    output_list=[]

    for targetData in target:
    
        img = ""
        for i in targetData['file'].split("http")[1:]:
            if i[-3:] in "jpg" or i[-3:] in "png" or i[-3:] in "JPG":
                img+="http"+i+";"
        
        output_dict = attraction_tb(id=targetData["_id"],name= targetData["stitle"],category=targetData["CAT2"],
        description=targetData["xbody"],address=targetData["address"],transport=targetData["info"],
        mrt=targetData["MRT"], latitude=targetData["latitude"],longitude=targetData["longitude"],images=img)

        output_list.append(output_dict)

    db.session.add_all(output_list)
    db.session.commit()

    return attraction_tb
    
    