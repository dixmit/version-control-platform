# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class VcpPlatformType(models.Model):
    _inherit = "vcp.platform.type"

    kind = fields.Selection(
        selection_add=[("github", "GitHub")],
        ondelete={"github": "cascade"},
    )

    @api.constrains("kind")
    def _check_kind_github(self):
        for record in self.filtered(lambda r: r.kind == "github"):
            platforms = self.env["vcp.platform"].search(
                [("platform_type_id", "!=", record.id), ("kind", "=", "github")],
                limit=1,
            )
            if platforms:
                raise ValidationError(_("Only one GitHub platform type is allowed."))
