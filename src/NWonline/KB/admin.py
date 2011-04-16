###############################################################################
# File: NWonline/KB/admin.py
# Author: Lukas Batteau
# Description: ModelAdmin classes customizing admin default behaviour 
# 
# CHANGE HISTORY  
# 20101209    Lukas Batteau        Added header.
# 20110329    Lukas Batteau        Reorganized persoon membership
###############################################################################
from NWonline.KB.models import GemeenteType, Gemeente, Geslacht, GezinsRol, \
    LidmaatschapVorm, Wijk, Huiskring, HuiskringLidRol, Land, Persoon, Gezin, \
    LidmaatschapStatus, Attestatie
from django.contrib import admin

admin.site.register(GemeenteType)
admin.site.register(Gemeente)
admin.site.register(Geslacht)
admin.site.register(GezinsRol)
admin.site.register(LidmaatschapVorm)
admin.site.register(LidmaatschapStatus)
admin.site.register(Wijk)
admin.site.register(Huiskring)
admin.site.register(HuiskringLidRol)
admin.site.register(Land)
admin.site.register(Attestatie)

class PersoonAdmin(admin.ModelAdmin):
    list_display = ('txtachternaam',
                    'txttussenvoegsels',
                    'txtvoorletters',
                    'txtroepnaam',
                    'dtmgeboortedatum',
                    'idgezin',
                    'idlidmaatschapstatus',
                    'idlidmaatschapvorm',
                    'idwijk',
                    )
    search_fields = ['txtachternaam', 'txtroepnaam']
    list_filter = ['idlidmaatschapstatus',
                   'idlidmaatschapvorm',
                   'idwijk']
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('txtachternaam',
                       'txttussenvoegsels',
                       'idgeslacht'),
                       ('txtvoorletters',
                       'txtdoopnaam'),
                       ('txtroepnaam',
                       'boolaansprekenmetroepnaam'),
                       ('dtmgeboortedatum',
                       'txtgeboorteplaats'),
                       'txtopmerking',
                       )
        }),
        ('Lidmaatschap', {
            'classes': ('collapse','wide',),
            'fields': (('idlidmaatschapstatus',
                       'idlidmaatschapvorm'),
                       'idwijk',
                       'boolgeborennw',
                       ('boolgastlidnw',
                       'idgasthoofdgemeente'),
                        'idgastgemeente',)
        }),
        ('Gezin', {
            'classes': ('collapse','wide',),
            'fields': ('idgezin', 'idgezinsrol')
        }),
        ('Historie', {
            'classes': ('collapse','wide',),
            'fields': (('dtmdatumdoop',
                       'iddoopgemeente'),
                       ('dtmdatumbelijdenis',
                       'idbelijdenisgemeente'),
                       ('dtmhuwelijksdatum',
                       'dtmdatumhuwelijksbevestiging',
                       'idhuwelijksgemeente'),
                       ('dtmdatumbinnenkomst',
                       'idbinnengekomenuitgemeente'),
                       ('dtmdatumvertrek',
                       'idvertrokkennaargemeente'),
                       'dtmoverlijdensdatum',
                       'dtmdatumonttrokken',
                       )
        }),
    )


admin.site.register(Persoon, PersoonAdmin)

class GezinAdmin(admin.ModelAdmin):
    list_display = ('txtgezinsnaam',
                    'txtstraatnaam',
                    'inthuisnummer',
                    'txthuisnummertoevoeging',
                    'txtpostcode',
                    'txtplaats',
                    'idland',
                    'txttelefoon',
                    )
    search_fields = ['txtgezinsnaam', 'txtstraatnaam', 'txttelefoon']
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('txtgezinsnaam',
                       ('txtstraatnaam',
                       'inthuisnummer',
                       'txthuisnummertoevoeging'),
                       ('txtpostcode',
                       'txtplaats',
                       'idland'),
                       'txttelefoon',
                       'txtopmerking',
                       )
        }),
    )

admin.site.register(Gezin, GezinAdmin)

