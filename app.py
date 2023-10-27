from flask import Flask,request
from flask.json import jsonify

app = Flask(__name__)

class Availability:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def to_json(self):
        return {"start": self.start, "end": self.end}

class Teacher:
    def __init__(self, name, location, availabilities, price):
        self.name = name
        self.location = location
        self.availabilities = availabilities  
        self.price = price
    def to_json(self):
        return {"name": self.name, "location": self.location, "availabilities": [a.to_json() for a in self.availabilities], "price": self.price}      

teachers = [
    Teacher("Natalia y Gabriel", "Buenos Aires", [Availability("2023-10-27T13:00:00", "2023-10-27T14:00:00")], 9.9),
    Teacher("Moira Castellano", "Paris", [Availability("2023-10-27T13:00:00", "2023-10-27T14:00:00")], 9.9),
]

@app.route('/add_teacher')
def add_teacher():
    if request.method == "POST":
        content = request.get_json()
        availabilties = [Availability(each["start"],each["end"]) for each in content["availabilities"]]
        teachers.append(Teacher(content["location"],availabilities,content["price"]))

@app.route('/search')
def search_by_location():
    location = request.args.get("location")
    if not location:
        return jsonify([teacher.to_json() for teacher in teachers])

    return jsonify([teacher.to_json() for teacher in teachers if location in teacher.location])
