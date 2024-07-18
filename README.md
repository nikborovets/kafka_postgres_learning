# Kafka-Postgres Learning Project

Этот проект создан для изучения работы с Apache Kafka и PostgreSQL с использованием Python  и Django.

## Описание

Проект включает четыре основных компонента:

1. **Producer**: Захватывает кадры с веб-камеры и отправляет их в Kafka.
2. **Consumer**: Читает кадры из Kafka, обрабатывает их (преобразует в оттенки серого) и сохраняет в PostgreSQL.
3. **Analyzer**: Анализирует кадры, хранящиеся в PostgreSQL, и может создавать видео из этих кадров.
4. **Web Interface**: Веб-интерфейс на Django, который повторяет функциональность **Analyzer**. Также в админской панели можно управлять кадрами (удалять, изменять, добавлять).


## Установка

### Bash

Запустите скрипт `setup.sh`, который автоматически создаст виртуальное окружение, установит необходимые зависимости из `requirements.txt`, настроит докер-контейнеры для Kafka, Zookeeper и PostgreSQL, а также проверит их состояние перед созданием таблицы в базе данных PostgreSQL.

Если Python установлен не в /usr/bin/python3, то измените файл `setup.sh`, заменив /usr/bin/python3 на путь к вашему python3. 

```sh
./setup.sh
```

### Настройка и запуск
`Django`

```sh
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
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


### Использование
1. `http://127.0.0.1:8000/admin/` - доступ к админке `Django`.
2. `http://127.0.0.1:8000/frames/` - функционал `analyzer.py`.
