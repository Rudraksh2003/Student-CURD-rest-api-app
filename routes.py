from flask import Blueprint, jsonify, request
from models import db, Student

students_bp = Blueprint('students', __name__)

@students_bp.route('/api/v1/students', methods=['POST'])
def add_student():
    data = request.json

    # Validate required fields
    if not data.get("name") or not data.get("age") or not data.get("grade"):
        return jsonify({"error": "Missing required fields: name, age, grade"}), 400

    student = Student(name=data["name"], age=data["age"], grade=data["grade"])
    db.session.add(student)
    db.session.commit()

    return jsonify({"id": student.id, "student": student.to_dict()}), 201

@students_bp.route('/api/v1/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify({"students": [student.to_dict() for student in students]})

@students_bp.route('/api/v1/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"student": student.to_dict()})
