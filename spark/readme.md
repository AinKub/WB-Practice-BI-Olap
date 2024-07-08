# Работа со Spark

Все решения заданий будут выложены подряд в конце данного файла \
А ниже представлен ход выполнения работы

## 1. Подготавливаем всё для лабораторной

Первоначально развернем кафку, в которую зальём данные и из которой мы будем читать, а затем писать спарком:

```
cd docker-compose/kafka/
docker compose up -d
```

В кафке создадим топик `shkCreate`. Затем настроим окружение:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

И запустим скрипт [ch_producer.py](./kafka-scripts/ch_producer.py) (предварительно дозаполнив [credentials_example.json](./Streams/credentials_example.json) и переименовав в `credentials.json`)

В kafka должны появиться сообщения:

![shkCreate topic](./img/kafka.png)

Затем подготовим кликхаус, в который будем заливать данные спарком. Поднимем его:

```
cd docker-compose/clickhouse/
docker build -t clickhouse:latest .
docker run -d --name clickhouse -p 8123:8123 -p 9000:9000 -v clickhouse_data:/var/lib/clickouse --ulimit nofile=262144:262144 clickhouse:latest
```

Создадим пользователя, таблицы, назначим необходимые права, выполнив скрипт [init.sql](./docker-compose/clickhouse/init.sql)

Также загрузим в таблицу `datamart.volume_by_nm` объемы через импорт csv