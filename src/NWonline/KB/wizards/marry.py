###############################################################################
# File: NWonline/KB/wizards/marry.py
# Author: Lukas Batteau
# Description: Wizard classes for marrying a person.
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
# 20110118    Lukas Batteau        Move kids from previous family to new family
#                                  Fixed bug where entered values were lost
# 20110118    Lukas Batteau        Restructured code for readability 
###############################################################################
from NWonline.KB.models import Gezin, Persoon, Geslacht, Land, GezinsRol, \
    Gemeente, LidmaatschapStatus
from NWonline.KB.widgets import AutoCompleteSelect
from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.forms.forms import Form
from django.http import HttpResponseRedirect
from string import atoi

class MarryForm1(Form):
    """
    Marry wizard screen 1. Determines if spouse is existing member or new.
    """
    isNew = forms.IntegerField(widget=forms.RadioSelect(choices=((1, "Nieuw"),(0, "Bestaand"))),
                               label="Lidmaatschap")
    idpersoonB = forms.ModelChoiceField(queryset=Persoon.objects.all(),
                                        widget=forms.HiddenInput(),
                                        required=False)
    txtachternaam = forms.CharField(label="Achternaam")
    txtroepnaam = forms.CharField(label="Roepnaam")
    txtvoorletters = forms.CharField(label="Voorletters")
    idgeslacht = forms.ModelChoiceField(queryset=Geslacht.objects.all(),
                                        label="Geslacht")
    txttussenvoegsels = forms.CharField(widget=forms.TextInput(attrs={"size":8}),
                                        label="Tussenvoegsels",
                                        required=False)
    
class MarryForm2(Form):
    """
    Marry wizard screen 2. Determines the marriage details.
    """
    dtmhuwelijksdatum = forms.DateField(label="Datum huwelijk")
    dtmdatumhuwelijksbevestiging = forms.DateField(label="Datum bevestiging")
    idhuwelijksgemeente = forms.ModelChoiceField(widget=AutoCompleteSelect(),
                                        queryset=Gemeente.objects.all(),
                                        label="Gemeente")
    

class MarryForm3(Form):
    """
    Marry wizard screen 3. Determines which persoon is the family head.
    """
    gezinshoofd = forms.CharField(widget=forms.HiddenInput())
    

class MarryForm4(Form):
    """
    Marry wizard screen 4. Determines the family address 
    """
    code = forms.CharField(widget=forms.RadioSelect(choices=(("A", "A"),("B", "B"),("NEW", "NEW"))))
    txtstraatnaam = forms.CharField(label="Straat")
    inthuisnummer = forms.IntegerField(
                        widget=forms.TextInput(attrs={"size":3}),
                        label="Nummer")
    txthuisnummertoevoeging = forms.CharField(
                        widget=forms.TextInput(attrs={"size":3}),
                        label="Toevoeging",
                        required=False)
    txtpostcode = forms.CharField(
                        widget=forms.TextInput(attrs={"size":5}),
                        label="Postcode",
                        required=False)    
    txtplaats = forms.CharField(label="Plaats")
    idland = forms.ModelChoiceField(queryset=Land.objects.all(),
                                    label="Land",
                                    initial=Land.objects.get(idland=1))
    
