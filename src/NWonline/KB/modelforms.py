###############################################################################
# File: NWonline/KB/modelforms.py
# Author: Lukas Batteau
# Description: ModelForm classes, customizing default form behavior for models. 
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
# 20110414    Lukas Batteau        Reorganized membership
###############################################################################
from NWonline.KB.widgets import AutoCompleteSelect, SelectWithPopup,\
    DatePicker
from django import forms
import models

class GezinForm(forms.ModelForm):
    txtgezinsnaam = forms.CharField(
                        widget=forms.TextInput(attrs={"size":40}),
                        label="Gezinsnaam")
    inthuisnummer = forms.IntegerField(
                        widget=forms.TextInput(attrs={"size":3}),
                        label="Nummer",
                        required=False)
    txthuisnummertoevoeging = forms.CharField(
                        widget=forms.TextInput(attrs={"size":3}),
                        label="Toevoeging",
                        required=False)
    txtpostcode = forms.CharField(
                        widget=forms.TextInput(attrs={"size":5}),
                        label="Postcode",
                        required=False)
    
    class Meta:
        model = models.Gezin
        widgets = {
                   "idland": AutoCompleteSelect()
                   }

class PersoonForm(forms.ModelForm):
    txttussenvoegsels = forms.CharField(
                            widget=forms.TextInput(attrs={"size":8}),
                            label="Tussenvoegsels",
                            required=False)
    txtvoorletters = forms.CharField(
                            widget=forms.TextInput(attrs={"size":8}),
                            label="Voorletters")
    idlidmaatschapstatus = forms.ModelChoiceField(label="Status",
                                                  queryset=models.LidmaatschapStatus.objects.all(),
                                                  widget=forms.RadioSelect(attrs = {"onClick": "updateStatus();"}),
                                                  empty_label=None,
                                                  required=False)
    
        
    class Meta:
        model = models.Persoon
        widgets = {
            "iddoopgemeente": AutoCompleteSelect(),
            "idbelijdenisgemeente": AutoCompleteSelect(),
            "idhuwelijksgemeente": AutoCompleteSelect(),
            "idbinnengekomenuitgemeente": AutoCompleteSelect(),
            "idvertrokkennaargemeente": AutoCompleteSelect(),
            "dtmgeboortedatum": DatePicker(),
            "dtmdatumdoop": DatePicker(),
            "dtmdatumbelijdenis": DatePicker(),
            "dtmhuwelijksdatum": DatePicker(),
            "dtmdatumhuwelijksbevestiging": DatePicker(),
            "dtmdatumbinnenkomst": DatePicker(),
            "dtmdatumvertrek": DatePicker(),
            "dtmdatumonttrokken": DatePicker(),
            "dtmoverlijdensdatum": DatePicker(),
            #"idgezinsrol": SelectWithPopup()
        }
        
class GemeenteForm(forms.ModelForm):
    
    class Meta:
        model = models.Gemeente
    
class GezinsRolForm(forms.ModelForm):
    
    class Meta:
        model = models.GezinsRol
    
