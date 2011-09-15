# -*- coding: iso-8859-15 -*-
import logging
import os
import pyodbc
import re
import simplejson
import string
import sys
import tempfile

MDB = 'leden.mdb'
DRV = '{Microsoft Access Driver (*.mdb)}'
PWD = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fh = logging.FileHandler('log.txt', mode = 'w')
fh.setLevel(logging.WARNING)

logger.addHandler(ch)
logger.addHandler(fh)



def get_geslacht_id(txtGeslacht):
    if txtGeslacht == 'M':
        return 1
    if txtGeslacht == 'V':
        return 2

def none_safe_string(txt_object):
    if txt_object is None:
        return ""
    else:
        return txt_object
        
def create_lid_label(lid):
    return "%s - %s %s %s" % (lid.idLid, lid.txtAchternaam, none_safe_string(lid.txtVoorvoegsels), lid.txtVoorletters)

def main():
    conn = pyodbc.connect('DRIVER=%s;DBQ=%s;PWD=%s' % (DRV,MDB,PWD))
    curs = conn.cursor()

    result = []
    
    logger.info("Converting tblGemeente")           
    curs.execute("select * from tblGemeente")        
    for gemeente in curs.fetchall():        
        opmerkingen = ""
        if gemeente.txtAdresKerkelijkBureau is not None:
            opmerkingen += gemeente.txtAdresKerkelijkBureau
        if gemeente.txtAdresKerkenraadRegel1 is not None:
            opmerkingen += ", "
            opmerkingen += gemeente.txtAdresKerkenraadRegel1
        if gemeente.txtAdresKerkenraadRegel2 is not None:
            opmerkingen += ", "
            opmerkingen += gemeente.txtAdresKerkenraadRegel2
        if gemeente.txtAdresKerkenraadRegel3 is not None:
            opmerkingen += ", "
            opmerkingen += gemeente.txtAdresKerkenraadRegel3
            
                        
        community = {
            "pk": gemeente.idGemeente,
            "model": "KB.gemeente",
            "fields": {
                "idgemeente": gemeente.idGemeente,
                "txtgemeentenaam": none_safe_string(gemeente.txtGemeenteNaam),
                "idgemeentetype": "1",
                "txtopmerking": none_safe_string(opmerkingen)
            }
        }
        result.append(community)
    
    
    logger.info("Converting tblGezinsRol")           
    curs.execute("select * from tblGezinsRol")
    for gezinsrol in curs.fetchall():               
        family_role = {
            "pk": gezinsrol.idGezinsRol,
            "model": "KB.gezinsrol",
            "fields": {
                "idgezinsrol": gezinsrol.idGezinsRol,
                "txtgezinsrol": none_safe_string(gezinsrol.txtRolBeschrijving)
            }
        }
        result.append(family_role)
    
    
    logger.info("Tabel Gezin")           
    curs.execute("select * from tblGezin")
    for gezin in  curs.fetchall():                
        if gezin.idAdres is not None:
            temp_cursor = conn.cursor()
            temp_cursor.execute("select * from tblAdres where idAdres=" +str(gezin.idAdres))
            gezinsadres = temp_cursor.fetchone()
            temp_cursor.close()
            
            if gezinsadres.txtHuisnummer is not None:
                m = re.match(r"(?P<huisnummer>[0-9]*)(?P<toevoeging>.*)", gezinsadres.txtHuisnummer)
                match_huisnummer = m.group('huisnummer')
                match_toevoeging = m.group('toevoeging')
                if match_huisnummer == '':
                    logger.warn('Gezin heeft geen huisnummer: %s - %s', str(gezin.idGezin), gezin.txtGezinsnaam)
                    match_huisnummer = -999
            else:
                logger.warn('Gezin heeft geen huisnummer: %s - %s', str(gezin.idGezin), gezin.txtGezinsnaam)
                match_huisnummer = -999
                match_toevoeging = ""
            
            txtStraatnaam = gezinsadres.txtStraatnaam            
            txtPostcode = gezinsadres.txtPostcode
            txtPlaats = gezinsadres.txtPlaats
            txtAdresExtra = gezinsadres.txtAdresExtra
            
            if none_safe_string(txtPostcode)!="":
                check_postcode = re.findall(r"(^[0-9]{4}[a-z|A-Z]{2}$)", txtPostcode)
                if len(check_postcode)!=1:
                    logger.warn("Gezin komt waarschijnlijk niet uit Nederland, handmatig controleren voor gezin: %s - %s", str(gezin.idGezin), gezin.txtGezinsnaam)
            else:
                logger.warn("Gezin heeft geen postcode: %s - %s", str(gezin.idGezin), gezin.txtGezinsnaam) 
            if none_safe_string(txtStraatnaam)=="":
                logger.warn("Gezin heeft geen straatnaam: %s - %s", str(gezin.idGezin), gezin.txtGezinsnaam) 
            if none_safe_string(txtPlaats)=="":
                logger.warn("Gezin heeft geen plaats: %s - %s", str(gezin.idGezin), gezin.txtGezinsnaam) 
                              
        else:
            logger.warn('Geen adres gevonden voor gezin: %s - %s', str(gezin.idGezin), gezin.txtGezinsnaam)
            match_huisnummer = -999
            match_toevoeging = "" 
            txtStraatnaam = ""
            txtPostcode = ""
            txtPlaats = ""
            txtAdresExtra = ""
            
                   
        family = {
            "pk": gezin.idGezin,
            "model": "KB.gezin",
            "fields": {
                "idgezin": gezin.idGezin,
                "txtgezinsnaam": gezin.txtGezinsnaam,
                "txtstraatnaam": none_safe_string(txtStraatnaam),
                "inthuisnummer": match_huisnummer,
                "txthuisnummertoevoeging": none_safe_string(match_toevoeging),
                "txtpostcode": none_safe_string(txtPostcode),
                "txtplaats": none_safe_string(txtPlaats),
                "idland": "149",
                "txttelefoon": none_safe_string(gezin.txtTelefoonnummer),
                "txtopmerking": none_safe_string(txtAdresExtra)
            }
        }
        result.append(family)
     
    logger.info("Converting tblLid")    
    curs.execute("select * from tblLid")
    
    nrOfBelijdend = 0
    nrOfDoop = 0
    nrOfBelijdendElders = 0
    nrOfDoopElders = 0
    for lid in curs.fetchall():                
        # Als persoon vertrokken is dan krijgt hij de status 2 = Vertrokken
        # tenzij hij naar gemeente id 338 (=onttrokken) of id 339 (=overleden) gaat
        if (lid.idLid in (300,)):#, 632, 1480, 1392, 1419, 1436, 1481, 1485, 1497, 518)):
            logger.warn("Lid overgeslagen bij importeren: %s" % (lid))
            continue
        
        id_wijk = lid.huiskringwijk
        if id_wijk is None or id_wijk==0:
            logger.warn("Lid heeft geen wijknummer, nu 11 (Overig) gegeven: %s", create_lid_label(lid))
            id_wijk = 11
        
        dtm_onttrokken = None
        dtm_overleden = None
        dtm_vertrokken = None
        id_vlg_gemeente = None
        if lid.dtmVertrokken is not None:
            if lid.idVolgendeGemeente == 338:
                ls_status = 3
                dtm_onttrokken = lid.dtmVertrokken.strftime("%Y-%m-%d") if lid.dtmVertrokken else None                             
            elif lid.idVolgendeGemeente == 339:
                ls_status = 4
                dtm_overleden = lid.dtmVertrokken.strftime("%Y-%m-%d") if lid.dtmVertrokken else None 
            else:    
                ls_status = 2
                dtm_vertrokken = lid.dtmVertrokken.strftime("%Y-%m-%d") if lid.dtmVertrokken else None 
                id_vlg_gemeente = lid.idVolgendeGemeente
            if lid.ysnLid == True:
                ls_status = 1
                logger.warn("Lid lijkt vertrokken (heeft vertrokken datum) maar is nog wel aangemerkt als lid: %s - %s", lid.idLid, lid.txtAchternaam)                  
        else:        
            ls_status = 1            
            if lid.ysnLid == False:
                ls_status = 2
                logger.warn("Lid is niet vetrokken, maar is ook geen lid meer: %s", create_lid_label(lid))    

        ## De status van het lid bepalen
        gastgemeente = None
        gasthoofdgemeente = None
        boolgastlidelders = False
        
        if lid.idStatus == 1: # Doop -> Doop
            ls_vorm = 1
            if lid.ysnLid:
                nrOfDoop += 1
        elif lid.idStatus == 2: # Belijdend -> Belijdend
            ls_vorm = 2
            if lid.ysnLid:
               nrOfBelijdend  += 1
        elif lid.idStatus == 3: # Cathechumeen -> Catechumeen
            ls_vorm = 5
        elif lid.idStatus == 4: # Overig -> Vriend
            ls_vorm = 6
        elif lid.idStatus == 5: # Gastlid (b) -> Gastlid B
            ls_vorm = 4
            logger.warn("Lid is belijdend gastlid - hoofdgemeente moet gecontroleerd worden: %s", create_lid_label(lid))
        elif lid.idStatus == 6: # Gastlid (d) -> Gastlid D
            ls_vorm = 3           
            logger.warn("Lid is belijdend gastlid - hoofdgemeente moet gecontroleerd worden: %s", create_lid_label(lid))
        elif lid.idStatus == 7: # Gastlid Elders (D) -> D
            ls_vorm = 1  
            if lid.ysnLid:
                nrOfDoopElders += 1          
                ls_status = 1
            else:
                ls_status = 2
            boolgastlidelders = True
            logger.warn("Lid is elders gastlid - status en gastgemeente moet gecontroleerd worden: %s", create_lid_label(lid))
        elif lid.idStatus == 8: # Gastlid Elders (B) -> B
            ls_vorm = 2
            
            if lid.ysnLid:
                nrOfBelijdendElders += 1
                ls_status = 1
            else:
                ls_status = 2
                
            boolgastlidelders = True
            logger.warn("Lid is elders gastlid - status en gastgemeente moet gecontroleerd worden: %s", create_lid_label(lid))
        else:
            ls_vorm = "6" # Overig -> Vriend
            #TODO: None in json moet null worden
            #TODO: datetime field ->> date field
        
        # Not null velden controleren
        if (lid.txtAchternaam == None or lid.txtAchternaam == ""):
            logger.error("Achternaam mag niet leeg zijn voor %s" % create_lid_label(lid))
            return
        
        # Huiskring
        if (lid.idHuiskring == 0):
            lid.idHuiskring = None
            
        if (lid.idHuiskringLidType == 0):
            lid.idHuiskringLidType = None    
        
            
        person = {
            "pk": lid.idLid,
            "model": "KB.persoon",
            "fields": {
                "idpersoon": lid.idLid,
                "idlidmaatschapvorm": ls_vorm,
                "idgezin": lid.idGezin,
                "idgezinsrol": lid.idGezinsRol,
                "txtachternaam": lid.txtAchternaam, 
                "txttussenvoegsels": none_safe_string(lid.txtVoorvoegsels),
                "txtvoorletters": none_safe_string(lid.txtVoorletters),
                "txtdoopnaam": none_safe_string(lid.txtDoopnaam),
                "txtroepnaam": none_safe_string(lid.txtRoepnaam),
                "boolaansprekenmetroepnaam": lid.ysnRoepnaam,
                "dtmgeboortedatum": lid.dtmGeboortedatum.strftime("%Y-%m-%d") if lid.dtmGeboortedatum else None,
                "txtgeboorteplaats": none_safe_string(lid.txtGeboorteplaats),
                "idgeslacht": get_geslacht_id(lid.txtGeslacht),
                "dtmdatumdoop": lid.dtmDoop.strftime("%Y-%m-%d") if lid.dtmDoop else None,
                "iddoopgemeente": lid.idDoopgemeente,
                "dtmdatumbelijdenis": lid.dtmBelijdenis.strftime("%Y-%m-%d") if lid.dtmBelijdenis else None,
                "idbelijdenisgemeente": lid.idBelijdenisgemeente,
                "dtmhuwelijksdatum": lid.dtmTrouwdatum.strftime("%Y-%m-%d") if lid.dtmTrouwdatum else None,
                "idhuwelijksgemeente": lid.idTrouwgemeente,
                "dtmdatumbinnenkomst": lid.dtmBinnenkomst.strftime("%Y-%m-%d") if lid.dtmBinnenkomst else None,
                "idbinnengekomenuitgemeente": lid.idVorigeGemeente,
                "dtmdatumvertrek": dtm_vertrokken,
                "idvertrokkennaargemeente": id_vlg_gemeente,
                "txttelefoonnummer": none_safe_string(lid.txtMobielNummer),
                "txtemailadres": none_safe_string(lid.txtEmailAdres),
                "dtmdatumhuwelijksbevestiging": lid.dtmTrouwbevestiging.strftime("%Y-%m-%d") if lid.dtmTrouwbevestiging else None,
                "txtopmerking": none_safe_string(lid.txtAantekeningen) + "\n" + none_safe_string(lid.txtAdresAmbtContact),
                "dtmoverlijdensdatum": dtm_overleden,
                "dtmdatumonttrokken": dtm_onttrokken,
                "idlidmaatschapstatus": ls_status,
                "idwijk": id_wijk,
                "boolgastlidelders": boolgastlidelders,
                "idgastgemeente": gastgemeente,
                "idgasthoofdgemeente": gasthoofdgemeente,
                "idhuiskring": lid.idHuiskring,
                "idhuiskringlidrol": lid.idHuiskringLidType                    
            }
        }
        result.append(person)
        logger.warn("OK: %s" % create_lid_label(lid))
    
    logger.warn("!!!!!!!!!!!!!!")    
    logger.warn("Doop: " + str(nrOfDoop))
    logger.warn("Belijdend: " + str(nrOfBelijdend))
    logger.warn("D elders: " + str(nrOfDoopElders))
    logger.warn("B elders: " + str(nrOfBelijdendElders))
        
    logger.warn("Huiskringleiders moeten nog zelf ingevuld worden!")
    logger.info("Insert Lidmaatschapstatussen")
    lidmaatschap_statussen = [(1,'Actief'),
                       (2,'Vertrokken'),
                       (3,'Onttrokken'),
                       (4,'Overleden')]
    for ls in lidmaatschap_statussen:
        lidmaatschap_status = {
            "pk":ls[0],
            "model": "KB.lidmaatschapstatus",
            "fields": {
                "idlidmaatschapstatus": ls[0],
                "txtlidmaatschapstatus": ls[1]
            }
        }
        result.append(lidmaatschap_status)

    logger.info("Insert Lidmaatschapvormen")
    lidmaatschap_vormen = [(1,'Dooplid', True, "D", "Doopattestatie"),
                       (2,'Belijdend lid', True, "B", "Belijdenisattestatie"),
                       (3,'Gastlid (doop)', False, "D(g)", "Doopattestatie als gastlid"),
                       (4,'Gastlid (belijdend)', False, "B(g)", "Belijdenisattestatie als gastlid"),
                       (5,'Catechumeen', False, "C", ""),
                       (6,'Vriend', False, "V", "")]
    for lv in lidmaatschap_vormen:
        lidmaatschap_vorm = {
            "pk":lv[0],
            "model": "KB.lidmaatschapvorm",
            "fields": {
                "idlidmaatschapvorm": lv[0],
                "txtlidmaatschapvorm": lv[1],
                "boolvoorquotum": lv[2],
                "txtlidmaatschapvormkort": lv[3],
                "txtattestatie": lv[4]
            }
        }
        result.append(lidmaatschap_vorm)

        
    logger.info("Gemeentetypes")
    community_types = [(1,'GKV'),
                       (2,'NGK'),
                       (3,'CGK'),
                       (4,'PKN'),
                       (5,'RK'),
                       (6,'Evangelisch'),
                       (7,'Zusterkerk buitenland')]
    for ct in community_types:
        community_type = {
            "pk": ct[0],
            "model": "KB.gemeentetype",
            "fields": {
                "idgemeentetype": ct[0],
                "txtgemeentetype": ct[1]
            }
        }
        result.append(community_type)
        
    logger.info("Wijken")    
    wijken = [(1,'Pijlsweerd / kop Lombok', 'P/KL'),
              (2,'Lombok', 'LO'),
              (3,'Oog in al, Schepenbuurt, Lombok', 'OSL'),
              (4,'Leidsche Rijn', 'LR'),
              (5,'Ondiep', 'OND'),
              (6,'Zuilen, omgeving Julianapark', 'ZJ'),
              (7,'Zuilen Noord', 'ZN'),
              (8,'Overvecht Zuid', 'OZ'),
              (9,'Overvecht Noord', 'ON'),
              (10,'Buitenland', 'BU'),
              (11,'Overig', 'OV')]
    for w in wijken:
        wijk = {
            "pk":w[0],
            "model": "KB.wijk",
            "fields": {
                "idwijk": w[0],
                "txtwijknaam": w[1],
                "txtwijknaamkort": w[2]
            }
        }
        result.append(wijk)
    
    logger.info("Huiskringen")
    curs.execute("select * from tblHuiskring")
    huiskringen = curs.fetchall()
    
    for hk in huiskringen:
        if hk[1] is None:
            # txthuiskringnaam is null
            continue
        
        huiskring = {
            "pk":hk[0],
            "model": "KB.huiskring",
            "fields": {
                "idhuiskring": hk[0],
                "txthuiskringnaam": hk[1],
                "idwijk": hk[2],
                "txtopmerking": "",
                "txtvolgnummer": hk[3]
            }
        }
        result.append(huiskring)
    
    
    logger.info("HuiskringLidRol")    
    lidrollen = [(1,'Huiskringlid'),
                 (2,'Huiskringlid kind'),
                 (3,'Wijklid'),
                 (4,'Wijklid kind'),
                 (5,'Huiskringleider')]
    for lr in lidrollen:
        lidrol = {
            "pk": lr[0],
            "model": "KB.huiskringlidrol",
            "fields": {
                "idhuiskringlidrol": lr[0],
                "txthuiskringlidrol": lr[1],
            }
        }
        result.append(lidrol)   
    
    
    
    logger.info("Geslacht")    
    geslachten = [(1,'M', 'man', 'de heer', 'dhr.', 'broeder', 'br.'),
                       (2,'V', 'vrouw', 'mevrouw', 'mw.', 'zuster', 'zr.')]
    for g in geslachten:
        geslacht = {
            "pk": g[0],
            "model": "KB.geslacht",
            "fields": {
                "idgeslacht": g[0],
                "txtgeslacht": g[1],
                "txtgeslachtlang": g[2],                
                "txtaanhef": g[3],
                "txtaanhefkort": g[4],                
                "txtaanhefkerk": g[5],
                "txtaanhefkerkkort": g[6]
            }
        }
        result.append(geslacht)   

    logger.info("Landen")
    landen=[u'Afghanistan',
            u'Åland',
            u'Albanië',
            u'Algerije',
            u'Amerikaanse Maagdeneilanden',
            u'Amerikaans-Samoa',
            u'Andorra',
            u'Angola',
            u'Anguilla',
            u'Antarctica',
            u'Antigua en Barbuda',
            u'Argentinië',
            u'Armenië',
            u'Aruba',
            u'Australië',
            u'Azerbeidzjan',
            u'Bahama\'s',
            u'Bahrein',
            u'Bangladesh',
            u'Barbados',
            u'Belarus',
            u'België',
            u'Belize',
            u'Benin',
            u'Bermuda',
            u'Bhutan',
            u'Bolivia',
            u'Bosnië-Herzegovina',
            u'Botswana',
            u'Brazilië',
            u'Britse Maagdeneilanden',
            u'Brunei',
            u'Bulgarije',
            u'Burkina Faso',
            u'Burundi',
            u'Cambodja',
            u'Canada',
            u'Caymaneilanden / Kaaimaneilanden',
            u'Centraal-Afrikaanse Republiek',
            u'Chili',
            u'China',
            u'Christmaseiland',
            u'Cocoseilanden',
            u'Colombia',
            u'Comoren',
            u'Congo',
            u'Congo',
            u'Cookeilanden',
            u'Costa Rica',
            u'Cuba',
            u'Curaçao',
            u'Cyprus',
            u'Denemarken',
            u'Djibouti',
            u'Dominica',
            u'Dominicaanse Republiek',
            u'Duitsland',
            u'Ecuador',
            u'Egypte',
            u'El Salvador',
            u'Equatoriaal-Guinea',
            u'Eritrea',
            u'Estland',
            u'Ethiopië',
            u'Faerøer',
            u'Falklandeilanden',
            u'Fiji',
            u'Filipijnen',
            u'Finland',
            u'Frankrijk',
            u'Frans-Guyana',
            u'Frans-Polynesië',
            u'Gabon',
            u'Gambia',
            u'Georgië',
            u'Ghana',
            u'Gibraltar',
            u'Grenada',
            u'Griekenland',
            u'Groenland',
            u'Groot-Brittannië',
            u'Guadeloupe',
            u'Guam',
            u'Guatemala',
            u'Guinee',
            u'Guinee-Bissau',
            u'Guyana',
            u'Haïti',
            u'Heilige Stoel',
            u'Honduras',
            u'Hongarije',
            u'Hongkong',
            u'Ierland',
            u'IJsland',
            u'India',
            u'Indonesië',
            u'Irak',
            u'Iran',
            u'Israël',
            u'Italië',
            u'Ivoorkust',
            u'Jamaica',
            u'Japan',
            u'Jemen',
            u'Jordanië',
            u'Kaaimaneilanden / Caymaneilanden',
            u'Kaapverdië',
            u'Kameroen',
            u'Kazachstan',
            u'Kenia',
            u'Kirgizië, Kyrgyzstan',
            u'Kiribati',
            u'Koeweit',
            u'Kosovo',
            u'Kroatië',
            u'Laos',
            u'Lesotho',
            u'Letland',
            u'Libanon',
            u'Liberia',
            u'Libië',
            u'Liechtenstein',
            u'Litouwen',
            u'Luxemburg',
            u'Macau',
            u'Macedonië',
            u'Madagaskar',
            u'Malawi',
            u'Maldiven, Malediven',
            u'Maleisië',
            u'Mali',
            u'Malta',
            u'Marokko',
            u'Marshalleilanden',
            u'Martinique',
            u'Mauritanië',
            u'Mauritius',
            u'Mexico',
            u'Micronesia',
            u'Moldavië',
            u'Monaco',
            u'Mongolië',
            u'Montenegro',
            u'Montserrat',
            u'Mozambique',
            u'Myanmar',
            u'Namibië',
            u'Nauru',
            u'Nederland',
            u'Nederlandse Antillen',
            u'Nepal',
            u'Nicaragua',
            u'Nieuw-Caledonië',
            u'Nieuw-Zeeland',
            u'Niger',
            u'Nigeria',
            u'Niue',
            u'Noordelijke Marianen',
            u'Noord-Korea',
            u'Noorwegen',
            u'Norfolkeiland',
            u'Oeganda',
            u'Oekraïne',
            u'Oezbekistan',
            u'Oman',
            u'Oostenrijk',
            u'Oost-Timor',
            u'Pakistan',
            u'Palau',
            u'Palestijnse Autonome Gebieden',
            u'Panama',
            u'Papoea-Nieuw-Guinea',
            u'Paraguay',
            u'Peru',
            u'Pitcairneilanden',
            u'Polen',
            u'Portugal',
            u'Puerto Rico, Porto Rico',
            u'Qatar',
            u'Réunion',
            u'Roemenië',
            u'Rusland',
            u'Rwanda',
            u'Saint Kitts en Nevis',
            u'Saint Lucia',
            u'Saint-Pierre en Miquelon',
            u'Saint Vincent en de Grenadines',
            u'Salomonseilanden',
            u'Samoa',
            u'San Marino',
            u'Sao Tomé en Principe',
            u'Saudi-Arabië',
            u'Senegal',
            u'Servië',
            u'Seychellen',
            u'Sierra Leone',
            u'Singapore',
            u'Sint-Helena',
            u'Sint Maarten',
            u'Slovakije',
            u'Slovenië',
            u'Soedan',
            u'Somalië',
            u'Spanje',
            u'Sri Lanka',
            u'Suriname',
            u'Swaziland',
            u'Syrië',
            u'Tadzjikistan',
            u'Taiwan',
            u'Tanzania',
            u'Thailand',
            u'Timor-Leste',
            u'Togo',
            u'Tokelau-eilanden',
            u'Tonga',
            u'Trinidad en Tobago',
            u'Tsjaad',
            u'Tsjechië',
            u'Tunesië',
            u'Turkije',
            u'Turkmenistan',
            u'Turks- en Caicoseilanden',
            u'Tuvalu',
            u'Uganda',
            u'Uruguay',
            u'Vanuatu',
            u'Vaticaanstad',
            u'Venezuela',
            u'Verenigde Arabische Emiraten',
            u'Verenigde Staten van Amerika',
            u'Verenigd Koninkrijk',
            u'Vietnam',
            u'Wallis en Futuna',
            u'Wit-Rusland',
            u'Zambia',
            u'Zimbabwe',
            u'Zuid-Afrika',
            u'Zuid-Korea',
            u'Zweden',
            u'Zwitserland']
    counter=1
    for l in landen:         
        land = {
            "pk": counter,
            "model": "KB.land",
            "fields": {
                "idland": counter,
                "txtlandnaam": l
            }
        }
        result.append(land)    
        counter += 1        
    
   
    fixture_filename = "kb.json"
    fixture_file = open(fixture_filename, 'w')
    fixture_file.write(simplejson.dumps(result, indent=4))
    fixture_file.close()
    
    logger.info("Wrote json to %s", fixture_filename)
    
if __name__ == "__main__":
    main()