# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpOdooModuleVersion(models.Model):
    _name = "vcp.odoo.module.version"
    _description = "Odoo Module Version"  # TODO

    module_id = fields.Many2one(
        "vcp.odoo.module",
        required=True,
        ondelete="cascade",
    )
    version = fields.Char(required=True)
    repository_branch_id = fields.Many2one(
        "vcp.repository.branch",
    )
    depends_on_module_ids = fields.Many2many(
        "vcp.odoo.module",
    )
