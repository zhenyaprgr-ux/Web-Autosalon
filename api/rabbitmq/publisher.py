import json
import pika
from .connection import RabbitMQConnection
from config import RABBITMQ_CONFIG
import logging

logger = logging.getLogger(__name__)

class EventPublisher:
    def __init__(self):
        self.rabbitmq = RabbitMQConnection()
        self.channel = self.rabbitmq.get_channel()

    def publish_car_event(self, event_type, car_data):
        """
        Публикует событие об автомобиле
        """
        try:
            event_message = {
                'eventType': event_type,
                'car': {
                    'id': car_data.get('id'),
                    'firm': car_data.get('firm'),
                    'model': car_data.get('model'),
                    'year': car_data.get('year'),
                    'power': car_data.get('power'),
                    'color': car_data.get('color'),
                    'price': car_data.get('price'),
                    'dealer_id': car_data.get('dealer_id')
                }
            }
            # Отправляем в RabbitMQ
            self.channel.basic_publish(
                exchange=RABBITMQ_CONFIG['exchange_name'],
                routing_key=RABBITMQ_CONFIG['routing_key'],
                body=json.dumps(event_message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Сохранять сообщения при перезапуске
                    content_type='application/json'
                )
            )

            logger.info(f"Car event published: {event_type} for car ID {car_data.get('id')}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            return False