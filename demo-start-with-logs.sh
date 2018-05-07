# Start Consul and our backend services - redis, backend - as docker containers
# The number of Consul instances should be above a quorum of three
docker-compose -p ce up --scale consul=3
