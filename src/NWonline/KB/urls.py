###############################################################################
# File: NWonline/KB/urls.py
# Author: Lukas Batteau
# Description: Url patterns file for the KB app
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header. Removed unused import.
###############################################################################
from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^login/$', 'NWonline.KB.views.handleLogin'),
    (r'^logout/$', 'NWonline.KB.views.handleLogout'),
    
    (r'^leden/search/$', 'NWonline.KB.views.handlePersoonSearch'),
        
    (r'^leden/$', 'NWonline.KB.views.handlePersoonList'),
    (r'^leden/gezin/(?P<gezinId>\d*)/*$', 'NWonline.KB.views.handleGezinDetails'),    
    (r'^leden/gezin/(?P<gezinId>\d*)/persoon/add$', 'NWonline.KB.views.handleGezinPersoonAdd'),    
    (r'^leden/gezin/add/*$', 'NWonline.KB.views.handleGezinAdd'),    
    (r'^leden/gezin/persoon/(?P<persoonId>\d*)/.*$', 'NWonline.KB.views.handlePersoonDetails'),
    
    (r'^wizard/', include('NWonline.KB.wizards.urls')),
    
    (r'^query/persoon/.*$', 'NWonline.KB.ajax.queryPersoon'),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'D:/Development/Projects/NWonline/media/KB'}),
)
