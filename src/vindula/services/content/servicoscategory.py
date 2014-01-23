# -*- coding: utf-8 -*-

from ComputedAttribute import ComputedAttribute
from Acquisition import aq_base

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from plone.app.folder.folder import ATFolder, ATFolderSchema

from vindula.services import MessageFactory as _
from vindula.services.config import PROJECTNAME
from vindula.services.interfaces import IServicosCategory

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

ServicosCategorySchema = ATFolderSchema.copy() + atapi.Schema((


    atapi.ReferenceField('imageCategory',
        multiValued=0,
        allowed_types=('Image'),
        label=_(u"Icone da categoria"),
        relationship='Imagem',
        widget=VindulaReferenceSelectionWidget(
            label=_(u"Imagem"),
            description='Imagem que vai aparecer ao lado da listagem de categorias.')
    ),

    atapi.BooleanField('is_open_aba',
        widget=atapi.BooleanWidget(
            label=_(u'Fechado/Aberto'),
            description=_(u'Marque essa flag para que a categoria do Serviço venha aberta.')
        ),
        required=False,
    ),


))


#ServicosCategorySchema['title'].storage = atapi.AnnotationStorage()
#ServicosCategorySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ServicosCategorySchema)


class ServicosCategory(ATFolder):
    """ ServicosCategory """

    implements(IServicosCategory)

    meta_type = "ServicosCategory"
    schema = ServicosCategorySchema

    _at_rename_after_creation = True
    
    def getImageIcone(self):
        image = self.getImageCategory()

        if image:
            return image.absolute_url() +'/image_tile'
        else:
            return ''

atapi.registerType(ServicosCategory, PROJECTNAME)
