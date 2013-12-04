from Products.CMFCore.utils import getToolByName


def setup_initial(context):
    pass


def upgrade_1000_to_1001(context):
    # update css and js
    # getToolByName(context, 'portal_css').cookResources()
    # getToolByName(context, 'portal_javascripts').cookResources()
    pass
