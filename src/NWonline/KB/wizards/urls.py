from NWonline.KB.wizards.marry import MarryWizard, MarryForm1, \
    MarryForm2, MarryForm3
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^marry/(?P<persoonId>\d*)/$', MarryWizard([MarryForm1, MarryForm2, MarryForm3])),
)
