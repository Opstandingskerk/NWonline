from NWonline.KB.forms import PersoonSearchForm
from NWonline.KB.models import GezinsRol
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from modelforms import GezinForm, PersoonForm
from models import Gezin, Persoon

@login_required
def handlePersoonList(request):
    # Retrieve list with all active members
    persoon_list = Persoon.objects.exclude(dtmdatumvertrek__lt=datetime.now()).exclude(boolactief=False)
    
    # Determine search filter
    try:
        filter = request.GET.get("filter")
        filter_words = filter.split(" ")
        
        # Join filtered queries
        for word in filter_words:
            # Check if word is empty
            if (word == ""):
                # Empty, skip
                continue
            
            persoon_list = persoon_list & Persoon.objects.all().filter(Q(txtachternaam__icontains=word) |
                                                                       Q(txtroepnaam__icontains=word) |
                                                                       Q(idgezin__txtgezinsnaam__icontains=word) |
                                                                       Q(idgezin__txtstraatnaam__icontains=word))
    except:
        # No search filter, continue
        pass
    
    # Determine ordering
    try:
        order_by = request.GET["sort"]
        persoon_list = persoon_list.order_by(order_by)
    except Exception as e:
        print e
        pass
        
    paginator = Paginator(persoon_list, 20)

    # Make sure page request is an int. If not, deliver first page.
    try:
        pageNr = int(request.GET.get("page", "1"))
    except ValueError:
        pageNr = 1
    
    # If page request (9999) is out of range, deliver last page of results.
    try:
        page = paginator.page(pageNr)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
        
    # Determine whether request is ajax call
    if request.GET.has_key("xhr"):
        # Ajax, render template component instead of full html
        return render_to_response("KB/persoonListTable.html",
                                  {"page": page},
                                  context_instance=RequestContext(request))
    else:
        # Regular request, render full html
        return render_to_response("KB/persoonList.html",
                                  {"page": page},
                                  context_instance=RequestContext(request))
        
@login_required
def handlePersoonSearch(request):
    # Check if form has been submitted
    if (request.method == "POST"):
        # A form bound to the POST data
        persoonSearchForm = PersoonSearchForm(request.POST)
        persoon_list =Persoon.objects.filter(txtachternaam__icontains=persoonSearchForm.data["txtachternaam"])
        paginator = Paginator(persoon_list, 20)
        page = paginator.page(1)        
        return render_to_response("KB/persoonSearch.html",
                                  {"page": page},
                                  context_instance=RequestContext(request))
    else:
        # No POST data
        persoonSearchForm = PersoonSearchForm()
        return render_to_response("KB/persoonSearch.html",
                                  {"searchForm": persoonSearchForm},
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
            return HttpResponseRedirect("../../persoon/%d/" % (persoonForm.instance.idpersoon))
        else:
            formState = "MODIFY"
    else:
        # No POST data
        persoon = Persoon()
        # Retrieve gezin
        persoon.idgezin = Gezin.objects.get(idgezin=gezinId)
        # Find head of family
        try:
            # Found, prefill new person"s last name
            head = Persoon.objects.get(idgezin=gezinId, idgezinsrol=GezinsRol.objects.get(pk=1))
            persoon.txtachternaam = head.txtachternaam
            persoon.txttussenvoegsels = head.txttussenvoegsels
        except:
            # Head not present, use gezin name
            persoon.txtachternaam = persoon.idgezin.txtgezinsnaam 
        
        persoonForm = PersoonForm(instance=persoon)
        
    persoonList = Persoon.objects.filter(idgezin=gezinId).order_by("idgezinsrol", "dtmgeboortedatum")
    
    return render_to_response("KB/persoonDetails.html",
                          {"persoonForm": persoonForm,
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
            formState = "VIEW"
        else:
            formState = "MODIFY"
    else:
        # No POST data
        persoonForm = PersoonForm(instance=persoon)

    persoonList = Persoon.objects.filter(idgezin=persoon.idgezin.idgezin).order_by("idgezinsrol", "dtmgeboortedatum")
    
    return render_to_response("KB/persoonDetails.html",
                              {"persoonForm": persoonForm,
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