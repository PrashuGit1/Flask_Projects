from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

# Create database
with app.app_context():
    db.create_all()

# ---------------- CRUD Routes ----------------

# Create Student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(name=data['name'], age=data['age'], grade=data['grade'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created successfully"}), 201

# Read All Students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    output = []
    for student in students:
        output.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "grade": student.grade
        })
    return jsonify(output)

# Read Single Student
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "grade": student.grade
    })

# Update Student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    student.name = data.get('name', student.name)
    student.age = data.get('age', student.age)
    student.grade = data.get('grade', student.grade)
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# Delete Student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})

# Run server
if __name__ == '__main__':
    app.run(debug=True)