class MarryWizard(FormWizard):
    
    def __init__(self, *args, **kwargs):
        FormWizard.__init__(self, *args, **kwargs)
        setattr(self, "storedFields", {})
        
    def parse_params(self, request, *args, **kwargs):
        """
        Extract the persoon from the url. To prevent this method from
        retrieving the same persoon in every screen we add a check to
        see if the persoon is already retrieved.
        """
        
        # Extract persoon ID from url
        persoonId = kwargs["persoonId"]
        
        # Check if persoon already retrieved
        if ("persoonA" not in self.storedFields 
            or self.storedFields["persoonA"].idpersoon != persoonId):
            # Not yet retrieved or someone else. Retrieve.
            persoon = Persoon.objects.get(pk=persoonId)
        
            # Add persoon to stored fields
            self.storedFields["persoonA"] = persoon        
        
        # Continue in super class
        FormWizard.parse_params(self, request, args, kwargs)
    
    
    def render_template(self, request, form, previous_fields, step, context=None):

        # Authenticate user
        if not request.user.is_authenticated():
            # User is anonymous, redirect to login
            return HttpResponseRedirect("/login?next=" + request.path)        
            
        if (step == 1):
            # Store persoonB from screen 1.
            idpersoon = request.POST["0-idpersoonB"]
            if (idpersoon):
                persoon = Persoon.objects.get(pk=idpersoon)
            else:
                persoon = Persoon()
                persoon.txtachternaam = request.POST["0-txtachternaam"]
                persoon.txtroepnaam = request.POST["0-txtroepnaam"]
                persoon.idgeslacht = Geslacht.objects.get(pk=atoi(request.POST["0-idgeslacht"]))
                persoon.txttussenvoegsels = request.POST["0-txttussenvoegsels"]
                persoon.txtvoorletters = request.POST["0-txtvoorletters"] 
            
            # Add persoon to context
            self.storedFields["persoonB"] = persoon
        
            gezinA = self.storedFields["persoonA"].idgezin
            self.storedFields["gezinA"] = gezinA
            
            gezinB = self.storedFields["persoonB"].idgezin
            self.storedFields["gezinB"] = gezinB

        # Copy data in stored fields to context        
        self.extra_context.update(self.storedFields)
        
        return FormWizard.render_template(self, request, form, previous_fields, step)
    
    def done(self, request, form_list):
        """
        Complete the wizard in three steps:
         1. Create the new family object and set the necessary values
         2. Move persoonA with any children to the new family
         3. Move persoonB with any children to the new family
        """
        
        # Stored data
        persoonA = self.storedFields["persoonA"]
        persoonB = self.storedFields["persoonB"]
        
        ################################
        # 1. CREATE NEW FAMILY OBJECT
        #    - Create object
        #    - Set new family name
        #    - Set new address
        ################################
        
        # We always create a new Gezin object for the married couple, 
        # then throw away the old Gezin objects if they are empty.
        gezin = Gezin()
        
        # Determine new family name
        if (form_list[2].cleaned_data["gezinshoofd"] == "A"):
            gezin.txtgezinsnaam = Gezin.create_gezins_naam(persoonA)
        else:
            gezin.txtgezinsnaam = Gezin.create_gezins_naam(persoonB)
        
        # Check what address the new family is using: A, B, or NEW
        code = form_list[3].cleaned_data["code"]
        
        # Retrieve the corresponding existing family (gezinB may be None)
        if "gezin"+code in self.storedFields:
            oldGezin = self.storedFields["gezin"+code] # gezinA or gezinB
        else:
            oldGezin = None 

        # If the user chose the address of person B, but person B is new,
        # we have the same situation as when the address is new.
        if (code == "NEW" or (code == "B" and oldGezin == None)):
            # New address, create gezin
            gezin.txtstraatnaam = form_list[3].cleaned_data["txtstraatnaam"]
            gezin.inthuisnummer = form_list[3].cleaned_data["inthuisnummer"]
            gezin.txthuisnummertoevoeging = form_list[3].cleaned_data["txthuisnummertoevoeging"]
            gezin.txtpostcode = form_list[3].cleaned_data["txtpostcode"]
            gezin.txtplaats = form_list[3].cleaned_data["txtplaats"]
            gezin.idland = form_list[3].cleaned_data["idland"]
            
        else:
            # Existing address, copy data from specified address
            gezin.txtstraatnaam = oldGezin.txtstraatnaam
            gezin.inthuisnummer = oldGezin.inthuisnummer
            gezin.txthuisnummertoevoeging = oldGezin.txthuisnummertoevoeging
            gezin.txtpostcode = oldGezin.txtpostcode
            gezin.txtplaats = oldGezin.txtplaats
            gezin.idland = oldGezin.idland
            
        # Save
        print "CREATING NEW GEZIN %s" % (gezin)
        gezin.save()

        #######################################
        # 2. UDPATE A:
        #    - Move any children to new family
        #    - Change family role for A
        #    - Move A to new family
        #    - Remove old family
        #    - Update marriage info
        #######################################
        
        # If persoonA is not a child
        if (persoonA.idgezinsrol_id != GezinsRol.KIND):
            # Move the existing children in the same family to the new family.
            children = persoonA.idgezin.persoon_set.filter(idgezinsrol=GezinsRol.KIND)
            for child in children:
                child.idgezin = gezin
                child.save()

        # Change family role
        if (form_list[2].cleaned_data["gezinshoofd"] == "A"):
            persoonA.idgezinsrol = GezinsRol.objects.get(pk=GezinsRol.GEZINSHOOFD)
        else:
            persoonA.idgezinsrol = GezinsRol.objects.get(pk=GezinsRol.PARTNER)

        # Move persoonA to new family
        persoonAGezinOld = persoonA.idgezin
        persoonA.idgezin = gezin
        
        # Remove old gezin of persoonA if empty
        if (len(persoonAGezinOld.persoon_set.all()) == 0):
            print "DELETING GEZIN " + str(persoonAGezinOld)
            persoonAGezinOld.delete()
            
        # Update marriage info
        persoonA.dtmhuwelijksdatum = form_list[1].cleaned_data["dtmhuwelijksdatum"]
        persoonA.dtmdatumhuwelijksbevestiging = form_list[1].cleaned_data["dtmdatumhuwelijksbevestiging"]
        persoonA.idhuwelijksgemeente = form_list[1].cleaned_data["idhuwelijksgemeente"]
        
        persoonA.save()
            
        #######################################
        # 3. UDPATE B:
        #    - Move any children to new family
        #    - Change family role for B
        #    - Move B to new family
        #    - Remove old family (if present)
        #######################################
        
        # Check if persoonB is an existing person, and not a child
        if (persoonB.idgezin and persoonB.idgezinsrol != GezinsRol.KIND):
            # If persoonB is not a child, move all children in the same family to 
            # the new family.
            children = persoonB.idgezin.persoon_set.filter(idgezinsrol=GezinsRol.KIND)
            for child in children:
                child.idgezin = gezin
                child.save()
        
        # Update the family role
        if (form_list[2].cleaned_data["gezinshoofd"] == "A"):
            persoonB.idgezinsrol = GezinsRol.objects.get(pk=GezinsRol.PARTNER)
        else:
            persoonB.idgezinsrol = GezinsRol.objects.get(pk=GezinsRol.GEZINSHOOFD)

        # Move persoonB to new family
        persoonBGezinOld = persoonB.idgezin
        persoonB.idgezin = gezin
 
        # Remove old gezin of persoonB if 'empty'
        if (persoonBGezinOld and len(persoonB.idgezin.persoon_set.all()) == 0):
            print "DELETING GEZIN " + str(persoonBGezinOld)
            persoonBGezinOld.delete()
        
        # Update marriage info
        persoonB.dtmhuwelijksdatum = form_list[1].cleaned_data["dtmhuwelijksdatum"]
        persoonB.dtmdatumhuwelijksbevestiging = form_list[1].cleaned_data["dtmdatumhuwelijksbevestiging"]
        persoonB.idhuwelijksgemeente = form_list[1].cleaned_data["idhuwelijksgemeente"]

        persoonB.save()
        
        return HttpResponseRedirect("/leden/gezin/%d/" % (gezin.idgezin))
    
    def get_template(self, step):
        return "KB/wizards/marry_%s.html" % step
        