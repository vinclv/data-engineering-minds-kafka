# Kafka Topic creation in secured way
Moving forward, please don't create topics via *kafka-topics.sh* connecting to zookeeper due to the following two reasons:

1. There is no support for *kafka-topics.sh* to connect to the zookeeper in secured manner. Hence, we still need to connect via the unsecured port 2181.
2. Zookeeper is going to be removed from the Apache Kafka ecosystem and all the external metadata management will be taken care by the brokers themselves. Hence, it is high time we need to slowly replace zookeeper-relevant parameters by broker-related parameters (such as bootstrap-server) whenever Kafka releases the new support. You can find more details [here](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum).

Therefore, from now on, we can create Kafka topics (and perform other topic related activities) via *kafka-topics.sh* connecting directly to the brokers.

## Steps:
### Method 1 (Not a recommended practice in Production):
1. Create a file *kafka-admin.properties* and add all the necessary configuration details. Please check [here](https://github.com/vinclv/data-engineering-minds-kafka/blob/main/config/sasl_ssl/kafka-admin.properties).
2. You can find the steps to create the truststore file [here](https://github.com/vinclv/data-engineering-minds-kafka/blob/main/config/ssl/README.md).
3. For SASL username/password, you can use the credentials you supplied for brokers (server.properties) since it has super-user access.
4. Finally, create the topic using the below command:

    ` 
    kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config kafka-admin.properties --create --topic my-topic --partitions 2 --replication-factor 3 --config min.insync.replicas=2
    `
### Method 2:
1. Follow the first two steps as in Method 1.
2. For Production environments, it is not a recommended practice to use the same credentials used for brokers for daily kafka administration activities. Hence, create a new SASL credential using the below command:

    `
    kafka-configs.sh --zookeeper localhost:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --entity-name kafka-admin --alter --add-config 'SCRAM-SHA-512=[password=Dem123]'
    `

3. Now, for granting the super-user access to the above credential, execute the following ACLs:
    <br/>
    **FULL ACCESS for Topics**<br/>
    `
    kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:kafka-admin --operation READ --operation WRITE --operation DESCRIBE --operation DESCRIBECONFIGS --operation ALTER --operation ALTERCONFIGS --operation CREATE --operation DELETE --topic '*'
    `
    
    **FULL ACCESS for Groups**<br/>
    `
    kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:kafka-admin --operation READ --operation DESCRIBE --operation DELETE --group '*'
    `
    
    **FULL ACCESS for delegation-tokens**<br/>
    `
    kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:kafka-admin --operation DESCRIBE --delegation-token '*'
    `
    
    **FULL ACCESS for transactional clients**<br/>
    `
    kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:kafka-admin --operation DESCRIBE --operation WRITE  --transactional-id '*'
    `
    
    **FULL ACCESS to the cluster**<br/>
    `
    kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:kafka-admin --operation ALTER --operation ALTERCONFIGS --operation CLUSTERACTION --operation CREATE --operation DESCRIBE --operation DESCRIBECONFIGS --operation IDEMPOTENTWRITE --cluster SdiG0K04TmqP-i-m7tWdsw
    `

    **Note** - If you want to know how to find the ID of your cluster, connect to zookeeper shell and execute *get /cluster/id*.

4. Finally, create the topic using the below command:

    ` 
    kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config kafka-admin.properties --create --topic my-topic --partitions 2 --replication-factor 3 --config min.insync.replicas=2
    `

5. For listing the available topics inside the Kafka cluster, execute the below command:

    ` 
    kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config kafka-admin.properties --list
    `

6. To describe a specific topic, execute the below command:

    ` 
    kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --command-config kafka-admin.properties --describe --topic my-topic
    `





