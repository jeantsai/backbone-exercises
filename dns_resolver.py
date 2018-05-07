import sys
import logging
from dns import resolver
import socket
import time


def lookup_consul_ip():
    logger = logging.getLogger(__name__)
    logger.info("Finding IP of Service Registry (Consul) ...")
    consul_server_ip = socket.gethostbyname('consului')

    logger.info("Found IP of Service Registry (Consul): %s" % consul_server_ip)
    return consul_server_ip


def lookup_redis_address(consul_server_ip):
    consul_resolver = resolver.Resolver()
    consul_resolver.port = 8600
    consul_resolver.nameservers = [consul_server_ip]

    logger = logging.getLogger(__name__)
    logger.info("Finding service address of Redis ...")
    dns_answer = consul_resolver.query("redis.service.consul", 'A')
    ip = str(dns_answer[0])
    dns_answer_srv = consul_resolver.query("redis.service.consul", 'SRV')
    port = int(str(dns_answer_srv[0]).split()[2])

    logger.info("Found service address of Redis: ip=%s port=%d" % (ip, port))
    return ip, port


def get_redis_address():
    consul_ip = lookup_consul_ip()
    count = 18
    while count > 0:
        try:
            time.sleep(10)
            (ip, port) = lookup_redis_address(consul_ip)
            return ip, port
        except:
            count -= 1
            if count == 0:
                raise


if __name__ == '__main__':
    # Setup logging facility
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s'))
    logger = logging.getLogger('')
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    # Run the main function of this module
    logger.info('This module resolve the address of '
                'a service (Redis) through Consul DNS SRV service.')
    get_redis_address()
