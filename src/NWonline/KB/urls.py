###############################################################################
# File: NWonline/KB/urls.py
# Author: Lukas Batteau
# Description: Url patterns file for the KB app
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header. Removed unused import.
# 20110414    Lukas Batteau        Static path changed. Fixed redirect.
###############################################################################
from django.conf.urls.defaults import patterns, include
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    (r'^login/$', 'NWonline.KB.views.handleLogin'),
    (r'^logout/$', 'NWonline.KB.views.handleLogout'),
    
    (r'^leden/$', 'NWonline.KB.views.handlePersoonListFilter'),
    (r'^leden/update$', 'NWonline.KB.views.handlePersoonListUpdate'),
    (r'^leden/search/$', 'NWonline.KB.views.handlePersoonListSearch'),
    (r'^leden/gezin/(?P<gezinId>\d*)/*$', 'NWonline.KB.views.handleGezinDetails'),    
    (r'^leden/gezin/(?P<gezinId>\d*)/persoon/add$', 'NWonline.KB.views.handleGezinPersoonAdd'),    
    (r'^leden/gezin/add/*$', 'NWonline.KB.views.handleGezinAdd'),    
    (r'^leden/gezin/persoon/(?P<persoonId>\d*)/.*$', 'NWonline.KB.views.handlePersoonDetails'),
    
    (r'^wizard/', include('NWonline.KB.wizards.urls')),
    
    (r'^query/persoon/.*$', 'NWonline.KB.ajax.queryPersoon'),
    (r'^query/gemeente/.*$', 'NWonline.KB.ajax.queryGemeente'),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'D:/Development/Projects/Django/NWonline/media/KB'}),
        
    (r'^$', redirect_to, {'url': 'leden/'}),
        
)
