# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from vindula.services.content import ServicosFolder as klass
from vindula.services.interfaces import IServicosFolder as interface
from vindula.services.testing import INTEGRATION_TESTING

ctype = klass.meta_type


class ContentTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_adding(self):
        self.failUnless('obj' in self.folder.objectIds())
        self.failUnless(interface.providedBy(self.obj))

    def test_interface(self):
        self.assertTrue(interface.implementedBy(klass))
        self.assertTrue(verifyClass(interface, klass))
        self.assertTrue(verifyObject(interface, self.obj))

    def test_type(self):
        types_tool = self.portal.portal_types
        self.failUnless(ctype in types_tool.objectIds())

    def test_factory(self):
        factory_tool = self.portal.portal_factory
        self.failUnless(ctype in factory_tool.getFactoryTypes().keys())

    def test_allowed_content_types(self):
        types = ['Servico']
        self.failUnlessEqual(self.obj.getLocallyAllowedTypes(), types)
        self.failUnlessEqual(self.obj.getImmediatelyAddableTypes(), types)
        self.assertRaises(ValueError,
                          self.obj.invokeFactory, 'Document', 'foo')
        try:
            self.obj.invokeFactory('Servico', 'foo')
        except Unauthorized:
            self.fail()


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
