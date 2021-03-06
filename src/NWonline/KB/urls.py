###############################################################################
# File: NWonline/KB/urls.py
# Author: Lukas Batteau
# Description: Url patterns file for the KB app
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header. Removed unused import.
# 20110414    Lukas Batteau        Static path changed. Fixed redirect.
###############################################################################
from NWonline import settings
from django.conf.urls.defaults import patterns, include
from django.views.generic.simple import redirect_to
import os

urlpatterns = patterns('',
    (r'^login/$', 'NWonline.KB.views.handleLogin'),
    (r'^logout/$', 'NWonline.KB.views.handleLogout'),
    
    (r'^leden/$', 'NWonline.KB.views.handlePersoonListFilter'),
    (r'^leden/export$', 'NWonline.KB.views.handlePersoonListExport'),
    (r'^leden/update$', 'NWonline.KB.views.handlePersoonListUpdate'),
    (r'^leden/gezin/(?P<gezinId>\d*)/*$', 'NWonline.KB.views.handleGezinDetails'),    
    (r'^leden/gezin/(?P<gezinId>\d*)/persoon/add$', 'NWonline.KB.views.handleGezinPersoonAdd'),    
    (r'^leden/gezin/add/*$', 'NWonline.KB.views.handleGezinAdd'),    
    (r'^leden/gezin/persoon/(?P<persoonId>\d*)/.*$', 'NWonline.KB.views.handlePersoonDetails'),
    
    (r'^wizard/', include('NWonline.KB.wizards.urls')),
    
    (r'^query/persoon/.*$', 'NWonline.KB.ajax.queryPersoon'),
    (r'^query/gemeente/.*$', 'NWonline.KB.ajax.queryGemeente'),
    
    (r'^add/(?P<model>.*)$', 'NWonline.KB.views.handleAddInstance'),
    
    (r'^dashboard/$', 'NWonline.KB.dashboard.handleDashboard'),
    (r'^dashboard/members$', 'NWonline.KB.dashboard.handleExportMembers'),
    (r'^dashboard/election$', 'NWonline.KB.dashboard.handleExportElection'),
    (r'^dashboard/birthdays$', 'NWonline.KB.dashboard.handleExportBirthdays'),
    (r'^dashboard/email$', 'NWonline.KB.dashboard.handleExportEmail'),
    (r'^dashboard/update$', 'NWonline.KB.dashboard.exportMembersToWebsite'),
    (r'^dashboard/progress$', 'NWonline.KB.dashboard.reportExportProgress'),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.MEDIA_ROOT, 'KB')}),
        
    (r'^$', redirect_to, {'url': 'dashboard/'}),
        
)
