import os
from odoo import fields, models
from datetime import date, datetime
import csv
import requests
import uuid
import boto3 
import pandas as pd

class CronBatchTransaction(models.Model):
    _name="openg2p.cron.batch.transaction"

    def cron_create_batch_transaction(self):
        
        batches_list=self.env["openg2p.disbursement.batch.transaction"].search([("state","=","draft")])

        if not batches_list:
            return

        for batch in batches_list:
            self.create_bulk_transfer_cron(batch)

    def create_bulk_transfer_cron(self,batch):
    
        batch._generate_uuid()

        limit = 100
        beneficiary_transactions = self.env["openg2p.disbursement.main"].search(
            [("batch_id", "=", batch.batch_id)], limit=limit
        )

        offset = 0

        # CSV filename as RequestID+Datetime
        csvname = (
            batch.request_id
            + "-"
            + str(datetime.now().strftime(r"%Y%m%d%H%M%S"))
            + ".csv"
        )

        while len(beneficiary_transactions) > 0:

            with open(csvname, "a") as csvfile:
                csvwriter = csv.writer(csvfile)
                for rec in beneficiary_transactions:
                    entry = [
                        rec.id,
                        rec.beneficiary_request_id,
                        rec.payment_mode,
                        rec.name,
                        rec.acc_holder_name,
                        rec.amount,
                        rec.currency_id.name,
                        rec.note
                    ]

                    # id,request_id,payment_mode,acc_number,acc_holder_name,amount,currency,note
                    beneficiary_transaction_records = []
                    beneficiary_transaction_records.append(entry)
                    csvwriter.writerows(
                        map(lambda x: [x], beneficiary_transaction_records)
                    )

            offset += len(beneficiary_transactions)

            if len(beneficiary_transactions) < limit:
                break
            beneficiary_transactions = self.env["openg2p.disbursement.main"].search(
                [("batch_id", "=", batch.batch_id)], limit=limit, offset=offset
            )

        # Uploading to AWS bucket
        uploaded = batch.upload_to_aws(csvname, "paymenthub-ee-dev")
        
        headers = {
            'Platform-TenantId': 'ibank-usa',
        }
        files = {
            "data": (csvname, open(csvname, "rb")),
            "request_id": (None, str(batch.request_id)),
            "note": (None, "Bulk transfers"),
            # "checksum": (None, str(batch.generate_hash(csvname))),
        }

        url="http://channel.ibank.financial/channel/bulk/transfer"

        try:
            response = requests.post(url, headers=headers, files=files)
            response_data = response.json()
            
            self.transaction_status = response_data["status"]
            self.transaction_batch_id = response_data["batch_id"]

        except BaseException as e:
            return e
        