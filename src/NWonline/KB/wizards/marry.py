from NWonline.KB.models import Gezin, Persoon, Geslacht, Land, \
    createGezinsNaam, GezinsRol
from django import forms
from django.contrib.auth.decorators import login_required
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
    Marry wizard screen 2. Determines which persoon is the family head.
    """
    gezinshoofd = forms.CharField(widget=forms.HiddenInput())
    

class MarryForm3(Form):
    """
    Marry wizard screen 3. Determines the family address 
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
                                    label="Land")
    
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
            # Screen 2. Select family head.
            
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
        elif (step == 2):
            # Screen 3. Address
            
            gezinA = self.storedFields["persoonA"].idgezin
            self.storedFields["gezinA"] = gezinA
            
            gezinB = self.storedFields["persoonB"].idgezin
            self.storedFields["gezinB"] = gezinB

        # Copy data in stored fields to context        
        self.extra_context.update(self.storedFields)
        
        return FormWizard.render_template(self, request, form, previous_fields, step)
    
    def done(self, request, form_list):
        """
        Process the completed wizard.
        """
        
        # Stored data
        persoonA = self.storedFields["persoonA"]
        persoonB = self.storedFields["persoonB"]
        
        # We always create a new Gezin object for the married couple, 
        # then throw away the old Gezin objects if they are empty.
        gezin = Gezin()
        
        # Head of family A or B
        if (form_list[1].cleaned_data["gezinshoofd"] == "A"):
            familyHead = persoonA
            persoonA.idgezinsrol = GezinsRol.objects.get(pk=1)
            persoonB.idgezinsrol = GezinsRol.objects.get(pk=2)
        else:
            familyHead = persoonB
            persoonB.idgezinsrol = GezinsRol.objects.get(pk=1)
            persoonA.idgezinsrol = GezinsRol.objects.get(pk=2)
        
        # Create gezinsnaam
        gezin.txtgezinsnaam = createGezinsNaam(familyHead)
            
        # Check what address the new family is using
        code = form_list[2].cleaned_data["code"]
        if (code == "NEW"):
            # New address, create gezin
            gezin.txtstraatnaam = form_list[2].cleaned_data["txtstraatnaam"]
            gezin.inthuisnummer = form_list[2].cleaned_data["inthuisnummer"]
            gezin.txthuisnummertoevoeging = form_list[2].cleaned_data["txthuisnummertoevoeging"]
            gezin.txtpostcode = form_list[2].cleaned_data["txtpostcode"]
            gezin.txtplaats = form_list[2].cleaned_data["txtplaats"]
            gezin.idland = form_list[2].cleaned_data["idland"]
            
        else:
            # Existing address, copy data from specified address
            oldGezin = self.storedFields["gezin"+code] # gezinA or gezinB
            gezin.txtstraatnaam = oldGezin.txtstraatnaam
            gezin.inthuisnummer = oldGezin.inthuisnummer
            gezin.txthuisnummertoevoeging = oldGezin.txthuisnummertoevoeging
            gezin.txtpostcode = oldGezin.txtpostcode
            gezin.txtplaats = oldGezin.txtplaats
            gezin.idland = oldGezin.idland
            
        # Save
        print "CREATING NEW GEZIN %s" % (gezin)
        gezin.save()

        # Move persoonA to gezin
        persoonAGezinOld = persoonA.idgezin
        persoonA.idgezin = gezin
        persoonA.save()
        
        # Remove old gezin if 'empty'
        if (len(persoonAGezinOld.persoon_set.all()) == 0):
            print "DELETING GEZIN " + str(persoonAGezinOld)
            persoonAGezinOld.delete()
            
        # Move persoonB to gezin
        persoonBGezinOld = persoonB.idgezin
        persoonB.idgezin = gezin
        persoonB.save()
 
        # Remove old gezin if 'empty'
        if (persoonBGezinOld and len(persoonBGezinOld.persoon_set.all()) == 0):
            print "DELETING GEZIN " + str(persoonBGezinOld)
            persoonBGezinOld.delete()
            
        return HttpResponseRedirect("/leden/gezin/%d/" % (gezin.idgezin))
    
    def get_template(self, step):
        return "KB/wizards/marry_%s.html" % step
        