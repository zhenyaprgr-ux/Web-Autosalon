import pika
import json

# Подключение к RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Объявляем очередь для чтения
channel.queue_declare(queue='cars_events_queue', durable=True)

print(" [*] Waiting for car events. Press CTRL+C to exit")

def callback(ch, method, properties, body):
    print(" [x] Received event:")
    event_data = json.loads(body)
    print(f"     Event Type: {event_data['eventType']}")
    print(f"     Car: {event_data['car']}")
    print("-" * 50)

# Подписываемся на очередь
channel.basic_consume(
    queue='cars_events_queue',
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()
