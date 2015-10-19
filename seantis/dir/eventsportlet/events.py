import urllib

from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope.schema import Bool, Int, Text, URI

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from seantis.dir.eventsportlet import _


class IEventsPortlet(IPortletDataProvider):

    """A portlet which renders events.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    url = URI(
        title=_(u'The URL of the events directory'),
        required=True,
    )

    max_events = Int(
        title=_(u'Maximum number of displayed events'),
        required=True,
        default=5,
        min=1
    )

    do_filter = Bool(
        title=_(u'Filter events'),
        required=False,
        default=False
    )

    cat1 = Text(
        title=_(u'What'),
        description=_(u'One category per line.'),
        required=False,
        default=u''
    )

    cat2 = Text(
        title=_(u'Where'),
        description=_(u'One category per line.'),
        required=False,
        default=u''
    )

    target_blank = Bool(
        title=_(u'Open links in a new window or tab'),
        required=False,
        default=False
    )


class Assignment(base.Assignment):

    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IEventsPortlet)

    def __init__(self, url=u'', max_events=5,
                 do_filter=False, cat1=u'', cat2=u'', target_blank=False):
        self.url = url
        self.max_events = max_events
        self.do_filter = do_filter
        self.cat1 = cat1
        self.cat2 = cat2
        self.target_blank = target_blank

    # title = _(u'Events portlet')

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Events portlet')


class Renderer(base.Renderer):

    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('events.pt')

    def as_query_param(self, label, values):
        if not label or not values:
            return ''

        categories = [
            urllib.quote_plus(cat.strip().encode('utf-8'))
            for cat in values.strip().split('\n') if cat.strip()
        ]

        if categories:
            categories.insert(0, '')
            return '&{}='.format(label).join(categories)

        return ''

    def build_url(self, json=True):

        url = self.data.url.strip() + '?'
        if json:
            url += 'type=json&imported=true&max=' + str(self.data.max_events)
            url += '&'
        if self.data.do_filter:
            url += 'filter=true'
            url += self.as_query_param('cat1', self.data.cat1)
            url += self.as_query_param('cat2', self.data.cat2)
        return url

    def export_url(self):
        return self.build_url()

    def events_url(self):
        return self.build_url(False)

    def target(self):
        if self.data.target_blank:
            return '_blank'
        else:
            return '_self'


class AddForm(base.AddForm):

    """Addd form

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added."""

    form_fields = form.Fields(IEventsPortlet)
    label = _(u"Add events portlet")
    description = _(u"A portlet which displays events.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display."""

    form_fields = form.Fields(IEventsPortlet)
    label = _(u"Edit events portlet")
    description = _(u"A portlet which displays events.")
