from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

#Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import secrete to generate user token
import secrets

#lask login to check for an authenticated user
from flask_login import UserMixin, LoginManager


#import for flask marshmallow
from flask_marshmallow import Marshmallow

#create an instance of SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager() #<-- do not forget parantheses
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref = 'owner', lazy = True)


    def __init__(self, email, password, first_name = '', last_name = '', id = '', token = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    camera_quality = db.Column(db.String(150))
    flight_time = db.Column(db.String(150))
    max_speed = db.Column(db.String(150))
    dimensions = db.Column(db.String(100))
    cost_of_prodcution = db.Column(db.Numeric(precision=12, scale=2))
    series = db.Column(db.String(100))
    random_joke = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token, random_joke='', id = ''):
       self.id = self.set_id()
       self.name = name
       self.description = description
       self.price = price
       self.camera_quality = camera_quality
       self.flight_time = flight_time
       self.max_speed = max_speed
       self.dimensions = dimensions
       self.weight = weight
       self.cost_of_prodcution = cost_of_production
       self.series = series
       self.random_joke = random_joke
       self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following drone has been added: {self.name}"


class DroneSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_production', 'series', 'random_joke' ]


drone_schema = DroneSchema()
drones_schema = DroneSchema(many = True)
