from odoo import models, fields


class Openg2pWorkflowStage(models.Model):
    _name = "openg2p.workflow"
    _description = "Workflows for OpenG2P Tasks"

    workflow_type = fields.Many2one("openg2p.workflow.type", string="Workflow type")

    curr_workflow_stage = fields.Many2one(
        "openg2p.workflow.stage", string="Current workflow stage"
    )

    workflow_completed = fields.Boolean(
        string="Workflow completed",
    )

    def name_get(self):
        for rec in self:
            yield f"{rec.workflow_type.name} ({rec.id})"
