from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
from json import loads
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ekgljqbp:YjJy6M...@ziggy.db.elephantsql.com:5432/ekgljqbp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

Profile_DB= {
    "sucess": True,
    "data": {
        "last_updated": "2/7/2021, 4:32:43 PM",
        "username": "Thumbtack",
        "role": "Engineer in Training",
        "color": "red"
    }
}

class Tank(db.Model):
    __tablename__ = "tanks"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.String(50), nullable=False)
    long = db.Column(db.String(50), nullable=False)
    percentage_full = db.Column(db.Integer, nullable=False)

class TankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tank
        fields = ("id","location","lat","long","percentage_full")

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "ECSE3038 - Lab 4"

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def get_profile():
    if request.method == "GET":
        return jsonify(Profile_DB)

    elif request.method == "POST":
        Profile_DB["data"]["last_updated"] = datetime.now().strftime("%c")
        Profile_DB["data"]["username"] = (request.json["username"])
        Profile_DB["data"]["role"] = (request.json["role"])
        Profile_DB["data"]["color"] = (request.json["color"])
       
        return jsonify(Profile_DB)

    elif request.method == "PATCH":
         Profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
    
         data = PROFILE_DB["data"]

         r = request.json
         r["last_updated"] = dt
         attributes = r.keys()
         for attribute in attributes:
             data[attribute] = r[attribute]

             return jsonify(PROFILE_DB)    

@app.route("/data", methods=["GET", "POST"])
def tank_data():
    if request.method == "GET":
        tanks = Tank.query.all()
        tank_list = TankSchema(many=True).dump(tanks)

        return jsonify(tank_list)
        
    elif request.method == "POST":
         new_tank = Tank(
            location = request.json["location"],
            lat = request.json["lat"],
            long = request.json["long"],
            percentage_full =  request.json["percentage_full"]
        )

    db.session.add(new_tank)
    db.session.commit()

    return TankSchema().dump(new_tank)

@app.route("/data/<int:id>", methods=["PATCH", "DELETE"])
def change_tank_info(id):
    if request.method == "PATCH":
        tank = Tank.query.get(id)
        update = request.json

        if "location" in update:
            tank.location = update["location"]
        elif "lat" in update:
            tank.lat = update["lat"]
        elif "long" in update:
            tank.long = update["long"]
        elif "percentage_full" in update:
            tank.percentage_full = update["percentage_full"]        

        db.session.commit()
        return TankSchema().dump(tank)

    if request.method == "DELETE":
        tank = Tank.query.get(id)
        db.session.delete(tank)
        db.session.commit()

        return {
            "success": True
        }


if __name__ == "__main__":
    app.run(
        debug=True
    )