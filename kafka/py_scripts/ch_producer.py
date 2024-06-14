import json
from time import sleep
from dataclasses import dataclass
from datetime import datetime
from confluent_kafka import Producer

from ch_client import client

@dataclass
class ratingWh:
    wh_id: int
    rating: float
    dt: datetime
    is_mp: int

    def to_json(self):
        return json.dumps(
            {
                'wh_id': self.wh_id,
                'rating': self.rating,
                'dt': self.dt.strftime('%Y-%m-%dT%H:%M:%S'),
                'is_mp': self.is_mp
            }
        )

config = {
    'bootstrap.servers': 'localhost:9093',  # адрес Kafka сервера
    'client.id': 'simple-producer',
    'sasl.mechanism':'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
}

producer = Producer(**config)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_message(data):
    try:
        # Асинхронная отправка сообщения
        producer.produce('ratingWh', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

def main():
    
    data = client.execute('select * from ratingWh where dt >= today()')

    for i in data:
        rating_wh = ratingWh(*i)
        send_message(rating_wh.to_json())
        sleep(2)

    producer.flush()

    

if __name__ == '__main__':
    main()