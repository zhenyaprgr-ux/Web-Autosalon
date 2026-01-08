from flask_restx import Resource, Namespace
from api.services.dealers_service import DealerService
from api.models import create_car_model, create_dealer_model


def register_dealers_routes(api):
    ns_dealers = Namespace('dealers', description='Операции с дилерами')
    dealer_model = create_dealer_model(api)
    car_model = create_car_model(api)

    @ns_dealers.route('/')
    class DealersList(Resource):
        @ns_dealers.marshal_list_with(dealer_model)
        def get(self):
            return DealerService.get_all_dealers()

        @ns_dealers.expect(dealer_model)
        @ns_dealers.marshal_with(dealer_model, code=201)
        def post(self):
            return DealerService.create_dealer(api.payload), 201

    @ns_dealers.route('/<int:id>')
    @ns_dealers.param('id', 'ID дилера')
    class Dealer(Resource):
        @ns_dealers.marshal_with(dealer_model)
        def get(self, id):
            dealer = DealerService.get_dealer_by_id(id)
            if dealer:
                return dealer
            ns_dealers.abort(404, f"Дилер с ID {id} не найден")

        @ns_dealers.expect(dealer_model)
        @ns_dealers.marshal_with(dealer_model)
        def put(self, id):
            dealer = DealerService.update_dealer(id, api.payload)
            if dealer:
                return dealer
            ns_dealers.abort(404, f"Дилер с ID {id} не найден")

        @ns_dealers.response(204, 'Удалено')
        def delete(self, id):
            if DealerService.delete_dealer(id):
                return '', 204
            ns_dealers.abort(404, f"Дилер с ID {id} не найдена")

    @ns_dealers.route('/<int:id>/cars')
    @ns_dealers.param('id', 'ID дилера')
    class DealerCars(Resource):
        @ns_dealers.marshal_list_with(car_model)
        def get(self, id):
            cars = DealerService.get_dealer_cars(id)
            if cars is not None:
                return cars
            ns_dealers.abort(404, f"Дилер с ID {id} не найден")

    api.add_namespace(ns_dealers)