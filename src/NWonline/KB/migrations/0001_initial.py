# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GemeenteType'
        db.create_table(u'ledendb_gemeentetypes', (
            ('idgemeentetype', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idGemeenteType')),
            ('txtgemeentetype', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtGemeenteType')),
        ))
        db.send_create_signal('KB', ['GemeenteType'])

        # Adding model 'Gemeente'
        db.create_table(u'ledendb_gemeenten', (
            ('idgemeente', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idGemeente')),
            ('txtgemeentenaam', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtGemeenteNaam', blank=True)),
            ('idgemeentetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.GemeenteType'], null=True, db_column='idGemeenteType', blank=True)),
            ('txtopmerking', self.gf('django.db.models.fields.TextField')(max_length=765, null=True, db_column='txtOpmerking', blank=True)),
        ))
        db.send_create_signal('KB', ['Gemeente'])

        # Adding model 'Geslacht'
        db.create_table(u'ledendb_geslachten', (
            ('idgeslacht', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idGeslacht')),
            ('txtgeslacht', self.gf('django.db.models.fields.CharField')(max_length=3, db_column='txtGeslacht', blank=True)),
            ('txtgeslachtlang', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtGeslachtLang', blank=True)),
            ('txtaanhef', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtAanhef', blank=True)),
            ('txtaanhefkort', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtAanhefKort', blank=True)),
            ('txtaanhefkerk', self.gf('django.db.models.fields.CharField')(max_length=135, db_column='txtAanhefKerk', blank=True)),
            ('txtaanhefkerkkort', self.gf('django.db.models.fields.CharField')(max_length=135, db_column='txtAanhefKerkKort', blank=True)),
        ))
        db.send_create_signal('KB', ['Geslacht'])

        # Adding model 'Land'
        db.create_table(u'ledendb_landen', (
            ('idland', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idLand')),
            ('txtlandnaam', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='txtLandnaam', blank=True)),
        ))
        db.send_create_signal('KB', ['Land'])

        # Adding model 'Gezin'
        db.create_table(u'ledendb_gezinnen', (
            ('idgezin', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idGezin')),
            ('txtgezinsnaam', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtGezinsnaam', db_index=True)),
            ('txtstraatnaam', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, db_column='txtStraatnaam', blank=True)),
            ('inthuisnummer', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='intHuisnummer', blank=True)),
            ('txthuisnummertoevoeging', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, db_column='txtHuisnummerToevoeging', blank=True)),
            ('txtpostcode', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, db_column='txtPostcode', blank=True)),
            ('txtplaats', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, db_column='txtPlaats', blank=True)),
            ('idland', self.gf('django.db.models.fields.related.ForeignKey')(default=149, to=orm['KB.Land'], null=True, db_column='idLand', blank=True)),
            ('txttelefoon', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=75, null=True, db_column='txtTelefoon', blank=True)),
            ('txtopmerking', self.gf('django.db.models.fields.TextField')(max_length=765, null=True, db_column='txtOpmerking', blank=True)),
        ))
        db.send_create_signal('KB', ['Gezin'])

        # Adding model 'GezinsRol'
        db.create_table(u'ledendb_gezinsrollen', (
            ('idgezinsrol', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idGezinsrol')),
            ('txtgezinsrol', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtGezinsrol', blank=True)),
        ))
        db.send_create_signal('KB', ['GezinsRol'])

        # Adding model 'Wijk'
        db.create_table(u'ledendb_wijken', (
            ('idwijk', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idWijk')),
            ('txtwijknaam', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtWijkNaam')),
            ('txtwijknaamkort', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, db_column='txtWijkNaamKort', blank=True)),
        ))
        db.send_create_signal('KB', ['Wijk'])

        # Adding model 'Huiskring'
        db.create_table(u'ledendb_huiskringen', (
            ('idhuiskring', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idHuiskring')),
            ('txthuiskringnaam', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtHuiskringNaam')),
            ('idwijk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.Wijk'], db_column='idWijk')),
            ('txtopmerking', self.gf('django.db.models.fields.TextField')(max_length=765, db_column='txtOpmerking', blank=True)),
            ('txtvolgnummer', self.gf('django.db.models.fields.CharField')(max_length=6, db_column='txtVolgnummer', blank=True)),
        ))
        db.send_create_signal('KB', ['Huiskring'])

        # Adding model 'HuiskringLidRol'
        db.create_table(u'ledendb_huiskringlidrollen', (
            ('idhuiskringlidrol', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idHuiskringLidrol')),
            ('txthuiskringlidrol', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtHuiskringLidrol')),
        ))
        db.send_create_signal('KB', ['HuiskringLidRol'])

        # Adding model 'LidmaatschapVorm'
        db.create_table(u'ledendb_lidmaatschapvormen', (
            ('idlidmaatschapvorm', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idLidmaatschapvorm')),
            ('txtlidmaatschapvorm', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtLidmaatschapvorm', blank=True)),
            ('boolvoorquotum', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='boolVoorQuotum')),
            ('txtlidmaatschapvormkort', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtLidmaatschapvormKort', blank=True)),
            ('txtattestatie', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtAttestatie', blank=True)),
        ))
        db.send_create_signal('KB', ['LidmaatschapVorm'])

        # Adding model 'LidmaatschapStatus'
        db.create_table(u'ledendb_lidmaatschapstatussen', (
            ('idlidmaatschapstatus', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idLidmaatschapstatus')),
            ('txtlidmaatschapstatus', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtLidmaatschapstatus', blank=True)),
        ))
        db.send_create_signal('KB', ['LidmaatschapStatus'])

        # Adding model 'Attestatie'
        db.create_table('KB_attestatie', (
            ('idattestatie', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('txtcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('txtbeschrijving', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('KB', ['Attestatie'])

        # Adding model 'Persoon'
        db.create_table(u'ledendb_personen', (
            ('idpersoon', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='idPersoon')),
            ('idlidmaatschapvorm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.LidmaatschapVorm'], db_column='idLidmaatschapVorm')),
            ('idgezin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.Gezin'], null=True, db_column='idGezin', blank=True)),
            ('idgezinsrol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.GezinsRol'], db_column='idGezinsRol')),
            ('txtachternaam', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='txtAchternaam', db_index=True)),
            ('txttussenvoegsels', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtTussenvoegsels', blank=True)),
            ('txtvoorletters', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtVoorletters', blank=True)),
            ('txtdoopnaam', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, db_column='txtDoopnaam', blank=True)),
            ('txtroepnaam', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtRoepnaam', db_index=True)),
            ('boolaansprekenmetroepnaam', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='boolAansprekenMetRoepnaam')),
            ('dtmgeboortedatum', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmGeboortedatum', blank=True)),
            ('txtgeboorteplaats', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtGeboorteplaats', blank=True)),
            ('idgeslacht', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.Geslacht'], null=True, db_column='idGeslacht', blank=True)),
            ('dtmdatumdoop', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmDatumDoop', blank=True)),
            ('iddoopgemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Gedoopt', null=True, db_column='idDoopgemeente', to=orm['KB.Gemeente'])),
            ('dtmdatumbelijdenis', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmDatumBelijdenis', blank=True)),
            ('idbelijdenisgemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Belijdenis', null=True, db_column='idBelijdenisgemeente', to=orm['KB.Gemeente'])),
            ('dtmhuwelijksdatum', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmHuwelijksDatum', blank=True)),
            ('idhuwelijksgemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Gehuwd', null=True, db_column='idHuwelijksGemeente', to=orm['KB.Gemeente'])),
            ('dtmdatumbinnenkomst', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmDatumBinnenkomst', blank=True)),
            ('idbinnengekomenuitgemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Binnengekomen', null=True, db_column='idBinnengekomenUitGemeente', to=orm['KB.Gemeente'])),
            ('dtmdatumvertrek', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmDatumVertrek', blank=True)),
            ('idvertrokkennaargemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Vertrokken', null=True, db_column='idVertrokkenNaarGemeente', to=orm['KB.Gemeente'])),
            ('txttelefoonnummer', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, db_column='txtTelefoonNummer', blank=True)),
            ('txtemailadres', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtEmailAdres', blank=True)),
            ('dtmdatumhuwelijksbevestiging', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmDatumHuwelijksbevestiging', blank=True)),
            ('txtopmerking', self.gf('django.db.models.fields.TextField')(max_length=765, null=True, db_column='txtOpmerking', blank=True)),
            ('dtmoverlijdensdatum', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmOverlijdensdatum', blank=True)),
            ('dtmdatumonttrokken', self.gf('django.db.models.fields.DateField')(null=True, db_column='dtmDatumOnttrokken', blank=True)),
            ('idlidmaatschapstatus', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['KB.LidmaatschapStatus'], null=True, db_column='idLidmaatschapStatus')),
            ('idwijk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.Wijk'], null=True, db_column='idWijk', blank=True)),
            ('idgastgemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Gastlid', null=True, db_column='idGastGemeente', to=orm['KB.Gemeente'])),
            ('idgasthoofdgemeente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Gastlid_hoofd', null=True, db_column='idGastHoofdGemeente', to=orm['KB.Gemeente'])),
            ('boolgastlidnw', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='boolGastlidNW')),
            ('boolgastlidelders', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='boolGastlidElders')),
            ('boolgeborennw', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='boolGeborenNW')),
            ('idhuiskring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.Huiskring'], null=True, db_column='idHuiskring', blank=True)),
            ('idhuiskringlidrol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['KB.HuiskringLidRol'], null=True, db_column='idHuiskringRol', blank=True)),
        ))
        db.send_create_signal('KB', ['Persoon'])

        # Adding model 'tblHuishouden'
        db.create_table(u'tblHuishouden', (
            ('idHuishouden', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('txtHuishoudenNaam', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('txtTelefoonnummer', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('txtStraatnaam', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('txtHuisnummer', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('txtPostcode', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('txtPlaats', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal('KB', ['tblHuishouden'])

        # Adding model 'tblLid'
        db.create_table(u'tblLid', (
            ('idLid', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='idLid')),
            ('ysnLid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('idHuishouden', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('idRol', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('txtAchternaam', self.gf('django.db.models.fields.CharField')(max_length=150, db_index=True)),
            ('txtVoorvoegsels', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('txtVoorletters', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('txtDoopnaam', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True)),
            ('txtRoepnaam', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, db_column='txtRoepnaam', db_index=True)),
            ('ysnRoepnaam', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dtmGeboortedatum', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('txtGeboorteplaats', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('txtGeslacht', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('idStatus', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('dtmDoop', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('idDoopgemeente', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dtmBelijdenis', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('idBelijdenisgemeente', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dtmBinnenkomst', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('idVorigeGemeente', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dtmVertrokken', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('idVolgendeGemeente', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('txtMobielNummer', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('ysnMobielNummer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('txtEmailAdres', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('ysnEmailAdres', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('txtAantekeningen', self.gf('django.db.models.fields.TextField')(max_length=765, null=True, blank=True)),
            ('dtmTrouwdatum', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('idTrouwgemeente', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dtmTrouwbevestiging', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('idHuiskring', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('idHuiskringLidType', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('huiskringwijk', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('KB', ['tblLid'])


    def backwards(self, orm):
        
        # Deleting model 'GemeenteType'
        db.delete_table(u'ledendb_gemeentetypes')

        # Deleting model 'Gemeente'
        db.delete_table(u'ledendb_gemeenten')

        # Deleting model 'Geslacht'
        db.delete_table(u'ledendb_geslachten')

        # Deleting model 'Land'
        db.delete_table(u'ledendb_landen')

        # Deleting model 'Gezin'
        db.delete_table(u'ledendb_gezinnen')

        # Deleting model 'GezinsRol'
        db.delete_table(u'ledendb_gezinsrollen')

        # Deleting model 'Wijk'
        db.delete_table(u'ledendb_wijken')

        # Deleting model 'Huiskring'
        db.delete_table(u'ledendb_huiskringen')

        # Deleting model 'HuiskringLidRol'
        db.delete_table(u'ledendb_huiskringlidrollen')

        # Deleting model 'LidmaatschapVorm'
        db.delete_table(u'ledendb_lidmaatschapvormen')

        # Deleting model 'LidmaatschapStatus'
        db.delete_table(u'ledendb_lidmaatschapstatussen')

        # Deleting model 'Attestatie'
        db.delete_table('KB_attestatie')

        # Deleting model 'Persoon'
        db.delete_table(u'ledendb_personen')

        # Deleting model 'tblHuishouden'
        db.delete_table(u'tblHuishouden')

        # Deleting model 'tblLid'
        db.delete_table(u'tblLid')


    models = {
        'KB.attestatie': {
            'Meta': {'object_name': 'Attestatie'},
            'idattestatie': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'txtbeschrijving': ('django.db.models.fields.TextField', [], {}),
            'txtcode': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'KB.gemeente': {
            'Meta': {'ordering': "['txtgemeentenaam']", 'object_name': 'Gemeente', 'db_table': "u'ledendb_gemeenten'"},
            'idgemeente': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idGemeente'"}),
            'idgemeentetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.GemeenteType']", 'null': 'True', 'db_column': "'idGemeenteType'", 'blank': 'True'}),
            'txtgemeentenaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtGemeenteNaam'", 'blank': 'True'}),
            'txtopmerking': ('django.db.models.fields.TextField', [], {'max_length': '765', 'null': 'True', 'db_column': "'txtOpmerking'", 'blank': 'True'})
        },
        'KB.gemeentetype': {
            'Meta': {'object_name': 'GemeenteType', 'db_table': "u'ledendb_gemeentetypes'"},
            'idgemeentetype': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idGemeenteType'"}),
            'txtgemeentetype': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtGemeenteType'"})
        },
        'KB.geslacht': {
            'Meta': {'object_name': 'Geslacht', 'db_table': "u'ledendb_geslachten'"},
            'idgeslacht': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idGeslacht'"}),
            'txtaanhef': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtAanhef'", 'blank': 'True'}),
            'txtaanhefkerk': ('django.db.models.fields.CharField', [], {'max_length': '135', 'db_column': "'txtAanhefKerk'", 'blank': 'True'}),
            'txtaanhefkerkkort': ('django.db.models.fields.CharField', [], {'max_length': '135', 'db_column': "'txtAanhefKerkKort'", 'blank': 'True'}),
            'txtaanhefkort': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtAanhefKort'", 'blank': 'True'}),
            'txtgeslacht': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "'txtGeslacht'", 'blank': 'True'}),
            'txtgeslachtlang': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtGeslachtLang'", 'blank': 'True'})
        },
        'KB.gezin': {
            'Meta': {'object_name': 'Gezin', 'db_table': "u'ledendb_gezinnen'"},
            'idgezin': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idGezin'"}),
            'idland': ('django.db.models.fields.related.ForeignKey', [], {'default': '149', 'to': "orm['KB.Land']", 'null': 'True', 'db_column': "'idLand'", 'blank': 'True'}),
            'inthuisnummer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'intHuisnummer'", 'blank': 'True'}),
            'txtgezinsnaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtGezinsnaam'", 'db_index': 'True'}),
            'txthuisnummertoevoeging': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'db_column': "'txtHuisnummerToevoeging'", 'blank': 'True'}),
            'txtopmerking': ('django.db.models.fields.TextField', [], {'max_length': '765', 'null': 'True', 'db_column': "'txtOpmerking'", 'blank': 'True'}),
            'txtplaats': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'db_column': "'txtPlaats'", 'blank': 'True'}),
            'txtpostcode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'db_column': "'txtPostcode'", 'blank': 'True'}),
            'txtstraatnaam': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'db_column': "'txtStraatnaam'", 'blank': 'True'}),
            'txttelefoon': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '75', 'null': 'True', 'db_column': "'txtTelefoon'", 'blank': 'True'})
        },
        'KB.gezinsrol': {
            'Meta': {'object_name': 'GezinsRol', 'db_table': "u'ledendb_gezinsrollen'"},
            'idgezinsrol': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idGezinsrol'"}),
            'txtgezinsrol': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtGezinsrol'", 'blank': 'True'})
        },
        'KB.huiskring': {
            'Meta': {'object_name': 'Huiskring', 'db_table': "u'ledendb_huiskringen'"},
            'idhuiskring': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idHuiskring'"}),
            'idwijk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.Wijk']", 'db_column': "'idWijk'"}),
            'txthuiskringnaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtHuiskringNaam'"}),
            'txtopmerking': ('django.db.models.fields.TextField', [], {'max_length': '765', 'db_column': "'txtOpmerking'", 'blank': 'True'}),
            'txtvolgnummer': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_column': "'txtVolgnummer'", 'blank': 'True'})
        },
        'KB.huiskringlidrol': {
            'Meta': {'object_name': 'HuiskringLidRol', 'db_table': "u'ledendb_huiskringlidrollen'"},
            'idhuiskringlidrol': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idHuiskringLidrol'"}),
            'txthuiskringlidrol': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtHuiskringLidrol'"})
        },
        'KB.land': {
            'Meta': {'ordering': "['txtlandnaam']", 'object_name': 'Land', 'db_table': "u'ledendb_landen'"},
            'idland': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idLand'"}),
            'txtlandnaam': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'txtLandnaam'", 'blank': 'True'})
        },
        'KB.lidmaatschapstatus': {
            'Meta': {'object_name': 'LidmaatschapStatus', 'db_table': "u'ledendb_lidmaatschapstatussen'"},
            'idlidmaatschapstatus': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idLidmaatschapstatus'"}),
            'txtlidmaatschapstatus': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtLidmaatschapstatus'", 'blank': 'True'})
        },
        'KB.lidmaatschapvorm': {
            'Meta': {'object_name': 'LidmaatschapVorm', 'db_table': "u'ledendb_lidmaatschapvormen'"},
            'boolvoorquotum': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'boolVoorQuotum'"}),
            'idlidmaatschapvorm': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idLidmaatschapvorm'"}),
            'txtattestatie': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtAttestatie'", 'blank': 'True'}),
            'txtlidmaatschapvorm': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtLidmaatschapvorm'", 'blank': 'True'}),
            'txtlidmaatschapvormkort': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtLidmaatschapvormKort'", 'blank': 'True'})
        },
        'KB.persoon': {
            'Meta': {'ordering': "['txtachternaam']", 'object_name': 'Persoon', 'db_table': "u'ledendb_personen'"},
            'boolaansprekenmetroepnaam': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'boolAansprekenMetRoepnaam'"}),
            'boolgastlidelders': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'boolGastlidElders'"}),
            'boolgastlidnw': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'boolGastlidNW'"}),
            'boolgeborennw': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'boolGeborenNW'"}),
            'dtmdatumbelijdenis': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmDatumBelijdenis'", 'blank': 'True'}),
            'dtmdatumbinnenkomst': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmDatumBinnenkomst'", 'blank': 'True'}),
            'dtmdatumdoop': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmDatumDoop'", 'blank': 'True'}),
            'dtmdatumhuwelijksbevestiging': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmDatumHuwelijksbevestiging'", 'blank': 'True'}),
            'dtmdatumonttrokken': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmDatumOnttrokken'", 'blank': 'True'}),
            'dtmdatumvertrek': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmDatumVertrek'", 'blank': 'True'}),
            'dtmgeboortedatum': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmGeboortedatum'", 'blank': 'True'}),
            'dtmhuwelijksdatum': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmHuwelijksDatum'", 'blank': 'True'}),
            'dtmoverlijdensdatum': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'dtmOverlijdensdatum'", 'blank': 'True'}),
            'idbelijdenisgemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Belijdenis'", 'null': 'True', 'db_column': "'idBelijdenisgemeente'", 'to': "orm['KB.Gemeente']"}),
            'idbinnengekomenuitgemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Binnengekomen'", 'null': 'True', 'db_column': "'idBinnengekomenUitGemeente'", 'to': "orm['KB.Gemeente']"}),
            'iddoopgemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Gedoopt'", 'null': 'True', 'db_column': "'idDoopgemeente'", 'to': "orm['KB.Gemeente']"}),
            'idgastgemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Gastlid'", 'null': 'True', 'db_column': "'idGastGemeente'", 'to': "orm['KB.Gemeente']"}),
            'idgasthoofdgemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Gastlid_hoofd'", 'null': 'True', 'db_column': "'idGastHoofdGemeente'", 'to': "orm['KB.Gemeente']"}),
            'idgeslacht': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.Geslacht']", 'null': 'True', 'db_column': "'idGeslacht'", 'blank': 'True'}),
            'idgezin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.Gezin']", 'null': 'True', 'db_column': "'idGezin'", 'blank': 'True'}),
            'idgezinsrol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.GezinsRol']", 'db_column': "'idGezinsRol'"}),
            'idhuiskring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.Huiskring']", 'null': 'True', 'db_column': "'idHuiskring'", 'blank': 'True'}),
            'idhuiskringlidrol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.HuiskringLidRol']", 'null': 'True', 'db_column': "'idHuiskringRol'", 'blank': 'True'}),
            'idhuwelijksgemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Gehuwd'", 'null': 'True', 'db_column': "'idHuwelijksGemeente'", 'to': "orm['KB.Gemeente']"}),
            'idlidmaatschapstatus': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['KB.LidmaatschapStatus']", 'null': 'True', 'db_column': "'idLidmaatschapStatus'"}),
            'idlidmaatschapvorm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.LidmaatschapVorm']", 'db_column': "'idLidmaatschapVorm'"}),
            'idpersoon': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idPersoon'"}),
            'idvertrokkennaargemeente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Vertrokken'", 'null': 'True', 'db_column': "'idVertrokkenNaarGemeente'", 'to': "orm['KB.Gemeente']"}),
            'idwijk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['KB.Wijk']", 'null': 'True', 'db_column': "'idWijk'", 'blank': 'True'}),
            'txtachternaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtAchternaam'", 'db_index': 'True'}),
            'txtdoopnaam': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'db_column': "'txtDoopnaam'", 'blank': 'True'}),
            'txtemailadres': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtEmailAdres'", 'blank': 'True'}),
            'txtgeboorteplaats': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtGeboorteplaats'", 'blank': 'True'}),
            'txtopmerking': ('django.db.models.fields.TextField', [], {'max_length': '765', 'null': 'True', 'db_column': "'txtOpmerking'", 'blank': 'True'}),
            'txtroepnaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtRoepnaam'", 'db_index': 'True'}),
            'txttelefoonnummer': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'db_column': "'txtTelefoonNummer'", 'blank': 'True'}),
            'txttussenvoegsels': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtTussenvoegsels'", 'blank': 'True'}),
            'txtvoorletters': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtVoorletters'", 'blank': 'True'})
        },
        'KB.tblhuishouden': {
            'Meta': {'object_name': 'tblHuishouden', 'db_table': "u'tblHuishouden'"},
            'idHuishouden': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'txtHuishoudenNaam': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'txtHuisnummer': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'txtPlaats': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtPostcode': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'txtStraatnaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtTelefoonnummer': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        'KB.tbllid': {
            'Meta': {'object_name': 'tblLid', 'db_table': "u'tblLid'"},
            'dtmBelijdenis': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtmBinnenkomst': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtmDoop': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtmGeboortedatum': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtmTrouwbevestiging': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtmTrouwdatum': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtmVertrokken': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'huiskringwijk': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idBelijdenisgemeente': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idDoopgemeente': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idHuishouden': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idHuiskring': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idHuiskringLidType': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idLid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'idLid'"}),
            'idRol': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idStatus': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'idTrouwgemeente': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idVolgendeGemeente': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'idVorigeGemeente': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'txtAantekeningen': ('django.db.models.fields.TextField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'txtAchternaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'txtDoopnaam': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtEmailAdres': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtGeboorteplaats': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtGeslacht': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtMobielNummer': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'txtRoepnaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'db_column': "'txtRoepnaam'", 'db_index': 'True'}),
            'txtVoorletters': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'txtVoorvoegsels': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'ysnEmailAdres': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ysnLid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ysnMobielNummer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ysnRoepnaam': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'KB.wijk': {
            'Meta': {'object_name': 'Wijk', 'db_table': "u'ledendb_wijken'"},
            'idwijk': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'idWijk'"}),
            'txtwijknaam': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'txtWijkNaam'"}),
            'txtwijknaamkort': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'db_column': "'txtWijkNaamKort'", 'blank': 'True'})
        }
    }

    complete_apps = ['KB']
