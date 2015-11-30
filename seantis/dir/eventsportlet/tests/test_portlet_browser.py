from seantis.dir.eventsportlet.tests import FunctionalTestCase
from zExceptions import NotFound


class BrowserTestCase(FunctionalTestCase):

    def setUp(self):
        super(BrowserTestCase, self).setUp()

        self.baseurl = self.portal.absolute_url()

        browser = self.new_browser()
        browser.login_admin()

        self.admin_browser = browser

    def tearDown(self):
        pass

    def test_browser_add_portlet(self):
        browser = self.admin_browser

        # Check if portlet available
        browser.open('/@@manage-portlets')
        self.assertTrue('seantis.dir.eventsportlet' in browser.contents)

        # Check saving settings
        browser.open(
            '++contextportlets++plone.rightcolumn/+/seantis.dir.eventsportlet'
        )
        browser.getControl('Save').click()
        self.assertTrue('Required input is missing.' in browser.contents)

        browser.getControl(name='form.url').value = 'test'
        browser.getControl('Save').click()
        self.assertTrue('The specified URI is not valid.' in browser.contents)

        browser.getControl(name='form.url').value = 'http://localhost:888'
        browser.getControl('Save').click()
        self.assertTrue('@@toggle-visibility' in browser.contents)

        browser.open('/')
        self.assertTrue('portletSeantisDirEvents' in browser.contents)

    def test_browser_add_multiple_portlets(self):
        browser = self.admin_browser

        # Add portlet
        browser.open(
            '++contextportlets++plone.rightcolumn/+/seantis.dir.eventsportlet'
        )
        browser.getControl(name='form.url').value = 'http://localhost:888'
        browser.getControl(name='form.max_events').value = '10'
        browser.getControl('Save').click()
        browser.open('/')
        self.assertTrue('max=10' in browser.contents)

        # Add portlet
        browser.open(
            '++contextportlets++plone.rightcolumn/+/seantis.dir.eventsportlet'
        )
        browser.getControl(name='form.url').value = 'http://localhost:888'
        browser.getControl(name='form.max_events').value = '15'
        browser.getControl('Save').click()
        browser.open('/')
        self.assertTrue('max=10' in browser.contents)
        self.assertTrue('max=15' in browser.contents)

    def test_browser_settings(self):
        browser = self.admin_browser

        # Add portlet
        browser.open(
            '++contextportlets++plone.rightcolumn/+/seantis.dir.eventsportlet'
        )
        browser.getControl(name='form.url').value = 'http://localhost:888'
        browser.getControl(name='form.max_events').value = '10'
        browser.getControl('Save').click()
        browser.open('/')
        self.assertTrue('max=10' in browser.contents)
        self.assertTrue('data-event-config-url="http://localhost:888?type=json'
                        in browser.contents)

        # Change max number of events
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.max_events').value = '8'
        browser.getControl(name='form.cat1').value = 'Category1'
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')
        self.assertTrue('max=8' in browser.contents)
        self.assertTrue('filter=true' not in browser.contents)
        self.assertTrue('cat1=Category1' not in browser.contents)
        self.assertTrue('cat2=' not in browser.contents)

        # Enable filtering
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.do_filter').value = True
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')
        s = '?type=json&amp;imported=true&amp;max=8&amp;filter=true&amp;' \
            'cat1=Category1'

        self.assertTrue(s in browser.contents)
        self.assertTrue('cat2=' not in browser.contents)

        # Change categories
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.cat1').value = ''
        browser.getControl(name='form.cat2').value = 'Category2'
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')
        s = '?type=json&amp;imported=true&amp;max=8&amp;filter=true&amp;' \
            'cat2=Category2'
        self.assertTrue(s in browser.contents)
        self.assertTrue('cat1=' not in browser.contents)

        # Change categories
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.cat1').value = 'Category1'
        browser.getControl(name='form.cat2').value = 'Category2'
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')
        s = '?type=json&amp;imported=true&amp;max=8&amp;filter=true&amp;' \
            'cat1=Category1&amp;cat2=Category2'
        self.assertTrue(s in browser.contents)

        # Change categories
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.cat1').value = 'Category1\nCategory1_1'
        browser.getControl(name='form.cat2').value = 'Category2\nCategory2_1'
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')
        s = '?type=json&amp;imported=true&amp;max=8&amp;filter=true&amp;' \
            'cat1=Category1&amp;cat1=Category1_1&amp;' \
            'cat2=Category2&amp;cat2=Category2_1'
        self.assertTrue(s in browser.contents)

        # Open in same window per default
        self.assertTrue('data-event-config-target="_self"' in browser.contents)
        self.assertTrue(
            'data-event-config-target="_blank"' not in browser.contents
        )
        self.assertTrue('target="_self">All events' in browser.contents)
        self.assertTrue('target="_blank">All events' not in browser.contents)

        # Change target
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.target_blank').value = True
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')

        self.assertTrue(
            'data-event-config-target="_blank"' in browser.contents
        )
        self.assertTrue(
            'data-event-config-target="_self"' not in browser.contents
        )
        self.assertTrue('target="_self">All events' not in browser.contents)
        self.assertTrue('target="_blank">All events' in browser.contents)

        # Change all events url
        browser.open(
            '++contextportlets++plone.rightcolumn/events-portlet/edit'
        )
        browser.getControl(name='form.all_url').value = 'http://new.to'
        try:
            browser.getControl('Save').click()
        except NotFound:
            pass
        browser.open('/')
        self.assertTrue('http://new.to' in browser.contents)
