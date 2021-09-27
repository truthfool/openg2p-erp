from odoo import api, fields, models

import os


class DetailedPaymentStatus(models.Model):
    _name = "openg2p.detailed.payment.status"
    _description = "Displaying detailed payment status for each batch"

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
    beneficiary_id = fields.Integer(
        string="Beneficiary ID"
    )
    workflowInstanceKey = fields.Integer(
        string="Workflow Instance Key"
    )
    transactionId = fields.Char(
        string="Transaction ID"
    )
    startedAt = fields.Char(
        string="Started At"
    )
    completedAt = fields.Char(
        string="Completed At"
    )
    status = fields.Char(
        string="Status"
    )
    statusDetail = fields.Char(
        string="Status Detail"
    )
    payeeDfspId = fields.Char(
        string="Payee dfsp ID"
    )
    payeePartyId = fields.Char(
        string="Payee Party ID"
    )
    payeePartyIdType = fields.Char(
        string="Payee Party Id Type"
    )
    payeeFee = fields.Char(
        string="Payee Fee"
    )
    payeeFeeCurrency = fields.Char(
        string="Payee Fee Currency"
    )
    payeeQuoteCode = fields.Char(
        string="Payee Quote Code"
    )
    payerDfspId = fields.Char(
        string="Payer Dfsp ID"
    )
    payerPartyId = fields.Char(
        string="Payer Party Id"
    )
    payerPartyIdType = fields.Char(
        string="Payer Party Id Type"
    )
    payerFee = fields.Char(
        string="Payer Fee"
    )
    payerFeeCurrency = fields.Char(
        string="Payer Fee Currency"
    )
    payerQuoteCode = fields.Char(
        string="Payer Quote Code"
    )
    amount = fields.Char(
        string="Amount"
    )
    currency = fields.Char(
        string="Currency"
    )
    direction = fields.Char(
        string="Direction"
    )
    errorInformation = fields.Char(
        string="Error Information"
    )
    batchId = fields.Char(
        string="Batch ID"
    )
