from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)


class Availability:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def to_json(self):
        return {"start": self.start, "end": self.end}


class Person:
    def __init__(self, first_name, last_name, location):
        if not first_name:
            raise ValueError("Missing first name")
        if not last_name:
            raise ValueError("Missing last name")
        self.first_name = first_name
        self.last_name = last_name
        self.location = location


class Teacher(Person):
    def __init__(
        self, first_name, last_name, location, verified, availabilities, price
    ):
        super().__init__(first_name, last_name, location)
        self.verified = verified
        self.availabilities = availabilities
        self.price = price

    def to_json(self):
        return {
            "name": self.name,
            "location": self.location,
            "availabilities": [a.to_json() for a in self.availabilities],
            "price": self.price,
        }


teachers = [
    Teacher(
        "Natalia y Gabriel",
        "Buenos Aires",
        [Availability("2023-10-27T13:00:00", "2023-10-27T14:00:00")],
        9.9,
    ),
    Teacher(
        "Moira Castellano",
        "Paris",
        [Availability("2023-10-27T13:00:00", "2023-10-27T14:00:00")],
        9.9,
    ),
]


@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    content = request.get_json()
    availabilities = [
        Availability(each["start"], each["end"]) for each in content["availabilities"]
    ]
    teachers.append(
        Teacher(content["name"], content["location"], availabilities, content["price"])
    )
    return jsonify({"message": "Teacher added successfully"}), 201


@app.route("/search")
def search_by_location():
    location = request.args.get("location")
    if not location:
        return jsonify([teacher.to_json() for teacher in teachers])

    return jsonify(
        [teacher.to_json() for teacher in teachers if location in teacher.location]
    )
