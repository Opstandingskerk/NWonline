###############################################################################
# File: NWonline/KB/wizards/membership.py
# Author: Lukas Batteau
# Description: Wizard classes for changing the membership of a person.
# 
# CHANGE HISTORY
# 20110314    Lukas Batteau        Initial version
# 20110416    Lukas Batteau        Added certificates (attestaties)
# 20110417    Lukas Batteau        Fix: Check for one parent families
###############################################################################
from NWonline.KB.modelforms import AutoCompleteSelect
from NWonline.KB.models import Persoon, LidmaatschapStatus, Gemeente, Gezin, \
    Attestatie, LidmaatschapVorm, Geslacht, GezinsRol
from NWonline.KB.widgets import JQueryDateField
from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.db.models.query_utils import Q
from django.forms.forms import Form
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.template.context import Context
from django.utils.translation import ugettext
import datetime

class MembershipForm1(Form):
    """
    Membership wizard screen 1
    """
    updateWholeFamily = forms.BooleanField(widget=forms.RadioSelect(choices=(("1", "Ja"),("0", "Nee"))),
                                           label="Hele gezin?",
                                           initial=False,
                                           required=False)
    generateCertificate = forms.BooleanField(widget=forms.RadioSelect(choices=(("1", "Ja"),("0", "Nee"))),
                                             label="Attestatie?",
                                             required=False)
    idlidmaatschapstatus = forms.ModelChoiceField(label="Status",
                                                  queryset=LidmaatschapStatus.objects.all(),
                                                  widget=forms.RadioSelect(attrs = {'onClick': 'updateStatus();'}),
                                                  empty_label=None)
    dtmdatumvertrek = forms.DateField(label="Datum vertrek", required=False,
                                      widget=JQueryDateField)
    idvertrokkennaargemeente = forms.ModelChoiceField(label="Gemeente", 
                                                      queryset=Gemeente.objects.all(), 
                                                      required=False,
                                                      widget=AutoCompleteSelect())
    dtmoverlijdensdatum = forms.DateField(label="Datum overlijden", required=False,
                                          widget=JQueryDateField)
    dtmdatumonttrokken = forms.DateField(label="Datum onttrokken", required=False,
                                         widget=JQueryDateField)

class MembershipForm2(Form):
    """
    Membership wizard screen 2
    """
    certificateType = forms.ModelChoiceField(label="Attestatie",
                                             queryset=Attestatie.objects.all(),
                                             widget=forms.RadioSelect(),
                                             empty_label=None)
    

class MembershipForm3(Form):
    """
    Membership wizard screen 3
    """
    certificate = None
    

