# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpOdooModuleVersion(models.Model):
    _name = "vcp.odoo.module.version"
    _description = "Odoo Module on an specific repository branch"
    _inherit = ["vcp.rule.information.mixin", "image.mixin"]

    name = fields.Char(required=True)
    path = fields.Char(required=True)
    module_id = fields.Many2one(
        "vcp.odoo.module",
        required=True,
        ondelete="cascade",
    )
    version = fields.Char(required=True)
    repository_branch_id = fields.Many2one(
        "vcp.repository.branch",
        required=True,
        ondelete="cascade",
    )
    depends_on_module_ids = fields.Many2many(
        "vcp.odoo.module",
    )
    auto_install = fields.Boolean()
    license = fields.Char(string="License (Manifest)", readonly=True)
    summary = fields.Char(string="Summary (Manifest)", readonly=True)
    website = fields.Char(string="Website (Manifest)", readonly=True)
    lib_python_ids = fields.Many2many(
        "vcp.odoo.lib.python",
        string="Python Libraries",
    )
    bin_package_ids = fields.Many2many(
        "vcp.odoo.bin.package",
        string="Python Binaries",
    )

    def _get_local_path(self):
        return f"{self.repository_branch_id.local_path}/{self.path}"
