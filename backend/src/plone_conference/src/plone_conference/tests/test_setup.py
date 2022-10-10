"""Setup tests for this package."""
from kitconcept import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone_conference.testing import PLONE_CONFERENCE_INTEGRATION_TESTING  # noqa: E501
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that plone_conference is properly installed."""

    layer = PLONE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if plone_conference is installed."""
        self.assertTrue(self.installer.is_product_installed("plone_conference"))

    def test_browserlayer(self):
        """Test that IPLONE_CONFERENCELayer is registered."""
        from plone.browserlayer import utils
        from plone_conference.interfaces import IPLONE_CONFERENCELayer

        self.assertIn(IPLONE_CONFERENCELayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("plone_conference:default")[0],
            "20221010001",
        )


class TestUninstall(unittest.TestCase):

    layer = PLONE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("plone_conference")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if plone_conference is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("plone_conference"))

    def test_browserlayer_removed(self):
        """Test that IPLONE_CONFERENCELayer is removed."""
        from plone.browserlayer import utils
        from plone_conference.interfaces import IPLONE_CONFERENCELayer

        self.assertNotIn(IPLONE_CONFERENCELayer, utils.registered_layers())
