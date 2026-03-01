# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from random import randint

from odoo import fields, models, tools


class VcpRequestLabel(models.Model):
    _name = "vcp.request.label"
    _description = "Vcp Request Label"

    name = fields.Char(required=True, readonly=True)

    color = fields.Char(default=lambda x: x._default_color())

    _sql_constraints = [("name_uniq", "unique(name)", "Label name must be unique.")]

    def _default_color(self):
        return randint(1, 11)

    @tools.ormcache("name")
    def _get_label(self, name):
        label = self.search([("name", "=", name)], limit=1)
        if not label:
            label = self.sudo().create({"name": name})
        return label.id
