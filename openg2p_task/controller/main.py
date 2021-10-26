from odoo import http
from odoo.http import request


class ErpEvents(http.Controller):

    @http.route('/events', website=True, auth='user')
    def erp_events_(self, **kw):
        all_events = request.env[''].sudo().search([])
        return request.render("om_hospital.patients_page", {
            'all_events': all_events
        })