class MembershipWizard(FormWizard):
    
    def __init__(self, *args, **kwargs):
        FormWizard.__init__(self, *args, **kwargs)
        setattr(self, "storedFields", {})
        
    def parse_params(self, request, *args, **kwargs):
        """
        There are two modes of entering this wizard:
        1. At 'gezin' level
        2. At 'persoon' level
        
        Which level is determined by the 'is_mode_family' flag passed
        on entering this wizard. There is also an additional 'updateWholeFamily'
        flag in the user form.
        """
        
        # Read 'whole family' flag
        is_mode_family = kwargs["is_mode_family"]
        
        if (is_mode_family):
            # Extract gezin ID from url
            gezinId = kwargs["gezinId"]
            
            # Check if gezin already retrieved
            if ("gezin" not in self.storedFields 
                or self.storedFields["gezin"].idgezin != gezinId):
                # Not yet retrieved or someone else. Retrieve.
                gezin = Gezin.objects.get(pk=gezinId)
                
                # Add gezin to stored fields
                self.storedFields["gezin"] = gezin
                
                # Check size of family
                if (len(gezin.persoon_set.all()) == 1):
                    # Can't process this as family
                    is_mode_family = False
                    # Store persoon separately
                    self.storedFields["persoon"] = gezin.persoon_set.get(pk=1)                
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
            
        self.storedFields["is_mode_family"] = is_mode_family

        # Copy data in stored fields to context        
        self.extra_context.update(self.storedFields)
        
        # Continue in super class
        FormWizard.parse_params(self, request, args, kwargs)
    
    def process_step(self, request, form, step):
        """
        Hook for dynamically modifying the wizard's pages based on user input
        """
        
        # Check which page we're processing
        if (step == 0):
            # Page 1
            
            # Check whether we should generate a certificate at the end
            # of the wizard
            generateCertificate = form.cleaned_data["generateCertificate"]
            if (generateCertificate):
                # Certificate request, add corresponding pages if not yet existing
                if (len(self.form_list) == 1):
                    self.form_list.append(MembershipForm2)
                    self.form_list.append(MembershipForm3)
            else:
                # Reset list
                self.form_list = [MembershipForm1]
                # The rest of the fiels are only necessary for generating
                # a certificate
                return
                
            # Store whether whole family should be updated
            updateWholeFamily = form.cleaned_data["updateWholeFamily"]
            
            # If mode on entering was not 'family', but the user wants
            # to update the whole family, we switch to mode 'family'
            if (not self.storedFields["is_mode_family"] and updateWholeFamily):
                self.storedFields["gezin"] = self.storedFields["persoon"].idgezin
                self.storedFields["is_mode_family"] = updateWholeFamily         
            
            # Store destination church for use in certificate 
            self.storedFields["idvertrokkennaargemeente"] = form.cleaned_data["idvertrokkennaargemeente"]

            # Determine which types of certificates to show
            queryset = Attestatie.objects.all()
            if (self.storedFields["is_mode_family"]
                and len(self.storedFields["gezin"].persoon_set.all()) > 1):
                # Show 'Gezins' and 'Kerkelijke gegevens'
                queryset = queryset.filter(Q(txtcode=Attestatie.CODE_GEZINS)| Q(txtcode=Attestatie.CODE_KERKELIJKEGEGEVENS))
            else:
                # Exclude 'Gezins'
                queryset = queryset.exclude(txtcode=Attestatie.CODE_GEZINS)
                
                # Check membership
                persoon = self.storedFields["persoon"]
                if (persoon.idlidmaatschapvorm == LidmaatschapVorm.objects.get(pk=1)):
                    # Dooplid
                    queryset = queryset.filter(Q(txtcode=Attestatie.CODE_DOOP)| Q(txtcode=Attestatie.CODE_KERKELIJKEGEGEVENS))
                else:
                    queryset = queryset.exclude(txtcode=Attestatie.CODE_DOOP)
            
            self.form_list[1].base_fields["certificateType"].queryset = queryset
             
                
        elif (step == 1):
            # Store selected certificate
            self.storedFields["certificateType"] = form.cleaned_data["certificateType"]
        
                            
    def render_template(self, request, form, previous_fields, step, context=None):
        # Authenticate user
        if not request.user.is_authenticated():
            # User is anonymous, redirect to login
            return HttpResponseRedirect("/login?next=" + request.path)
        
        elif (step == 2):
            # Page 3: Generate certificate
            certificateType = self.storedFields["certificateType"]
            gemeente = self.storedFields["idvertrokkennaargemeente"]
            
            # Determine mode
            is_mode_family = self.storedFields["is_mode_family"]
            
            if (is_mode_family):
                # Check certificate type
                if (certificateType.txtcode == Attestatie.CODE_GEZINS
                    or certificateType.txtcode == Attestatie.CODE_KERKELIJKEGEGEVENS):
                    # Gezinsattestatie or Kerkelijke gegevens for gezin
                    gezin = self.storedFields["gezin"]
                    
                    # Determine head of the family
                    head = gezin.persoon_set.get(idgezinsrol=GezinsRol.GEZINSHOOFD)
                    
                    # Check if head has partner
                    if (gezin.persoon_set.filter(idgezinsrol=GezinsRol.PARTNER)):
                        # Has partner
                        partner = gezin.persoon_set.get(idgezinsrol=GezinsRol.PARTNER)
                    else:
                        # No partner, create new 'empty' person of other sex
                        partner = Persoon(idgeslacht=Geslacht.objects.get(pk=3 - head.idgeslacht.pk))
                    
                    if (certificateType.txtcode == Attestatie.CODE_GEZINS):
                        template = loader.get_template("KB/wizards/certificates/gezins.html")
                    else:
                        template = loader.get_template("KB/wizards/certificates/kerkelijke_gegevens.html")
                    
                    context = Context({
                        'gezin': gezin,
                        'persoon': head,
                        'partner': partner,
                        'children': gezin.persoon_set.filter(idgezinsrol=GezinsRol.KIND),
                        'gemeente': gemeente
                    })
                    
                    # Create certificate
                    form.certificate = template.render(context)
            else:
                # Person
                persoon = self.storedFields["persoon"]
            
                # Check type of certificate
                if (certificateType.txtcode == Attestatie.CODE_DOOP):
                    template = loader.get_template("KB/wizards/certificates/doop.html")
                elif (certificateType.txtcode == Attestatie.CODE_VERBLIJFS):
                    template = loader.get_template("KB/wizards/certificates/verblijfs.html")
                elif (certificateType.txtcode == Attestatie.CODE_BELIJDENIS):
                    template = loader.get_template("KB/wizards/certificates/belijdenis.html")
                elif (certificateType.txtcode == Attestatie.CODE_KERKELIJKEGEGEVENS):
                    template = loader.get_template("KB/wizards/certificates/kerkelijke_gegevens.html")
                    
                context = Context({
                    'gezin': persoon.idgezin,
                    'persoon': persoon,
                    'gemeente': gemeente
                })
                
                # Create certificate
                form.certificate = template.render(context)
        
        # Copy data in stored fields to context        
        self.extra_context.update(self.storedFields)
        
        return FormWizard.render_template(self, request, form, previous_fields, step)
    
    def done(self, request, form_list):
        """
        Processes submitted form
        """
        # Read mode
        is_mode_family = self.storedFields["is_mode_family"]
        
        # Processed form data
        form_data = form_list[0].cleaned_data
        
        # Create list of persons to update.
        if (is_mode_family):
            # Update whole family
            gezin = self.storedFields["gezin"]
            persoonList = gezin.persoon_set.all()
        else:
            # Update one person?
            persoon = self.storedFields["persoon"]    
            # List of persons for just one person
            persoonList = [persoon]
            
        # Now update all persons in persoonList
        for persoon in persoonList:
            persoon.idlidmaatschapstatus = form_data["idlidmaatschapstatus"]
            
            # First reset the fields, e.g. departure date should be made
            # empty if a member becomes active again.
            persoon.dtmdatumvertrek = None
            persoon.idvertrokkennaargemeente = None
            persoon.dtmdatumonttrokken = None
            persoon.dtmoverlijdensdatum = None
            
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
        if (is_mode_family):
            return HttpResponseRedirect("/leden/gezin/%d/" % (gezin.idgezin))
        else:
            return HttpResponseRedirect("/leden/gezin/persoon/%d/" % (persoon.idpersoon))
        
        
        return HttpResponse("Done")
    
    def get_template(self, step):
        return "KB/wizards/membership_%s.html" % step
        