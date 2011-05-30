###############################################################################
# File: NWonline/KB/views.py
# Author: Lukas Batteau
# Description: Request handlers, usually mapping directly to a certain page.
# 
# CHANGE HISTORY
# 20101209    Lukas Batteau        Added header.
# 20110328    Lukas Batteau        Persoon list page now separated in two: One
#                                  with ajax 'quick filter' and one for 
#                                  advanced searching via form post. Both pages
#                                  share column sorting and pagination. 
# 20110329    Lukas Batteau        Lidmaatschap is gewijzigd, bestaat nu uit
#                                  vorm (doop, etc) en status (actief, etc).
# 20110414    Lukas Batteau        Moved membership description method to model
#                                  Persoon list now filtered by status
###############################################################################
from NWonline.KB.forms import PersoonSearchForm
from NWonline.KB.modelforms import GemeenteForm
from NWonline.KB.models import GezinsRol, LidmaatschapStatus, LidmaatschapVorm
from datetime import datetime
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext, Context
from django.template import loader
from django.utils import simplejson
from django.utils.html import escape
from modelforms import GezinForm, PersoonForm, GezinsRolForm
from models import Gezin, Persoon

def createPersoonListPage(request):
    """
    Apply ordering and pagination to existing persoon list in session.
    
    Assume the persoon list is present in the session, otherwise something
    is very wrong. Calling methods are responsible for retrieving the list
    and storing it in the session as 'persoon_list'.
    
    Look for GET parameters 'order_by' and 'page', where 'order_by' contains
    the name of the column (prepended with "-" for descending order), and
    'page' contains the current page number.
    
    Default max number of items on one page: 20
    """
    persoon_list = request.session["persoon_list"]
    
    # Determine ordering
    try:
        order_by = request.GET["order_by"]
        persoon_list = persoon_list.order_by(order_by)
    except:
        # Parameter 'order_by' not present in GET
        pass
        
    # Create paginator with max twenty items per page
    paginator = Paginator(persoon_list, 20)
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        pageNr = int(request.GET.get("page", "1"))
    except ValueError:
        pageNr = 1
        
    # If page request is out of range, deliver last page of results.
    if (pageNr > paginator.num_pages):
        # Out of range, take last page
        pageNr = paginator.num_pages
        
    return paginator.page(pageNr)

@login_required
def handlePersoonListExport(request):
    persoon_list = request.session["persoon_list"]

    #response = render_to_response("KB/export/persoonListTable.csv", 
    #                              { 'persoon_list': persoon_list})
   
    template = loader.get_template("KB/export/persoonListTable.csv")
    context = Context({
        'persoon_list': persoon_list,
    })
    
    response = HttpResponse() 
    filename = "leden_%s.csv" % (datetime.now().strftime("%Y%m%d%H%M%S"))
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'text/csv; charset=utf-8'
    # Add UTF-8 'BOM' signature, otherwise Excel will assume the CSV file
    # encoding is ASCII and special characters will be mangled
    response.write("\xEF\xBB\xBF")
    response.write(template.render(context))
    
    return response
    
