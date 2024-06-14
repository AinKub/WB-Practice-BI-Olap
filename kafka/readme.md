# Работа с kafka

## 1. Поднимаем кафку с sasl

```
$ cd docker_with_sasl/
$ docker compose up -d
...
$ docker compose ps
NAME                IMAGE                          COMMAND                  SERVICE             CREATED             STATUS              PORTS
kafka               confluentinc/cp-kafka:latest   "/etc/confluent/dock…"   kafka               9 seconds ago       Up 8 seconds        0.0.0.0:9092-9093->9092-9093/tcp, :::9092-9093->9092-9093/tcp
zookeeper           zookeeper:latest               "/docker-entrypoint.…"   zookeeper           9 seconds ago       Up 8 seconds        2888/tcp, 3888/tcp, 8080/tcp, 0.0.0.0:1560->2181/tcp, :::1560->2181/tcp
```

Проверяем и подключаемся

![Success connection to kafka](./img/success_connection_kafka.png "Успешно подключились к кафке")

## 2. Создаем топик

Сделал через offset explorer

![Create topic](./img/create_topic.png "Создал топик ratingWh")
