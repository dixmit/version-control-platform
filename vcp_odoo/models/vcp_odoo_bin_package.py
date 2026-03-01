# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpOdooBinPackage(models.Model):
    _name = "vcp.odoo.bin.package"
    _description = "Binary Package required by an Odoo Module"

    name = fields.Char(required=True, readonly=True)

    @tools.ormcache("name")
    def _get_bin(self, name):
        bin_src = self.search([("name", "=", name)], limit=1)
        if not bin_src:
            bin_src = self.create({"name": name})
        return bin_src.id
