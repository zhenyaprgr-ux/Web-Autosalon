from .cars_service import CarService
from .dealers_service import DealerService
from api.rabbitmq.decorators import CarServiceDecorator
from api.rabbitmq.publisher import EventPublisher

# Создаем экземпляры с декораторами
event_publisher = EventPublisher()
car_service = CarServiceDecorator(CarService(), event_publisher)

__all__ = ['car_service', 'DealerService']



