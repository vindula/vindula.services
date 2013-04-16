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

ServicoSchema = VindulaNews_schema.copy() + atapi.Schema((

    atapi.LinesField('links',
        widget=atapi.LinesWidget(
            label=_(u'Links'),
            description=_(u'Informe o(s) link(s) para o serviço. Um por linha.')
        ),
        required=False,
    ),

    atapi.BooleanField('imersao',
        widget=atapi.BooleanWidget(
            label=_(u'Imersão'),
            description=_(u'Se selecionado, o serviço será exibido em um iframe.')
        ),
        required=False,
    ),

    atapi.BooleanField(
        name='activ_portletRight',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Portlet Direita'),
            description=_(u'Se selecionado, ativa a visualização dos portet na coluna da direita.'),
        ),
        required=False,
    ),

    atapi.BooleanField(
        name='activ_portletLeft',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Portlet Esquerda'),
            description=_(u'Se selecionado, ativa a visualização dos portet na coluna da esquerda.'),
        ),
        required=False,
    ),
    ))

schemata.finalizeATCTSchema(ServicoSchema)


class Servico(VindulaNews):
    """ Servico """

    implements(IServico)

    meta_type = "Servico"
    schema = ServicoSchema

    _at_rename_after_creation = True

atapi.registerType(Servico, PROJECTNAME)
