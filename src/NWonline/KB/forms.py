from django import forms

class PersoonSearchForm(forms.Form):
    txtachternaam = forms.CharField()
    txtroepnaam = forms.CharField()
    dtmgeboortedatumvan = forms.DateField()
    dtmgeboortedatumtot = forms.DateField()
    boolactief = forms.BooleanField()
    
    
