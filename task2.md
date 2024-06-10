# Задание 2 (развернуть 2 контейнера через docker)

## Ubuntu

Качаем образ

```
$ sudo docker pull ubuntu:20.04
```

Смотрим, что образ появился

```
$ sudo docker images
REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
ubuntu       20.04     5f5250218d28   6 days ago   72.8MB
```

Запускаем в интерактивном режиме, где:
* `-i` интерактивный режим
* `-t` подключает виртуальный терминал
* `--rm` удалит контейнер сразу после выхода из него
* `/bin/bash` запуск терминала в ubuntu

```
$ sudo docker run -ti --rm ubuntu:20.04 /bin/bash
```

После того, как зашли в терминал в ubuntu в докере, можно вызвать разные команды

```
root@6c663a937575:/# cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

Выходим

```
# exit
```

Проверяем, что контейнер удалился

```
$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ sudo docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ sudo docker images
REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
ubuntu       20.04     5f5250218d28   6 days ago   72.8MB
```

Запустим и ограничим ресурсы. Также назовем контейнер `Ubuntu`, чтобы в командах дальше указывать имя, а не id. Используем флаг `-d`, чтобы запустить контейнер в detached режиме, а флаг `-t` для того, чтобы после запуска контейнер не останавливался (т.к. будет работать виртуальный терминал)

```
$ sudo docker run -t -d --name Ubuntu -m 2048m --cpus="2" ubuntu:20.04
```

Проверим работоспособность

```
$ sudo docker ps
CONTAINER ID   IMAGE          COMMAND       CREATED              STATUS              PORTS     NAMES
488f584b855c   ubuntu:20.04   "/bin/bash"   About a minute ago   Up About a minute             Ubuntu
```

Посмотрим ресурсы

```
$ sudo docker inspect Ubuntu | grep Memory
            "Memory": 2147483648,
            "MemoryReservation": 0,
            "MemorySwap": 4294967296,
            "MemorySwappiness": null,
$ sudo docker inspect Ubuntu | grep Cpu
            "CpuShares": 0,
            "NanoCpus": 2000000000,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "CpuCount": 0,
            "CpuPercent": 0,
```
   
Остановим и удалим контейнер

```
$ sudo docker stop Ubuntu
Ubuntu
$ sudo docker rm Ubuntu
Ubuntu
$ sudo docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
