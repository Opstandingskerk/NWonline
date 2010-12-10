###############################################################################
# File: NWonline/KB/admin.py
# Author: Lukas Batteau
# Description: ModelAdmin classes customizing admin default behaviour 
# 
# CHANGE HISTORY  
# 20101209    Lukas Batteau        Added header.
###############################################################################
from NWonline.KB.models import GemeenteType, Gemeente, Geslacht, \
    GezinsRol, LidmaatschapStatus, Wijk, Huiskring, HuiskringLidRol, Land, Persoon, \
    Gezin
from django.contrib import admin

admin.site.register(GemeenteType)
admin.site.register(Gemeente)
admin.site.register(Geslacht)
admin.site.register(GezinsRol)
admin.site.register(LidmaatschapStatus)
admin.site.register(Wijk)
admin.site.register(Huiskring)
admin.site.register(HuiskringLidRol)
admin.site.register(Land)

class PersoonAdmin(admin.ModelAdmin):
    list_display = ('txtachternaam',
                    'txttussenvoegsels',
                    'txtvoorletters',
                    'txtroepnaam',
                    'dtmgeboortedatum',
                    'idgezin',
                    'idlidmaatschapstatus',
                    'idwijk',
                    )
    search_fields = ['txtachternaam', 'txtroepnaam']
    list_filter = ['idlidmaatschapstatus',
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
                       'boolactief'),
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

