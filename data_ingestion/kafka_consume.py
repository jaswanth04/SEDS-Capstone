from kafka import KafkaProducer, KafkaConsumer
import json


consumer = KafkaConsumer(group_id='test', bootstrap_servers=['localhost:29092'], auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
topics = consumer.topics()
print(topics)
consumer.subscribe(['news'])


for message in consumer:
    print(message.value)

