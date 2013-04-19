# -*- coding: utf-8 -*-

from ComputedAttribute import ComputedAttribute
from Acquisition import aq_base

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from plone.app.folder.folder import ATFolder, ATFolderSchema

from vindula.services import MessageFactory as _
from vindula.services.config import PROJECTNAME
from vindula.services.interfaces import IServicosFolder

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

ServicosFolderSchema = ATFolderSchema.copy() + atapi.Schema((


    atapi.ReferenceField('destaques',
        multiValued=1,
        allowed_types=('Servico'),
        label=_(u"Destaques"),
        relationship='destaques',
        widget=VindulaReferenceSelectionWidget(
            label=_(u"Destaques"),
            description='Selecione os Serviços em destaque.'
        ),
    ),

))


ServicosFolderSchema['title'].storage = atapi.AnnotationStorage()
ServicosFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ServicosFolderSchema)


class ServicosFolder(ATFolder):
    """ ServicosFolder """

    implements(IServicosFolder)

    meta_type = "ServicosFolder"
    schema = ServicosFolderSchema

    _at_rename_after_creation = True

atapi.registerType(ServicosFolder, PROJECTNAME)
