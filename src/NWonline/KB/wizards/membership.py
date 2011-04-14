###############################################################################
# File: NWonline/KB/wizards/membership.py
# Author: Lukas Batteau
# Description: Wizard classes for changing the membership of a person.
# 
# CHANGE HISTORY
# 20110314    Lukas Batteau        Initial version
###############################################################################
from NWonline.KB.models import Persoon, LidmaatschapStatus, Gemeente, Gezin
from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.forms.forms import Form
from django.http import HttpResponseRedirect, HttpResponse

class MembershipForm1(Form):
    """
    Membership wizard screen 1
    """
    updateWholeFamily = forms.BooleanField(widget=forms.RadioSelect(choices=(("1", "Ja"),("2", "Nee"))),
                                           label="Hele gezin?",
                                           initial=False,
                                           required=False)
    idlidmaatschapstatus = forms.ModelChoiceField(label="Status",
                                                  queryset=LidmaatschapStatus.objects.all(),
                                                  widget=forms.RadioSelect(attrs = {'onClick': 'updateStatus();'}),
                                                  empty_label=None)
    dtmdatumvertrek = forms.DateField(label="Datum vertrek", required=False)
    idvertrokkennaargemeente = forms.ModelChoiceField(label="Gemeente", queryset=Gemeente.objects.all(), required=False)
    dtmoverlijdensdatum = forms.DateField(label="Datum overlijden", required=False)
    dtmdatumonttrokken = forms.DateField(label="Datum onttrokken", required=False)
    

class MembershipWizard(FormWizard):
    
    def __init__(self, *args, **kwargs):
        FormWizard.__init__(self, *args, **kwargs)
        setattr(self, "storedFields", {})
        
    def parse_params(self, request, *args, **kwargs):
        """
        There are two modes of entering this wizard:
        1. At 'gezin' level
        2. At 'persoon' level
        
        Which level is determined by the 'updateWholeFamily' flag passed
        on entering this wizard. There is also an additional 'updateWholeFamily'
        flag in the user form.
        """
        
        # Read 'whole family' flag
        updateWholeFamily = kwargs["updateWholeFamily"]
        self.storedFields["updateWholeFamily"] = updateWholeFamily 
        
        if (updateWholeFamily):
            # Extract gezin ID from url
            gezinId = kwargs["gezinId"]

            # Check if gezin already retrieved
            if ("gezin" not in self.storedFields 
                or self.storedFields["gezin"].idgezin != gezinId):
                # Not yet retrieved or someone else. Retrieve.
                gezin = Gezin.objects.get(pk=gezinId)
            
                # Add gezin to stored fields
                self.storedFields["gezin"] = gezin
            
        else:
            # Extract persoon Id from url
            persoonId = kwargs["persoonId"]
        
            # Check if persoon already retrieved
            if ("persoon" not in self.storedFields 
                or self.storedFields["persoon"].idpersoon != persoonId):
                # Not yet retrieved or someone else. Retrieve.
                persoon = Persoon.objects.get(pk=persoonId)
            
                # Add persoon to stored fields
                self.storedFields["persoon"] = persoon
            
        # Continue in super class
        FormWizard.parse_params(self, request, args, kwargs)
    
    def render_template(self, request, form, previous_fields, step, context=None):
        # Authenticate user
        if not request.user.is_authenticated():
            # User is anonymous, redirect to login
            return HttpResponseRedirect("/login?next=" + request.path)        
            
        # Copy data in stored fields to context        
        self.extra_context.update(self.storedFields)
        
        return FormWizard.render_template(self, request, form, previous_fields, step)
    
    def done(self, request, form_list):
        """
        Processes submitted form
        """
        # Read 'whole family' flag
        updateWholeFamily = self.storedFields["updateWholeFamily"]
        
        # Processed form data
        form_data = form_list[0].cleaned_data
        
        # Create list of persons to update.
        if (updateWholeFamily):
            # Update whole family
            gezin = self.storedFields["gezin"]
            persoonList = gezin.persoon_set.all()
        else:
            # Update one person?
            persoon = self.storedFields["persoon"]                
            # Check for 'whole family' flag in form
            if (form_data["updateWholeFamily"]):
                # User has indicated whole family should be updated
                gezin = persoon.idgezin
                persoonList = gezin.persoon_set.all()
            else:
                persoonList = [self.storedFields["persoon"]]
            
        # Now update all persons in persoonList
        for persoon in persoonList:
            persoon.idlidmaatschapstatus = form_data["idlidmaatschapstatus"]
            
            if (persoon.idlidmaatschapstatus.pk == 2):
                # Vertrokken
                persoon.dtmdatumvertrek = form_data["dtmdatumvertrek"]
                persoon.idvertrokkennaargemeente = form_data["idvertrokkennaargemeente"]
            elif (persoon.idlidmaatschapstatus.pk == 3):
                # Onttrokken
                persoon.dtmdatumonttrokken = form_data["dtmdatumonttrokken"]
            elif (persoon.idlidmaatschapstatus.pk == 4):
                # Overleden
                persoon.dtmoverlijdensdatum = form_data["dtmoverlijdensdatum"]
            
            persoon.save()
        
        # Redirect the user to either family or person detail page
        if (updateWholeFamily or form_data["updateWholeFamily"]):
            return HttpResponseRedirect("/leden/gezin/%d/" % (gezin.idgezin))
        else:
            return HttpResponseRedirect("/leden/gezin/persoon/%d/" % (persoon.idpersoon))
        
        
        return HttpResponse("Done")
    
    def get_template(self, step):
        return "KB/wizards/membership_%s.html" % step
        