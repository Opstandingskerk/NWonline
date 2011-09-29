###############################################################################
# File: NWonline/urls.py
# Author: Lukas Batteau
# Description: Url patterns file for the NWonline project.
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header. Reorganized imports.
###############################################################################
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
admin.autodiscover()

import locale
locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

urlpatterns = patterns('',
    # Example:
    # (r'^Ledenadministratie/', include('NWonline.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('NWonline.KB.urls')),
)
