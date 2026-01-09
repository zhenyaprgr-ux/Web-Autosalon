from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

API_BASE_URL = 'http://localhost:5000'

@app.route('/')
def index():
    """Главная страница с каталогом автомобилей"""
    return render_template('index.html')

@app.route('/api/cars', methods=['GET'])
def get_cars():
    """Прокси для получения автомобилей из API"""
    try:
        response = requests.get(f'{API_BASE_URL}/cars/')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Прокси для получения автомобиля по ID"""
    try:
        response = requests.get(f'{API_BASE_URL}/cars/{car_id}')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    """Прокси для обновления автомобиля"""
    try:
        data = request.get_json()
        response = requests.put(f'{API_BASE_URL}/cars/{car_id}', json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """Прокси для удаления автомобиля"""
    try:
        response = requests.delete(f'{API_BASE_URL}/cars/{car_id}')
        return '', response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dealers', methods=['GET'])
def get_dealers():
    """Прокси для получения дилеров (для формы редактирования)"""
    try:
        response = requests.get(f'{API_BASE_URL}/dealers/')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Запускаем на другом порту, чтобы не конфликтовать с API
    app.run(debug=True, port=5001, host='0.0.0.0')
