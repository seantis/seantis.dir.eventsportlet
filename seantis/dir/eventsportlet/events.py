from zope import schema
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
# from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from seantis.dir.eventsportlet import _
from seantis.dir.eventsportlet.interfaces import IEventsPortlet


class Assignment(base.Assignment):
    implements(IEventsPortlet)

    def __init__(self, url=u'', max_events=5,
                 do_filter=False, cat1=u'', cat2=u''):
        self.url = url
        self.max_events = max_events
        self.do_filter = do_filter
        self.cat1 = cat1
        self.cat2 = cat2

    title = _(u'Events portlet')


class Renderer(base.Renderer):

    """Portlet renderer."""

    render = ViewPageTemplateFile('templates/events.pt')

    @property
    def available(self):
        return len(self.data.url) > 0

    # def text(self):
    #     return self.data.text

    # def css_class(self):
    #     """Generate a CSS class from the portlet header
    #     """
    #     header = self.data.header
    #     normalizer = component.getUtility(IIDNormalizer)
    #     return "portlet-embed-%s" % normalizer.normalize(header)


class AddForm(base.AddForm):

    """Addd form"""

    form_fields = form.Fields(IEventsPortlet)
    label = _(u"Add events portlet")
    description = _(u"A portlet which displays events.")

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):

    """Portlet edit form."""

    form_fields = form.Fields(IEventsPortlet)
    label = _(u"Edit events portlet")
    description = _(u"A portlet which displays events.")
