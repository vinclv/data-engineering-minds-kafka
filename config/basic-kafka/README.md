# Basic Kafka Cluster
This repository contains the configuration files required for zookeeper and Kafka brokers for launching a basic 3-node kafka cluster locally without any security. Please check the step-by-step [video tutorial](https://www.youtube.com/watch?v=gwrslUOSez8) on my Youtube channel.

## To check all the brokers connected to the Zookeeper
`
zookeeper-shell.sh localhost:2181
ls /brokers/ids
`

## To check all the topics available on Kafka
`
kafka-topics.sh --zookeeper localhost:2181 --list
`

## To create a topic inside Kafka
`
kafka-topics.sh --zookeeper localhost:2181 --create --topic mytopic --partitions 2 --replication-factor 3
`
## To describe a topic
`
kafka-topics.sh --zookeeper localhost:2181 --describe --topic ssl-topic 
`

## To Monitor the consumer groups
`
kafka-run-class.sh kafka.admin.ConsumerGroupCommand --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --group first-consumer --describe
`

## To check latest Offset on the partition level for a topic
`
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092,localhost:9093 --topic mytopic
`
