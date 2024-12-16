from flask import Flask, request, jsonify
import json
import os

app = Flask(name)

cars_file = 'data.json'

def load_data():
    if os.path.exists(cars_file):
        with open(cars_file, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open(cars_file, 'w') as file:
        json.dump(data, file)

@app.route('/cars', methods=['GET'])
def get_cars():
    return jsonify(load_data())

@app.route('/cars/<int:id>', methods=['GET'])
def get_car_by_id(id):
    cars = load_data()
    for car in cars:
        if car['id'] == id:
            return jsonify(car)
    return jsonify({'error': 'Car not found'}), 404 

@app.route('/cars', methods=['POST'])
def add_car():
    cars = load_data()
    new_car = request.get_json()
    new_car['id'] = max([car['id'] for car in cars], default=0) + 1
    cars.append(new_car)  
    save_data(cars)  
    return jsonify(new_car), 201

@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    cars = load_data()
    updated_car = request.get_json()
    for car in cars:
        if car['id'] == id:
            car.update(updated_car) 
            save_data(cars)  
            return jsonify(car)
    return jsonify({'error': 'Car not found'}), 404  

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    cars = load_data()
    for car in cars:
        if car['id'] == id:
            cars.remove(car)
            save_data(cars) 
            return '', 204  
    return jsonify({'error': 'Car not found'}), 404

if name == 'main':
    app.run(debug=True)
