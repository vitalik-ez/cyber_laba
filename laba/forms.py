from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

#class DateInput(forms.DateInput):
#	input_type = 'date'

#class DateForm(forms.Form):
#	date_1 = forms.DateField(widget=DateInput)
#	date_2 = forms.DateField(widget=DateInput)



class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )