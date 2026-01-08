from functools import wraps
from .publisher import EventPublisher

class CarServiceDecorator:

    def __init__(self, car_service, event_publisher):
        self.car_service = car_service
        self.event_publisher = event_publisher

    def get_all_cars(self):
        return self.car_service.get_all_cars()

    def get_car_by_id(self, car_id):
        return self.car_service.get_car_by_id(car_id)

    def create_car(self, car_data):

        result = self.car_service.create_car(car_data)

        if result:
            self.event_publisher.publish_car_event('CREATE', result)

        return result

    def update_car(self, car_id, car_data):
        old_car = self.car_service.get_car_by_id(car_id)

        result = self.car_service.update_car(car_id, car_data)

        if result:
            self.event_publisher.publish_car_event('UPDATE', result)

        return result

    def delete_car(self, car_id):
        car_to_delete = self.car_service.get_car_by_id(car_id)

        result = self.car_service.delete_car(car_id)

        if result and car_to_delete:
            self.event_publisher.publish_car_event('DELETE', car_to_delete)

        return result
