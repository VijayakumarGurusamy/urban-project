from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:vinsys%40007@localhost:3306/urban'
app.json.sort_keys = False

db = SQLAlchemy(app)
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mobile_number = db.Column(db.String(20))
    email = db.Column(db.String(30))
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))
    status = db.Column(db.String(20))
    delete_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def dict(self):
    
        return {
            "id": self.id,
            "name": self.name,
            "mobile_number": self.mobile_number,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "status": self.status,
            "delete_status": self.delete_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

@app.route('/')
def home():
    return "Vijay your Flask API is running"
@app.route('/users', methods=['POST'])
def create_user():

    data = request.json

    new_user = User(
        name=data["name"],
        mobile_number=data["mobile_number"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        status=data["status"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User Created ",
        "user": new_user.dict()
    })

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.filter_by(delete_status=False).all()

    result = []

    for user in users:
        result.append(user.dict())

    return jsonify(result)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):

    user = User.query.get(id)

    if not user or user.delete_status:
        return jsonify({"message": "User not found"})

    return jsonify(user.dict())

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):

    data = request.json

    user = User.query.get(id)

    if not user or user.delete_status:
        return jsonify({"message": "User not found"})

    user.name = data["name"]
    user.mobile_number = data["mobile_number"]
    user.email = data["email"]
    user.password = data["password"]
    user.role = data["role"]
    user.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "Updated",
        "user": user.dict()
    })
@app.route("/users/<int:id>/status", methods=["GET","PUT"])
def update_user_status(id):

    user = User.query.get(id)

    if not user or user.delete_status:
        return jsonify({"message": "User not found"})

    if request.method == "GET":
        return jsonify({
            "status": user.status
        })

    data = request.get_json()

    user.status = data["status"]
    db.session.commit()

    return jsonify({
        "message": "Status updated successfully",
        "user": user.dict()
    })
@app.route("/users/<int:id>/delete", methods=["PUT"])
def delete_user(id):

    user = User.query.get(id)

    if not user or user.delete_status:
        return jsonify({"message": "User not found"}), 404

    user.delete_status = True

    db.session.commit()

    return jsonify({
        "message": "User deleted successfully",
        "delete_status": user.delete_status
    })
if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True)
