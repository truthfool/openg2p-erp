from odoo import models, fields, api


class Openg2pWorkflow(models.Model):
    _name = "openg2p.workflow"
    _description = "Workflows for OpenG2P Tasks"

    # name = fields.Char(string="Workflow Name")

    workflow_type = fields.Many2one("openg2p.workflow.type", string="Workflow type")

    curr_workflow_stage = fields.Many2one(
        "openg2p.workflow.stage", string="Current workflow stage"
    )

    workflow_completed = fields.Boolean(
        string="Workflow completed",
    )

    workflow_context = fields.Text(
        string="Context",
    )

    def _update_context(self, event_code, obj, status):
        pass

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        self.env["openg2p.task"].create(
            {
                "type_id": 4,
                "subtype_id": 15,
                "entity_type_id": "openg2p.disbursement.batch.transaction",
                "entity_id": 0,
                "status_id": 1,
                "workflow_id": res.id,
            }
        )
        return res

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.workflow_type.name} ({rec.id})"

    def handle_tasks(self, event_code, obj):

        if event_code == "regd_create":
            task = self.env["openg2p.task"].search(
                [
                    "&",
                    ("entity_type_id", "=", "openg2p.registration"),
                    ("entity_id", "=", 0),
                ]
            )
            if task:
                task.write(
                    {
                        "entity_id": obj.id,
                        "status_id": 3,
                        "target_url": f"http://localhost:8069/web#id={obj.id}&model=openg2p.registration",
                    }
                )
                self.env["openg2p.task"].create(
                    {
                        "type_id": 8,
                        "subtype_id": 37,
                        "entity_type_id": "openg2p.beneficiary",
                        "entity_id": 0,
                        "status_id": 1,
                        "workflow_id": task.workflow_id,
                    }
                )
                workflow = self.env["openg2p.workflow"].search(
                    [("id", "=", task.workflow_id)]
                )
                workflow.write(
                    {
                        "curr_workflow_stage": workflow.curr_workflow_stage.id + 1,
                    }
                )
        elif event_code == "ben_create":
            task = self.env["openg2p.task"].search(
                [
                    "&",
                    ("entity_type_id", "=", "openg2p.beneficiary"),
                    ("entity_id", "=", 0),
                ]
            )
            if task:
                task.write(
                    {
                        "entity_id": obj.id,
                        "status_id": 3,
                        "target_url": f"http://localhost:8069/web#id={obj.id}&model=openg2p.beneficiary",
                    }
                )
                self.env["openg2p.task"].create(
                    {
                        "type_id": 9,
                        "subtype_id": 40,
                        "entity_type_id": "openg2p.beneficiary",
                        "entity_id": 0,
                        "status_id": 1,
                        "workflow_id": task.workflow_id,
                    }
                )
        elif event_code == "batch_create":
            task = self.env["openg2p.task"].search(
                [
                    "&",
                    ("entity_type_id", "=", "openg2p.disbursement.batch.transaction"),
                    ("entity_id", "=", 0),
                ]
            )

            if task:
                task.write(
                    {
                        "entity_id": obj.id,
                        "status_id": 3,
                        "target_url": f"http://localhost:8069/web#id={obj.id}&model=openg2p.disbursement.batch.transaction",
                    }
                )
                self.env["openg2p.task"].create(
                    {
                        "type_id": 5,
                        "subtype_id": 18,
                        "entity_type_id": "openg2p.disbursement.batch.transaction",
                        "entity_id": 0,
                        "status_id": 1,
                        "workflow_id": task.workflow_id,
                    }
                )
        elif event_code == "batch_approve":
            task = self.env["openg2p.task"].search(
                [
                    "&",
                    ("entity_type_id", "=", "openg2p.disbursement.batch.transaction"),
                    ("entity_id", "=", 0),
                ]
            )

            if task:
                task.write(
                    {
                        "entity_id": obj.id,
                        "status_id": 3,
                        "target_url": f"http://localhost:8069/web#id={obj.id}&model=openg2p.disbursement.batch.transaction",
                    }
                )
                self.env["openg2p.task"].create(
                    {
                        "type_id": 5,
                        "subtype_id": 19,
                        "entity_type_id": "openg2p.disbursement.batch.transaction",
                        "entity_id": 0,
                        "status_id": 1,
                        "workflow_id": task.workflow_id,
                    }
                )
        elif event_code == "batch_send":
            task = self.env["openg2p.task"].search(
                [
                    "&",
                    ("entity_type_id", "=", "openg2p.disbursement.batch.transaction"),
                    ("entity_id", "=", 0),
                ]
            )

            if task:
                task.write(
                    {
                        "entity_id": obj.id,
                        "status_id": 3,
                        "target_url": f"http://localhost:8069/web#id={obj.id}&model=openg2p.disbursement.batch.transaction",
                    }
                )
                self.env["openg2p.task"].create(
                    {
                        "type_id": 5,
                        "subtype_id": 23,
                        "entity_type_id": "openg2p.disbursement.batch.transaction",
                        "entity_id": 0,
                        "status_id": 1,
                        "workflow_id": task.workflow_id,
                    }
                )
            elif event_code == "complete_report":
                task = self.env["openg2p.task"].search(
                    [
                        "&",
                        ("entity_type_id", "=", "openg2p.disbursement.batch.transaction"),
                        ("entity_id", "=", 0),
                    ]
                )

                if task:
                    task.write(
                        {
                            "entity_id": obj.id,
                            "status_id": 3,
                            "target_url": f"http://localhost:8069/web#id={obj.id}&model=openg2p.disbursement.batch.transaction",
                        }
                    )
                    self.env["openg2p.task"].create(
                        {
                            "type_id": 5,
                            "subtype_id": 24,
                            "entity_type_id": "openg2p.disbursement.batch.transaction",
                            "entity_id": 0,
                            "status_id": 1,
                            "workflow_id": task.workflow_id,
                        }
                    )

    def api_json(self):
        return {
            "workflow-type": self.workflow_type.id,
            "current-workflow-stage": self.curr_workflow_stage.id,
            "workflow-completed": self.workflow_completed,
        }
