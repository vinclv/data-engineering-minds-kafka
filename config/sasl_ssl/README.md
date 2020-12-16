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
