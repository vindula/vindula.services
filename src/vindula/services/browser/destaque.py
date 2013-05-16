# -*- coding: utf-8 -*-

from five import grok

from Acquisition import aq_inner
from zope.component import getMultiAdapter

from vindula.services.interfaces import IServicosFolder

grok.templatedir('templates')


class DestaquesView(grok.View):
    grok.context(IServicosFolder)
    grok.require('zope2.View')
    grok.name('macro_destaque')

    def update(self):
        super(DestaquesView,self).update()
        context = aq_inner(self.context)
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request), name=u'plone_tools')


    def getDestaques(self):
        context = self.context
        itens = context.getDestaques()
        return itens
