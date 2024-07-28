#!/usr/bin/env python3

from faker import Faker
from models import db, Restaurant, Pizza, RestaurantPizza
from app import app

fake = Faker()

with app.app_context():
    print("Deleting data...")
    db.session.query(RestaurantPizza).delete()
    db.session.query(Restaurant).delete()
    db.session.query(Pizza).delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="address1")
    sanjay = Restaurant(name="Sanjay's Pizza", address="address2")
    kiki = Restaurant(name="Kiki's Pizza", address="address3")
    
    db.session.add_all([shack, sanjay, kiki])
    db.session.commit()

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    custom = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    
    db.session.add_all([cheese, pepperoni, custom])
    db.session.commit()

    print("Creating RestaurantPizza...")
    pr1 = RestaurantPizza(restaurant_id=shack.id, pizza_id=cheese.id, price=1)
    pr2 = RestaurantPizza(restaurant_id=sanjay.id, pizza_id=pepperoni.id, price=20)
    pr3 = RestaurantPizza(restaurant_id=kiki.id, pizza_id=custom.id, price=30)
    
    db.session.add_all([pr1, pr2, pr3])
    db.session.commit()

    print("Seeding done!")
