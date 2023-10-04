# KRAFT - Basic Cluster
This repository contains all the necessary configuration files for launching a Kafka cluster that runs in,
* Kraft mode, i.e., without zookeeper
* With no security - PLAINTEXT mechanism

**Please Note**: The configurations are tested, as of this date, with Apache Kafka V3.5.1

### Steps to launch a Kafka cluster in Kraft Mode

* Generate a cluster ID
```
    KAFKA_CLUSTER_ID="$(kafka-storage.sh random-uuid)"
```
* Format the data and metdata directories for each node
```
    kafka-storage --cluster-id $KAFKA_CLUSTER_ID --config /PATH-TO-YOUR-KAFKA-DIR/config/kraft/server-0.properties
```
* Set the path for logging for each node
```
    export KAFKA_LOG4J_OPTS="-Dlog4j.configuration=file:/PATH-TO-YOUR-KAFKA-DIR/config/node-0-log4j.properties"
```
* Start the server application for each node
```
    kafka-server-start -daemon /PATH-TO-YOUR-KAFKA-DIR/config/kraft/server-0.properties
```

### Shell Utilities and Useful commands
#### kafka-cluster.sh
* To check the Kafka cluster ID
```
    kafka-cluster cluster-id --bootstrap-server localhost:9092,localhost:9096,localhost:9097
```
####  kafka-metadata-quorum.sh
* To check the leader, followers and observers of the Quorum Controller
```
    kafka-metadata-quorum.sh --bootstrap-server localhost:9092,localhost:9096,localhost:9097 describe --status
```
* To check the replication status & metadata lag between leader, followers and observers of the Quorum Controller
```
    kafka-metadata-quorum.sh --bootstrap-server localhost:9092,localhost:9096,localhost:9097 describe --replication
```
####  kafka-metadata-shell.sh 
* Open a shell terminal with one of the metadata files as input
```
    kafka-metadata-shell.sh --snapshot /PATH-TO-YOUR-KAFKA-DIR/metadata/node-0/__cluster_metadata-0/00000000000000000000.log
```
* To check the version of Apache Kafka
```
    cat local/version
``` 
* To check all the available brokers in the cluster
```
    ls /image/cluster
```
* To find some useful statuses of a broker by means of its node ID
```
    cat /image/cluster/0
```
* To check find the topics in the cluster
```
    ls /image/topics/byName
```
* To check the status of each partition in a topic, for example - my-topic
```
    cat /image/topics/byName/my-topic/0
    cat /image/topics/byName/my-topic/1
```

### Topics, Produce and Consume messages (including other useful commands)

* Create a topic
```
    kafka-topics --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --create --topic kraft-topic --partitions 2 --replication-factor 3
```
* List all the topics inside the cluster
```
    kafka-topics --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --list
```
* Describe a topic
```
    kafka-topics --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --describe --topic kraft-topic
```
* Produce messages to a topic
```
    kafka-console-producer --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --topic kraft-topic
```
* Consume messages from a topic
```
    kafka-console-consumer --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --topic kraft-topic --from-beginning --group kraft-group
```
* List all the consumer groups inside the cluster
```
    kafka-consumer-groups --bootstrap-server localhost:9092,localhost:9096,localhost:9097  --list
```
* Check the status of a consumer group
```
    kafka-consumer-groups --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --describe --group kraft-group
```
* List all the consumers inside a consumer group
```
    kafka-consumer-groups --bootstrap-server localhost:9092,localhost:9096,localhost:9097 --describe --group kraft-group --members --verbose
```
* Describe the assignment stratgey and state of a consumer group
```
    kafka-consumer-groups --bootstrap-server  localhost:9092,localhost:9096,localhost:9097 --describe --group kraft-group --state
```