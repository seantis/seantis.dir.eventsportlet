# from seantis.dir.eventsportlet.tests import IntegrationTestCase
from seantis.dir.eventsportlet.tests import FunctionalTestCase


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

        self.assertTrue(True)

        browser = self.admin_browser

        # Check if portlet available
        browser.open('/@@manage-portlets')
        self.assertTrue('seantis.dir.eventsportlet' in browser.contents)

        # Check saving settings
        browser.open(
            '++contextportlets++plone.rightcolumn/+/seantis.dir.eventsportlet')
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
