from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from api.controllers import register_cars_routes, register_dealers_routes
app = Flask(__name__)
CORS(app)
api = Api(
    app,
    version='1.0',
    title='Autosalon API',
    description='API для управления автомобилями и дилерами',
    doc='/swagger/'
)
# Регистрируем маршруты
register_cars_routes(api)
register_dealers_routes(api)

@app.route('/')
def index():
    return {
        'message': 'Autosalon API',
        'version': '1.0',
        'endpoints': {
            'cars': '/cars/',
            'dealers': '/dealers/',
            'swagger': '/swagger/'
        }
    }
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')