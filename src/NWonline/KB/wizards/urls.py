from NWonline.KB.wizards.marry import MarryWizard, MarryForm1, MarryForm2, MarryForm3, MarryForm4
from NWonline.KB.wizards.membership import MembershipWizard, MembershipForm1
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^marry/(?P<persoonId>\d*)/$', MarryWizard([MarryForm1, MarryForm2, MarryForm3, MarryForm4])),
    (r'^membership/gezin/(?P<gezinId>\d*)/$', MembershipWizard([MembershipForm1]), { 'updateWholeFamily': True }),
    (r'^membership/(?P<persoonId>\d*)/$', MembershipWizard([MembershipForm1]), { 'updateWholeFamily': False }),
)
