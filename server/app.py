#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)  # Initialize Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Set the database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.json_handler = None  # Initialize JSON handler

migrate = Migrate(app, db)  # Initialize Flask-Migrate with the app and db instance

db.init_app(app)  # Initialize the database with the Flask app

@app.route('/')  # Define route for the home page
def index():
    """Render the home page."""
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')  # Define route for retrieving all bakeries
def bakeries():
    """Retrieve all bakeries from the database."""
    bakeries = Bakery.query.all()
    bakery_list = []
    for bakery in bakeries:
        bakery_list.append({
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>')  # Define route for retrieving a specific bakery by ID
def bakery_by_id(id):
    """Retrieve a bakery by its ID."""
    bakery = db.session.get(Bakery, id)
    if bakery is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    return jsonify({
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/baked_goods/by_price')  # Define route for retrieving baked goods sorted by price
def baked_goods_by_price():
    """Retrieve baked goods sorted by price."""
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = []
    for baked_good in baked_goods:
        baked_goods_list.append({
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')  # Define route for retrieving the most expensive baked good
def most_expensive_baked_good():
    """Retrieve the most expensive baked good."""
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good is None:
        return make_response(jsonify({'error': 'No baked goods found'}), 404)
    return jsonify({
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price,
        'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)  # Run the Flask app