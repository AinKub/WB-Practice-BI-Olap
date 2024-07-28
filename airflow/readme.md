# Работа с Airflow

## 1. Поднимаем контейнеры

Предварительно создадим общую для контейнеров сеть:

```
docker network create airflow_network
```

Затем перейдем в [/airflow](./docker-compose/airflow), [/clickhouse](./docker-compose/clickhouse), [/postgres](./docker-compose/postgres) и везде выполним команду `docker compose up -d`

