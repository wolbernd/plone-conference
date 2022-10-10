from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import plone_conference


class PLONE_CONFERENCELayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plone_conference)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone_conference:default")
        applyProfile(portal, "plone_conference:initial")


PLONE_CONFERENCE_FIXTURE = PLONE_CONFERENCELayer()


PLONE_CONFERENCE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_CONFERENCE_FIXTURE,),
    name="PLONE_CONFERENCELayer:IntegrationTesting",
)


PLONE_CONFERENCE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_CONFERENCE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="PLONE_CONFERENCELayer:FunctionalTesting",
)


PLONE_CONFERENCEACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_CONFERENCE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="PLONE_CONFERENCELayer:AcceptanceTesting",
)
