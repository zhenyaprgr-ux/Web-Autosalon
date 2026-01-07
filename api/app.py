from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import psycopg2
import sys
import os
app = Flask(__name__)
CORS(app)
from config import DB_CONFIG


# Настраиваем Swagger
api = Api(
    app,
    version='1.0',
    title='Autosalon API',
    description='API для управления автомобилями и дилерами',
    doc='/swagger/'
)


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


# Модели для Swagger
car_model = api.model('Car', {
    'id': fields.Integer(readonly=True),
    'firm': fields.String(required=True),
    'model': fields.String(required=True),
    'year': fields.Integer(required=True),
    'power': fields.Integer(required=True),
    'color': fields.String(required=True),
    'price': fields.Float(required=True),
    'dealer_id': fields.Integer
})

dealer_model = api.model('Dealer', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'city': fields.String(required=True),
    'address': fields.String(required=True),
    'area': fields.String,
    'rating': fields.Float(required=True)
})

# Пространство имен для автомобилей
ns_cars = api.namespace('cars', description='Операции с автомобилями')


@ns_cars.route('/')
class CarsList(Resource):
    @ns_cars.marshal_list_with(car_model)
    def get(self):
        """Получить все автомобили"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars ORDER BY id')
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'firm': row[1],
                'model': row[2],
                'year': row[3],
                'power': row[4],
                'color': row[5],
                'price': float(row[6]),
                'dealer_id': row[7]
            })

        cursor.close()
        conn.close()
        return result


@ns_cars.route('/<int:id>')
@ns_cars.param('id', 'ID автомобиля')
class Car(Resource):
    @ns_cars.marshal_with(car_model)
    def get(self, id):
        """Получить автомобиль по ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = %s', (id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return {
                'id': row[0],
                'firm': row[1],
                'model': row[2],
                'year': row[3],
                'power': row[4],
                'color': row[5],
                'price': float(row[6]),
                'dealer_id': row[7]
            }
        api.abort(404, f"Автомобиль с ID {id} не найден")


# Пространство имен для дилеров
ns_dealers = api.namespace('dealers', description='Операции с дилерами')


@ns_dealers.route('/')
class DealersList(Resource):
    @ns_dealers.marshal_list_with(dealer_model)
    def get(self):
        """Получить всех дилеров"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dealers ORDER BY id')
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'name': row[1],
                'city': row[2],
                'address': row[3],
                'area': row[4],
                'rating': float(row[5])
            })

        cursor.close()
        conn.close()
        return result


@ns_dealers.route('/<int:id>')
@ns_dealers.param('id', 'ID дилера')
class Dealer(Resource):
    @ns_dealers.marshal_with(dealer_model)
    def get(self, id):
        """Получить дилера по ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dealers WHERE id = %s', (id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return {
                'id': row[0],
                'name': row[1],
                'city': row[2],
                'address': row[3],
                'area': row[4],
                'rating': float(row[5])
            }
        api.abort(404, f"Дилер с ID {id} не найден")


# Дополнительно: автомобили дилера
@ns_dealers.route('/<int:id>/cars')
@ns_dealers.param('id', 'ID дилера')
class DealerCars(Resource):
    @ns_dealers.marshal_list_with(car_model)
    def get(self, id):
        """Получить автомобили дилера"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверяем существование дилера
        cursor.execute('SELECT id FROM dealers WHERE id = %s', (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            api.abort(404, f"Дилер с ID {id} не найден")

        # Получаем автомобили
        cursor.execute('SELECT * FROM cars WHERE dealer_id = %s ORDER BY id', (id,))
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'firm': row[1],
                'model': row[2],
                'year': row[3],
                'power': row[4],
                'color': row[5],
                'price': float(row[6]),
                'dealer_id': row[7]
            })

        cursor.close()
        conn.close()
        return result


# Корневой маршрут
@app.route('/')
def index():
    return {'message': 'Autosalon API', 'swagger': '/swagger/'}


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')