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
"""

$Id$
"""
import unittest, os.path
from zope.interface import implements
from zojax.content.documents.container import DocumentsContainer
from zojax.content.documents.interfaces import IDocuments, IDocumentsFactory
from zojax.content.space.content import ContentSpace
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory
from zojax.layoutform.interfaces import ILayoutFormLayer
from zope import event, interface, component
from zope.app.rotterdam import Rotterdam
from zope.lifecycleevent import ObjectCreatedEvent
from zope.testing import doctest
import zope.app.testing.functional

import zope.app.testing.functional
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.testing.functional import getRootFolder
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.personal.space.manager import PersonalSpaceManager, IPersonalSpaceManager
from zojax.bulkupload.interfaces import IBulkUploadAware

ZCMLLayer = zope.app.testing.functional.ZCMLLayer
FunctionalTestSetup = zope.app.testing.functional.FunctionalTestSetup


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxBulkuploadLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxBulkuploadLayer', allow_teardown=True)


class TestSpace(ContentSpace):
    implements(IContentSpace, IBulkUploadAware)
    title = 'Test Space'


def setUp(test):
    root = getRootFolder()
    root['intids'] = IntIds()
    root['intids'].register(root)
    root.getSiteManager().registerUtility(root['intids'], IIntIds)

    catalog = Catalog()
    root['catalog'] = catalog
    root.getSiteManager().registerUtility(root['catalog'], ICatalog)

    manager = PersonalSpaceManager()
    root['people'] = manager
    root.getSiteManager().registerUtility(root['people'], IPersonalSpaceManager)

    space = TestSpace(title=u'Space')
    event.notify(ObjectCreatedEvent(space))
    root['space'] = space


def FunctionalDocFileSuite(*paths, **kw):
    if 'layer' in kw:
        layer = kw['layer']
        del kw['layer']
    else:
        layer = zope.app.testing.functional.Functional

    globs = kw.setdefault('globs', {})
    globs['http'] = zope.app.testing.functional.HTTPCaller()
    globs['getRootFolder'] = zope.app.testing.functional.getRootFolder
    globs['sync'] = zope.app.testing.functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')

    def setUp(test):
        FunctionalTestSetup().setUp()

        if kwsetUp is not None:
            kwsetUp(test)

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')

    def tearDown(test):
        if kwtearDown is not None:
            kwtearDown(test)
        FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite(
            './tests.txt', setUp=setUp, layer=zojaxBulkuploadLayer),))
