from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_countries import widgets, countries
from django_countries.fields import CountryField
from .models import Warehouse, Part

PAYMENT_OPTIONS = [("1", "First"), ("2", "Second")]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SearchParts(forms.Form):
    part_name = forms.CharField(label='Enter part name', max_length=100)


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    # both solutions below are ok
    # country = forms.ChoiceField(widget=widgets.CountrySelectWidget, choices=countries)  # -> handled with django-countries
    country = CountryField(blank_label="select country").formfield()  # -> handled with django-countries
    zip = forms.CharField()
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_information_for_later = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTIONS)


# class EnlistPartOnlineForm(forms.Form):
#     warehouse = forms.Select(choices=Warehouse.objects.all())
#     producer_name = forms.CharField(max_length=100)
#     part_name = forms.CharField(max_length=100)
#     car = forms.CharField(max_length=100)
#     price_netto = forms.FloatField()
#     amount = forms.IntegerField()
#     slug = forms.SlugField()
#     description = forms.CharField(max_length=5000)
#     photo = forms.ImageField(allow_empty_file=True, required=False)


class EnlistPartOnlineForm(ModelForm):
    class Meta:
        model = Part
        fields = ['warehouse', 'producer_name', 'part_name', 'car', 'price_netto', 'amount', 'slug', 'description',
                  'photo']

    photo = forms.ImageField(required=False)