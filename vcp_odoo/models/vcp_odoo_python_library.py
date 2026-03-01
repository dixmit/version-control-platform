# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpOdooPythonLibrary(models.Model):
    _name = "vcp.odoo.python.library"
    _description = "Python Library required by an Odoo Module"

    name = fields.Char(required=True, readonly=True)

    module_version_ids = fields.Many2many(
        "vcp.odoo.module.version",
        string="Odoo Module Versions",
        readonly=True,
    )

    @tools.ormcache("name")
    def _get_python_library(self, name):
        lib = self.search([("name", "=", name)], limit=1)
        if not lib:
            lib = self.create({"name": name})
        return lib.id
