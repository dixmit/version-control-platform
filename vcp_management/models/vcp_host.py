# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpHost(models.Model):
    _name = "vcp.host"
    _description = "Vcp Platform Type"  # TODO

    name = fields.Char(required=True)
    kind = fields.Selection([], required=True)
    active = fields.Boolean(default=True)

    @tools.ormcache("self.id", "username")
    def _get_user(self, username):
        user = (
            self.env["vcp.user"]
            .with_context(active_test=False)
            .search([("external_id", "=ilike", username)], limit=1)
        )
        if not user:
            user = self.env["vcp.user"].create(
                {
                    "name": username,
                    "external_id": username,
                    "host_id": self.id,
                }
            )
        return user.id

    @tools.ormcache("self.id", "organization")
    def _get_organization(self, organization):
        org = (
            self.env["vcp.organization"]
            .with_context(active_test=False)
            .search([("external_id", "=ilike", organization)], limit=1)
        )
        if not org:
            org = self.env["vcp.organization"].create(
                {
                    "name": organization,
                    "external_id": organization,
                    "host_id": self.id,
                }
            )
        return org.id
