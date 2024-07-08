# Работа со Spark

Все решения заданий будут выложены подряд в конце данного файла \
А ниже представлен ход выполнения работы

## 1. Поднимаем кафку и заливаем туда данные

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

## 2. Подготавливаем clickhouse

Затем подготовим кликхаус, в который будем заливать данные спарком. Поднимем его:

```
cd docker-compose/clickhouse/
docker build -t clickhouse:latest .
docker run -d --name clickhouse -p 8123:8123 -p 9000:9000 -v clickhouse_data:/var/lib/clickouse --ulimit nofile=262144:262144 clickhouse:latest
```

Создадим пользователя, таблицы, назначим необходимые права, выполнив скрипт [init.sql](./docker-compose/clickhouse/init.sql)

Также загрузим в таблицу `datamart.volume_by_nm` объемы через импорт csv

## 3. Разворачиваем Spark

В директории `spark`, где лежит [docker-compose файл](./docker-compose/spark/docker-compose.yml), необходимо создать файл .env и прописать там имя компьютера: `SPARK_HOSTNAME=YOUR_HOSTNAME`

Затем поднять командой:

```
docker compose up -d
```

Теперь можно зайти по адресу http://YOUR_HOSTNAME:8080:

![Spark master](./img/spark_master.png)
