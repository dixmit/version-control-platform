# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo_test_helper import FakeModelLoader

from odoo.fields import Date
from odoo.tests import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo, HttpCaseWithUserPortal


@tagged("post_install", "-at_install")
class TestUi(HttpCaseWithUserDemo, HttpCaseWithUserPortal):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fake order model
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models.vcp_host import VcpHost

        cls.loader.update_registry((VcpHost,))
        cls.kind = cls.env["vcp.host"].create(
            {
                "name": "Dummy Platform",
                "kind": "dummy",
            }
        )
        # be sure some expected values are set otherwise homepage may fail
        date = Date.today()
        date = date - timedelta(days=date.day + 1)
        cls.partner_portal.write(
            {
                "city": "Bayonne",
                "company_name": "YourCompany",
                "country_id": cls.env.ref("base.us").id,
                "phone": "(683)-556-5104",
                "street": "858 Lynn Street",
                "zip": "07002",
            }
        )
        platform = cls.env["vcp.platform"].create(
            {
                "name": "oca",
                "short_description": "OCA",
                "description": "OCA",
                "host_id": cls.kind.id,
            }
        )
        repository = cls.env["vcp.repository"].create(
            {
                "name": "contributors-module",
                "description": "OCA/contributors-module",
                "platform_id": platform.id,
                "from_date": date,
            }
        )
        user_01 = cls.env["vcp.user"].create(
            {
                "name": "Enric Tobella",
                "external_id": "etobella",
                "host_id": cls.kind.id,
            }
        )
        user_02 = cls.env["vcp.user"].create(
            {
                "name": "Luis Rodriguez",
                "external_id": "lrodriguez",
                "host_id": cls.kind.id,
            }
        )
        user_03 = cls.env["vcp.user"].create(
            {
                "name": "Jordi Ballester",
                "external_id": "jballester",
                "host_id": cls.kind.id,
            }
        )
        org_01 = cls.env["vcp.organization"].create(
            {
                "name": "Dixmit",
                "external_id": "dixmit",
                "host_id": cls.kind.id,
            }
        )
        org_02 = cls.env["vcp.organization"].create(
            {
                "name": "ForgeFlow",
                "external_id": "forgeflow",
                "host_id": cls.kind.id,
            }
        )
        pull_request_01 = cls.env["vcp.request"].create(
            {
                "external_id": 1,
                "name": "Test PR",
                "repository_id": repository.id,
                "user_id": user_01.id,
                "organization_id": org_01.id,
                "created_at": date,
                "closed_at": date,
                "is_merged": True,
            }
        )
        cls.env["vcp.request"].create(
            {
                "external_id": 2,
                "name": "Test PR",
                "repository_id": repository.id,
                "user_id": user_02.id,
                "organization_id": org_01.id,
                "created_at": date,
                "is_merged": False,
            }
        )
        cls.env["vcp.request"].create(
            {
                "external_id": 3,
                "name": "Test PR",
                "repository_id": repository.id,
                "user_id": user_03.id,
                "organization_id": org_02.id,
                "created_at": date,
                "is_merged": False,
            }
        )
        cls.env["vcp.review"].create(
            {
                "external_id": 1,
                "body": "Test Review",
                "state": "APPROVED",
                "request_id": pull_request_01.id,
                "user_id": user_01.id,
                "submitted_at": date,
            }
        )
        cls.env["vcp.comment"].create(
            {
                "external_id": 1,
                "body": "Test Comment",
                "request_id": pull_request_01.id,
                "user_id": user_01.id,
                "created_at": date,
            }
        )

    def test_01_portal_load_tour(self):
        self.start_tour("/", "portal_load_vcp", login="portal")
