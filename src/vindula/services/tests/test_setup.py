# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from vindula.services.config import PROJECTNAME
from vindula.services.testing import INTEGRATION_TESTING


class TestInstall(unittest.TestCase):
    """ensure product is properly installed"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getattr(self.portal, 'portal_quickinstaller')

    def test_installed(self):
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)


class TestUninstall(unittest.TestCase):
    """ensure product is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))
