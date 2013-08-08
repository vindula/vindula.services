# -*- coding: utf-8 -*-

from five import grok

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from vindula.services.interfaces import IServico
from vindula.services.interfaces import IServicosFolder

grok.templatedir('templates')


class ServicoView(grok.View):
    grok.context(IServico)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        super(ServicoView,self).update()
        context = aq_inner(self.context)
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request), name=u'plone_tools')



class ServicosFolderView(grok.View):
    grok.context(IServicosFolder)
    grok.require('zope2.View')
    grok.name('view')