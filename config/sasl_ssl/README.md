# SASL_SSL
This repository contains the configuration files for zookeeper, Kafka brokers, producers, and consumers for launching a basic 3-node kafka cluster with SASL_SSL security.

## Note
Please remember just for showing a demo, I have shown the password directly inside the property files. Please never do that on a production environment; oor make sure that the property files are placed inside admin-only directorires with highly restricted access.

### Example command to create a SASL/SCRAM username/password
`kafka-configs.sh --zookeeper localhost:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --entity-name my-user --alter --add-config 'SCRAM-SHA-512=[password=DEM123]'`

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

### To Monitor the consumer groups
`
kafka-run-class.sh kafka.admin.ConsumerGroupCommand --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --group first-consumer --describe
`

### To check latest Offset on the partition level for a topic
`
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092,localhost:9093 --topic mytopic
`