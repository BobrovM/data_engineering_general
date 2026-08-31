'''
This one just tests consumer side
'''
import json
from kafka import KafkaConsumer


if __name__ == '__main__':
    row = 0
    consumer = KafkaConsumer(
        'customs_log',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
    )
    for message in consumer:
        try:
            print(json.loads(message.value))
            row += 1
            print(row)
        except json.decoder.JSONDecodeError as e:
            print(f'Not json: {e}')
            continue