import django_filters
from django import forms
from .models import *
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.db.models import ForeignKey

class buyersFilter(django_filters.FilterSet):
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche')]
    
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    lot_type = django_filters.ChoiceFilter(empty_label='Select Lot Type',choices=lot_choices)
    terms = django_filters.ChoiceFilter(empty_label='Terms',choices=terms_choices)
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')
    class Meta:
        model = BuyersFormModel
        fields = '__all__'

class buyerslogsFilter(django_filters.FilterSet):
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche')]
    
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    lot_type = django_filters.ChoiceFilter(empty_label='Select Lot Type',choices=lot_choices)
    terms = django_filters.ChoiceFilter(empty_label='Terms',choices=terms_choices)
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')
    fullname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = BuyersFormLogs
        fields = '__all__'

class appointmentFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(widget=DatePickerInput(attrs={'class':'form-control'}))
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    reason = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = BookAppointmentModel
        fields = '__all__'
class appointmentlogsFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(widget=DatePickerInput(attrs={'class':'form-control'}))
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    status_choices=[('Approved','Approved'),
                      ('Resched','Resched')]
    status = django_filters.ChoiceFilter(empty_label='Status',choices=status_choices)

    class Meta:
        model = BookAppointmentLogs
        fields = '__all__'

class clientpaymentFilter(django_filters.FilterSet):
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]
    
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment','Apartment')]

    terms = django_filters.ChoiceFilter(empty_label='Terms',choices=terms_choices)
    customer = django_filters.CharFilter(field_name='customer__username',lookup_expr='icontains')
    product_lottype = django_filters.ChoiceFilter(empty_label='Lot Type:',choices=lot_choices,field_name='product__lot')
    product_phase = django_filters.NumberFilter(field_name='product__phase')
    product_block = django_filters.NumberFilter(field_name='product__block')
    product_lotno = django_filters.CharFilter(field_name='product__lotno')
    due_date = django_filters.DateFilter(widget=DatePickerInput(attrs={'class':'form-control','onfocus':'(this.type=date)'}))
    paid_date = django_filters.DateFilter(widget=DatePickerInput(attrs={'class':'form-control'}))

    class Meta:
        model = LotOrder
        fields = '__all__'

class inquiryFilter(django_filters.FilterSet):
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment Type','Apartment Type')]

    lot_type = django_filters.ChoiceFilter(empty_label='Select Lot Type',choices=lot_choices)
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')
    lotno = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = InquiryFormModel
        fields = '__all__'

class inquirylogsFilter(django_filters.FilterSet):
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment Type','Apartment Type')]

    fullname = django_filters.CharFilter(lookup_expr='icontains')
    lot_type = django_filters.ChoiceFilter(empty_label='Select Lot Type',choices=lot_choices)
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')
    lotno = django_filters.CharFilter(lookup_expr='icontains')
    status_choices=[('Approved','Approved'),
                      ('Declined','Declined')]
    status = django_filters.ChoiceFilter(empty_label='Status',choices=status_choices)
    class Meta:
        model = InquiryFormLogs
        fields = '__all__'
        
        
class productFilter(django_filters.FilterSet):
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment','Apartment')]

    lot = django_filters.ChoiceFilter(empty_label='Select Lot Type',choices=lot_choices)
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')
    lotno = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = '__all__'

class applicationFilter(django_filters.FilterSet):
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = ApplicationFormModel
        fields = '__all__'

class applicationlogsFilter(django_filters.FilterSet):
    phase = django_filters.NumberFilter(lookup_expr='icontains')
    block = django_filters.NumberFilter(lookup_expr='icontains')
    lotno = django_filters.CharFilter(lookup_expr='icontains')
    status_choices=[('Approved','Approved'),
                      ('Declined','Declined')]
    status = django_filters.ChoiceFilter(empty_label='Status',choices=status_choices)

    class Meta:
        model = ApplicationFormLogs
        fields = '__all__'

class deadsFilter(django_filters.FilterSet):
    lot_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment','Apartment')]

    deceased = django_filters.CharFilter(lookup_expr='icontains')
    lot_lottype = django_filters.ChoiceFilter(empty_label='Lot Type:',choices=lot_choices,field_name='owner__product__lot')
    lot_phase = django_filters.NumberFilter(field_name='owner__product__phase')
    lot_block = django_filters.NumberFilter(field_name='owner__product__block')
    lot_lotno = django_filters.CharFilter(field_name='owner__product__lotno')

    class Meta:
        model = Deads
        fields = '__all__'