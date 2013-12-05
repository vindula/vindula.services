# -*- coding: utf-8 -*-
from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator
from zope.app.component.hooks import getSite

from AccessControl.SecurityManagement import newSecurityManager, getSecurityManager, setSecurityManager
from Products.CMFCore.utils import getToolByName

class UpdateStructureOfService:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        context = kwargs.get('instance', None)
        if context:
            old_structure = context.getStructures()
            if old_structure:
                uid_old_structure = old_structure.UID()
                if value != uid_old_structure:
                    roles = context.get_local_roles()
                    for role in roles:
                        if uid_old_structure in role[0]:
                            context.manage_delLocalRoles(role)