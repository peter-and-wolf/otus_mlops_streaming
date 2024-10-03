# otus_mlops_streaming

Предполагаем, что в YaC создан управляемый кластер Kafka.

## Как стартануть ksqldb

Стартуем дополнительные сервисы [kafka-ui](https://docs.kafka-ui.provectus.io/) и [ksql-db](https://ksqldb.io/):

```bash
cd services
docker-compose up
```

## Где писать запросы

Заходим в консоль (`ksqldb-cli`), которая исполняется в docker-контейнере:

```bash
# в корне репозитория
bash run-ksqldb-shell.sh
```

Примечание: этот bash-скрипт выполнит команду `docker exec -it otus-ksqldb-cli ksql http://otus-ksqldb-server:8088`, которая запустит утилиту `ksql` внутри контейнера `otus-ksqldb-cli` и отласт вам терминал.

## Какие запросы мы писали на лекции

1. Создали стрим из топика:

```bash
CREATE STREAM predictions (pred DOUBLE, gt DOUBLE) WITH (kafka_topic='predictions', value_format='json', partitions=3);
```

2. Написали простой [push-запрос](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/select-push-query/) (это такой, который запускается и обрабатывает изменения, пока мы его не прибьем) в стрим:

```bash
SELECT POWER(pred-gt, 2) AS se FROM predictions EMIT CHANGES;
```

3. Написали запрос с агрегацией в [непересекающемся окне](https://docs.ksqldb.io/en/latest/concepts/time-and-windows-in-ksqldb-queries/#tumbling-window), который печатал срочки слишком часто:

```bash
SELECT AVG(POWER(pred-gt, 2)) AS mse FROM predictions WINDOW TUMBLING(SIZE 10 SECONDS) EMIT CHANGES;
```

4. Добавили в предыдущий запрос границы окна и убедились, что границы верные, просто строчки частят:

```bash
SELECT FROM_UNIXTIME(WINDOWSTART) AS ws, FROM_UNIXTIME(WINDOWEND) AS we, AVG(POWER(pred-gt, 2)) AS mse FROM predictions WINDOW TUMBLING(SIZE 10 SECONDS) EMIT CHANGES;
```

5. Поменяли `EMIT CHANGES` на `EMIT FINAL` и получили то, что хотели (агрегацию среднеквадратичной ошибки в 10-секундных окнах):

```bash
SELECT FROM_UNIXTIME(WINDOWSTART) AS ws, FROM_UNIXTIME(WINDOWEND) AS we, AVG(POWER(pred-gt, 2)) AS mse FROM predictions WINDOW TUMBLING(SIZE 10 SECONDS) EMIT FINAL;
```








