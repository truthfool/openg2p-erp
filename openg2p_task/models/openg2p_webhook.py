from odoo import models, fields
from odoo.http import Controller, route, request


class CreateWebhook(models.Model):
    _name = "openg2p.webhook"
    _description = "Create Webhook for Events"

    webhook_url = fields.Text(
        blank=False
    )
    events = fields.Many2one(
        "openg2p.task.subtype",
        required=True,
        string="Events"
    )
