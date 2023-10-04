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

