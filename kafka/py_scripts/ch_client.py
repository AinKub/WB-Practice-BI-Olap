import json
from pathlib import Path
from clickhouse_driver import Client

# Директория secrets должна находится в директории kafka
logopass_file_path = Path(__file__).parent.parent / 'secrets' / 'ch_db.json'

with open(logopass_file_path) as json_file:
    param_сonnect = json.load(json_file)

client = Client(param_сonnect['server'][0]['host'],
                user=param_сonnect['server'][0]['user'],
                password=param_сonnect['server'][0]['password'],
                port=param_сonnect['server'][0]['port'],
                verify=False,
                database='',
                settings={"numpy_columns": True, 'use_numpy': True},
                compression=True)
