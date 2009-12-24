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
"""Container adapter for IBulkUpload

$Id$
"""
import os

from zope.app.container.interfaces import IContainer, INameChooser
from zope.component import adapts, queryAdapter
from zope.filerepresentation.interfaces import IFileFactory
from zope.interface import implements

from zojax.bulkupload.interfaces import IBulkUpload


class ContainerBulkUpload(object):
    implements(IBulkUpload)
    adapts(IContainer)
    
    def __init__(self, context):
        self.context = context

    def add(self, data, name=None, content_type=None):
        # this is just like zope FTP system does
        ext = os.path.splitext(name)[1]
        factory = queryAdapter(self.context, IFileFactory, ext)
        if factory is None:
            factory = IFileFactory(self.context)

        obj = factory(name, content_type, data)
        name = INameChooser(self.context).chooseName(name, obj)
        self.context[name] = obj