@login_required
def handlePersoonListFilter(request):
    """
    Handle the persoon list page.
    
    Render an initial list containing all active Persoons in the database
    with their related Gezin. Active means idlidmaatschapstatus=1 (Actief)
    
    Render a search field above the list, that the user can use to quickly
    filter the list by the following fields:
     - txtachternaam
     - txtroepnaam
     - txtgezinsnaam
     - txtstraatnaam
     
    Store the list in the session, in order for the column ordering and
    pagination to work without having to retrieve the list. 
    """
    
    # Create extended search form
    persoonSearchForm = PersoonSearchForm()
    
    if (request.GET):
        # Retrieve default list with all members
        persoon_list = Persoon.objects.all()

        # Determine quick search filter
        if ("filter" in request.GET):
            filter = request.GET["filter"]
        else:
            filter = ""
        
        # Create the list of search criteria, assuming they are separated by spaces 
        filter_words = filter.split(" ")
    
        # Join filtered queries
        for word in filter_words:
            # Check if word is empty
            if (word == ""):
                # Empty, skip
                continue
            
            # Apply the filter by creating a combined query, testing if one of the
            # fields contains this word.
            persoon_list = persoon_list.filter(Q(txtachternaam__icontains=word) |
                                               Q(txtroepnaam__icontains=word) |
                                               Q(idgezin__txtgezinsnaam__icontains=word) |
                                               Q(idgezin__txtstraatnaam__icontains=word))
    
        # Bind the form to the GET data
        persoonSearchForm = PersoonSearchForm(request.GET)
        if (persoonSearchForm.is_valid()):
            # Now check the form fields and apply filter when present
            
            idlidmaatschapstatus = persoonSearchForm.cleaned_data["idlidmaatschapstatus"]
            if (idlidmaatschapstatus):
                persoon_list = persoon_list.filter(idlidmaatschapstatus=idlidmaatschapstatus)
            
            idlidmaatschapvorm = persoonSearchForm.cleaned_data["idlidmaatschapvorm"]
            if (idlidmaatschapvorm):
                persoon_list = persoon_list.filter(idlidmaatschapvorm=idlidmaatschapvorm)
            
            idwijk = persoonSearchForm.cleaned_data["idwijk"]
            if (idwijk):
                persoon_list = persoon_list.filter(idwijk=idwijk)
            
            dtmgeboortedatumvan = persoonSearchForm.cleaned_data["dtmgeboortedatumvan"]
            if (dtmgeboortedatumvan):
                persoon_list = persoon_list.filter(dtmgeboortedatum__gte=dtmgeboortedatumvan)
                
            dtmgeboortedatumtot = persoonSearchForm.cleaned_data["dtmgeboortedatumtot"]
            if (dtmgeboortedatumtot):
                persoon_list = persoon_list.filter(dtmgeboortedatum__lt=dtmgeboortedatumtot)
                
            idgezinsrol = persoonSearchForm.cleaned_data["idgezinsrol"]
            if (idgezinsrol):
                persoon_list = persoon_list.filter(idgezinsrol=idgezinsrol)
                
            txtachternaam = persoonSearchForm.cleaned_data["txtachternaam"]
            if (txtachternaam):
                persoon_list = persoon_list.filter(txtachternaam__icontains=txtachternaam)
                
            txttussenvoegsels = persoonSearchForm.cleaned_data["txttussenvoegsels"]
            if (txttussenvoegsels):
                persoon_list = persoon_list.filter(txttussenvoegsels__icontains=txttussenvoegsels)
                
            txtvoorletters = persoonSearchForm.cleaned_data["txtvoorletters"]
            if (txtvoorletters):
                persoon_list = persoon_list.filter(txtvoorletters__icontains=txtvoorletters)
                
            txtroepnaam = persoonSearchForm.cleaned_data["txtroepnaam"]
            if (txtroepnaam):
                persoon_list = persoon_list.filter(txtroepnaam__icontains=txtroepnaam)
                
            txtdoopnaam = persoonSearchForm.cleaned_data["txtdoopnaam"]
            if (txtdoopnaam):
                persoon_list = persoon_list.filter(txtdoopnaam__icontains=txtdoopnaam)
            
            dtmdatumbinnenkomstvan = persoonSearchForm.cleaned_data["dtmdatumbinnenkomstvan"]
            if (dtmdatumbinnenkomstvan):
                persoon_list = persoon_list.filter(dtmdatumbinnenkomst__gte=dtmdatumbinnenkomstvan)
                
            dtmdatumbinnenkomsttot = persoonSearchForm.cleaned_data["dtmdatumbinnenkomsttot"]
            if (dtmdatumbinnenkomsttot):
                persoon_list = persoon_list.filter(dtmdatumbinnenkomst__lt=dtmdatumbinnenkomsttot)
                
            dtmdatumvertrekvan = persoonSearchForm.cleaned_data["dtmdatumvertrekvan"]
            if (dtmdatumvertrekvan):
                persoon_list = persoon_list.filter(dtmdatumvertrek__gte=dtmdatumvertrekvan)
                
            dtmdatumvertrektot = persoonSearchForm.cleaned_data["dtmdatumvertrektot"]
            if (dtmdatumvertrektot):
                persoon_list = persoon_list.filter(dtmdatumvertrek__lt=dtmdatumvertrektot)
                
            dtmdatumonttrokkenvan = persoonSearchForm.cleaned_data["dtmdatumonttrokkenvan"]
            if (dtmdatumonttrokkenvan):
                persoon_list = persoon_list.filter(dtmdatumonttrokken__gte=dtmdatumonttrokkenvan)
                
            dtmdatumonttrokkentot = persoonSearchForm.cleaned_data["dtmdatumonttrokkentot"]
            if (dtmdatumonttrokkentot):
                persoon_list = persoon_list.filter(dtmdatumonttrokken__lt=dtmdatumonttrokkentot)
                
            dtmoverlijdensdatumvan = persoonSearchForm.cleaned_data["dtmoverlijdensdatumvan"]
            if (dtmoverlijdensdatumvan):
                persoon_list = persoon_list.filter(dtmoverlijdensdatum__gte=dtmoverlijdensdatumvan)
                
            dtmoverlijdensdatumtot = persoonSearchForm.cleaned_data["dtmoverlijdensdatumtot"]
            if (dtmoverlijdensdatumtot):
                persoon_list = persoon_list.filter(dtmoverlijdensdatum__lt=dtmoverlijdensdatumtot)
                
    else:
        # Nothing posted

        # Retrieve default list with all active members
        persoon_list = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.objects.get(pk=1))
    
    # Store the list in the session
    request.session["persoon_list"] = persoon_list
    
    # Apply ordering and pagination
    page = createPersoonListPage(request)
    
    # This handler can be called in two different modes: Either the user has
    # browsed here directly, in which case the full page should be rendered,
    # or it is called by an ajax call from the page, in which case just the
    # persoon_list should be rendered.
    if (request.GET.has_key("xhr")):
        # Ajax, render persoonListTable template instead of full html
        return render_to_response("KB/persoonListTable.html",
                                  {"page": page },
                                  context_instance=RequestContext(request))
    else:
        # Regular request, render full template
        return render_to_response("KB/persoonList.html",
                                  {"page": page,
                                   "persoonSearchForm": persoonSearchForm },
                                  context_instance=RequestContext(request))

