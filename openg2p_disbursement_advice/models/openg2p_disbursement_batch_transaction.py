# -*- coding: utf-8 -*-
# Copyright 2020 OpenG2P (https://openg2p.org)
# @author: Salton Massally <saltonmassally@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
import csv
import hashlib
import logging
import uuid
from datetime import date, datetime
from io import StringIO
from dotenv import load_dotenv  # for python-dotenv method
import boto3
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)
BATCH_SIZE = 500

load_dotenv()  # for python-dotenv method


class BatchTransaction(models.Model):
    _name = "openg2p.disbursement.batch.transaction"
    _description = "Disbursement Batch"
    _inherit = ["generic.mixin.no.unlink", "mail.thread", "openg2p.mixin.has_document"]
    allow_unlink_domain = [("state", "=", "draft")]

    name = fields.Char(
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        track_visibility="onchange",
    )
    program_id = fields.Many2one(
        "openg2p.program",
        required=True,
        readonly=True,
        index=True,
        states={"draft": [("readonly", False)]},
        track_visibility="onchange",
    )
    state = fields.Selection(
        [
            ("draft", "Drafting"),
            ("confirm", "Confirmed"),
            ("pending", "Pending"),
            ("paymentstatus", "Completed"),
        ],
        string="Status",
        readonly=True,
        default="draft",
    )
    date_start = fields.Date(
        string="Date From",
        required=True,
        default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
        track_visibility="onchange",
    )
    date_end = fields.Date(
        string="Date To",
        required=True,
        default=lambda self: fields.Date.to_string(
            (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()
        ),
        track_visibility="onchange",
    )

    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        readonly=True,
        ondelete="restrict",
        default=lambda self: self.env.user.company_id,
    )
    transaction_batch_id = fields.Char(readonly=True, string="Batch ID")

    request_id = fields.Char(string="Request ID", compute="_generate_uuid", store=True)

    transaction_status = fields.Char(
        readonly=True,
    )

    total = fields.Char(string="Total", readonly=True)

    successful = fields.Char(string="Successful", readonly=True)

    failed = fields.Char(string="Failed", readonly=True)

    def action_confirm(self):
        for rec in self:
            rec.state = "confirm"

    def action_pending(self):
        for rec in self:
            rec.state = "pending"

    def action_transaction(self):
        for rec in self:
            rec.state = "paymentstatus"

    def _generate_uuid(self):
        for rec in self:
            if not rec.request_id:
                rec.request_id = uuid.uuid4().hex

    def create_bulk_transfer(self):
        self._generate_uuid()

        limit = 100
        beneficiary_transactions = self.env["openg2p.disbursement.main"].search(
            [("batch_id", "=", self.id)], limit=limit
        )

        offset = 0

        # CSV filename as RequestID+Datetime
        csvname = (
            self.request_id
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
                [("batch_id", "=", self.id)], limit=limit, offset=offset
            )

        # Uploading to AWS bucket
        uploaded = self.upload_to_aws(csvname, "paymenthub-ee-dev")

        headers = {
            'Platform-TenantId': 'ibank-usa',
        }
        files = {
            "data": (csvname, open(csvname, "rb")),
            "request_id": (None, str(self.request_id)),
            "note": (None, "Bulk transfers"),
            # "checksum": (None, str(self.generate_hash(csvname))),
        }

        url="http://channel.ibank.financial/channel/bulk/transfer"

        try:
            response = requests.post(url, headers=headers, files=files)
            response_data = response.json()
            
            self.transaction_status = response_data["status"]
            self.transaction_batch_id = response_data["batch_id"]

        except BaseException as e:
            return e

    def bulk_transfer_status(self):
        params = (
            ("batch_id", str(self.transaction_batch_id)),
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Accept': 'application/json, text/plain, /',
            'Accept-Language': 'en-US,en;q=0.5',
            'Platform-TenantId': 'ibank-usa',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiaWRlbnRpdHktcHJvdmlkZXIiLCJpYmFuay11c2EiXSwidXNlcl9uYW1lIjoibWlmb3MiLCJzY29wZSI6WyJpZGVudGl0eSJdLCJleHAiOjE2MjgwOTU4NjMsImF1dGhvcml0aWVzIjpbIlJFRlVORCIsIkFMTF9GVU5DVElPTlMiXSwianRpIjoidWxDNlFVQURzWWFuUzlFNGlVNWV2QkdyK0hBPSIsImNsaWVudF9pZCI6ImNsaWVudCJ9.yResYuOVEL1CVryXH1bH0MEZvLLhaJ3dlr7SfTX6C18ZY2_hn-1tL06ZPXLyOY0Ur5S3pYaSRljihoIRzvMzrBm40IawkdhcdPTSG5z05EVL5Icn1szcvOzx6lzsX5SmFLboa28eorwtHWE0a0EfUuGWl_7XwRjlfceRv91JEyxT8EEqjPA0V5ow-UBdU9lA3XIZBJgWNq9aUCVPg91kfKIhsWinnG7SxJzq3Pr2M8TyESYlL6d_dcc94UXmOiMregYFBI6hbjWilYo4MIK-uowgV6Mfl2HIteWGyRO938fGTqHazbB59V_FybaoO3QB-PYQRMrNSYVFVmimC-iRhw',
            'Connection': 'keep-alive'
        }


        url="http://ops-bk.ibank.financial/api/v1/batch"

        try:
            response = requests.get(url, params=params,headers=headers)
            response_data = response.json()
            
            self.transaction_status = response_data["status"]
            self.total = response_data["total"]
            self.successful = response_data["successful"]
            self.failed = response_data["failed"]

        except BaseException as e:
            return e

    def upload_to_aws(self, local_file, bucket):

        try:
            hc = pd.read_csv(local_file)

            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.environ.get(
                    "access_key"
                ),
                aws_secret_access_key=os.environ.get(
                    "secret_access_key"
                ),
            )
            csv_buf = StringIO()

            hc.to_csv(csv_buf, header=True, index=False)
            csv_buf.seek(0)

            s3.put_object(Bucket=bucket, Body=csv_buf.getvalue(), Key=local_file)

        except FileNotFoundError:
            return False

    def all_transactions_status(self):
        try:
            response = requests.get("https://15.207.23.72:5000/channel/transfer")
            return response
        except BaseException as e:
            return e

    def generate_hash(self, csvname):
        sha256 = hashlib.sha256()
        block_size = 256 * 128

        try:
            with open(csvname, "rb") as f:
                for chunk in iter(lambda: f.read(block_size), b""):
                    sha256.update(chunk)

            res = sha256.hexdigest()
            return res
        except BaseException as e:
            return e
