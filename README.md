# Kafka-Postgres Learning Project

Этот проект создан для изучения работы с Apache Kafka и PostgreSQL с использованием Python.

## Описание

Проект включает три основных компонента:

1. **Producer**: Генерирует данные заказов и отправляет их в Kafka.
2. **Consumer**: Читает данные заказов из Kafka и сохраняет их в PostgreSQL.
3. **Analyzer**: Анализирует данные заказов, хранящиеся в PostgreSQL.

## Установка

### Bash

Запустите скрипт `setup.sh`, который автоматически создаст виртуальное окружение, установит необходимые зависимости из `requirements.txt`, настроит докер-контейнеры для Kafka, Zookeeper и PostgreSQL, а также проверит их состояние перед созданием таблицы в базе данных PostgreSQL.

Если Python установлен не в /usr/bin/python3, то измените файл `setup.sh`, заменив /usr/bin/python3 на путь к вашему python3. 

```sh
./setup.sh
```

### Важно!

Для наглядности рекомендуется запускать `producer.py`, `consumer.py` и `analyzer.py` в отдельных терминалах.

```sh
source myenv/bin/activate && python producer.py
```

```sh
source myenv/bin/activate && python consumer.py
```

```sh
source myenv/bin/activate && python analyzer.py
```