@login_required
def handlePopupAdd(request, form, model):

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                instance = {"id": newObject._get_pk_val(),
                         "value": newObject }
                return HttpResponse(simplejson.dumps(instance),
                                    mimetype='application/json')
    else:
        form = form()
    
    return render_to_response("KB/add_related_popup.html", {'form': form, 'field': model })

@login_required
def handleAddInstance(request, model):
    form = eval("%sForm" % (model))
    return handlePopupAdd(request, form, model)

@login_required
def handlePersoonListUpdate(request):
    """
    Handle a request where the Persoon list does not need to be retrieved.
    
    Apply column ordering and pagination and render either the page or 
    just the list, depending on whether the request is ajax or not.
    
    It is unlikely that this handler is called directly, as it is only used
    for ordering and pagination of an existing list.
    """
    
    # Apply ordering and pagination
    page = createPersoonListPage(request)
        
    # Determine whether request is ajax call
    # TODO: Check if we really need to distinguish the request 
    if (request.GET.has_key("xhr")):
        # Ajax, render template component instead of full html
        return render_to_response("KB/persoonListTable.html",
                                  {"page": page },
                                  context_instance=RequestContext(request))
    else:
        # Regular request, render full html
        return render_to_response("KB/persoonList.html",
                                  {"page": page },
                                  context_instance=RequestContext(request))
    
    
@login_required
def handleGezinDetails(request, gezinId):
    gezin = Gezin.objects.get(idgezin=gezinId)
    persoonList = list(Persoon.objects.filter(idgezin=gezinId).order_by("idgezinsrol", "dtmgeboortedatum"))
        
    # Default mode is "view"
    formState = "VIEW"
    
    # On cancel reload current page
    cancelRedirect = ""
    
    # Check if form has been submitted
    if (request.method == "POST"):
        # A form bound to the POST data
        gezinForm = GezinForm(request.POST, instance=gezin)
        # Check if validations pass
        if (gezinForm.is_valid()):
            # Form is valid
            gezinForm.save()
            gezinId = gezinForm.instance.idgezin
            formState = "VIEW"
        else:
            formState = "MODIFY"
    else:
        # No POST data
        gezinForm = GezinForm(instance=gezin)
    
    return render_to_response("KB/gezinDetails.html",
                              {"gezinForm": gezinForm,
                               "persoonList": persoonList,
                               "formState": formState,
                               "cancelRedirect": cancelRedirect},
                               context_instance=RequestContext(request))
@login_required
def handleGezinAdd(request):
    # Default mode is "view"
    formState = "ADD"
    
    # On cancel redirect to list
    cancelRedirect = "/leden"
    
    # Check if form has been submitted
    if (request.method == "POST"):
        # A form bound to the POST data
        gezinForm = GezinForm(request.POST)
        # Check if validations pass
        if (gezinForm.is_valid()):
            # Form is valid
            gezinForm.save()
            return HttpResponseRedirect("./%d/" % (gezinForm.instance.idgezin))
        else:
            formState = "MODIFY"
    else:
        # No POST data
        gezinForm = GezinForm()
    
    return render_to_response("KB/gezinDetails.html",
                              {"gezinForm": gezinForm,
                               "formState": formState,
                               "cancelRedirect": cancelRedirect},
                               context_instance=RequestContext(request))
    

