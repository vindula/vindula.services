# -*- coding: utf-8 -*-
from five import grok

from ComputedAttribute import ComputedAttribute
from Acquisition import aq_base

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IObjectEditedEvent, IObjectInitializedEvent

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from vindula.content.content.vindulanews import VindulaNews, VindulaNews_schema

from vindula.services import MessageFactory as _
from vindula.services.config import PROJECTNAME
from vindula.services.interfaces import IServico

from vindula.controlpanel.browser.at.widget import VindulaReferenceSelectionWidget

ServicoSchema = VindulaNews_schema.copy() + atapi.Schema((

    atapi.ReferenceField('structures',
        multiValued=0,
        allowed_types=('OrganizationalStructure',),
        relationship='structures',
        widget=VindulaReferenceSelectionWidget(
            #default_search_index='SearchableText',
            typeview='list',
            label=_(u"Unidade Organizacional"),
            description=_(u"Selecione uma Unidade Organizacional."),
            ),
        required=True,
        validators = ('isNewStructure',),
    ),

    atapi.TextField('link',
        widget=atapi.TextAreaWidget(
            label=_(u'Link'),
            description=_(u'Informe o link para o serviço (campo antigo, está aqui somente até migração para o novo formato).')
        ),
        required=False,
    ),
    
    DataGridField('linkDataGrid',
        columns=('title','link',),
        allow_delete = True,
        allow_insert = True,
        allow_reorder = True,
        widget = DataGridWidget(label="Links",
            description="Relecione o título do links com o seu valor.",
            columns= {
                "title" : Column(_(u"Título")),
                "link" : Column(_(u"Link")),
        }),
    ),

    atapi.BooleanField('parametri',
        widget=atapi.BooleanWidget(
            label=_(u'Parametros'),
            description=_(u'Se selecionado, será passado no link do serviço os parametros de username e token.')
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
                                                          
    atapi.IntegerField(
        name='height_iframe',
        widget=atapi.IntegerWidget(
            label=_(u"Altura do iframe"),
            description=_(u"Tamanho em pixels do iframe.<br />Só será utilizado caso a opção Imersão estiver ativa."),
        ),
        default=600,
        required=True,
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

    atapi.BooleanField(
        name='activ_portletAccessory',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Portlet Acessório'),
            description=_(u'Se selecionado, ativa a visualização dos portet na coluna  acessória.'),
        ),
        required=False,
    ),
                                                          
    atapi.BooleanField(
        name='hide_service',
        default=False,
        widget=atapi.BooleanWidget(
            label=_(u'Ocultar serviço'),
            description=_(u'Oculta o serviço da listagem do bloco de serviços.'),
        ),
        required=False,
        schemata='settings'
    ),
                                                          
    atapi.BooleanField(
        name='hide_rating',
        default=False,
        widget=atapi.BooleanWidget(
            label=_(u'Ocultar avaliação'),
            description=_(u'Oculta a opção de avaliar o serviço.'),
        ),
        required=False,
        schemata='settings'
    ),
                                                          
    atapi.BooleanField(
        name='hide_social_bar',
        default=False,
        widget=atapi.BooleanWidget(
            label=_(u'Ocultar barra social'),
            description=_(u'Oculta a barra social.'),
        ),
        required=False,
        schemata='settings'
    ),
                                                          
    atapi.BooleanField(
        name='show_properties',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Mostrar propriedades'),
            description=_(u'Mostra a opção de propriedades do serviço.'),
        ),
        required=False,
        schemata='settings'
    ),
    
    atapi.BooleanField(
        name='show_changes',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Mostrar modificações'),
            description=_(u'Mostra a opção de modificações do serviço.'),
        ),
        required=False,
        schemata='settings'
    ),
    
    atapi.BooleanField(
        name='show_last_access',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Mostrar últimos acessos'),
            description=_(u'Mostra a opção de últimos acessos do serviço.'),
        ),
        required=False,
        schemata='settings'
    ),
    
    atapi.BooleanField(
        name='show_see_also',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Mostrar veja também'),
            description=_(u'Mostra a opção de veja também do serviço.'),
        ),
        required=False,
        schemata='settings'
    ),
    
    atapi.BooleanField(
        name='show_tags',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u'Mostrar tags'),
            description=_(u'Mostra as tags do serviço.'),
        ),
        required=False,
        schemata='settings'
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

@grok.subscribe(IServico, IObjectEditedEvent)
def object_edited(context, event):
    structure = context.getStructures()
    if structure:
        acl_users = getToolByName(context, 'acl_users')
        group_list = acl_users.source_groups.getGroups()
        structure_title = structure.Title()
        
        for group in group_list:
            if group is None:
                continue
            group_title = group.title or group.getProperty('title')
            if not group_title:
                continue
            if structure_title.lower() in group_title.lower():
                context.manage_addLocalRoles(group.getName(), ['Reader',])
    context.reindexObject()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
