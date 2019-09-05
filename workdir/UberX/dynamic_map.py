from flask import Flask, jsonify, abort, request, make_response, url_for,render_template

import datetime
app = Flask(__name__)

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('main.html', **templateData)

cars = [
    {
        'id': 1,
        'make': 'Ford',
        'model': 'Focus',
        'colour': 'red',
        'driver_name': 'Zelda',
        'current_block_location': 300, 
        'number_of_passengers': 1,
        'spare_seats_in_car': 2,
        'available': False
    },
    {
        'id': 2,
        'make': 'Chevy',
        'model': 'Volt',
        'colour': 'white',
        'driver_name': 'Jeff',
        'current_block_location': 221, 
        'number_of_passengers': 0,
        'spare_seats_in_car': 4,
        'available': True
    }
]

@app.route('/cars', methods=['GET'])
def get_cars():
    return jsonify({'cars': cars})
'''    
@app.route('/cars', methods=['GET'])
def get_cars():
    return jsonify({'cars': [make_public_car(car) for car in cars]})
''' 
    
@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = [car for car in cars if car['id'] == car_id]
    if len(car) == 0:
        abort(404)
    return jsonify({'car': car[0]})
    

@app.route('/cars', methods=['POST'])
def create_car():
    if not request.json or not 'driver_name' in request.json:
        abort(400)
    car = {
        'id': cars[-1]['id'] + 1,
        'driver_name': request.json['driver_name'],
        'public_key': request.json.get('public_key', ""),
        'current_block_location': request.json.get('current_block_location', ""),
        'spare_seats_in_car': request.json.get('spare_seats_in_car', ""),
        'number_of_passengers': request.json.get('number_of_passengers', ""),
        'available': True
    }
    cars.append(car)
    return jsonify({'car': car}), 201

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    print('car_id:'+str(car_id))
    car = [car for car in cars if car['id'] == car_id]
    print(car)
    print(len(car))
    if len(car) == 0:
        abort(404)
    if not request.json:
        print('Oops!')
        abort(400)    
    car[0]['driver_name'] = request.json.get('driver_name', car[0]['driver_name'])
    car[0]['public_key'] = request.json.get('public_key', car[0]['public_key'])
    car[0]['current_block_location'] = request.json.get('current_block_location', car[0]['current_block_location'])
    car[0]['spare_seats_in_car'] = request.json.get('spare_seats_in_car', car[0]['spare_seats_in_car'])
    car[0]['number_of_passengers'] = request.json.get('number_of_passengers', car[0]['number_of_passengers'])
    car[0]['available'] = request.json.get('available', car[0]['available'])    
    return jsonify({'car': car[0]})

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = [car for car in cars if car['id'] == car_id]
    if len(car) == 0:
        abort(404)
    cars.remove(car[0])
    return jsonify({'result': True})
    
def make_public_car(car):
    new_car = {}
    for field in car:
        if field == 'id':
            new_car['uri'] = url_for('get_car', car_id=car['id'], _external=True)
        else:
            new_car[field] = car[field]
    return new_car

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)