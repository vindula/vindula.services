# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from ComputedAttribute import ComputedAttribute
from Acquisition import aq_base

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from plone.app.folder.folder import ATFolder, ATFolderSchema

from vindula.content.content.vindulanews import VindulaNews, VindulaNews_schema

from vindula.services import MessageFactory as _
from vindula.services.config import PROJECTNAME
from vindula.services.interfaces import IServico

ServicoSchema = VindulaNews_schema.copy() + atapi.schema((

    atapi.LinesField('links',
        widget=atapi.LinesWidget(
            label=_(u'Links'),
        ),
    ),
))

schemata.finalizeATCTSchema(ServicoSchema)


class Servico(VindulaNews):
    """ Servico """

    implements(IServico)

    meta_type = "Servico"
    schema = ServicoSchema

    _at_rename_after_creation = True

atapi.registerType(ServicosFolder, PROJECTNAME)
