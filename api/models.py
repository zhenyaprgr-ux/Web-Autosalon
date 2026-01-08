from flask_restx import fields, Model

def create_car_model(api):
    """Создает модель автомобиля для Swagger"""
    return api.model('Car', {
        'id': fields.Integer(readonly=True, description='ID автомобиля'),
        'firm': fields.String(required=True, description='Марка'),
        'model': fields.String(required=True, description='Модель'),
        'year': fields.Integer(required=True, description='Год выпуска'),
        'power': fields.Integer(required=True, description='Мощность (л.с.)'),
        'color': fields.String(required=True, description='Цвет'),
        'price': fields.Float(required=True, description='Цена'),
        'dealer_id': fields.Integer(description='ID дилера')
    })

def create_dealer_model(api):
    """Создает модель дилера для Swagger"""
    return api.model('Dealer', {
        'id': fields.Integer(readonly=True, description='ID дилера'),
        'name': fields.String(required=True, description='Название'),
        'city': fields.String(required=True, description='Город'),
        'address': fields.String(required=True, description='Адрес'),
        'area': fields.String(description='Район'),
        'rating': fields.Float(required=True, description='Рейтинг')
    })