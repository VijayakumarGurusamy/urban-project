from flask import Flask, jsonify, request,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:vinsys%40007@localhost/urban'
app.json.sort_keys = False

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    profile_image_url = db.Column(db.String(200), nullable=True, default="default.png")
    role = db.Column(db.String(20))
    status = db.Column(db.String(20))
    delete_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def dict(self):
        if self.profile_image_url:
            full_url = f"http://127.0.0.1:5000/uploads/{self.profile_image_url}"
        else:
            full_url = None
        return {
            "id": self.id,
            "name": self.name,
            "mobile_number": self.mobile_number,
            "email": self.email,
            "password": self.password,
            "profile_image_url": full_url,
            "role": self.role,
            "status": self.status,
            "delete_status": self.delete_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
# --------------- Serve Uploaded Images ---------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def home():
    return "Flask API"
# -------- create user --------
@app.route('/users', methods=['POST'])
def create_user():

    data = request.json
    image =data["profile_image_url"]

    new_user = User(
        name=data["name"],
        mobile_number=data["mobile_number"],
        email=data["email"],
        password=data["password"],
        profile_image_url=data["profile_image_url"],
        role=data["role"],
        status=data["status"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": new_user.dict()
    })


# -------- get all users--------

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.filter_by(delete_status=False).all()

    result = []

    for user in users:
        result.append(user.dict())

    return jsonify(result)


# --------get userby id--------

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):

    user = User.query.get(id)

    if not user or user.delete_status:
        return jsonify({"message": "User not found"})

    return jsonify(user.dict())


# --------update user--------#

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
    user.profile_image_url = data["profile_image_url"]
    user.role = data["role"]
    user.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "User updated successfully",
        "user": user.dict()
    })
#---------update userby sts----#
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
        "message": "User status updated successfully",
        "user": user.dict()
    })
#-------- deleteuser --------
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
