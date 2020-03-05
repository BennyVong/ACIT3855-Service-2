import datetime
import json
import connexion
from connexion import NoContent
import requests
from pykafka import KafkaClient

from Lab2.inventory import Inventory
from Lab2.status import Status


# Your function here
def add_inventory(inventoryReading):
    # r = requests.post('http://0.0.0.0:8090/report/inventory', data=Inventory(inventoryReading['item_id'],
    #                                                                          inventoryReading['name'],
    #                                                                          inventoryReading['manufacturer'],
    #                                                                          inventoryReading['warehouse']))
    client = KafkaClient(hosts='localhost:9092')
    topic = client.topics['events']
    producer = topic.get_sync_producer()
    msg = {
        "type": "inventory",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": inventoryReading
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201


def add_status(itemStatus):
    # r = requests.post('http://0.0.0.0:8090/report/status', data=Status(itemStatus['item_id'],
    #                                                                    itemStatus['status'],
    #                                                                    itemStatus['destination'],
    #                                                                    itemStatus['deliverydate']))

    client = KafkaClient(hosts='localhost:9092')
    topic = client.topics['events']
    producer = topic.get_sync_producer()
    msg = {
        "type": "status",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": itemStatus
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)
