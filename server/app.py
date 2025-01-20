# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake:
        response = jsonify(earthquake.to_dict())
        response.status_code = 200
    else:
        response = jsonify({'message': f'Earthquake {id} not found.'})
        response.status_code = 404
    return response


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response_data = {
        "count": len(quakes),
        "quakes": [quake.to_dict() for quake in quakes]
    }
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
