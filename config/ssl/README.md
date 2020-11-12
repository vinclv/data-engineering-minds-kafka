# ssl
This repository contains the configuration files for zookeeper, Kafka brokers, producers, and consumers for launching a basic 3-node kafka cluster with SSL security.


### Steps to generate CA, Truststore and Keystore 

**Please Note** - For Truststores and Keystores, I have shown the steps only to generate *kafka.zookeeper.truststore.jks* and *kafka.zookeeper.keystore.jks*. The procedure is the same for generating such files for brokers, producers, and consumers.

**1. Generate CA**
openssl req -new -x509 -keyout ca-key -out ca-cert -days 3650

**2. Create Truststore**
keytool -keystore kafka.zookeeper.truststore.jks -alias ca-cert -import -file ca-cert

**3. Create Keystore**
keytool -keystore kafka.zookeeper.keystore.jks -alias zookeeper -validity 3650 -genkey -keyalg RSA -ext SAN=dns:localhost

**4. Create certificate signing request (CSR)**
keytool -keystore kafka.zookeeper.keystore.jks -alias zookeeper -certreq -file ca-request-zookeeper

**5. Sign the CSR**
openssl x509 -req -CA ca-cert -CAkey ca-key -in ca-request-zookeeper -out ca-signed-zookeeper -days 3650 -CAcreateserial

**6. Import the CA into Keystore**
keytool -keystore kafka.zookeeper.keystore.jks -alias ca-cert -import -file ca-cert

**7. Import the signed certificate from step 5 into Keystore**
keytool -keystore kafka.zookeeper.keystore.jks -alias zookeeper -import -file ca-signed-zookeeper



