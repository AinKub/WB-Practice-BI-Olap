# Работа с Clickhouse

Поднимем clickhouse через docker:

```
docker volume create clickhouse_data
docker run -d --name clickhouse -p 18123:8123 -v clickhouse_data:/var/lib/clickouse --ulimit nofile=262144:262144 clickhouse/clickhouse-server
```

Проверим, что clickhouse поднят и к нему можно подключиться:

![Clickhouse поднят](./img/connect_clickhouse.png "Clickhouse поднят")
