from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    family = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'name': self.name, 'family': self.family, 'email': self.email}


with app.app_context():
    db.create_all()


# create test route 
@app.route('/test', methods = ['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# create a person
@app.route('/person', methods = ['POST'])
def create_person():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['name', 'family', 'email']):
            return make_response(jsonify({'message': 'Invalid input data!'}), 400)
        
        new_user = Person(name=data['name'], family=data['family'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        
        return make_response(jsonify({'message': 'User created'}), 201)

    except Exception as e:
        return make_response(jsonify({'message': f'Error creating user: {str(e)}'}), 500)

#get all people
@app.route('/person', methods = ['GET'])
def get_people():
    try:
        people = Person.query.all()
        return make_response(jsonify({'people': [person.json() for person in people]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting users!'}), 500)

#get person by id
@app.route('/person/<int:id>', methods = ['GET'])
def get_person(id):
    try:
        person = Person.query.filter_by(id=id).first()
        if person:
            return make_response(jsonify({'person': person.json()}), 200)
        return make_response(jsonify({'message': 'Person not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error founding person'}), 500)

#update a user
@app.route('/person/<int:id>', methods = ['PUT'])
def update_person(id):
    try:
        person = Person.query.filter_by(id=id).first()
        if person:
            data = request.get_json()
            person.name = data['name']
            person.family = data['family']
            person.email = data['email']

            db.session.commit()
            return make_response(jsonify({'message': 'Person updated!'}), 200)
        else:
            return make_response(jsonify({'message': 'Person not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating person!'}), 500)

#delete a user 
@app.route('/person/<int:id>', methods = ['DELETE'])
def delete_person(id):
    try:
        person = Person.query.filter_by(id=id).first()
        if person:
            db.session.delete(person)
            db.session.commit()
            return make_response(jsonify({'message': 'Person deleted successfully'}),200)
        return make_response(jsonify({'message': 'Person not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting person!'}), 500)
