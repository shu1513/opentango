from flask import Flask,request
from flask.json import jsonify
from flask_talisman import Talisman

app = Flask(__name__)

from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Enable HSTS with a max-age of 31536000 seconds (1 year) and includeSubDomains
csp = {
    'default-src': '\'self\'',
    'img-src': '*',
    'style-src': ['\'self\'', 'https://stackpath.bootstrapcdn.com'],
    'script-src': ['\'self\'', 'https://code.jquery.com'],
}

talisman = Talisman(app, content_security_policy=csp, force_https=True, max_age=31536000, preload=True)


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

@app.route('/add_teacher', methods=["POST"])
def add_teacher():
    content = request.get_json()
    availabilities = [Availability(each["start"],each["end"]) for each in content["availabilities"]]
    teachers.append(Teacher(content["name"],content["location"],availabilities,content["price"]))
    return jsonify({"message": "Teacher added successfully"}), 201


@app.route('/search')
def search_by_location():
    location = request.args.get("location")
    if not location:
        return jsonify([teacher.to_json() for teacher in teachers])

    return jsonify([teacher.to_json() for teacher in teachers if location in teacher.location])
