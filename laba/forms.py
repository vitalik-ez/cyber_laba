from django import forms
from .models import electricalAppliances

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


class Laba2Form(forms.Form):
    heat_lost = forms.DecimalField(min_value=0, max_value=500, initial=30,label='Питомі тепловтрати будівлі (Вт/м²)',widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    house_area = forms.DecimalField(min_value=0, max_value=2000, initial=80, label='Опалювальна площа будинку (м²) (квартири)',widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    number_people = forms.IntegerField(min_value=1, max_value=20, initial=4, label='Кількість людей', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    incoming_temperature = forms.DecimalField(min_value=0, max_value=100, decimal_places=1, initial=15, label='Температура вхідної води Т (за вмовчуванням 15°C)', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    end_temperature = forms.DecimalField(min_value=0, max_value=100, decimal_places=1, initial=85, label='Кінцеву температуру бака Т (за вмовчуванням 85°C)', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    shower_temperature = forms.DecimalField(min_value=0, max_value=100, initial=80, decimal_places=1, label='Температура води при прийомі душу', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    count_shower = forms.IntegerField(min_value=0, max_value=100, initial=4, label='Кількість прийомів душу на добу', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    count_litters_shower = forms.DecimalField(min_value=0, max_value=200, initial=50,decimal_places=1, label='Кількість літрів води, яка витрачається на прийом душу', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))

    bath_temperature = forms.DecimalField(min_value=0, max_value=100, initial=90, decimal_places=1, label='Температура води при прийомі ванни', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    count_bath = forms.IntegerField(min_value=0, max_value=100, initial=2, label='Кількість прийомів ванни на добу', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))
    count_litters_bath = forms.DecimalField(min_value=0, max_value=300, initial=150, decimal_places=1,  label='Кількість літрів води, яка витрачається на прийом ванни', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))

    air_temperature = forms.DecimalField(min_value=0, max_value=100, initial=20, decimal_places=1, label='Температура повітря всередині будівлі (за вмовчуванням +20°С)', widget=forms.NumberInput(attrs={'class':'form-control col-3',}))



class electricalAppliancesForm(forms.ModelForm):
    class Meta:
        model = electricalAppliances
        fields = '__all__'