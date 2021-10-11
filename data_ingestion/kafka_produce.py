from kafka import KafkaProducer, KafkaConsumer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:29092'])#, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
print("Connected to Kafka!!")
for x in range(1100, 1150):
    data = json.dumps({'number': x})
    print(f'Upload Data: {data}')
    producer.send('news', value=bytes(data, encoding="utf8"))