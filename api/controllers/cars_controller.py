from flask_restx import Resource, Namespace
from api.services.cars_service import CarService
from api.models import create_car_model


def register_cars_routes(api):
    ns_cars = Namespace('cars', description='Операции с автомобилями')
    car_model = create_car_model(api)

    @ns_cars.route('/')
    class CarsList(Resource):
        @ns_cars.marshal_list_with(car_model)
        def get(self):
            return CarService.get_all_cars()

        @ns_cars.expect(car_model)
        @ns_cars.marshal_with(car_model, code=201)
        def post(self):
            return CarService.create_car(api.payload), 201

    @ns_cars.route('/<int:id>')
    @ns_cars.param('id', 'ID автомобиля')
    class Car(Resource):
        @ns_cars.marshal_with(car_model)
        def get(self, id):
            car = CarService.get_car_by_id(id)
            if car:
                return car
            ns_cars.abort(404, f"Автомобиль с ID {id} не найден")

        @ns_cars.expect(car_model)
        @ns_cars.marshal_with(car_model)
        def put(self, id):
            car = CarService.update_car(id, api.payload)
            if car:
                return car
            ns_cars.abort(404, f"Автомобиль с ID {id} не найден")

        @ns_cars.response(204, 'Удалено')
        def delete(self, id):
            if CarService.delete_car(id):
                return '', 204
            ns_cars.abort(404, f"Автомобиль с ID {id} не найден")

    api.add_namespace(ns_cars)