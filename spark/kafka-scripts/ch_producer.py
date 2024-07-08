import json
from time import sleep
from dataclasses import dataclass
from datetime import datetime
from confluent_kafka import Producer

from ch_client import client


@dataclass
class shkCreate:
    shk_id: int
    barcode: str
    chrt_id: int
    nm_id: int
    create_dt: str
    dt: str
    employee_id: int
    place_cod: int
    state_id: str
    gi_id: int
    supplier_id: int
    invdet_id: int
    expire_dt: str
    supplier_box_id: int
    is_surplus: int
    has_excise: int
    ext_ids: str
    entry: str
    dt_load: str

config = {
    'bootstrap.servers': 'localhost:9093',  # адрес Kafka сервера
    'client.id': 'shkCreate-producer',
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
        producer.produce('shkCreate', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")


def main():
    data = client.execute('select * from shkCreate_full where dt_load >= today() limit 50000')

    for row in data:
        row = [i if not isinstance(i, datetime) else i.strftime('%Y-%m-%dT%H:%M:%S') for i in row]
        shk = shkCreate(*row)
        send_message(json.dumps(shk.__dict__))

    producer.flush()

    
if __name__ == '__main__':
    main()