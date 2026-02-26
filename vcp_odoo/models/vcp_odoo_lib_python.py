# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpOdooLibPython(models.Model):
    _name = "vcp.odoo.lib.python"
    _description = "Python Library required by an Odoo Module"

    name = fields.Char(required=True)

    @tools.ormcache("name")
    def _get_lib_python(self, name):
        lib = self.search([("name", "=", name)], limit=1)
        if not lib:
            lib = self.create({"name": name})
        return lib.id
