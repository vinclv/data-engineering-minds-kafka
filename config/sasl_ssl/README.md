# SASL_SSL
This repository contains the configuration files for zookeeper, Kafka brokers, producers, and consumers for launching a basic 3-node kafka cluster with SASL_SSL security. Please check the step-by-step [video tutorial](https://www.youtube.com/watch?v=U0XennY3_Ac) on my Youtube channel.

## Note
Please remember just for showing a demo, I have shown the password directly inside the property files. Please never do that on a production environment; oor make sure that the property files are placed inside admin-only directorires with highly restricted access.


### kafka-configs.sh commands to create, delete and list SASL/SCRAM credentials
#### To create a SASL/SCRAM user
`kafka-configs.sh --zookeeper localhost:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --entity-name my-user --alter --add-config 'SCRAM-SHA-512=[password=DEM123]'`

#### To describe a SASL/SCRAM user
`kafka-configs.sh --zookeeper localhost:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --entity-name my-user --describe`

#### To describe/list all available SASL/SCRAM users
`kafka-configs.sh --zookeeper localhost:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --describe`

#### To delete a SASL/SCRAM user
`kafka-configs.sh --zookeeper localhost:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --entity-name my-user --alter --delete-config 'SCRAM-SHA-512'`

### Example ACL commands 
#### To grant PRODUCER access for the user to the topic *mytopic*
`kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:my-user --operation WRITE --operation DESCRIBE --operation DESCRIBECONFIGS --topic mytopic`

#### To grant CONSUMER access for the user to the topic *mytopic* and with consumer group *mycgroup*

`kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:my-user --operation READ --operation DESCRIBE --topic mytopic`

`kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:my-user --operation READ --group mycgroup`

#### To list all the ACLs associated with the user
`kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --list --principal User:my-user`

### To check all the brokers connected to the Zookeeper running in 2-way SSL mode
`
zookeeper-shell.sh localhost:2182 -zk-tls-config-file zookeeper-client.properties
ls /brokers/ids
`

### To check all the topics available on Kafka
`
kafka-topics.sh --zookeeper localhost:2181 --list
`

### To create a topic inside Kafka
`
kafka-topics.sh --zookeeper localhost:2181 --create --topic mytopic --partitions 2 --replication-factor 3
`

### To describe a topic
`
kafka-topics.sh --zookeeper localhost:2181 --describe --topic ssl-topic 
`

## Commands for kafka-consumer-groups.sh

### To list all the consumer groups
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config consumer-group-client.properties --list
`

### To describe the consumer group
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config consumer-group-client.properties --describe --group sasl-consumer
`

### To describe all the members of the consumer group
´
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config consumer-group-client.properties --describe --group sasl-consumer --members
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config consumer-group-client.properties --describe --group sasl-consumer --members --verbose
`

### To describe the state of the consumer group
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config consumer-group-client.properties --describe --group sasl-consumer --state
`

### To reset the offsets of the consumer group on a topic level

#### To latest offset
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094  --command-config consumer-group-client.properties --group sasl-consumer --reset-offsets --topic  ssl-topic --to-latest --execute
`

#### To least offset 
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094  --command-config consumer-group-client.properties --group sasl-consumer --reset-offsets --topic  ssl-topic --to-earliest --execute
`

#### To shift by number of offsets
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094  --command-config consumer-group-client.properties --group sasl-consumer --dry-run --reset-offsets --topic  ssl-topic --shift-by 1 --execute
`

#### To perform dry run without executing
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094  --command-config consumer-group-client.properties --group sasl-consumer --dry-run --reset-offsets --topic  ssl-topic --to-latest
`

#### To reset offsets on partition level 
`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094  --command-config consumer-group-client.properties --group sasl-consumer --reset-offsets --topic  ssl-topic:0 --to-latest --execute
`

`
kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094  --command-config consumer-group-client.properties --group sasl-consumer --reset-offsets --topic  ssl-topic:1 --to-latest --execute
`
