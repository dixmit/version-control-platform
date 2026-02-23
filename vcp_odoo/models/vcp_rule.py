# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import ast
import copy
import logging

from odoo import fields, models
from odoo.fields import Command
from odoo.modules.module import _DEFAULT_MANIFEST

_logger = logging.getLogger(__name__)


class VcpRule(models.Model):
    _inherit = "vcp.rule"

    rule_type = fields.Selection(
        selection_add=[("odoo_module", "Odoo Module Analysis")],
        ondelete={"odoo_module": "cascade"},
    )

    def _process_rule_odoo_module(self, repository_branch):
        """
        Process the rule as a cloc analysis.
        """
        repository_branch._download_code()

        manifests = self._cloc_get_matches(repository_branch.local_path)
        for manifest in manifests:
            path = repository_branch.local_path + "/" + manifest
            _path, module_name, _manifest_name = path.rsplit("/", 2)
            module_id = self.env["vcp.odoo.module"]._get_odoo_module(module_name)

            vals = self._process_rule_odoo_module_prepare_vals(
                repository_branch, module_id, path
            )
            module_version = self.env["vcp.odoo.module.version"].search(
                [
                    ("module_id", "=", module_id),
                    ("repository_branch_id", "=", repository_branch.id),
                ],
                limit=1,
            )
            if not module_version:
                self.env["vcp.odoo.module.version"].create(vals)
            else:
                module_version.write(vals)

    def _load_odoo_module_manifest(self, path):
        manifest = copy.deepcopy(_DEFAULT_MANIFEST)
        with open(path) as f:
            manifest.update(ast.literal_eval(f.read()))
        return manifest

    def _process_rule_odoo_module_prepare_vals(
        self, repository_branch, module_id, manifest_path
    ):
        manifest = self._load_odoo_module_manifest(manifest_path)
        depends = []
        for dependancy in manifest.get("depends", []):
            depends.append(self.env["vcp.odoo.module"]._get_odoo_module(dependancy))
        return {
            "module_id": module_id,
            "version": manifest.get(
                "version", repository_branch.branch_id.name + ".0.0-dev"
            ),
            "repository_branch_id": repository_branch.id,
            "depends_on_module_ids": [Command.set(depends)],
        }
