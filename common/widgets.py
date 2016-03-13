# -*- coding: utf-8 -*-
# widgets.py
from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms

import datetime, time
from django.utils.safestring import mark_safe


class CalendarWidget(forms.widgets.DateInput):
    cal_js = u'''
        <script  type="text/javascript">
            $(function() {
               $("#%s").datepicker({ dateFormat: 'yy-mm-dd' });
            });
        </script>'''
    
    class Media:
        css = {
            'all' : (
                'jqueryui/theme/jquery-ui-1.8.css',
                )
            }
        js = (
            'jquery/jquery-1.4.2.js',
            'jqueryui/jquery-ui-1.8.min.js',
            )

    def render(self, name, value, attrs=None):
        if not attrs.has_key('id'):
            attrs['id'] = u'%s_id' % (name)
        id = attrs['id']
        
        js = CalendarWidget.cal_js % (id)
        input = super(CalendarWidget, self).render(name, value, attrs)
        return mark_safe(input+js)


class CalTimeWidget(forms.widgets.MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes
    useing CalendarWidget for date.
    """
    date_format = CalendarWidget.format
    time_format = forms.widgets.TimeInput.format

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (CalendarWidget(attrs=attrs, format=date_format),
                   forms.widgets.TimeInput(attrs=attrs, format=time_format))
        super(CalTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]


#----------------------------------------------------------------------#

class AutoCompleteText(forms.widgets.TextInput):
    autocomplete_js = '''
<script type="text/javascript">
	$(function() {
		$("#%(id)s").autocomplete({
			source: "%(url)s",
                        minLength: "%(minchars)d"
		});
	});
	</script>
'''

    class Media:
        css = {
            'all' : (
                'jqueryui/theme/jquery-ui-1.8.css',
                )
            }
        js = (
            'jquery/jquery-1.4.2.js',
            'jqueryui/jquery-ui-1.8.min.js',
            )


    def __init__(self, callback, minchars=2, attrs=None):
        super(AutoCompleteText, self).__init__(attrs)
        self.callback = callback
        self.minchars = minchars

    def render(self, name, value, attrs=None):
        if value is None: 
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        final_attrs['autocomplete'] = 'no'

        id = final_attrs['id']
        callback = self.callback
        minchars = self.minchars

        code = self.autocomplete_js %  { 'id' : id, 'url' : callback, 'minchars': minchars }
        output = u'<input%s />%s' % (forms.util.flatatt(final_attrs), code)
        return mark_safe(output)

#----------------------------------------------------------------------#

autocomplete_js = u'''
<div id="%(id)s_choices" class="autocomplete"></div>
<script type="text/javascript">
        new Ajax.Autocompleter("%(id)s", "%(id)s_choices", "%(url)s", {
        paramName: "query", 
        minChars: %(minchars)s,     
        });
</script>
'''

class AutoCompleteText2(forms.widgets.TextInput):
    class Media:
        css = {
            'all': (
                    'css/autocomplete.css',
                    )
            }
        js = ( 'js/prototype.js', 'js/scriptacolous.js',
               'js/effects.js',
               'js/controls.js', 'js/builder.js' )

    def __init__(self, callback, minchars=2, attrs=None):
        super(AutoCompleteText, self).__init__(attrs)
        self.callback = callback
        self.minchars = minchars

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        final_attrs['autocomplete'] = 'no'

        id = final_attrs['id']
        callback = self.callback
        minchars = self.minchars

        code = autocomplete_js %  { 'id' : id, 'url' : callback, 'minchars': minchars }
        output = u'<input%s />%s' % (forms.util.flatatt(final_attrs), code)
        return mark_safe(output)
