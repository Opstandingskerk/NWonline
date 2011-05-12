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
    Attestatie, LidmaatschapVorm, Geslacht
from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.db.models.query_utils import Q
from django.forms.forms import Form
from django.http import HttpResponseRedirect, HttpResponse
import datetime
import time

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
    dtmdatumvertrek = forms.DateField(label="Datum vertrek", required=False)
    idvertrokkennaargemeente = forms.ModelChoiceField(label="Gemeente", 
                                                      queryset=Gemeente.objects.all(), 
                                                      required=False,
                                                      widget=AutoCompleteSelect())
    dtmoverlijdensdatum = forms.DateField(label="Datum overlijden", required=False)
    dtmdatumonttrokken = forms.DateField(label="Datum onttrokken", required=False)
    

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
            self.storedFields["updateWholeFamily"] = updateWholeFamily
            
            # Store family
            if (not self.storedFields["is_mode_family"] and updateWholeFamily):
                self.storedFields["gezin"] = self.storedFields["persoon"].idgezin                         
            
            # Store destination church for use in certificate 
            self.storedFields["idvertrokkennaargemeente"] = form.cleaned_data["idvertrokkennaargemeente"]

            # Modify which types of certificates to show
            queryset = Attestatie.objects.all()
            if ((self.storedFields["is_mode_family"] 
                 or self.storedFields["updateWholeFamily"])
                and len(self.storedFields["gezin"].persoon_set.all()) > 1):
                # Only show 'Gezins'
                queryset = queryset.filter(txtcode="Gezins")
            else:
                # Exclude 'Gezins'
                queryset = queryset.exclude(txtcode="Gezins")
                
                # Check membership
                persoon = self.storedFields["persoon"]
                if (persoon.idlidmaatschapvorm == LidmaatschapVorm.objects.get(pk=1)):
                    # Dooplid
                    queryset = queryset.filter(Q(txtcode="Doop")| Q(txtcode="Kerkelijke gegevens"))
                else:
                    queryset = queryset.exclude(txtcode="Doop")
            
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
            
            # Check certificate type
            if (certificateType.txtcode.upper() == "GEZINS"):
                # GEZINSATTESTATIE
                gezin = self.storedFields["gezin"]
                
                head = gezin.persoon_set.get(idgezinsrol__pk=1)
                
                if (gezin.persoon_set.filter(idgezinsrol__pk=2)):
                    partner = gezin.persoon_set.get(idgezinsrol__pk=2)
                else:
                    partner = Persoon(idgeslacht=Geslacht.objects.get(pk=3 - head.idgeslacht.pk))
                
                head_achternaam = ("%s %s" % (head.txttussenvoegsels, head.txtachternaam)).strip()
                partner_achternaam = ("%s %s" % (partner.txttussenvoegsels, partner.txtachternaam)).strip()
                
                if (head.idgeslacht.pk==1):
                    spouse = "zijn echtgenote"
                else:
                    spouse = "haar echtgenoot"
                    
                # Apply date formatting (have to check for 'None' types)

                if (head.dtmgeboortedatum):
                    head.dtmgeboortedatum = head.dtmgeboortedatum.strftime("%d-%m-%Y")
                else:
                    head.dtmgeboortedatum = ""                
                
                if (head.dtmdatumbelijdenis):
                    head.dtmdatumbelijdenis = head.dtmdatumbelijdenis.strftime("%d-%m-%Y")
                else:
                    head.dtmdatumbelijdenis = ""
                    
                if (head.dtmdatumdoop):
                    head.dtmdatumdoop = head.dtmdatumdoop.strftime("%d-%m-%Y")
                else:
                    head.dtmdatumdoop = ""
                    
                if (partner.dtmgeboortedatum):
                    partner.dtmgeboortedatum = partner.dtmgeboortedatum.strftime("%d-%m-%Y")
                else:
                    partner.dtmgeboortedatum = ""
                    
                if (partner.dtmdatumbelijdenis):
                    partner.dtmdatumbelijdenis = partner.dtmdatumbelijdenis.strftime("%d-%m-%Y")
                else:
                    partner.dtmdatumbelijdenis = ""
                    
                if (partner.dtmdatumdoop):
                    partner.dtmdatumdoop = partner.dtmdatumdoop.strftime("%d-%m-%Y")
                else:
                    partner.dtmdatumdoop = ""
                
                # Create certificate
                form.certificate = certificateType.txtbeschrijving % (gezin.txtgezinsnaam,
                                                                      gezin.createAddress(),
                                                                      gezin.txtpostcode,
                                                                      gezin.txtplaats,
                                                                      gezin.idland,
                                                                      datetime.datetime.now().strftime("%d %B %Y"),
                                                                      head.idgeslacht.txtaanhefkerk,
                                                                      head.txtdoopnaam, 
                                                                      head_achternaam,
                                                                      head.txtroepnaam,
                                                                      head.dtmgeboortedatum,
                                                                      head.txtgeboorteplaats,
                                                                      head.dtmdatumdoop,
                                                                      head.iddoopgemeente,
                                                                      head.dtmdatumbelijdenis,
                                                                      head.idbelijdenisgemeente,
                                                                      spouse,
                                                                      partner.idgeslacht.txtaanhefkerk,
                                                                      partner.txtdoopnaam, 
                                                                      partner_achternaam,
                                                                      partner.txtroepnaam,
                                                                      partner.dtmgeboortedatum,
                                                                      partner.txtgeboorteplaats,
                                                                      partner.dtmdatumdoop,
                                                                      partner.iddoopgemeente,
                                                                      partner.dtmdatumbelijdenis,
                                                                      partner.idbelijdenisgemeente,
                                                                      gemeente)
            
            else:
                # Person
                persoon = self.storedFields["persoon"]
            
                achternaam = ("%s %s" % (persoon.txttussenvoegsels, persoon.txtachternaam)).strip()
                aanhef = persoon.idgeslacht.txtaanhefkerk
                
                # Determine pronoun
                if (persoon.idgeslacht.txtgeslacht == "M"):
                    aanwijzend = "hij"
                elif (persoon.idgeslacht.txtgeslacht == "V"):
                    aanwijzend = "zij"  
                
                # Check type of certificate
                if (certificateType.txtcode.upper() == "DOOP"):
                    # DOOPATTESTATIE                                
                    form.certificate = certificateType.txtbeschrijving % (persoon.txtroepnaam,
                                                                          achternaam,
                                                                          persoon.idgezin.createAddress(),
                                                                          persoon.idgezin.txtpostcode,
                                                                          persoon.idgezin.txtplaats,
                                                                          persoon.idgezin.idland,
                                                                          datetime.datetime.now().strftime("%d %B %Y"),
                                                                          aanhef,
                                                                          persoon.txtdoopnaam, 
                                                                          achternaam,
                                                                          persoon.txtroepnaam,
                                                                          persoon.dtmgeboortedatum.strftime("%d-%m-%Y"),
                                                                          persoon.txtgeboorteplaats,
                                                                          persoon.dtmdatumdoop.strftime("%d-%m-%Y") if persoon.dtmdatumdoop else "",
                                                                          persoon.iddoopgemeente,
                                                                          aanhef,
                                                                          gemeente)
                elif (certificateType.txtcode.upper() == "VERBLIJFS"):
                    
        
                    # VERBLIJFSATTESTATIE
                    form.certificate = certificateType.txtbeschrijving % (persoon.txtroepnaam,
                                                                          achternaam,
                                                                          persoon.idgezin.createAddress(),
                                                                          persoon.idgezin.txtpostcode,
                                                                          persoon.idgezin.txtplaats,
                                                                          persoon.idgezin.idland,
                                                                          datetime.datetime.now().strftime("%d %B %Y"),
                                                                          aanhef,
                                                                          persoon.txtdoopnaam, 
                                                                          achternaam,
                                                                          persoon.txtroepnaam,
                                                                          persoon.dtmgeboortedatum.strftime("%d-%m-%Y") if persoon.dtmgeboortedatum else "",
                                                                          persoon.txtgeboorteplaats,
                                                                          persoon.dtmdatumdoop.strftime("%d-%m-%Y") if persoon.dtmdatumdoop else "",
                                                                          persoon.iddoopgemeente,
                                                                          persoon.dtmdatumbelijdenis,
                                                                          persoon.idbelijdenisgemeente,
                                                                          aanwijzend.capitalize(),
                                                                          aanhef,
                                                                          gemeente,
                                                                          aanhef)
            
                elif (certificateType.txtcode.upper() == "BELIJDENIS"):
                    # BELIJDENISATTESTATIE
                    form.certificate = certificateType.txtbeschrijving % (persoon.txtroepnaam,
                                                                          achternaam,
                                                                          persoon.idgezin.createAddress(),
                                                                          persoon.idgezin.txtpostcode,
                                                                          persoon.idgezin.txtplaats,
                                                                          persoon.idgezin.idland,
                                                                          datetime.datetime.now().strftime("%d %B %Y"),
                                                                          aanhef,
                                                                          persoon.txtdoopnaam, 
                                                                          achternaam,
                                                                          persoon.txtroepnaam,
                                                                          persoon.dtmgeboortedatum.strftime("%d-%m-%Y") if persoon.dtmgeboortedatum else "",
                                                                          persoon.txtgeboorteplaats,
                                                                          persoon.dtmdatumdoop.strftime("%d-%m-%Y") if persoon.dtmdatumdoop else "",
                                                                          persoon.iddoopgemeente,
                                                                          persoon.dtmdatumbelijdenis,
                                                                          persoon.idbelijdenisgemeente,
                                                                          aanhef,
                                                                          gemeente,
                                                                          aanhef)
                elif (certificateType.txtcode.upper() == "KERKELIJKE GEGEVENS"):
                    # KERKELIJKE GEGEVENS
                    form.certificate = certificateType.txtbeschrijving % (persoon.txtroepnaam,
                                                                          achternaam,
                                                                          persoon.idgezin.createAddress(),
                                                                          persoon.idgezin.txtpostcode,
                                                                          persoon.idgezin.txtplaats,
                                                                          persoon.idgezin.idland,
                                                                          datetime.datetime.now().strftime("%d %B %Y"),
                                                                          aanhef,
                                                                          persoon.txtdoopnaam, 
                                                                          achternaam,
                                                                          persoon.txtroepnaam,
                                                                          persoon.dtmgeboortedatum.strftime("%d-%m-%Y") if persoon.dtmgeboortedatum else "",
                                                                          persoon.txtgeboorteplaats,
                                                                          persoon.dtmdatumdoop.strftime("%d-%m-%Y") if persoon.dtmdatumdoop else "",
                                                                          persoon.iddoopgemeente,
                                                                          persoon.dtmdatumbelijdenis,
                                                                          persoon.idbelijdenisgemeente,
                                                                          str(persoon.idlidmaatschapvorm).lower())
            
        
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
        if (is_mode_family or form_data["updateWholeFamily"]):
            return HttpResponseRedirect("/leden/gezin/%d/" % (gezin.idgezin))
        else:
            return HttpResponseRedirect("/leden/gezin/persoon/%d/" % (persoon.idpersoon))
        
        
        return HttpResponse("Done")
    
    def get_template(self, step):
        return "KB/wizards/membership_%s.html" % step
        