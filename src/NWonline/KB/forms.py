###############################################################################
# File: NWonline/KB/forms.py
# Author: Lukas Batteau
# Description: Form classes
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
###############################################################################
from NWonline.KB.models import GezinsRol
from django import forms

class PersoonSearchForm(forms.Form):
    """
    This form is used for the advanced search page for persons.
    Its submission is handled by view.handlePersoonListSearch
    """
    idgezinsrol = forms.ModelChoiceField(
                            queryset=GezinsRol.objects.all(), 
                            empty_label="",
                            required=False,
                            label="Gezinsrol")
    txtachternaam = forms.CharField(label="Achternaam",
                                    required=False)
    txttussenvoegsels = forms.CharField(
                            label="Tussenvoegsels",
                            required=False)
    txtvoorletters = forms.CharField(
                            label="Voorletters",
                            required=False)
    txtroepnaam = forms.CharField(label="Roepnaam",
                                    required=False)
    txtdoopnaam = forms.CharField(label="Doopnaam",
                                    required=False)
    dtmgeboortedatumvan = forms.DateField(label="Geboortedatum van",
                                          required=False)
    dtmgeboortedatumtot = forms.DateField(label="tot",
                                          required=False)
    boolactief = forms.BooleanField(label="Actief", 
                                    initial=True,
                                    required=False)
    
    
