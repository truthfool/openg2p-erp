from odoo import api, fields, models

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os


class DetailedPaymentStatus(models.Model):
    _name = "openg2p.detailed.payment.status"
    _description = "Displaying detailed payment status for each batch"

    batch_id = fields.Many2one(
        "openg2p.disbursement.batch.transaction",
        string="Batch ID"
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
