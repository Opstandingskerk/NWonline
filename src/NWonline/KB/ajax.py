###############################################################################
# File: NWonline/KB/ajax.py
# Author: Lukas Batteau
# Description: Ajax request handlers
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
###############################################################################
from NWonline.KB.models import Persoon
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import force_unicode

def queryPersoon(request):
    query = request.GET.get('term')
    query_words = query.split(" ")
    # Create empty list
    persoon_list = Persoon.objects.all()
   
    # Join filtered queries
    for word in query_words:
        # Check if word is empty
        if (word == ""):
            # Empty, skip
            continue
        
        persoon_list = persoon_list & Persoon.objects.all().filter(Q(txtachternaam__icontains=word) |
                                                                   Q(txttussenvoegsels__icontains=word) |
                                                                   Q(txtroepnaam__icontains=word))   
            
            
    
    result = []
    for persoon in persoon_list:
        result.append({'value': str(persoon),
                       'idpersoon': str(persoon.idpersoon),
                       'txtachternaam': force_unicode(persoon.txtachternaam),
                       'txttussenvoegsels': str(persoon.txttussenvoegsels),
                       'txtroepnaam': force_unicode(persoon.txtroepnaam),
                       'txtvoorletters': str(persoon.txtvoorletters),
                       'idgeslacht': str(persoon.idgeslacht.idgeslacht)})
        
    # Redirect to a success page.
    return HttpResponse(simplejson.dumps(result),
                        mimetype='application/json')

