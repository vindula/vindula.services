# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from vindula.services.content import IServicosFolder
from vindula.services.testing import INTEGRATION_TESTING

ctype = 'ServicosFolder'


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

    def test_factory(self):
        self.failUnless('ServicoFolder' in self.portal.portal_factory.getFactoryTypes().keys(),
                    '%s content type not installed' % 'ServicoFolder')

    def test_create(self):
        self.failUnless('foo' in self.folder.objectIds())

    def test_interface(self):
        self.failUnless(IServicosFolder.providedBy(self.obj))

    def test_allowed_content_types(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        types = ['Servico',]
        allowed_types = [t.getId() for t in self.obj.allowedContentTypes()]
        for t in types:
            self.assertTrue(t in allowed_types)
        # trying to add any other content type raises an error
        self.assertRaises(ValueError,
                          self.obj.invokeFactory, 'Document', 'foo')

        try:
            self.obj.invokeFactory('Servico', 'foo')
        except Unauthorized:
            self.fail()


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
