# config.example.py
# заполните своими данными ( не пушим настоящий конфиг )

DB_CONFIG = {
    'dbname': 'ВАША БД',
    'user': 'ВАШЕ ИМЯ_ПОЛЬЗОВАТЕЛЯ',
    'password': 'ПАРОЛЬ',
    'host': 'localhost',
    'port': '5432'
}
RABBITMQ_CONFIG = {
    'host': 'localhost',
    'port': 5672,
    'username': 'ВАШЕ ИМЯ_ПОЛЬЗОВАТЕЛЯ',
    'password': 'ПАРОЛЬ',
    'exchange_name': 'cars_events_exchange',
    'queue_name': 'cars_events_queue',
    'routing_key': 'car.event'
}