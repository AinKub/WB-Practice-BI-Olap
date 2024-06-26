import json
import random
import time
from datetime import datetime
from pathlib import Path

from clickhouse_driver import Client


def openKeyfile():

    cwd = Path.cwd()

    with open(cwd / "ch_key.json") as json_file:
        param_сonnect = json.load(json_file)

    return param_сonnect


def connect_CH():

    param_сonnect = openKeyfile()

    for _ in range(7):
        try:
            client = Client(param_сonnect['server'][0]['host'],
                            user=param_сonnect['server'][0]['user'],
                            password=param_сonnect['server'][0]['password'],
                            port=param_сonnect['server'][0]['port'],
                            verify=False,
                            database='',
                            compression=True)
            return client
        except Exception as e:
            print(e, "Нет коннекта к КликХаус")
            time.sleep(60)


def main():

    # Сгенерируем несколько wh_id
    wh_ids = [i for i in range(1, 31)]

    # Также несколько supplier_id
    suppliers_ids = [random.randint(10000, 20000) for i in range(30)]

    comments = ['Очень долго разгружали', '', 'Хамское отношение', '', 'Очень быстро разгрузили', '', 'Парни - молодцы, быстро приняли']

    client = connect_CH()

    while True:

        data = []

        # Будем вставлять пачками по 20 штук
        for i in range(20):
            wh_id = random.choice(wh_ids)
            supplier_id = random.choice(suppliers_ids)
            rating = random.randint(1, 5)
            comment = random.choice(comments)
            dt_date = datetime.now().date()#.strftime('%Y-%m-%d')

            data.append((wh_id, supplier_id, rating, comment, dt_date))
            
        rows = client.execute(
            'INSERT INTO direct_log.rating_wh_by_suppliers (*) VALUES',
            data
        )

        print(f'Вставлено строк: {rows}')

        time.sleep(10)


if __name__ == '__main__':
    main()