###############################################################################
# File: NWonline/KB/modelforms.py
# Author: Lukas Batteau
# Description: ModelForm classes, customizing default form behavior for models. 
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
# 20110414    Lukas Batteau        Reorganized membership
###############################################################################
from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
import models

class AutoCompleteSelect(widgets.Select):
    """
    Custom form widget, displaying an autocomplete text input that is connected
    to the original select.
    """
    def __init__(self, attrs=None, choices=()):
        super(AutoCompleteSelect, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        # Make original hidden
        if (attrs):
            attrs["style"] = "display: none"
        else:
            attrs = {"style": "display: none"}
            
        # Create original select field.
        select = super(AutoCompleteSelect, self).render(name, value, attrs, choices)

        # Add auto complete field
        name_auto = name + "_auto"
        attrs_auto = {"id": attrs["id"]+"_auto" }
        final_attrs = self.build_attrs(attrs_auto, type="text", name=name_auto)
        
        autocomplete = u"""<input%s onClick="this.value=''"/>""" % widgets.flatatt(final_attrs)
        
        javascript = u"""<script language="javascript">
        $(document).ready(function(){
            select_autocomplete("%s", "%s");
        });</script>""" % ("#%s" % (attrs_auto["id"]), "#%s" % (attrs["id"]))
        
        
        return mark_safe("%s %s %s" % (select, autocomplete, javascript))

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
        }
    
