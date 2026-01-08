import pika
from config import RABBITMQ_CONFIG
import logging

logger = logging.getLogger(__name__)


class RabbitMQConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        """Инициализирует подключение и создает exchange/queue"""
        try:
            credentials = pika.PlainCredentials(
                RABBITMQ_CONFIG['username'],
                RABBITMQ_CONFIG['password']
            )
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_CONFIG['host'],
                port=RABBITMQ_CONFIG['port'],
                credentials=credentials,
                heartbeat=600
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            # Создаем exchange
            self.channel.exchange_declare(
                exchange=RABBITMQ_CONFIG['exchange_name'],
                exchange_type='direct',
                durable=True
            )

            # Создаем queue
            self.channel.queue_declare(
                queue=RABBITMQ_CONFIG['queue_name'],
                durable=True
            )

            # Bind queue to exchange
            self.channel.queue_bind(
                exchange=RABBITMQ_CONFIG['exchange_name'],
                queue=RABBITMQ_CONFIG['queue_name'],
                routing_key=RABBITMQ_CONFIG['routing_key']
            )

            logger.info("RabbitMQ connection established successfully")

        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def get_channel(self):
        """Возвращает канал для публикации сообщений"""
        return self.channel

    def close(self):
        """Закрывает соединение"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def __del__(self):
        self.close()