#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestaurantList(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants])

    def post(self):
        data = request.get_json()
        new_restaurant = Restaurant(name=data['name'], address=data['address'])
        db.session.add(new_restaurant)
        db.session.commit()
        return new_restaurant.to_dict(), 201

class RestaurantById(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return jsonify(restaurant.to_dict())

    def put(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        data = request.get_json()
        restaurant.name = data['name']
        restaurant.address = data['address']
        db.session.commit()
        return restaurant.to_dict()

    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)

        # Delete all related restaurant_pizzas records
        RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()

        # Now delete the restaurant
        db.session.delete(restaurant)
        db.session.commit()
        
        return '', 204

class PizzaList(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas])

    def post(self):
        data = request.get_json()
        new_pizza = Pizza(name=data['name'], ingredients=data['ingredients'])
        db.session.add(new_pizza)
        db.session.commit()
        return new_pizza.to_dict(), 201

class PizzaById(Resource):
    def get(self, pizza_id):
        pizza = Pizza.query.get_or_404(pizza_id)
        return jsonify(pizza.to_dict())

    def put(self, pizza_id):
        pizza = Pizza.query.get_or_404(pizza_id)
        data = request.get_json()
        pizza.name = data['name']
        pizza.ingredients = data['ingredients']
        db.session.commit()
        return pizza.to_dict()

    def delete(self, pizza_id):
        pizza = Pizza.query.get_or_404(pizza_id)
        db.session.delete(pizza)
        db.session.commit()
        return '', 204

class RestaurantPizzaList(Resource):
    def get(self):
        restaurant_pizzas = RestaurantPizza.query.all()
        return jsonify([restaurant_pizza.to_dict() for restaurant_pizza in restaurant_pizzas])

    def post(self):
        data = request.get_json()
        new_restaurant_pizza = RestaurantPizza(restaurant_id=data['restaurant_id'], pizza_id=data['pizza_id'], price=data['price'])
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return new_restaurant_pizza.to_dict(), 201

class RestaurantPizzaById(Resource):
    def get(self, restaurant_pizza_id):
        restaurant_pizza = RestaurantPizza.query.get_or_404(restaurant_pizza_id)
        return jsonify(restaurant_pizza.to_dict())

    def put(self, restaurant_pizza_id):
        restaurant_pizza = RestaurantPizza.query.get_or_404(restaurant_pizza_id)
        data = request.get_json()
        restaurant_pizza.restaurant_id = data['restaurant_id']
        restaurant_pizza.pizza_id = data['pizza_id']
        restaurant_pizza.price = data['price']
        db.session.commit()
        return restaurant_pizza.to_dict()

    def delete(self, restaurant_pizza_id):
        restaurant_pizza = RestaurantPizza.query.get_or_404(restaurant_pizza_id)
        db.session.delete(restaurant_pizza)
        db.session.commit()
        return '', 204

# Register the resources with Flask-RESTful
api.add_resource(RestaurantList, '/restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:restaurant_id>')
api.add_resource(PizzaList, '/pizzas')
api.add_resource(PizzaById, '/pizzas/<int:pizza_id>')
api.add_resource(RestaurantPizzaList, '/restaurant_pizzas')
api.add_resource(RestaurantPizzaById, '/restaurant_pizzas/<int:restaurant_pizza_id>')

if __name__ == '__main__':
    app.run(debug=True)