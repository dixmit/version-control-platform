# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpUser(models.Model):
    _name = "vcp.user"
    _description = "User"

    name = fields.Char(required=True, readonly=True)
    external_id = fields.Char(required=True, readonly=True, index=True)
    platform_type_id = fields.Many2one(
        comodel_name="vcp.platform.type",
        required=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
    )

    _sql_constraints = [
        (
            "external_id_uniq",
            "unique(external_id, platform_type_id)",
            "External ID must be unique.",
        )
    ]

    def _get_contributor_url(self):
        return False

    def _get_contributors_name(self, kind, **kwargs):
        return self.partner_id.name or self.name
