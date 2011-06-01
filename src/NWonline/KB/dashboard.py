###############################################################################
# File: NWonline/KB/export.py
# Author: Lukas Batteau
# Description: Handlers for the exports page
###############################################################################
from NWonline.KB.models import Persoon, LidmaatschapStatus, GezinsRol, \
    LidmaatschapVorm
from NWonline.KB.widgets import DatePicker
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext, Context
import datetime

class MembersForm(forms.Form):
    filter_heads = forms.BooleanField(label="Alleen gezinshoofden?",
                                      initial=False,
                                      required=False)
    
class BirthdaysForm(forms.Form):
    CATEGORY_LTE12 = 0
    CATEGORY_GT12 = 1
    
    # Initialize from and to dates.
    today = datetime.date.today()
    # The from date is the first of the year
    initial_date_from = today.replace(day=1, month=1)
    # The to date is the last day of the year
    initial_date_to = today.replace(day=31, month=12)
    
    date_from = forms.DateField(label="Datum van",
                                widget=DatePicker(),
                                initial=initial_date_from)
    date_to = forms.DateField(label="tot",
                              widget=DatePicker(),
                              initial=initial_date_to)
    category = forms.TypedChoiceField(label="Categorie",
                                      choices=((CATEGORY_LTE12, '12-'), (CATEGORY_GT12, '12+')),
                                      widget=forms.RadioSelect(),
                                      initial=CATEGORY_LTE12,
                                      coerce=int)

class Statistics():
    def __init__(self):
        self.label = ""
        self.value = 0
            
@login_required
def handleExport(request):
    members_form = MembersForm()
    birthdays_form = BirthdaysForm()
    
    # Create members stats
    stats = []

    for membership in LidmaatschapVorm.objects.all():
        stat = Statistics()
        stat.label = str(membership)
        stat.value = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.ACTIEF, idlidmaatschapvorm=membership).count()
        stats.append(stat)
    
    total = Statistics()
    total.label = "Totaal"
    total.value = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.ACTIEF).count()
       
    return render_to_response("KB/dashboard.html",
                              {"members_form": members_form,
                               "birthdays_form": birthdays_form,
                               "stats": stats,
                               "total": total},
                              context_instance=RequestContext(request))

@login_required
def handleExportMembers(request):
    members = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.ACTIEF)
    members = members.order_by("idgezin__txtgezinsnaam")
    template = loader.get_template("KB/export/members.csv")
    context = Context({
        'members': members,
    })
    
    response = HttpResponse() 
    filename = "leden_%s.csv" % (datetime.datetime.now().strftime("%Y%m%d"))
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'text/csv; charset=utf-8'
    # Add UTF-8 'BOM' signature, otherwise Excel will assume the CSV file
    # encoding is ASCII and special characters will be mangled
    response.write("\xEF\xBB\xBF")
    response.write(template.render(context))

    return response

@login_required
def handleExportElection(request):
    list = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.ACTIEF)
    list = list.filter(idlidmaatschapvorm=LidmaatschapVorm.BELIJDEND)
    list = list.exclude(idgezinsrol=GezinsRol.KIND)
    list = list.order_by("idgezin__txtgezinsnaam", "idgezinsrol")
    
    template = loader.get_template("KB/export/election.html")
    context = Context({
        'list': list,
    })
    
    response = HttpResponse() 
    filename = "stemlijst_%s.doc" % (datetime.datetime.now().strftime("%Y%m%d"))
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-word'
    # Add UTF-8 'BOM' signature, otherwise Excel will assume the CSV file
    # encoding is ASCII and special characters will be mangled
    response.write("\xEF\xBB\xBF")
    response.write(template.render(context))

    return response

@login_required
def handleExportBirthdays(request):
    if (request.method == "POST"):
        birthdays_form = BirthdaysForm(request.POST)
        # Assume valid - if not, constrain client side better
        birthdays_form.is_valid()        
        
        today = datetime.date.today()
        date_from = birthdays_form.cleaned_data["date_from"]
        date_to = birthdays_form.cleaned_data["date_to"]
        category = birthdays_form.cleaned_data["category"]

        # Initial list
        list = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.ACTIEF)
        list = list.filter(dtmgeboortedatum__isnull=False)
        
        # We can't select members with birthdates within a certain range 
        # using the default querying methods, because we're looking at a
        # 'sub set' of the birthdate - the month and day. 
        birthday_members = []
        for persoon in list:
            born = persoon.dtmgeboortedatum
            
            # Check if date of birth is present
            if (born):
                # Present. Determine if the birthday (not the same as 
                # date of birth) lies in the specified period.
                try: 
                    # Determine birthday from date of birth
                    birthday = born.replace(year=date_to.year)
                except ValueError:
                    # Raised when birth date is February 29 and the current year is not a leap year
                    birthday = born.replace(year=date_to.year, day=born.day-1)
                
                # Check if birthday is in range
                if (birthday >= date_from and birthday <= date_to):
                    # In range, store birthday
                    persoon.birthday = birthday
                
                # Birthday not in range, but it could be that the start date 
                # lies in a previous year.
                elif (date_from.year < date_to.year):
                    # Try again with the birthday of the previous year
                    try:
                        birthday = born.replace(year=date_to.year-1)
                    except ValueError:
                        # Raised when birth date is February 29 and the current year is not a leap year
                        birthday = born.replace(year=date_to.year-1, day=born.day-1)
                    
                    # Check if birthday is in range 
                    if (birthday >= date_from and birthday <= date_to):
                        # In range, store birthday
                        persoon.birthday = birthday
                    else: 
                        # Not in range
                        persoon.birthday = None
                else:
                    # Not in range
                    persoon.birthday = None
                
                # CHeck if person has birthday
                if (persoon.birthday):    
                    persoon.age = persoon.calculate_age(persoon.birthday)
                    
                    # Check if age fits in category
                    if (persoon.age <= 12 and category == BirthdaysForm.CATEGORY_LTE12
                        or persoon.age > 12 and category == BirthdaysForm.CATEGORY_GT12):
                        # Append person to list of birthday people
                        birthday_members.append(persoon)                        
        
        # Order list by birthday
        birthday_members.sort(key=lambda member: member.birthday)
    
        template = loader.get_template("KB/export/birthdays.html")
        context = Context({
            'list': birthday_members,
        })
        
        response = HttpResponse() 
        filename = "verjaardagen_%s.doc" % (datetime.datetime.now().strftime("%Y%m%d"))
        response['Content-Disposition'] = 'attachment; filename='+filename
        response['Content-Type'] = 'application/vnd.ms-word'
        # Add UTF-8 'BOM' signature, otherwise Excel will assume the CSV file
        # encoding is ASCII and special characters will be mangled
        response.write("\xEF\xBB\xBF")
        response.write(template.render(context))
    
        return response
    
@login_required
def handleExportEmail(request):
    members = Persoon.objects.filter(idlidmaatschapstatus=LidmaatschapStatus.ACTIEF)
    members = members.order_by("idgezin__txtgezinsnaam")
    
    response = HttpResponse() 
    filename = "emailadressen_%s.txt" % (datetime.datetime.now().strftime("%Y%m%d"))
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'text/plain; charset=utf-8'
    for persoon in members:
        if (persoon.txtemailadres):
            response.write(persoon.txtemailadres.lower())
            response.write("\r\n")

    return response

