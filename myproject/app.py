from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#App
app = Flask(__name__)

#DB Setting
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

#model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

#create Databse
with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return "Hello ! Welcome to the home page"

@app.route('/second')
def second():
    return "Welcome to the second page"

@app.route('/second/<int:val>')
def sencond_val(val):
    return f"Welcome the second+value page and value is: {val}"



if __name__ == "__main__":
    app.run(debug=True)
