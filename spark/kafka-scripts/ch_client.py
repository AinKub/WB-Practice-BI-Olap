import json
from pathlib import Path
from clickhouse_driver import Client

logopass_file_path = Path(__file__).parent.parent / 'Streams' / 'credentials.json'

with open(logopass_file_path) as json_file:
    param_сonnect = json.load(json_file)

client = Client(param_сonnect['ch'][0]['host'],
                user=param_сonnect['ch'][0]['user'],
                password=param_сonnect['ch'][0]['password'],
                verify=False,
                database='',
                settings={"numpy_columns": True, 'use_numpy': True},
                compression=True)
