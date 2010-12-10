###############################################################################
# File: NWonline/KB/forms.py
# Author: Lukas Batteau
# Description: Form classes
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
###############################################################################
from django import forms

class PersoonSearchForm(forms.Form):
    txtachternaam = forms.CharField()
    txtroepnaam = forms.CharField()
    dtmgeboortedatumvan = forms.DateField()
    dtmgeboortedatumtot = forms.DateField()
    boolactief = forms.BooleanField()
    
    
