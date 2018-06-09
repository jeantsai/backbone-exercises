from kafka import KafkaConsumer
# from kafka.errors import KafkaError
import redis
from dns_resolver import get_redis_address


API_USAGE_KEY = 'visit:api:total'
API_USAGE_TOPIC = 'api-visits'

# Fetch the address of service redis from Consul
(redis_ip, redis_port) = get_redis_address()
print('Got the address of service redis as: %s:%i' % (redis_ip, redis_port))
r = redis.Redis(host=redis_ip, port=redis_port, decode_responses=True)

consumer = KafkaConsumer(API_USAGE_TOPIC, bootstrap_servers=['kafka:29092'])

for msg in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (
        msg.topic, msg.partition, msg.offset, msg.key, msg.value))
    r.incr(API_USAGE_KEY)

# def on_send_success(record_metadata):
#     print(record_metadata.topic)
#     print(record_metadata.partition)
#     print(record_metadata.offset)

# def on_send_error(excp):
#     log.error('I am an errback', exc_info=excp)
#     # handle exception

# # produce asynchronously with callbacks
# producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

# # block until all async messages are sent
# producer.flush()

# # configure multiple retries
# producer = KafkaProducer(retries=5)
