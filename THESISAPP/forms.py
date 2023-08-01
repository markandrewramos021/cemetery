from enum import unique
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import *
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.utils.safestring import mark_safe

class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password2")

class SignupForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField(label="Confirm Password")
    is_client = forms.BooleanField(initial=True, required=True)
    birth = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = forms.ChoiceField(choices=gender_choices)
    contacts = forms.CharField()
    address = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2','is_admin','birth','gender','contacts','address','is_client')

class InquiryFormForm(forms.ModelForm):
    lot_type_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment Type','Apartment Type')]
    
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    lot_type = forms.ChoiceField(choices= lot_type_choices, widget=forms.RadioSelect, required=True)
    phase = forms.CharField()
    block = forms.CharField()
    lotno = forms.CharField()
    terms = forms.ChoiceField(choices= terms_choices, widget=forms.RadioSelect, required=True)
    fullname = forms.CharField()
    birth = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = forms.ChoiceField(choices=gender_choices)
    contacts = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = InquiryFormModel
        fields = ('lot_type','phase','block','lotno','terms','fullname','birth','gender','contacts','address','email')

        def contacts(self):
            n = self.cleaned_data.get('contacts')
            allowed_characters = '0123456789'
            for char in n:
                if char not in allowed_characters:
                    raise forms.ValidationError("Please only use numbers")
            return n

class NoticeForm(forms.Form):
    client = forms.CharField()
    receiver = forms.CharField()
    content = forms.CharField()

class ApplicationFormForm(forms.ModelForm):
    # pk = forms.IntegerField()
    date = forms.DateField()
    phase = forms.CharField()
    block = forms.CharField()
    lotno = forms.CharField()
    fullname = forms.CharField()
    birth = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = forms.ChoiceField(choices=gender_choices)
    contacts = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = ApplicationFormModel
        fields = ('date','phase','block','lotno','fullname','birth','gender','contacts','address','email')

class BuyersFormForm(forms.ModelForm):
    lot_type_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),]
    
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    # pk = forms.IntegerField()
    lot_type = forms.ChoiceField(choices= lot_type_choices, widget=forms.RadioSelect, required=True)
    phase = forms.CharField()
    block = forms.CharField()
    lotno = forms.CharField()
    terms = forms.ChoiceField(choices= terms_choices, widget=forms.RadioSelect, required=True)
    fullname = forms.CharField()
    birth = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = forms.ChoiceField(choices=gender_choices)
    contacts = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = BuyersFormModel
        fields = ('lot_type','phase','block','lotno','terms','fullname','birth','gender','contacts','address','email')

        def contacts(self):
            n = self.cleaned_data.get('contacts')
            allowed_characters = '0123456789'
            for char in n:
                if char not in allowed_characters:
                    raise forms.ValidationError("Please only use numbers")
            return n

class BookAppointmentForm(forms.ModelForm):
    reason = forms.CharField()
    fullname = forms.CharField()
    contacts = forms.CharField()
    email = forms.EmailField()
    date = forms.DateField()

    class Meta:
        model = BookAppointmentModel
        fields = ('reason', 'fullname','contacts','email','date')

        def contacts(self):
            n = self.cleaned_data.get('contacts')
            allowed_characters = '0123456789'
            for char in n:
                if char not in allowed_characters:
                    raise forms.ValidationError("Please only use numbers")
            return n

class LotOrderForm(forms.ModelForm):
    paid_date = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    due_date = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    
    class Meta:
        model=LotOrder
        fields = ('customer','product','terms','pay','balance','paid_date','due_date','status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].disabled = True

class NotifierForm(forms.Form):
    email = forms.CharField()
    name = forms.CharField()
    totalamountdue = forms.FloatField()
    duedate = forms.DateField(widget=DatePickerInput(attrs={'class':'form-control'}))

class ProductForm(forms.ModelForm):
    lot_type_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment','Apartment')]

    lot = forms.ChoiceField(choices= lot_type_choices, required=False)

    class Meta:
        model = Product
        fields = ('lot','phase','block','lotno','latitude','longitude')

class DeceasedForm(forms.ModelForm):
    deceased = forms.CharField()
    born = forms.DateField(widget=DatePickerInput(attrs={'class':'form-control'}))
    died = forms.DateField(widget=DatePickerInput(attrs={'class':'form-control'}))

    class Meta:
        model = Deads
        fields = ('owner','deceased','born','died')
        
    def __init__(self, user, *args, **kwargs):
        super(DeceasedForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = LotOrder.objects.filter(status='Fully Paid')


class PaymentHistoryForm(forms.ModelForm):
    paid_date = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))
    due_date = forms.DateTimeField(required=False,widget=DatePickerInput(attrs={'class':'form-control'}))

    class Meta:
        model=PaymentHistory
        fields = ('customer','product','terms','pay','balance','paid_date','due_date','status')
