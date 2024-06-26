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

После того, как зашли в терминал в ubuntu в докере, можно например проверить версию ubuntu

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

## Portainer

Качаем образ

```
$ sudo docker pull portainer/portainer-ce:latest
...
$ sudo docker images
REPOSITORY               TAG       IMAGE ID       CREATED       SIZE
ubuntu                   20.04     5f5250218d28   6 days ago    72.8MB
portainer/portainer-ce   latest    a3f85c245ec3   7 weeks ago   293MB
```

Создаём папку, куда пробросим volume для портейнера

```
$ mkdir ./portainer_data
```

Запустим контейнер в detached режиме, пробросив порты 8000 и 9443 на локальную машину, указав, что контейнер должен перезапускаться всегда, а также данные в директории `/data` в контейнере будут проброшены в папку `./portainer_data` на локальной машине. `/var/run/docker.sock:/var/run/docker.sock` позволяет Portainer взаимодействовать с Docker на локальном хосте

```
$ sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v ./portainer_data:/data portainer/portainer-ce:latest
9504b302...
$ sudo docker ps
CONTAINER ID   IMAGE                           COMMAND        CREATED         STATUS         PORTS                                                                                            NAMES
9504b302b84f   portainer/portainer-ce:latest   "/portainer"   7 seconds ago   Up 6 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp, 0.0.0.0:9443->9443/tcp, :::9443->9443/tcp, 9000/tcp   portainer
```

Проверим у себя папку `./portainer_data`

```
$ ls ./portainer_data/
bin  certs  chisel  compose  docker_config  portainer.db  portainer.key  portainer.pub  tls
```

Теперь можно перейти по адресу https://localhost:9443, чтобы проверить работоспособность портейнера

![Portainer](./img/portainer.png)

Остановим контейнер, удалим данные

```
$ sudo docker stop portainer
portainer
$ sudo docker rm portainer
portainer
$ sudo rm -R ./portainer_data/
$ ls ./portainer_data
ls: невозможно получить доступ к './portainer_data': Нет такого файла или каталога
```