@login_required
def handleGezinPersoonAdd(request, gezinId):
    # Default mode is "view"
    formState = "ADD"
    
    # On cancel redirect to list
    cancelRedirect = "../"
    
    # Check if form has been submitted
    if (request.method == "POST"):
        # A form bound to the POST data
        persoonForm = PersoonForm(request.POST)
        # Check if validations pass
        if (persoonForm.is_valid()):
            # Form is valid
            persoonForm.save()
            
            # Update gezin name if persoon is family head
            persoon = persoonForm.instance
            if (persoon.idgezinsrol == GezinsRol.GEZINSHOOFD):
                persoon.idgezin.txtgezinsnaam = Gezin.create_gezins_naam(persoon)
                persoon.idgezin.save()
                
            return HttpResponseRedirect("../../persoon/%d/" % (persoonForm.instance.idpersoon))
        else:
            formState = "MODIFY"

        # Remember the selected tab
        selectedTab = request.POST["selectedTab"]
    else:
        # No POST data
        persoon = Persoon()
        # Retrieve gezin
        persoon.idgezin = Gezin.objects.get(idgezin=gezinId)
        # Find head of family
        try:
            # Found, prefill new person's last name
            head = Persoon.objects.get(idgezin=gezinId, idgezinsrol=GezinsRol.objects.get(pk=1))
            persoon.txtachternaam = head.txtachternaam
            persoon.txttussenvoegsels = head.txttussenvoegsels
        except:
            # Head not present, use gezin name
            persoon.txtachternaam = persoon.idgezin.txtgezinsnaam 
        
        persoonForm = PersoonForm(instance=persoon)
        
        # Default to first tab
        selectedTab = 0
        
    persoonList = Persoon.objects.filter(idgezin=gezinId).order_by("idgezinsrol", "dtmgeboortedatum")
    
    return render_to_response("KB/persoonDetails.html",
                          {"persoonForm": persoonForm,
                           "selectedTab": selectedTab,
                           "persoonList": persoonList,
                           "formState": formState,
                           "cancelRedirect": cancelRedirect},
                           context_instance=RequestContext(request))
    
@login_required
def handlePersoonDetails(request, persoonId):
    persoon = Persoon.objects.get(idpersoon=persoonId)    
    
    # Check if form state is passed
    try:
        formState = request.GET["state"]
    except:
        # Default mode is "view"
        formState = "VIEW"

        
    # If user came in modify mode, redirect goes back
    if (formState == "MODIFY"):
        # On cancel redirect back
        cancelRedirect = request.META.get("HTTP_REFERER")
    else:
        #Otherwise redirect stays on page
        cancelRedirect = ""
    
    # Check if form has been submitted
    if (request.method == "POST"):
        # Check whether the form contains an existing person
        persoon = None
        persoonId = eval(request.POST["idpersoon"])
        if (persoonId):
            persoon = Persoon.objects.get(idpersoon=persoonId)
            
        # A form bound to the POST data
        persoonForm = PersoonForm(request.POST, instance=persoon)
        # Check if validations pass
        if (persoonForm.is_valid()):
            # Form is valid
            persoonForm.save()
            persoon = persoonForm.instance

            # Update gezin name if persoon is family head
            if (persoon.idgezinsrol.pk == GezinsRol.GEZINSHOOFD):
                persoon.idgezin.txtgezinsnaam = Gezin.create_gezins_naam(persoon)
                persoon.idgezin.save()
            
            formState = "VIEW"
        else:
            formState = "MODIFY"
            
        # Remember the selected tab
        selectedTab = request.POST["selectedTab"]
    else:
        # No POST data
        persoonForm = PersoonForm(instance=persoon)
        selectedTab = 0

    # Create membership description
    membership = persoon.membership()
    
    persoonList = Persoon.objects.filter(idgezin=persoon.idgezin.idgezin).order_by("idgezinsrol", "dtmgeboortedatum")
    
    return render_to_response("KB/persoonDetails.html",
                              {"persoonForm": persoonForm,
                               "selectedTab": selectedTab,
                               "membership": membership,
                               "persoonList": persoonList,
                               "formState": formState,
                               "cancelRedirect": cancelRedirect},
                               context_instance=RequestContext(request))
    
def handleLogin(request):
    # Check if post data present
    if (request.method == "POST"):
        # Post data present
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect
                try:
                    # Target path could be included
                    path = request.GET["next"]
                    return HttpResponseRedirect(path)
                except:
                    return HttpResponseRedirect("/leden")
            else:
                # Return a "disabled account" error message
                return render_to_response("KB/error.html",
                                          {"message": "Dit account is niet langer geldig."})
        else:
            # Return an "invalid login" error message.
            return render_to_response("KB/login.html",
                                          {"message": "Ongeldige gebruikersnaam of wachtwoord."})
    else:
        # No post data, show login screen
        return render_to_response("KB/login.html")
    
def handleLogout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/login")