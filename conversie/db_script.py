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

logging.basicConfig(level=logging.INFO)

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
    
    
    logger.info("Converting tblGezin")           
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
                    match_huisnummer = -999
            else:
                match_huisnummer = -999
                match_toevoeging = ""
            
            txtStraatnaam = gezinsadres.txtStraatnaam
            txtPostcode = gezinsadres.txtPostcode
            txtPlaats = gezinsadres.txtPlaats
            txtAdresExtra = gezinsadres.txtAdresExtra
                              
        else:
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
                "txtstraatnaam": txtStraatnaam,
                "inthuisnummer": match_huisnummer,
                "txthuisnummertoevoeging": match_toevoeging,
                "txtpostcode": txtPostcode,
                "txtplaats": txtPlaats,
                "idland": "1",
                "txttelefoon": gezin.txtTelefoonnummer,
                "txtopmerking": txtAdresExtra
            }
        }
        result.append(family)
     
    logger.info("Converting tblLid")          
    curs.execute("select * from tblLid")
    for lid in curs.fetchall():                
        # Als persoon vertrokken is dan krijgt hij de status 2 = Vertrokken
        # tenzij hij naar gemeente id 338 (=onttrokken) of id 339 (=overleden) gaat
                  
        dtm_onttrokken = ""
        dtm_overleden = "" 
        dtm_vertrokken = ""
        id_vlg_gemeente = ""        
        if lid.dtmVertrokken is not None:
            if lid.idVolgendeGemeente == 338:
                ls_vorm = 3
                dtm_onttrokken = str(lid.dtmVertrokken)                                
            if lid.idVolgendeGemeente == 339:
                ls_vorm = 4
                dtm_overleden = str(lid.dtmVertrokken)
            else:    
                ls_vorm = 2
                dtm_vertrokken = str(lid.dtmVertrokken)
                id_vlg_gemeente = lid.idVolgendeGemeente
        else:
            ls_vorm = 1            
        
        ## De status van het lid bepalen
        gastgemeente =""
        gasthoofdgemeente =""
        
        if lid.idStatus == 1: # Belijdend -> Belijdend
            ls_status = "1"
        elif lid.idStatus == 2: # Doop -> Doop
            ls_status = "2"
        elif lid.idStatus == 3: # Cathechumeen -> Catechumeen
            ls_status = "5"
        elif lid.idStatus == 4: # Overig -> Vriend
            ls_status = "6"
        elif lid.idStatus == 5: # Gastlid (b) -> Gastlid B
            ls_status = "4"
            gasthoofdgemeente = "" #TODO
            
        elif lid.idStatus == 6: # Gastlid (d) -> Gastlid D
            ls_status = "3"
            gasthoofdgemeente = "" #TODO
            
        elif lid.idStatus == 7: # Gastlid Elders (D) -> D
            ls_status = "1"
            gastgemeente = "" #TODO
            
        elif lid.idStatus == 8: # Gastlid Elders (B) -> B
            ls_status = "2"
            gastgemeente ="" #TODO
            
        else:
            ls_status = "6" # Overig -> Vriend
        #TODO: None in json moet null worden
        #TODO: datetime field ->> date field
        person = {
            "pk": lid.idLid,
            "model": "KB.persoon",
            "fields": {
                "idpersoon": lid.idLid,
                "idlidmaatschapvorm": ls_vorm,
                "idgezin": lid.idGezin,
                "idgezinsrol": lid.idGezinsRol,
                "txtachternaam": lid.txtAchternaam, 
                "txttussenvoegsels": lid.txtVoorvoegsels,
                "txtvoorletters": lid.txtVoorletters,
                "txtdoopnaam": lid.txtDoopnaam,
                "txtroepnaam": lid.txtRoepnaam,
                "boolaansprekenmetroepnaam": lid.ysnRoepnaam,
                "dtmgeboortedatum": str(lid.dtmGeboortedatum),
                "txtgeboorteplaats": lid.txtGeboorteplaats,
                "idgeslacht": get_geslacht_id(lid.txtGeslacht),
                "dtmdatumdoop": str(lid.dtmDoop),
                "iddoopgemeente": lid.idDoopgemeente,
                "dtmdatumbelijdenis": str(lid.dtmBelijdenis),
                "idbelijdenisgemeente": lid.idBelijdenisgemeente,
                "dtmhuwelijksdatum": str(lid.dtmTrouwdatum),
                "idhuwelijksgemeente": lid.idTrouwgemeente,
                "dtmdatumbinnenkomst": str(lid.dtmBinnenkomst),
                "idbinnengekomenuitgemeente": lid.idVorigeGemeente,
                "dtmdatumvertrek": dtm_vertrokken,
                "idvertrokkennaargemeente": id_vlg_gemeente,
                "txttelefoonnummer": lid.txtMobielNummer,
                "txtemailadres": lid.txtEmailAdres,
                "dtmdatumhuwelijksbevestiging": str(lid.dtmTrouwbevestiging),
                "txtopmerking": lid.txtAantekeningen,
                "dtmoverlijdensdatum": dtm_overleden,
                "dtmdatumonttrokken": dtm_onttrokken,
                "idlidmaatschapstatus": ls_status,
                "idwijk": "1",
                "idgastgemeente": gastgemeente,
                "idgasthoofdgemeente": gasthoofdgemeente,                
                "boolgeborennw": ""
            }
        }
        result.append(person)
    
    
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
    lidmaatschap_vormen = [(1,'Dooplid', "True", "D", "Doopattestatie"),
                       (2,'Belijdend lid', "True", "B", "Belijdenisattestatie"),
                       (3,'Gastlid (doop)', "False", "D(g)", "Doopattestatie als gastlid"),
                       (4,'Gastlid (belijdend)', "False", "B(g)", "Belijdenisattestatie als gastlid"),
                       (5,'Catechumeen', "False", "C", ""),
                       (6,'Vriend', "False", "V", "")]
    for lv in lidmaatschap_vormen:
        lidmaatschap_vorm = {
            "pk":lv[0],
            "model": "KB.lidmaatschapvorm",
            "fields": {
                "idlidmaatschapvorm": lv[0],
                "txtlidmaatschapstatus": lv[1],
                "boolvoorquotum": lv[2],
                "txtlidmaatschapvormkort": lv[3],
                "txtattestatie": lv[4]
            }
        }
        result.append(lidmaatschap_status)

        
    logger.info("Insert CommunityTypes")
    #### Community Types ###
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
    
    
    #inode, tmp_filename = tempfile.mkstemp(suffix='.json')
    tmp_filename = "kb.json"
    open(tmp_filename, 'w').write(simplejson.dumps(result, indent=4))
    logger.info("Wrote json to %s", tmp_filename)
    
if __name__ == "__main__":
    main()
