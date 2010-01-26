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
"""Tickets system to work-around security

This is needed, because Flash doesn't use browser cookies.

$Id$
"""
from random import random
from zope.app.cache.ram import RAMCache
from zope.traversing.browser.absoluteurl import absoluteURL

ticketCache = RAMCache()

def issueTicket(ident):
    ticket = str(random())
    ticketCache.set(True, ident, {'ticket': ticket})
    return ticket


def validateTicket(ident, ticket):
    ticket = ticketCache.query(ident, {'ticket': ticket})
    return (ticket is not None)


def invalidateTicket(ident, ticket):
    ticketCache.invalidate(ident, {'ticket': ticket})
