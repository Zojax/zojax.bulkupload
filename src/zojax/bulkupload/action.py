##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Action for bulk file uploads

$Id$
"""
from zope.component import adapts
from zope.interface import implements, Interface
from zope.traversing.browser import absoluteURL
from zojax.content.actions.action import Action
from zojax.content.actions.interfaces import IAddContentCategory, IAction

from zojax.bulkupload.interfaces import _, IBulkUploadAware


class IBulkUploadAction(IAction, IAddContentCategory):
    pass


class BulkUploadAction(Action):
    adapts(IBulkUploadAware, Interface)
    implements(IBulkUploadAction)
    
    title = _(u'Upload multiple files')
    permission = 'zojax.ModifyContent'
    
    @property
    def url(self):
        return '%s/bulk-upload.html' % absoluteURL(self.context, self.request)
