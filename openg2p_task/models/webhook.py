import requests
import json
from .kafka_producer_events import producer_events


# from odoo.http import Controller, route, request
#
#
# class WebhookReceiver(Controller):
#     @route("/webhook-events", type="json", auth="user", methods=["POST"])
#     def events(self):
#         if request.method == "POST":
#             print(request.json)
#         else:
#             print("No data")

def webhook_event(webhook_data):

    webhook_url = "https://webhook.site/d71e0313-1842-4da9-93e8-088ce92f9a67"

    print(webhook_data)

    producer_events(webhook_data)

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(webhook_data),
                                 headers=headers)

    except BaseException as e:
        print(e)
