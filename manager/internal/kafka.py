from typing import List, Tuple

from confluent_kafka import KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions

from config import KAFKA_HOST, KAFKA_PORT

__all__ = ('KafkaHandler',)


# TODO
#  1. log errors with logger
#  2. add ACLs to topics for that every module has access to its own topic only
#  3. ...


class KafkaHandler:
    def __init__(self, kafka_host=KAFKA_HOST, kafka_port=KAFKA_PORT):
        assert kafka_host is not None, 'kafka_host shouldn\'t be None'
        assert kafka_port is not None, 'kafka_port shouldn\'t be None'

        self.kafka_host = kafka_host
        self.kafka_port = kafka_port

        self.kafka_admin_conf = {
            'bootstrap.servers': f'{self.kafka_host}:{self.kafka_port}'
        }
        self.kafka_admin = AdminClient(self.kafka_admin_conf)

    def create_topics(self, new_topics: List[Tuple[str, int, int]]) -> None:
        new_topics = [
            NewTopic(topic, num_partitions=parts, replication_factor=replicas)
            for
            topic, parts, replicas in new_topics
        ]

        topic_futures = self.kafka_admin.create_topics(new_topics)

        for topic, future in topic_futures.items():
            try:
                future.result()
                print(f"Topic {topic} created")
            except KafkaException as e:
                print(e)

    def delete_topics(self, topics: List[str]):

        topic_futures = self.kafka_admin.delete_topics(topics)

        for topic, future in topic_futures.items():
            try:
                future.result()
                print(f'Topic {topic} deleted')
            except KafkaException as e:
                raise e

    def create_partitions(self, topic_counts: List[Tuple[str, int]]):

        new_parts = [
            NewPartitions(topic, new_count)
            for
            topic, new_count in topic_counts
        ]

        topic_futures = self.kafka_admin.create_partitions(new_parts)

        for topic, future in topic_futures:
            try:
                future.result()
                print(f"Additional partitions created for topic {topic}")
            except KafkaException as e:
                raise e

    def list_topics(self):
        md = self.kafka_admin.list_topics(timeout=10)
        print(" {} topics:".format(len(md.topics)))

        for t in iter(md.topics.values()):
            if t.error is not None:
                errstr = ": {}".format(t.error)
            else:
                errstr = ""

            print(
                "  \"{}\" with {} partition(s){}".format(t, len(t.partitions),
                                                         errstr))

            for p in iter(t.partitions.values()):
                if p.error is not None:
                    errstr = ": {}".format(p.error)
                else:
                    errstr = ""

                print("partition {} leader: {}, replicas: {},"
                      " isrs: {} errstr: {}".format(p.id, p.leader, p.replicas,
                                                    p.isrs, errstr))

    def list_brokers(self):
        md = self.kafka_admin.list_topics(timeout=10)
        print(" {} brokers:".format(len(md.brokers)))
        for b in iter(md.brokers.values()):
            if b.id == md.controller_id:
                print("  {}  (controller)".format(b))
            else:
                print("  {}".format(b))

    def list_groups(self):
        groups = self.kafka_admin.list_groups(timeout=10)
        print(" {} consumer groups".format(len(groups)))
        for g in groups:
            if g.error is not None:
                errstr = ": {}".format(t.error)
            else:
                errstr = ""

            print(" \"{}\" with {} member(s), protocol: {}, protocol_type: "
                  "{}{}".format(
                g, len(g.members), g.protocol, g.protocol_type, errstr)
            )

            for m in g.members:
                print("id {} client_id: {} client_host: {}".format(
                    m.id, m.client_id, m.client_host))
