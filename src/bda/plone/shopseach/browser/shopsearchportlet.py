#from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets.search import ISearchPortlet

from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base


class IShopSearchPortlet(ISearchPortlet):
    """ A portlet displaying a (live) search box for bda.plone.shop.
    """

    enableLivesearch = schema.Bool(
            title = _(u"Enable LiveSearch"),
            description = _(u"Enables the LiveSearch feature, which shows "
                             "live results if the browser supports "
                             "JavaScript."),
            default = True,
            required = False)

    showImages = schema.Bool(
            title = _(u"Show images"),
            description = _(u"Should the seach show images"),
            default = True,
            required = False)


    b_end = schema.Bool(
                         title = _(u"How many to show"),
                         description = _(u"How many to show in each batch"),
                         default = 30,
                         required = True)


class Assignment(base.Assignment):
    implements(IShopSearchPortlet)

    def __init__(self, enableLivesearch=True):
        self.enableLivesearch=enableLivesearch

    @property
    def title(self):
        return _(u"Search for products")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('shopsearch.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        portal_state = getMultiAdapter((context, request), name='plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()

    def enable_livesearch(self):
        return self.data.enableLivesearch

    def search_action(self):
        return '%s/@@search' % self.navigation_root_url


class AddForm(base.AddForm):
    form_fields = form.Fields(ISearchPortlet)
    label = _(u"Add Shopsearch Portlet")
    description = _(u"A search box for bda.plone.shop.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    form_fields = form.Fields(ISearchPortlet)
    label = _(u"Edit Shopsearch Portlet")
    description = _(u"A search box for bda.plone.shop.")
