import time
import json
import pandas as pd
import gc
from kafka import KafkaProducer
from pathlib import Path


TOPIC = 'customs_log'
BATCH_SIZE = 5000


def get_file() -> str:
    paths = []
    paths.append(Path('/') /'data_share' / '01_indigestion' / 'out')
    paths.append(Path('..') / '..' / 'data_share' / '01_indigestion' / 'out')
    outpath = '/'

    for path in paths:
        path = path.resolve()
        if path.exists():
            outpath = path
            break

    return str(outpath / 'customs_data.csv')


def serializer(value):
    return json.dumps(value).encode('utf-8')


def send_batch(producer, messages, batch):
    for message in messages:
        producer.send(topic=TOPIC, value=message)

    if batch % 20 == 0:
        producer.flush(timeout=60)


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer,
    compression_type='gzip',
    acks=1,
)


if __name__ == '__main__':
    time_start = time.perf_counter()

    csv = get_file()

    chunk_size = 100000
    batch_messages = []
    batch = 1

    for chunk in pd.read_csv(csv, sep='\t', chunksize=chunk_size):
        messages = chunk.to_dict(orient='records')

        for message in messages:
            batch_messages.append(message)

            if len(batch_messages) >= BATCH_SIZE:
                send_batch(producer, batch_messages, batch)
                batch_messages = []
                batch += 1

        if batch_messages:
            send_batch(producer, batch_messages, batch)
            batch_messages = []
            batch += 1

        del messages
        del chunk
        gc.collect()

    '''
    df = pd.read_csv(csv, sep='\t')

    for row in df.itertuples():
        message = {col: getattr(row, col) for col in df.columns}
        producer.send(topic=TOPIC, value=message)
    '''

    producer.flush(timeout=300)
    producer.close()

    time_end = time.perf_counter()
    total_time = time_end - time_start
    print(f'Total time: {total_time:.2f}')