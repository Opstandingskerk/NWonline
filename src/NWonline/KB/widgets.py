###############################################################################
# File: NWonline/KB/widgets.py
# Author: Lukas Batteau
# Description: Custom form widgets 
# 
###############################################################################
from NWonline import settings
from django import forms
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class AutoCompleteSelect(widgets.Select):
    """
    Custom form widget, displaying an autocomplete text input that is connected
    to the original select.
    """
    def __init__(self, attrs=None, choices=()):
        super(AutoCompleteSelect, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        # Make original hidden
        if (attrs):
            attrs["style"] = "display: none"
        else:
            attrs = {"style": "display: none"}
            
        # Create original select field.
        select = super(AutoCompleteSelect, self).render(name, value, attrs, choices)

        # Add auto complete field
        name_auto = name + "_auto"
        attrs_auto = {"id": attrs["id"]+"_auto" }
        final_attrs = self.build_attrs(attrs_auto, type="text", name=name_auto)
        
        autocomplete = u"""<input%s onClick="this.value=''"/>""" % widgets.flatatt(final_attrs)
        
        javascript = u"""<script language="javascript">
        $(document).ready(function(){
            select_autocomplete("%s", "%s");
        });</script>""" % ("#%s" % (attrs_auto["id"]), "#%s" % (attrs["id"]))
        
        
        return mark_safe("%s %s %s" % (select, autocomplete, javascript))

class SelectWithPopup(forms.Select):

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPopup, self).render(name, *args, **kwargs)
        model = self.choices.queryset.model.__name__
        form = eval("%sForm" % (model))
        popupplus = render_to_string("KB/add_related_popup_link.html", {'form': form, 'model': model})
        return html+popupplus

class MultipleSelectWithPopup(forms.SelectMultiple):

    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPopup, self).render(name, *args, **kwargs)
        popupplus = render_to_string("KB/add_related_popup_link.html", {'field': name})
        return html+popupplus
    
class DatePicker(widgets.DateInput):

    def render(self, name, value, attrs=None):
        html = super(DatePicker, self).render(name, value, attrs)
        jquery = u"""<script language="javascript">
        $(document).ready(function(){
            $('#%s').datepicker({ dateFormat: '%s' });
        });</script>""" % (attrs["id"], settings.DATE_FORMAT_JQUERY)
        return html+jquery

