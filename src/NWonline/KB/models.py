###############################################################################
# File: NWonline/KB/models.py
# Author: Lukas Batteau
# Description: Business models, mapping directly to the data model used.
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
# 20110118    Lukas Batteau        Added constants for GezinsRol
#                                  Moved createGezinsNaam to class Gezin
#                                  Added default "NEDERLAND" for Land 
# 20110328    Lukas Batteau        Added indexes for quick filter
# 20110329    Lukas Batteau        Reorganized persoon membership
# 20110414    Lukas Batteau        Moved membership description method to model
###############################################################################
from NWonline import settings
from django.db import models
import datetime

class MySQLBooleanField(models.BooleanField):
    """
    The database stores boolean fields as MySQL BIT fields, so we have to 
    customize reading/writing.
    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, bool):
            return value
        return bool(bytearray(value)[0])

class GemeenteType(models.Model):
    idgemeentetype = models.AutoField(primary_key=True, db_column="idGemeenteType") # Field name made lowercase.
    txtgemeentetype = models.CharField(max_length=150, db_column="txtGemeenteType") # Field name made lowercase.

    def __unicode__(self):
        return self.txtgemeentetype

    class Meta:
        db_table = u"ledendb_gemeentetypes"

class Gemeente(models.Model):
    idgemeente = models.AutoField(primary_key=True, db_column="idGemeente") # Field name made lowercase.
    txtgemeentenaam = models.CharField("Naam", max_length=150, db_column="txtGemeenteNaam", blank=True) # Field name made lowercase.
    idgemeentetype = models.ForeignKey(GemeenteType, verbose_name="Type", db_column="idGemeenteType", blank=True, null=True) # Field name made lowercase.
    txtopmerking = models.TextField("Opmerkingen", max_length=765, db_column="txtOpmerking", blank=True, null=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtgemeentenaam

    class Meta:
        db_table = u"ledendb_gemeenten"
        ordering = ["txtgemeentenaam"]


class Geslacht(models.Model):
    idgeslacht = models.AutoField(primary_key=True, db_column="idGeslacht") # Field name made lowercase.
    txtgeslacht = models.CharField(max_length=3, db_column="txtGeslacht", blank=True) # Field name made lowercase.
    txtgeslachtlang = models.CharField(max_length=150, db_column="txtGeslachtLang", blank=True) # Field name made lowercase.
    txtaanhef = models.CharField(max_length=150, db_column="txtAanhef", blank=True) # Field name made lowercase.
    txtaanhefkort = models.CharField(max_length=150, db_column="txtAanhefKort", blank=True) # Field name made lowercase.
    txtaanhefkerk = models.CharField(max_length=135, db_column="txtAanhefKerk", blank=True) # Field name made lowercase.
    txtaanhefkerkkort = models.CharField(max_length=135, db_column="txtAanhefKerkKort", blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtgeslachtlang

    class Meta:
        db_table = u"ledendb_geslachten"

class Land(models.Model):
    NEDERLAND = 149
    
    idland = models.AutoField(primary_key=True, db_column="idLand") # Field name made lowercase.
    txtlandnaam = models.CharField(max_length=300, db_column="txtLandnaam", blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtlandnaam

    class Meta:
        db_table = u"ledendb_landen"
        ordering = ["txtlandnaam"]

class Gezin(models.Model):
    idgezin = models.AutoField(primary_key=True, db_column="idGezin") # Field name made lowercase.
    txtgezinsnaam = models.CharField("Gezin", max_length=150, db_column="txtGezinsnaam", db_index=True) # Field name made lowercase.
    txtstraatnaam = models.CharField("Straat", max_length=150, db_column="txtStraatnaam", blank=True, null=True, db_index=True) # Field name made lowercase.
    inthuisnummer = models.IntegerField("Huisnummer", db_column="intHuisnummer", blank=True, null=True) # Field name made lowercase.
    txthuisnummertoevoeging = models.CharField("Toevoeging", max_length=60, db_column="txtHuisnummerToevoeging", blank=True, null=True) # Field name made lowercase.
    txtpostcode = models.CharField("Postcode", max_length=60, db_column="txtPostcode", db_index=True, blank=True, null=True) # Field name made lowercase.
    txtplaats = models.CharField("Plaats", max_length=150, db_column="txtPlaats", db_index=True, blank=True, null=True) # Field name made lowercase.
    idland = models.ForeignKey(Land, verbose_name="Land", db_column="idLand", blank=True, null=True, default=Land.NEDERLAND) # Field name made lowercase.
    txttelefoon = models.CharField("Telefoon", max_length=75, db_column="txtTelefoon", db_index=True, blank=True, null=True) # Field name made lowercase.
    txtopmerking = models.TextField("Opmerking", max_length=765, db_column="txtOpmerking", blank=True, null=True) # Field name made lowercase.
    
    @classmethod
    def create_gezins_naam(cls, persoon):
        return ("%s, %s (%s)") % ((("%s %s") % (persoon.txtachternaam, persoon.txttussenvoegsels)).strip(),
                                                persoon.txtvoorletters.replace(" ", ""),
                                                persoon.txtroepnaam)
        
    def create_address(self):
        return ("%s %s%s" % (self.txtstraatnaam, str(self.inthuisnummer), self.txthuisnummertoevoeging)).strip()

    def __unicode__(self):
        return self.txtgezinsnaam

    class Meta:
        db_table = u"ledendb_gezinnen"

class GezinsRol(models.Model):
    GEZINSHOOFD = 1
    PARTNER = 2
    KIND = 3
    
    idgezinsrol = models.AutoField(primary_key=True, db_column="idGezinsrol") # Field name made lowercase.
    txtgezinsrol = models.CharField("Rol", max_length=150, db_column="txtGezinsrol", blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtgezinsrol

    class Meta:
        db_table = u"ledendb_gezinsrollen"

class Wijk(models.Model):
    idwijk = models.AutoField(primary_key=True, db_column="idWijk") # Field name made lowercase.
    txtwijknaam = models.CharField(max_length=150, db_column="txtWijkNaam") # Field name made lowercase.
    txtwijknaamkort = models.CharField(max_length=9, db_column="txtWijkNaamKort", blank=True, null=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtwijknaam

    class Meta:
        db_table = u"ledendb_wijken"

class Huiskring(models.Model):
    idhuiskring = models.AutoField(primary_key=True, db_column="idHuiskring") # Field name made lowercase.
    txthuiskringnaam = models.CharField(max_length=150, db_column="txtHuiskringNaam") # Field name made lowercase.
    idwijk = models.ForeignKey(Wijk, db_column="idWijk") # Field name made lowercase.
    txtopmerking = models.TextField(max_length=765, db_column="txtOpmerking", blank=True) # Field name made lowercase.
    txtvolgnummer = models.CharField(max_length=6, db_column="txtVolgnummer", blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txthuiskringnaam

    class Meta:
        db_table = u"ledendb_huiskringen"

class HuiskringLidRol(models.Model):
    idhuiskringlidrol = models.AutoField(primary_key=True, db_column="idHuiskringLidrol") # Field name made lowercase.
    txthuiskringlidrol = models.CharField(max_length=150, db_column="txtHuiskringLidrol") # Field name made lowercase.

    def __unicode__(self):
        return self.txthuiskringlidrol

    class Meta:
        db_table = u"ledendb_huiskringlidrollen"

class LidmaatschapVorm(models.Model):
    DOOP = 1
    BELIJDEND = 2
    GASTLID_DOOP = 3
    GASTLID_BELIJDEND = 4
    
    idlidmaatschapvorm = models.AutoField(primary_key=True, db_column="idLidmaatschapvorm") # Field name made lowercase.
    txtlidmaatschapvorm = models.CharField(max_length=150, db_column="txtLidmaatschapvorm", blank=True) # Field name made lowercase.
    boolvoorquotum = MySQLBooleanField(db_column="boolVoorQuotum") # Field name made lowercase. This field type is a guess.
    txtlidmaatschapvormkort = models.CharField(max_length=150, db_column="txtLidmaatschapvormKort", blank=True) # Field name made lowercase.
    txtattestatie = models.CharField(max_length=150, db_column="txtAttestatie", blank=True, null=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtlidmaatschapvorm

    class Meta:
        db_table = u"ledendb_lidmaatschapvormen"

class LidmaatschapStatus(models.Model):
    ACTIEF = 1
    VERTROKKEN = 2
    ONTTROKKEN = 3
    OVERLEDEN = 4
    
    idlidmaatschapstatus = models.AutoField(primary_key=True, db_column="idLidmaatschapstatus") # Field name made lowercase.
    txtlidmaatschapstatus = models.CharField(max_length=150, db_column="txtLidmaatschapstatus", blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtlidmaatschapstatus

    class Meta:
        db_table = u"ledendb_lidmaatschapstatussen"

class Attestatie(models.Model):
    CODE_BELIJDENIS = "Belijdenis"
    CODE_KERKELIJKEGEGEVENS = "Kerkelijke gegevens"
    CODE_DOOP = "Doop"
    CODE_GEZINS = "Gezins"
    CODE_VERBLIJFS = "Verblijfs"
    
    idattestatie = models.AutoField(primary_key=True)
    txtcode = models.CharField("Code", max_length=20)
    txtbeschrijving = models.TextField("Beschrijving")

    def __unicode__(self):
        return self.txtcode

class Persoon(models.Model):
    idpersoon = models.AutoField(primary_key=True, db_column="idPersoon") # Field name made lowercase.
    idlidmaatschapvorm = models.ForeignKey(LidmaatschapVorm, verbose_name="Lidmaatschap", null=False, db_column="idLidmaatschapVorm", blank=False) # Field name made lowercase.
    idgezin = models.ForeignKey(Gezin, verbose_name="Huishouden", null=True, blank=True, db_column="idGezin") # Field name made lowercase.
    idgezinsrol = models.ForeignKey(GezinsRol, verbose_name="Rol huishouden", db_column="idGezinsRol") # Field name made lowercase.
    txtachternaam = models.CharField("Achternaam", max_length=150, db_column="txtAchternaam", db_index=True) # Field name made lowercase.
    txttussenvoegsels = models.CharField("Tussenvoegsels", max_length=150, db_column="txtTussenvoegsels", blank=True, null=True) # Field name made lowercase.
    txtvoorletters = models.CharField("Voorletters", max_length=150, db_column="txtVoorletters", blank=True, null=True) # Field name made lowercase.
    txtdoopnaam = models.CharField("Doopnaam", max_length=150, db_column="txtDoopnaam", blank=True, db_index=True, null=True) # Field name made lowercase.
    txtroepnaam = models.CharField("Roepnaam", max_length=150, db_column="txtRoepnaam", db_index=True, null=True) # Field name made lowercase.
    boolaansprekenmetroepnaam = MySQLBooleanField("Aanspreken met roepnaam ", db_column="boolAansprekenMetRoepnaam", blank=True, default=True) # Field name made lowercase. This field type is a guess.
    dtmgeboortedatum = models.DateField("Geboortedatum", null=True, db_column="dtmGeboortedatum", blank=True) # Field name made lowercase.
    txtgeboorteplaats = models.CharField("te", max_length=150, null=True, db_column="txtGeboorteplaats", blank=True) # Field name made lowercase.
    idgeslacht = models.ForeignKey(Geslacht, verbose_name="Geslacht", null=True, db_column="idGeslacht", blank=True) # Field name made lowercase.
    dtmdatumdoop = models.DateField("Datum doop", null=True, db_column="dtmDatumDoop", blank=True) # Field name made lowercase.
    iddoopgemeente = models.ForeignKey(Gemeente, verbose_name="Doopgemeente", null=True, db_column="idDoopgemeente", blank=True, related_name="Gedoopt") # Field name made lowercase.
    dtmdatumbelijdenis = models.DateField("Datum belijdenis", null=True, db_column="dtmDatumBelijdenis", blank=True) # Field name made lowercase.
    idbelijdenisgemeente = models.ForeignKey(Gemeente, verbose_name="Belijdenisgemeente", null=True, db_column="idBelijdenisgemeente", blank=True, related_name="Belijdenis") # Field name made lowercase.
    dtmhuwelijksdatum = models.DateField("Datum huwelijk", null=True, db_column="dtmHuwelijksDatum", blank=True) # Field name made lowercase.
    idhuwelijksgemeente = models.ForeignKey(Gemeente, verbose_name="Huwelijksgemeente", null=True, db_column="idHuwelijksGemeente", blank=True, related_name="Gehuwd") # Field name made lowercase.
    dtmdatumbinnenkomst = models.DateField("Datum binnenkomst", null=True, db_column="dtmDatumBinnenkomst", blank=True) # Field name made lowercase.
    idbinnengekomenuitgemeente = models.ForeignKey(Gemeente, verbose_name="Binnengekomen uit", null=True, db_column="idBinnengekomenUitGemeente", blank=True, related_name="Binnengekomen") # Field name made lowercase.
    dtmdatumvertrek = models.DateField("Datum vertrek", null=True, db_column="dtmDatumVertrek", blank=True) # Field name made lowercase.
    idvertrokkennaargemeente = models.ForeignKey(Gemeente, verbose_name="Vertrokken naar", null=True, db_column="idVertrokkenNaarGemeente", blank=True, related_name="Vertrokken") # Field name made lowercase.
    txttelefoonnummer = models.CharField("Telefoon", max_length=75, null=True, db_column="txtTelefoonNummer", blank=True) # Field name made lowercase.
    txtemailadres = models.CharField("E-mailadres", max_length=150, null=True, db_column="txtEmailAdres", blank=True) # Field name made lowercase.
    dtmdatumhuwelijksbevestiging = models.DateField("Datum huwelijksbevestiging", null=True, db_column="dtmDatumHuwelijksbevestiging", blank=True) # Field name made lowercase.
    txtopmerking = models.TextField("Opmerkingen", max_length=765, null=True, db_column="txtOpmerking", blank=True) # Field name made lowercase.
    dtmoverlijdensdatum = models.DateField("Datum overlijden", null=True, db_column="dtmOverlijdensdatum", blank=True) # Field name made lowercase.
    dtmdatumonttrokken = models.DateField("Datum onttrekking", null=True, db_column="dtmDatumOnttrokken", blank=True) # Field name made lowercase.
    idlidmaatschapstatus = models.ForeignKey(LidmaatschapStatus, default=1, verbose_name="Status", null=True, db_column="idLidmaatschapStatus") # Field name made lowercase.
    idwijk = models.ForeignKey(Wijk, verbose_name="Wijk", null=True, blank=True, db_column="idWijk") # Field name made lowercase.
    idgastgemeente = models.ForeignKey(Gemeente, verbose_name="Gastgemeente", null=True, blank=True, db_column="idGastGemeente", related_name="Gastlid") # Field name made lowercase.
    idgasthoofdgemeente = models.ForeignKey(Gemeente, verbose_name="Gasthoofdgemeente", null=True, blank=True, db_column="idGastHoofdGemeente", related_name="Gastlid_hoofd") # Field name made lowercase.
    boolgastlidnw = MySQLBooleanField("Gastlid Noord-West", db_column="boolGastlidNW") # Field name made lowercase. This field type is a guess.
    boolgastlidelders = models.BooleanField("Gastlid elders", db_column="boolGastlidElders") # Field name made lowercase. This field type is a guess.
    boolgeborennw = MySQLBooleanField("Geboren in Noord-West", db_column="boolGeborenNW") # Field name made lowercase. This field type is a guess.
    idhuiskring = models.ForeignKey(Huiskring, verbose_name="Huiskring", db_column="idHuiskring", null=True, blank=True) # Field name made lowercase.
    idhuiskringlidrol = models.ForeignKey(HuiskringLidRol, verbose_name="Rol in huiskring", db_column="idHuiskringRol", null=True, blank=True) # Field name made lowercase.    


    def calculate_age(self, some_date=None):
        if (some_date):
            today = some_date 
        else:
            today = datetime.date.today()
        
        born = self.dtmgeboortedatum
        if (not born):
            # Age unknown
            return 999
        
        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year
        
    def create_address(self, separator=", "):
        address = ("%s %s%s%s" % (self.idgezin.txtstraatnaam, ("%s%s" % (self.idgezin.inthuisnummer, self.idgezin.txthuisnummertoevoeging)).strip(), separator, self.idgezin.txtpostcode))
        if (self.idgezin.txtplaats and self.idgezin.txtplaats.lower() != settings.HOME_TOWN.lower()):
            address += ("%s%s") % (separator, self.idgezin.txtplaats)
        if (self.idgezin.idland and str(self.idgezin.idland).lower() != settings.HOME_COUNTRY.lower()):
            address += ("%s%s") % (separator, self.idgezin.idland)
        return address
    
    def __unicode__(self):
        return ("%s %s") % (self.txtroepnaam, ("%s %s" % (self.txttussenvoegsels, self.txtachternaam)).strip())        
        
    def create_sir_name_sortable(self):
        sir_name = self.txtachternaam
        if (self.txttussenvoegsels):
            sir_name += ", %s" % (self.txttussenvoegsels)
        return sir_name           
        
    def create_sir_name(self):
        return ((self.txttussenvoegsels  + " ") if self.txttussenvoegsels else "") + self.txtachternaam       
        
    def create_display_name(self, mode_church=False):
        # Formatting of name depends on member age
        age = self.calculate_age()
        if (age > 50):
            # dhr. T.C. van Asch
            return ("%s %s %s") % (self.idgeslacht.txtaanhefkort if self.idgeslacht else "", self.txtvoorletters, ("%s %s" % (self.txttussenvoegsels, self.txtachternaam)).strip())
        else:
            # Esther (F.E.) Avci van der Zee
            return ("%s (%s) %s") % (self.txtroepnaam, self.txtvoorletters, ("%s %s" % (self.txttussenvoegsels, self.txtachternaam)).strip())
            
    def create_short_name(self):
        # Formatting of name depends on member age
        age = self.calculate_age()
        if (age > 50):
            # br. T.C. van Asch
            return ("%s %s %s") % (self.idgeslacht.txtaanhefkerkkort if self.idgeslacht else "", self.txtvoorletters, ("%s %s" % (self.txttussenvoegsels, self.txtachternaam)).strip())
        else:
            # zr. Esther Avci van der Zee
            return ("%s %s %s") % (self.idgeslacht.txtaanhefkerkkort if self.idgeslacht else "", self.txtroepnaam, ("%s %s" % (self.txttussenvoegsels, self.txtachternaam)).strip())
            
    
    def membership(self):
        status = self.idlidmaatschapstatus
        lidmaatschap = self.idlidmaatschapvorm
        if (status == LidmaatschapStatus.objects.get(pk=1)):
            # Active: If set, show form
            if (lidmaatschap):
                membership = str(lidmaatschap)
            else:
                membership = str(status)
                
            # If guest member away, show info
            if (self.boolgastlidelders):
                membership += " (gastlid bij %s)" % (self.idgastgemeente)
                
            # If guest member here, show info
            # TODO: The membership forms for guests should be replaced by the
            # boolgastlidnw field
            if (self.boolgastlidnw
                or self.idlidmaatschapvorm == LidmaatschapVorm.objects.get(pk=LidmaatschapVorm.GASTLID_BELIJDEND)
                or self.idlidmaatschapvorm == LidmaatschapVorm.objects.get(pk=LidmaatschapVorm.GASTLID_DOOP)):
                membership += " (lid bij %s)" % (self.idgasthoofdgemeente)
            
        else:
            membership = str(status)
            if (status == LidmaatschapStatus.objects.get(pk=2)):
                # Vertrokken: Show date and destination
                if (self.dtmdatumvertrek):
                    membership += " %s" % (self.dtmdatumvertrek.strftime("%d-%m-%Y"))
                if (self.idvertrokkennaargemeente):
                    membership += " naar %s" % (str(self.idvertrokkennaargemeente))
            elif (status == LidmaatschapStatus.objects.get(pk=3)):
                # Onttrokken: Show date
                if (self.dtmdatumonttrokken):
                    membership += " %s" % (self.dtmdatumonttrokken.strftime("%d-%m-%Y"))
            elif (status == LidmaatschapStatus.objects.get(pk=4)):
                # Overleden: Show date
                if (self.dtmoverlijdensdatum):
                    membership += " %s" % (self.dtmoverlijdensdatum.strftime("%d-%m-%Y"))
        
        return membership
    
    def first_letter_gezin(self):
        if (self.idgezin.txtgezinsnaam):
            return self.idgezin.txtgezinsnaam[0]
        else:
            return ''
     
    def birth_month(self):
        return self.dtmgeboortedatum.strftime("%B") if self.dtmgeboortedatum else ""   
    
    class Meta:
        db_table = u"ledendb_personen"
        ordering = ["txtachternaam"]
        
class tblHuishouden(models.Model):
    """
    This model corresponds with the Geloofhet.nl families table. 
    Data in the Gezin table is exported to this table to be used 
    on the website.
    """
    idHuishouden = models.IntegerField(primary_key=True)
    txtHuishoudenNaam = models.CharField("Gezin", max_length=150)
    txtTelefoonnummer = models.CharField("Telefoon", max_length=75, blank=True, null=True)
    txtStraatnaam = models.CharField("Straat", max_length=150, blank=True, null=True)
    txtHuisnummer = models.CharField("Huisnummer", max_length=20, blank=True, null=True)
    txtPostcode = models.CharField("Postcode", max_length=60, blank=True, null=True)
    txtPlaats = models.CharField("Plaats", max_length=150, blank=True, null=True)
    
    class Meta:
        db_table = u"tblHuishouden"
            
class tblLid(models.Model):
    """
    This model corresponds with the Geloofhet.nl members table. 
    Data in the Persoon table is exported to this table to be used 
    on the website.  
    """
    idLid = models.IntegerField(primary_key=True, db_column="idLid") # Field name made lowercase.
    ysnLid = MySQLBooleanField("Actief lid")
    idHuishouden = models.IntegerField(verbose_name="Gezin", null=True, blank=True) # Field name made lowercase.
    idRol = models.IntegerField(verbose_name="Gezinsrol", null=True, blank=True) # Field name made lowercase.
    txtAchternaam = models.CharField("Achternaam", max_length=150, db_index=True) # Field name made lowercase.
    txtVoorvoegsels = models.CharField("Tussenvoegsels", max_length=150, blank=True, null=True) # Field name made lowercase.
    txtVoorletters = models.CharField("Voorletters", max_length=150, blank=True, null=True) # Field name made lowercase.
    txtDoopnaam = models.CharField("Doopnaam", max_length=150, blank=True, db_index=True, null=True) # Field name made lowercase.
    txtRoepnaam = models.CharField("Roepnaam", max_length=150, db_column="txtRoepnaam", db_index=True, null=True) # Field name made lowercase.
    ysnRoepnaam = MySQLBooleanField("Aanspreken met roepnaam ", blank=True, default=True) # Field name made lowercase. This field type is a guess.
    dtmGeboortedatum = models.DateField("Geboortedatum", null=True, blank=True) # Field name made lowercase.
    txtGeboorteplaats = models.CharField("te", max_length=150, null=True, blank=True) # Field name made lowercase.
    txtGeslacht = models.CharField("Geslacht", max_length=150, null=True, blank=True) # Field name made lowercase.
    idStatus = models.IntegerField("Status", null=True) # Field name made lowercase.
    dtmDoop = models.DateField("Datum doop", null=True, blank=True) # Field name made lowercase.
    idDoopgemeente = models.IntegerField("Doopgemeente", null=True, blank=True) # Field name made lowercase.
    dtmBelijdenis = models.DateField("Datum belijdenis", null=True, blank=True) # Field name made lowercase.
    idBelijdenisgemeente = models.IntegerField("Belijdenisgemeente", null=True, blank=True) # Field name made lowercase.
    dtmBinnenkomst = models.DateField("Datum binnenkomst", null=True, blank=True) # Field name made lowercase.
    idVorigeGemeente = models.IntegerField("Binnengekomen uit", null=True, blank=True) # Field name made lowercase.
    dtmVertrokken = models.DateField("Datum vertrek", null=True, blank=True) # Field name made lowercase.
    idVolgendeGemeente = models.IntegerField("Vertrokken naar", null=True, blank=True) # Field name made lowercase.
    txtMobielNummer = models.CharField("Telefoon", max_length=75, null=True, blank=True) # Field name made lowercase.
    ysnMobielNummer = MySQLBooleanField("Mobiel zichtbaar?")
    txtEmailAdres = models.CharField("E-mailadres", max_length=150, null=True, blank=True) # Field name made lowercase.
    ysnEmailAdres = MySQLBooleanField("E-mailadres zichtbaar?")
    txtAantekeningen = models.TextField("Opmerkingen", max_length=765, null=True, blank=True) # Field name made lowercase.
    dtmTrouwdatum = models.DateField("Datum huwelijk", null=True, blank=True) # Field name made lowercase.
    idTrouwgemeente = models.IntegerField("Huwelijksgemeente", null=True, blank=True) # Field name made lowercase.
    dtmTrouwbevestiging = models.DateField("Datum huwelijksbevestiging", null=True, blank=True) # Field name made lowercase.
    idHuiskring = models.IntegerField("Huiskring", null=True, blank=True) # Field name made lowercase.
    idHuiskringLidType = models.IntegerField("Rol in huiskring", null=True, blank=True) # Field name made lowercase.    
    huiskringwijk = models.IntegerField("Wijk", null=True, blank=True) # Field name made lowercase.
    
    class Meta:
            db_table = u"tblLid"    