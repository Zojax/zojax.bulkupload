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
"""Interfaces related to bulk uploading

$Id$
"""
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface


_ = MessageFactory('zojax.bulkupload')


class IBulkUploadAware(Interface):
    """Marker interface for objects that support bulk upload"""


class IBulkUpload(IBulkUploadAware):
    """Bulk uploading interface"""
    
    def add(data, name=None, content_type=None):
        """Add a single file from bulk
        
        `data` is a file-like object
        `name` is uploaded/desired file name (the final name can differ)
        `content_type` is its mime content type
        
        Returns created and added object.
        
        """
