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
"""Bulk file upload view

$Id$
"""
from zope.app.component.hooks import getSite
from zope.i18n import translate
from zope.security.interfaces import Unauthorized
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zojax.resourcepackage.library import includeInplaceSource

from zojax.bulkupload.interfaces import _, IBulkUpload 
from zojax.bulkupload.ticket import issueTicket, validateTicket


INIT_TEMPLATE = '''<script type="text/javascript">
    $(document).ready(function() {
        $('#bulk-upload').uploadify({
            uploader: '%(uploader_url)s',
            script: '%(script_url)s',
            buttonText: '%(button_text)s',
            cancelImg: '%(cancel_image_url)s',
            scriptData: {ticket: %(ticket)s},
            multi: true
        });

        $('#bulk-upload-button').click(function() {
            $('#bulk-upload').uploadifyUpload();
        });
    });
</script>'''


class BulkUploadPage(object):

    buttonText = _(u'Select files')
    
    def update(self):
        base_resource_url = '%s/@@/jquery-uploadify/' % absoluteURL(getSite(), self.request)
        url = self.request.getURL()
        params = {
            'uploader_url': base_resource_url + 'uploadify.swf',
            'script_url': '%s/bulk-upload-process' % absoluteURL(self.context, self.request),
            'ticket': issueTicket(url),
            'button_text': translate(self.buttonText, context=self.request),
            'cancel_image_url': base_resource_url + 'cancel.png',
        }
        includeInplaceSource(INIT_TEMPLATE % params, ('jquery-uploadify',))


class BulkUpload(object):
    
    def __call__(self):
        request = self.request
        
        url = absoluteURL(self.context, self.request) + '/bulk-upload.html'
        ticket = request.form.get('ticket', None)
        if ticket is None or not validateTicket(url, ticket):
            raise Unauthorized

        upload = self.request.form['Filedata']
        content_type = self.request.form.get('Content-Type', None)

        # removing security proxy, because we worked around zope security
        # with tickets before and current interaction is unauthorized
        adder = IBulkUpload(removeSecurityProxy(self.context))
        adder.add(upload, upload.filename, content_type)

        # TODO: think about how to invalidate ticket after the full queue
        # has been uploaded.
        return '1'
        