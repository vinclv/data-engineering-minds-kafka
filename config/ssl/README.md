# SSL
This repository contains the configuration files for zookeeper, zookeeper clients, Kafka brokers, producers, and consumers for launching a basic 3-node kafka cluster with SSL security. Please check the step-by-step [video tutorial](https://www.youtube.com/watch?v=hR_OuiqLgOo) on my Youtube channel.


### Steps to generate CA, Truststore and Keystore 

**Please Note** - For Truststores and Keystores, I have shown the steps only to generate *kafka.zookeeper.truststore.jks* and *kafka.zookeeper.keystore.jks*. The procedure is the same for generating such files for brokers, producers, and consumers.

**1. Generate CA** <br />
openssl req -new -x509 -keyout ca-key -out ca-cert -days 3650

**2. Create Truststore** <br />
keytool -keystore kafka.zookeeper.truststore.jks -alias ca-cert -import -file ca-cert

**3. Create Keystore** <br />
keytool -keystore kafka.zookeeper.keystore.jks -alias zookeeper -validity 3650 -genkey -keyalg RSA -ext SAN=dns:localhost

**4. Create certificate signing request (CSR)** <br />
keytool -keystore kafka.zookeeper.keystore.jks -alias zookeeper -certreq -file ca-request-zookeeper

**5. Sign the CSR** <br />
openssl x509 -req -CA ca-cert -CAkey ca-key -in ca-request-zookeeper -out ca-signed-zookeeper -days 3650 -CAcreateserial

**6. Import the CA into Keystore** <br />
keytool -keystore kafka.zookeeper.keystore.jks -alias ca-cert -import -file ca-cert

**7. Import the signed certificate from step 5 into Keystore** <br />
keytool -keystore kafka.zookeeper.keystore.jks -alias zookeeper -import -file ca-signed-zookeeper


### To check all the brokers connected to the Zookeeper running in 2-way SSL mode
`
zookeeper-shell.sh localhost:2182 -zk-tls-config-file zookeeper-client.properties
ls /brokers/ids
`

### To check all the topics available on Kafka
`
kafka-topics.sh --zookeeper localhost:2181 --list
`

*For latest versions of Apache Kafka,*<br/>
`
kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --list
`
### To create a topic inside Kafka
`
kafka-topics.sh --zookeeper localhost:2181 --create --topic mytopic --partitions 2 --replication-factor 3
`

*For latest versions of Apache Kafka,*<br/>
`
kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --create --topic mytopic --partitions 2 --replication-factor 3
`
#### To create a topic with additional configurations
`
kafka-topics.sh --zookeeper localhost:2181 --create --topic my-topic --partitions 2 --replication-factor 3 --config min.insync.replicas=2
`

*For latest versions of Apache Kafka,*<br/>
`
kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --create --topic my-topic --partitions 2 --replication-factor 3 --config min.insync.replicas=2
`
### To describe a topic
`
kafka-topics.sh --zookeeper localhost:2181 --describe --topic my-topic
`

*For latest versions of Apache Kafka,*<br/>
`
kafka-topics.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --describe --topic my-topic
`