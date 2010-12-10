###############################################################################
# File: NWonline/KB/modelforms.py
# Author: Lukas Batteau
# Description: ModelForm classes, customizing default form behavior for models. 
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
###############################################################################
from django import forms
import models

class GezinForm(forms.ModelForm):
    txtgezinsnaam = forms.CharField(
                        widget=forms.TextInput(attrs={'size':40}),
                        label="Gezinsnaam")
    inthuisnummer = forms.IntegerField(
                        widget=forms.TextInput(attrs={'size':3}),
                        label="Nummer",
                        required=False)
    txthuisnummertoevoeging = forms.CharField(
                        widget=forms.TextInput(attrs={'size':3}),
                        label="Toevoeging",
                        required=False)
    txtpostcode = forms.CharField(
                        widget=forms.TextInput(attrs={'size':5}),
                        label="Postcode",
                        required=False)
    
    class Meta:
        model = models.Gezin

class PersoonForm(forms.ModelForm):
    txttussenvoegsels = forms.CharField(
                            widget=forms.TextInput(attrs={'size':8}),
                            label="Tussenvoegsels",
                            required=False)
    txtvoorletters = forms.CharField(
                            widget=forms.TextInput(attrs={'size':8}),
                            label="Voorletters")
    
    class Meta:
        model = models.Persoon
    
