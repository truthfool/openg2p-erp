import requests
import json
from .kafka_producer_events import producer_events


def webhook_event(webhook_data, webhook_url):
    print(webhook_data)

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(webhook_data),
                                 headers=headers)

        # Sending to kafka topic
        producer_events(webhook_data)

    except BaseException as e:
        print(e)
