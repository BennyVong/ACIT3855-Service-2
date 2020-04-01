import json
from threading import Thread

import connexion
import pykafka
import yaml
import logging.config
from connexion import NoContent
from pykafka import KafkaClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Date, cast
from .base import Base
from .inventory import Inventory
from .status import Status
import datetime

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(
    'mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +
    app_config['datastore']['hostname'] + ':' + app_config['datastore']['port'] + '/' + app_config['datastore']['db'])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_inventory(start_date=None, end_date=None):
    logger.info("Get Inventory")
    """ Get inventory reports from the data store """

    results_list = []

    session = DB_SESSION()

    if start_date is None:
        results = session.query(Inventory).filter(Inventory.date_created.between('2018-01-01', '2021-01-01'))
    else:
        results = session.query(Inventory).filter(Inventory.date_created.between(start_date, end_date))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200


def get_status(start_date=None, end_date=None):
    logger.info("Get Status")
    """ Get status reports from the data store """

    results_list = []

    session = DB_SESSION()

    if start_date is None:
        results = session.query(Status).filter(Status.date_created.between('2018-01-01', '2021-01-01'))
    else:
        results = session.query(Status).filter(Status.date_created.between(start_date, end_date))

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 200


def process_messages():
    logger.info("Process Messages")
    client = KafkaClient(hosts="{}:{}".format(app_config["kafka"]["host"], app_config["kafka"]["port"]))
    topic = client.topics[app_config["kafka"]["topic"]]
    consumer = topic.get_simple_consumer(consumer_group="events", auto_offset_reset=pykafka.common.OffsetType.EARLIEST,
                                         reset_offset_on_start=False,
                                         auto_commit_enable=True,
                                         auto_commit_interval_ms=1000)
    for message in consumer:
        if message is not None:
            msg_str = message.value.decode('utf-8')
            msg = json.loads(msg_str)

            print(msg)

            session = DB_SESSION()

            if msg['type'] == 'inventory':
                session.add(Inventory(msg['payload']['item_id'], msg['payload']['name'], msg['payload']['manufacturer'], msg['payload']['warehouse']))
            elif msg['type'] == 'status':
                session.add(Status(msg['payload']['item_id'], msg['payload']['status'], msg['payload']['destination'], msg['payload']['deliverydate']))

            session.commit()
            session.close()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    app.run(port=8090)
