# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class VcpOdooModule(models.Model):
    _name = "vcp.odoo.module"
    _description = "Odoo Module"

    name = fields.Char(required=True)
    version_ids = fields.One2many("vcp.odoo.module.version", inverse_name="module_id")
    version_count = fields.Integer(
        compute="_compute_version_count",
        help="number of versions in which the module is available",
        store=True,
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "The module name must be unique"),
    ]

    @api.depends("version_ids")
    def _compute_version_count(self):
        for record in self:
            record.version_count = len(record.version_ids)

    @tools.ormcache("name")
    def _get_odoo_module(self, name):
        """
        Get the Odoo module with the given name, creating it if it doesn't exist.
        """
        module = self.search(
            [("name", "=", name)],
            limit=1,
        )
        if not module:
            module = self.env["vcp.odoo.module"].create({"name": name})
        return module.id
