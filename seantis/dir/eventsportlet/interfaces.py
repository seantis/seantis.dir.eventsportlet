from plone.portlets.interfaces import IPortletDataProvider
from zope.schema import Bool, Int, TextLine, URI

from seantis.dir.eventsportlet import _


class IEventsPortlet(IPortletDataProvider):

    """A portlet which renders events."""

    url = URI(
        title=_(u'The URL of the events directory'),
        required=True,
    )

    max_events = Int(
        title=_(u'Maximum number of displayed events'),
        required=True,
        default=5
    )

    do_filter = Bool(
        title=_(u'Filter events by category names'),
        required=False,
        default=False
    )

    cat1 = TextLine(
        title=_(u'Filter: 1st category name'),
        required=False,
        default=u''
    )

    cat2 = TextLine(
        title=_(u'Filter: 2nd category name'),
        required=False,
        default=u''
    )
