# Copyright 2026 GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class VcpHost(models.Model):
    _inherit = "vcp.host"

    kind = fields.Selection(
        selection_add=[("dummy", "Dummy Value")],
        ondelete={"dummy": "cascade"},
    )
