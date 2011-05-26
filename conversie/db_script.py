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
                "txtstraatnaam": none_safe_string(txtStraatnaam),
                "inthuisnummer": match_huisnummer,
                "txthuisnummertoevoeging": none_safe_string(match_toevoeging),
                "txtpostcode": none_safe_string(txtPostcode),
                "txtplaats": none_safe_string(txtPlaats),
                "idland": "1",
                "txttelefoon": none_safe_string(gezin.txtTelefoonnummer),
                "txtopmerking": none_safe_string(txtAdresExtra)
            }
        }
        result.append(family)
     
    logger.info("Converting tblLid")          
    curs.execute("select * from tblLid")
    for lid in curs.fetchall():                
        # Als persoon vertrokken is dan krijgt hij de status 2 = Vertrokken
        # tenzij hij naar gemeente id 338 (=onttrokken) of id 339 (=overleden) gaat
        if (lid.idLid in (300, 632, 1480, 1392, 1405, 1406, 1407, 1408, 1419, 1436, 1481, 1485, 1497, 518)):
            logger.info("Skipping %s" % (lid))
            continue
                  
        dtm_onttrokken = None
        dtm_overleden = None
        dtm_vertrokken = None
        id_vlg_gemeente = "1"        
        if lid.dtmVertrokken is not None:
            if lid.idVolgendeGemeente == 338:
                ls_status = 3
                dtm_onttrokken = lid.dtmVertrokken.strftime("%Y-%m-%d") if lid.dtmVertrokken else None                             
            if lid.idVolgendeGemeente == 339:
                ls_status = 4
                dtm_overleden = lid.dtmVertrokken.strftime("%Y-%m-%d") if lid.dtmVertrokken else None 
            else:    
                ls_status = 2
                dtm_vertrokken = lid.dtmVertrokken.strftime("%Y-%m-%d") if lid.dtmVertrokken else None 
                id_vlg_gemeente = lid.idVolgendeGemeente
        else:
            ls_status = 1            
        
        ## De status van het lid bepalen
        gastgemeente ="1"
        gasthoofdgemeente ="1"
        
        if lid.idStatus == 1: # Belijdend -> Belijdend
            ls_vorm = "1"
        elif lid.idStatus == 2: # Doop -> Doop
            ls_vorm = "2"
        elif lid.idStatus == 3: # Cathechumeen -> Catechumeen
            ls_vorm = "5"
        elif lid.idStatus == 4: # Overig -> Vriend
            ls_vorm = "6"
        elif lid.idStatus == 5: # Gastlid (b) -> Gastlid B
            ls_vorm = "4"
            gasthoofdgemeente = "1" #TODO
            
        elif lid.idStatus == 6: # Gastlid (d) -> Gastlid D
            ls_vorm = "3"
            gasthoofdgemeente = "1" #TODO
            
        elif lid.idStatus == 7: # Gastlid Elders (D) -> D
            ls_vorm = "1"
            gastgemeente = "1" #TODO
            
        elif lid.idStatus == 8: # Gastlid Elders (B) -> B
            ls_vorm = "2"
            gastgemeente ="1" #TODO
            
        else:
            ls_vorm = "6" # Overig -> Vriend
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
                "txtopmerking": none_safe_string(lid.txtAantekeningen),
                "dtmoverlijdensdatum": dtm_overleden,
                "dtmdatumonttrokken": dtm_onttrokken,
                "idlidmaatschapstatus": ls_status,
                "idwijk": "1",
                "idgastgemeente": gastgemeente,
                "idgasthoofdgemeente": gasthoofdgemeente,                
                "boolgeborennw": False
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
