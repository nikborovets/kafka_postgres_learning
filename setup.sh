#!/bin/bash

set -e

virtualenv -p /usr/bin/python3 myenv
source myenv/bin/activate

pip install -r requirements.txt

docker-compose up -d

echo "Waiting for containers to start..."
containers=(kafka_postgres_learning-postgres-1 kafka_postgres_learning-zookeeper-1 kafka_postgres_learning-kafka-1)

for container in "${containers[@]}"; do
  while [ "$(docker inspect -f '{{.State.Running}}' $container)" != "true" ]; do
    echo "Waiting for container $container..."
    sleep 5
  done
done

sleep 3

docker exec -i kafka_postgres_learning-postgres-1 psql -U user -d orders_db << EOF
CREATE TABLE IF NOT EXISTS frames (
    frame_id SERIAL PRIMARY KEY,
    frame_data TEXT NOT NULL,
    timestamp BIGINT NOT NULL
);
EOF

# python producer.py &
# python consumer.py &
# python analyzer.py &