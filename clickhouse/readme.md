# Работа с Clickhouse

## 1. Поднимаем clickhouse через docker

Соберем образ и пробросим туда измененный [users.xml](./users.xml), чтобы мы могли из-под пользователя default назначить все права новому администратору

```
docker volume create clickhouse_data
docker build -t clickhouse:latest .
docker run -d --name clickhouse -p 18123:8123 -v clickhouse_data:/var/lib/clickouse --ulimit nofile=262144:262144 clickhouse:latest
```

Проверим, что clickhouse поднят и к нему можно подключиться:

![Clickhouse поднят](./img/connect_clickhouse.png "Clickhouse поднят")

## 2. Создаем и настраиваем пользователя-администратора

Выполняем скрипт [task_2.sql](./scripts/task_2.sql)

Подключаемся под clickhouse_admin и проверяем его права:

![Права clickhouse_admin](./img/clickhouse_admin.png "Права clickhouse_admin")

## 3. Создаем необходимые слои и таблицы

Создаем базы `stg`, `history`, `current` и `direct_log`. В каждом слое создаем таблицу `rating_wh_by_suppliers` - туда будем складывать что-то похожее на оценку блоков поставщиками.

Выполняем скрипт [task_3.sql](./scripts/task_3.sql)

Должна получиться следующая схема:

![Базы данных и таблицы](./img/create_databases_and_tables.png "Базы данных и таблицы")
