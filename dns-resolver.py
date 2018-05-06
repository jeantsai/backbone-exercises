import sys
import logging
from dns import resolver
import socket


consul_server_ip = socket.gethostbyname('consului')

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

consul_resolver = resolver.Resolver()
consul_resolver.port = 8600
consul_resolver.nameservers = [consul_server_ip]

dnsanswer = consul_resolver.query("redis.service.consul", 'A')
ip = str(dnsanswer[0])
dnsanswer_srv = consul_resolver.query("redis.service.consul", 'SRV')
port = int(str(dnsanswer_srv[0]).split()[2])

log.info("Got Redis service address from Consul: ip=%s port=%d" % (ip, port))

