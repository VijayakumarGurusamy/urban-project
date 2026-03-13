from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
students = [
    {"id": 1, "name": "Rahul"},
    {"id": 2, "name": "Anita"}
]

# GET API - get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# GET API - get student by id
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student)
    return jsonify({"message": "Student not found"})

# POST API - add student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = {
        "id": len(students) + 1,
        "name": data["name"]
    }
    students.append(new_student)
    return jsonify(new_student)

# PUT API - update student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    for student in students:
        if student["id"] == id:
            student["name"] = data["name"]
            return jsonify(student)
    return jsonify({"message": "Student not found"})

# DELETE API - delete student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            return jsonify({"message": "Student deleted"})
    return jsonify({"message": "Student not found"})

if __name__ == '__main__':
    app.run(debug=True)