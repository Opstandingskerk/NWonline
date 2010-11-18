from django.db import models

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

class Gemeente(models.Model):
    idgemeente = models.AutoField(primary_key=True, db_column='idGemeente') # Field name made lowercase.
    txtgemeentenaam = models.CharField(max_length=150, db_column='txtGemeenteNaam', blank=True) # Field name made lowercase.
    idgemeentetype = models.IntegerField(db_column='idGemeenteType') # Field name made lowercase.
    txtopmerking = models.TextField(max_length=765, db_column='txtOpmerking', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtgemeentenaam

    class Meta:
        db_table = u'ledendb_gemeenten'
        ordering = ['txtgemeentenaam']


class GemeenteType(models.Model):
    idgemeentetype = models.AutoField(primary_key=True, db_column='idGemeenteType') # Field name made lowercase.
    txtgemeentetype = models.CharField(max_length=150, db_column='txtGemeenteType') # Field name made lowercase.

    def __unicode__(self):
        return self.txtgemeentetype

    class Meta:
        db_table = u'ledendb_gemeentetypes'

class Geslacht(models.Model):
    idgeslacht = models.AutoField(primary_key=True, db_column='idGeslacht') # Field name made lowercase.
    txtgeslacht = models.CharField(max_length=3, db_column='txtGeslacht', blank=True) # Field name made lowercase.
    txtgeslachtlang = models.CharField(max_length=150, db_column='txtGeslachtLang', blank=True) # Field name made lowercase.
    txtaanhef = models.CharField(max_length=150, db_column='txtAanhef', blank=True) # Field name made lowercase.
    txtaanhefkort = models.CharField(max_length=150, db_column='txtAanhefKort', blank=True) # Field name made lowercase.
    txtaanhefkerk = models.CharField(max_length=135, db_column='txtAanhefKerk', blank=True) # Field name made lowercase.
    txtaanhefkerkkort = models.CharField(max_length=135, db_column='txtAanhefKerkKort', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtgeslachtlang

    class Meta:
        db_table = u'ledendb_geslachten'

class Land(models.Model):
    idland = models.AutoField(primary_key=True, db_column='idLand') # Field name made lowercase.
    txtlandnaam = models.CharField(max_length=300, db_column='txtLandnaam', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtlandnaam

    class Meta:
        db_table = u'ledendb_landen'
        ordering = ['txtlandnaam']

def createGezinsNaam(persoon):
    return ("%s, %s (%s)") % ((("%s %s") % (persoon.txtachternaam, persoon.txttussenvoegsels)).strip(),
                                            persoon.txtvoorletters.replace(" ", ""),
                                            persoon.txtroepnaam)

class Gezin(models.Model):
    idgezin = models.AutoField(primary_key=True, db_column='idGezin') # Field name made lowercase.
    txtgezinsnaam = models.CharField("Gezin", max_length=150, db_column='txtGezinsnaam') # Field name made lowercase.
    txtstraatnaam = models.CharField("Straat", max_length=150, db_column='txtStraatnaam', blank=True, null=True) # Field name made lowercase.
    inthuisnummer = models.IntegerField("Huisnummer", db_column='intHuisnummer', blank=True, null=True) # Field name made lowercase.
    txthuisnummertoevoeging = models.CharField("Toevoeging", max_length=60, db_column='txtHuisnummerToevoeging', blank=True, null=True) # Field name made lowercase.
    txtpostcode = models.CharField("Postcode", max_length=60, db_column='txtPostcode', blank=True, null=True) # Field name made lowercase.
    txtplaats = models.CharField("Plaats", max_length=150, db_column='txtPlaats', blank=True, null=True) # Field name made lowercase.
    idland = models.ForeignKey(Land, verbose_name="Land", db_column='idLand', blank=True, null=True) # Field name made lowercase.
    txttelefoon = models.CharField("Telefoon", max_length=75, db_column='txtTelefoon', blank=True) # Field name made lowercase.
    txtopmerking = models.TextField("Opmerking", max_length=765, db_column='txtOpmerking', blank=True) # Field name made lowercase.
    
    def __unicode__(self):
        return self.txtgezinsnaam

    class Meta:
        db_table = u'ledendb_gezinnen'

class GezinsRol(models.Model):
    idgezinsrol = models.AutoField(primary_key=True, db_column='idGezinsrol') # Field name made lowercase.
    txtgezinsrol = models.CharField(max_length=150, db_column='txtGezinsrol', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtgezinsrol

    class Meta:
        db_table = u'ledendb_gezinsrollen'

class Wijk(models.Model):
    idwijk = models.AutoField(primary_key=True, db_column='idWijk') # Field name made lowercase.
    txtwijknaam = models.CharField(max_length=150, db_column='txtWijkNaam') # Field name made lowercase.
    txtwijknaamkort = models.CharField(max_length=9, db_column='txtWijkNaamKort', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtwijknaam

    class Meta:
        db_table = u'ledendb_wijken'

class Huiskring(models.Model):
    idhuiskring = models.AutoField(primary_key=True, db_column='idHuiskring') # Field name made lowercase.
    txthuiskringnaam = models.CharField(max_length=150, db_column='txtHuiskringNaam') # Field name made lowercase.
    idwijk = models.ForeignKey(Wijk, db_column='idWijk') # Field name made lowercase.
    txtopmerking = models.TextField(max_length=765, db_column='txtOpmerking', blank=True) # Field name made lowercase.
    txtvolgnummer = models.CharField(max_length=6, db_column='txtVolgnummer', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txthuiskringnaam

    class Meta:
        db_table = u'ledendb_huiskringen'

class HuiskringLidRol(models.Model):
    idhuiskringrol = models.AutoField(primary_key=True, db_column='idHuiskringrol') # Field name made lowercase.
    txthuiskringrol = models.CharField(max_length=150, db_column='txtHuiskringrol') # Field name made lowercase.

    def __unicode__(self):
        return self.txthuiskringrol

    class Meta:
        db_table = u'ledendb_huiskringlidrollen'

class HuiskringLid(models.Model):
    idpersoon = models.AutoField(primary_key=True, db_column='idPersoon') # Field name made lowercase.
    idhuiskring = models.ForeignKey(Huiskring, db_column='idHuiskring') # Field name made lowercase.
    idhuiskringrol = models.ForeignKey(HuiskringLidRol, db_column='idHuiskringRol') # Field name made lowercase.
    idhuiskringlid = models.IntegerField(db_column='idHuiskringLid') # Field name made lowercase.
    class Meta:
        db_table = u'ledendb_huiskringleden'

class LidmaatschapStatus(models.Model):
    idlidmaatschapstatus = models.AutoField(primary_key=True, db_column='idLidmaatschapstatus') # Field name made lowercase.
    txtlidmaatschapstatus = models.CharField(max_length=150, db_column='txtLidmaatschapstatus', blank=True) # Field name made lowercase.
    boolvoorquotum = MySQLBooleanField(db_column='boolVoorQuotum') # Field name made lowercase. This field type is a guess.
    txtlidmaatschapstatuskort = models.CharField(max_length=150, db_column='txtLidmaatschapstatusKort', blank=True) # Field name made lowercase.
    txtattestatie = models.CharField(max_length=150, db_column='txtAttestatie', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.txtlidmaatschapstatus

    class Meta:
        db_table = u'ledendb_lidmaatschapstatussen'

class Persoon(models.Model):
    idpersoon = models.AutoField(primary_key=True, db_column='idPersoon') # Field name made lowercase.
    idlidmaatschapstatus = models.ForeignKey(LidmaatschapStatus, verbose_name="Status", null=True, db_column='idLidmaatschapStatus', blank=True) # Field name made lowercase.
    idgezin = models.ForeignKey(Gezin, verbose_name="Gezin", null=True, blank=True, db_column='idGezin') # Field name made lowercase.
    idgezinsrol = models.ForeignKey(GezinsRol, verbose_name="Gezinsrol", db_column='idGezinsRol') # Field name made lowercase.
    txtachternaam = models.CharField("Achternaam", max_length=150, db_column='txtAchternaam') # Field name made lowercase.
    txttussenvoegsels = models.CharField("Tussenvoegsels", max_length=150, db_column='txtTussenvoegsels', blank=True, null=True) # Field name made lowercase.
    txtvoorletters = models.CharField("Voorletters", max_length=150, db_column='txtVoorletters', blank=True) # Field name made lowercase.
    txtdoopnaam = models.CharField("Doopnaam", max_length=150, db_column='txtDoopnaam', blank=True) # Field name made lowercase.
    txtroepnaam = models.CharField("Roepnaam", max_length=150, db_column='txtRoepnaam') # Field name made lowercase.
    boolaansprekenmetroepnaam = MySQLBooleanField("Aanspreken met roepnaam ", db_column='boolAansprekenMetRoepnaam', blank=True) # Field name made lowercase. This field type is a guess.
    dtmgeboortedatum = models.DateField("Geboortedatum", null=True, db_column='dtmGeboortedatum', blank=True) # Field name made lowercase.
    txtgeboorteplaats = models.CharField("te", max_length=150, db_column='txtGeboorteplaats', blank=True) # Field name made lowercase.
    idgeslacht = models.ForeignKey(Geslacht, verbose_name="Geslacht", null=True, db_column='idGeslacht', blank=True) # Field name made lowercase.
    dtmdatumdoop = models.DateField("Datum doop", null=True, db_column='dtmDatumDoop', blank=True) # Field name made lowercase.
    iddoopgemeente = models.ForeignKey(Gemeente, verbose_name="Doopgemeente", null=True, db_column='idDoopgemeente', blank=True, related_name='Gedoopt') # Field name made lowercase.
    dtmdatumbelijdenis = models.DateField("Datum belijdenis", null=True, db_column='dtmDatumBelijdenis', blank=True) # Field name made lowercase.
    idbelijdenisgemeente = models.ForeignKey(Gemeente, verbose_name="Belijdenisgemeente", null=True, db_column='idBelijdenisgemeente', blank=True, related_name='Belijdenis') # Field name made lowercase.
    dtmhuwelijksdatum = models.DateField("Datum huwelijk", null=True, db_column='dtmHuwelijksDatum', blank=True) # Field name made lowercase.
    idhuwelijksgemeente = models.ForeignKey(Gemeente, verbose_name="Huwelijksgemeente", null=True, db_column='idHuwelijksGemeente', blank=True, related_name='Gehuwd') # Field name made lowercase.
    dtmdatumbinnenkomst = models.DateField("Datum binnenkomst", null=True, db_column='dtmDatumBinnenkomst', blank=True) # Field name made lowercase.
    idbinnengekomenuitgemeente = models.ForeignKey(Gemeente, verbose_name="Binnengekomen uit", null=True, db_column='idBinnengekomenUitGemeente', blank=True, related_name='Binnengekomen') # Field name made lowercase.
    dtmdatumvertrek = models.DateField("Datum vertrek", null=True, db_column='dtmDatumVertrek', blank=True) # Field name made lowercase.
    idvertrokkennaargemeente = models.ForeignKey(Gemeente, verbose_name="Vertrokken naar", null=True, db_column='idVertrokkenNaarGemeente', blank=True, related_name='Vertrokken') # Field name made lowercase.
    txttelefoonnummer = models.CharField("Telefoon", max_length=75, db_column='txtTelefoonNummer', blank=True) # Field name made lowercase.
    txtemailadres = models.CharField("E-mailadres", max_length=150, db_column='txtEmailAdres', blank=True) # Field name made lowercase.
    dtmdatumhuwelijksbevestiging = models.DateField("Datum huwelijksbevestiging", null=True, db_column='dtmDatumHuwelijksbevestiging', blank=True) # Field name made lowercase.
    txtopmerking = models.TextField("Opmerkingen", max_length=765, db_column='txtOpmerking', blank=True) # Field name made lowercase.
    dtmoverlijdensdatum = models.DateField("Datum overlijden", null=True, db_column='dtmOverlijdensdatum', blank=True) # Field name made lowercase.
    dtmdatumonttrokken = models.DateField("Datum onttrekking", null=True, db_column='dtmDatumOnttrokken', blank=True) # Field name made lowercase.
    boolactief = MySQLBooleanField("Actief", db_column='boolActief', default=True) # Field name made lowercase. This field type is a guess.
    idwijk = models.ForeignKey(Wijk, verbose_name="Wijk", null=True, blank=True, db_column='idWijk') # Field name made lowercase.
    idgastgemeente = models.ForeignKey(Gemeente, verbose_name="Gastgemeente", null=True, blank=True, db_column='idGastGemeente', related_name='Gastlid') # Field name made lowercase.
    idgasthoofdgemeente = models.ForeignKey(Gemeente, verbose_name="Gasthoofdgemeente", null=True, blank=True, db_column='idGastHoofdGemeente', related_name='Gastlid_hoofd') # Field name made lowercase.
    boolgastlidnw = MySQLBooleanField("Gastlid Noord-West", db_column='boolGastlidNW') # Field name made lowercase. This field type is a guess.
    boolgeborennw = MySQLBooleanField("Geboren in Noord-West", db_column='boolGeborenNW') # Field name made lowercase. This field type is a guess.

    def __unicode__(self):
        return ("%s %s") % (("%s %s" % (self.txtroepnaam, self.txttussenvoegsels)).strip(), self.txtachternaam)
    
    class Meta:
        db_table = u'ledendb_personen'
        ordering = ['txtachternaam']

