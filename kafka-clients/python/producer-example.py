from confluent_kafka import Producer
from faker import Faker # to generate random names
from random import randint # to generate random IDs
import time

def delivery_report(err, msg):
    if err:
        """
         - In case of KafkaError, check whether the error is retriable (via setting retries in producer config) or not
         - If not retriable, then the producer may take any action as part of this application
         - For example, such failed records which are not retriable can be written to backup files and retried manually later
        """
        if str(type(err).__name__) == "KafkaError":
            print(f"Message failed with error : {str(err)}")
            print(f"Message Retry? :: {err.retriable()}")
        else:
            print(f"Message failed with error : {str(err)}")
    else:
        print(f"Message delivered to partition {msg.partition()}; Offset Value - {msg.offset()}")
        print(f"{msg.value()}")

def run_producer():
    p = Producer({'bootstrap.servers':'localhost:9092,localhost:9093,localhost:9094',
                  'security.protocol':'sasl_ssl','sasl.mechanism':'SCRAM-SHA-512',
                  'ssl.ca.location':'/Users/vinod/mymac/kafka/ssl/ca-cert',
                  'sasl.username':'demo-user','sasl.password':'Vinod123',
                  'acks':'-1','partitioner':'consistent_random','batch.num.messages':'1000',
                  'linger.ms':'100',
                  'queue.buffering.max.messages':'10000'})

    #topic_info = p.list_topics()
    #print(topic_info.brokers)

    for i in range(0,3):
        msg_value = {'id': randint(0, 100),'name': Faker('en_US').name()}
        msg_header = {"source" : b'DEM'}
        while True:
            try:
                p.poll(timeout=0)
                p.produce(topic='demo-topic', value=str(msg_value), headers=msg_header, on_delivery=delivery_report)
                break
            except BufferError as buffer_error:
                print(f"{buffer_error} :: Waiting until Queue gets some free space")
                time.sleep(1)
    p.flush()



if __name__ == "__main__":
    run_producer()