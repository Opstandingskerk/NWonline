###############################################################################
# File: NWonline/KB/forms.py
# Author: Lukas Batteau
# Description: Form classes
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
# 20110329    Lukas Batteau        Reorganized persoon membership
###############################################################################
from NWonline.KB.models import GezinsRol, LidmaatschapStatus, LidmaatschapVorm,\
    Wijk
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
    idlidmaatschapstatus = forms.ModelChoiceField(
                                    queryset=LidmaatschapStatus.objects.all(),
                                    label="Status lidmaatschap",
                                    required=False,
                                    initial=LidmaatschapStatus.objects.get(pk=1))
    idlidmaatschapvorm = forms.ModelChoiceField(
                                    queryset=LidmaatschapVorm.objects.all(),
                                    label="Lidmaatschap vorm",
                                    required=False)
    idwijk = forms.ModelChoiceField(queryset=Wijk.objects.all(),
                                    label="Wijk",
                                    required=False)
    dtmdatumbinnenkomstvan = forms.DateField(label="Datum binnenkomst van",
                                          required=False)
    dtmdatumbinnenkomsttot = forms.DateField(label="tot",
                                          required=False)
    dtmdatumvertrekvan = forms.DateField(label="Datum vertrek van",
                                          required=False)
    dtmdatumvertrektot = forms.DateField(label="tot",
                                          required=False)
    dtmdatumonttrokkenvan = forms.DateField(label="Datum onttrokken van",
                                          required=False)
    dtmdatumonttrokkentot = forms.DateField(label="tot",
                                          required=False)
    dtmoverlijdensdatumvan = forms.DateField(label="Datum overleden van",
                                          required=False)
    dtmoverlijdensdatumtot = forms.DateField(label="tot",
                                          required=False)
    
    
