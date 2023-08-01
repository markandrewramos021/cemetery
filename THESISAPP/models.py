from email.policy import default
from enum import unique
from random import choices
from secrets import choice
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_client = models.BooleanField('Is client', default=False)
    is_clerk1 = models.BooleanField('Is clerk1', default=False)
    is_clerk2 = models.BooleanField('Is clerk2', default=False)
    is_clerk3= models.BooleanField('Is clerk3', default=False)
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    address = models.CharField(max_length=99, verbose_name='address', null=True)

    def __str__(self):
        return f'{self.username} | {self.first_name} {self.last_name}'
    

class InquiryFormModel(models.Model):
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

    lot_type = models.CharField(max_length=30, choices=lot_type_choices, verbose_name='lot_type')
    phase = models.CharField(max_length=30, verbose_name='phase')
    block = models.CharField(max_length=30, verbose_name='block')
    lotno = models.CharField(max_length=30, verbose_name='lot_no.')
    terms = models.CharField(max_length=30, choices=terms_choices, verbose_name='termsofpayment')
    fullname = models.CharField(max_length=99, verbose_name='fullname')
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts')
    address = models.CharField(max_length=99, verbose_name='address')
    email = models.EmailField(max_length=99, verbose_name='email')

    def __str__(self):
        return f'{self.fullname}'

class ApplicationFormModel(models.Model):
    date = models.DateField(verbose_name='date', null=True)
    phase = models.CharField(max_length=30, verbose_name='phase', null=True)
    block = models.CharField(max_length=30, verbose_name='block', null=True)
    lotno = models.CharField(max_length=30, verbose_name='lot_no.', null=True)
    fullname = models.CharField(max_length=99, verbose_name='fullname', null=True)
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    address = models.CharField(max_length=99, verbose_name='address', null=True)
    email = models.EmailField(max_length=99, verbose_name='email', null=True)

class BuyersFormModel(models.Model):
    lot_type_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche')]
    
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    lot_type = models.CharField(max_length=30, choices=lot_type_choices, verbose_name='lot_type', null=True)
    phase = models.CharField(max_length=30, verbose_name='phase', null=True)
    block = models.CharField(max_length=30, verbose_name='block', null=True)
    lotno = models.CharField(max_length=30, verbose_name='lot_no.', null=True)
    terms = models.CharField(max_length=30, choices=terms_choices, verbose_name='termsofpayment', null=True)
    fullname = models.CharField(max_length=99, verbose_name='fullname', null=True)
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    address = models.CharField(max_length=99, verbose_name='address', null=True)
    email = models.EmailField(max_length=99, verbose_name='email', null=True)

class BookAppointmentModel(models.Model):
    reason = models.CharField(max_length=250, verbose_name='reason', null=True)
    fullname = models.CharField(max_length=250, verbose_name='fullname', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    email = models.CharField(max_length=250, verbose_name='email', null=True)
    date = models.DateField(verbose_name='date', null=True)

class Product(models.Model):
    lot_choices = [('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche'),
                      ('Apartment', 'Apartment')]
    
    lot = models.CharField(max_length=50,choices=lot_choices ,null=True, verbose_name='lot')
    phase = models.CharField(max_length=200, null=True, verbose_name='phase')
    block = models.CharField(max_length=30, null=True, verbose_name='block')
    lotno = models.CharField(max_length=30, null=True, verbose_name='lot_no.')
    latitude = models.CharField(max_length=200, null=True, verbose_name='latitude.')
    longitude = models.CharField(max_length=200, null=True, verbose_name='longitude.')

    def __str__(self):
        return f'{self.lot} Phase:{self.phase} Block:{self.block} Lot No.:{self.lotno}'


class LotOrder(models.Model):
    STATUS = [
        ('Fully Paid', 'Fully Paid'),
        ('Partially Paid','Partially Paid'),
        ('Resell', 'Resell')]

    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='customer', blank=True,default=None)
    product = models.OneToOneField(Product, null=True, on_delete=models.SET_NULL, verbose_name='product')
    terms = models.CharField(max_length=50,choices=terms_choices, null=True, verbose_name='terms', blank=True)
    pay = models.FloatField(null=True, verbose_name='pay', blank=True,default=None)
    balance = models.FloatField(null=True, verbose_name='balance', blank=True,default=None)
    paid_date = models.DateField(null=True,verbose_name='paid date', blank=True,default=None)
    status = models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='status', blank=True,default=None)
    due_date = models.DateField(null=True,verbose_name='due date', blank=True,default=None)

    def __str__(self):
        return f'{self.customer.username} | {self.product.lot} Phase:{self.product.phase} Block:{self.product.block} Lot No.:{self.product.lotno}'

    def calculate(self):
        pay = self.pay
        amount = self.balance

        if pay == None and amount == None:
            print("None")
        else:
            balance = amount-pay

            return balance

    
    def save(self,*args,**kwargs):
        if self.pay == None and self.balance == None:
            print("None")
            super().save(*args, **kwargs)
        else:
            self.balance = float(self.calculate())
            super().save(*args, **kwargs)
        
        if self.balance == 0 and self.terms != None:
            self.status = "Fully Paid"
            super().save(*args, **kwargs)
        elif self.balance != 0 and self.terms != None:
            self.status = "Partially Paid"
            super().save(*args, **kwargs)
        else:
            pass

class Deads(models.Model):
    owner = models.ForeignKey(LotOrder, null=True, on_delete=models.SET_NULL, verbose_name='owner', blank=True,default=None)
    deceased = models.CharField(max_length=200, blank=True, null=True,default=None, verbose_name='deceased.')
    born = models.DateField(null=True,blank=True,default=None, verbose_name='born.')
    died = models.DateField(null=True,blank=True,default=None, verbose_name='died.')

    # def save(self, *args, **kwargs):
    #     if Deads.objects.filter(owner__product__lot='Apartment').count() < 1 and Deads.objects.filter(owner=self.owner):
    #         return super(Deads,self).save(*args,**kwargs)
    #     raise ValidationError("Deceased Limit")

    
class PaymentHistory(models.Model):
    STATUS = [
        ('Fully Paid', 'Fully Paid'),
        ('Partially Paid','Partially Paid')]

    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='customer', blank=True,default=None)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name='product', blank=True,default=None)
    terms = models.CharField(max_length=50,choices=terms_choices, null=True, verbose_name='terms', blank=True)
    pay = models.FloatField(null=True, verbose_name='pay', blank=True,default=None)
    balance = models.FloatField(null=True, verbose_name='balance', blank=True,default=None)
    paid_date = models.DateField(null=True,verbose_name='paid date', blank=True,default=None)
    status = models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='status', blank=True,default=None)
    due_date = models.DateField(null=True,verbose_name='due date', blank=True,default=None)

    def calculate(self):
        pay = self.pay
        amount = self.balance

        if pay == None and amount == None:
            print("None")
        else:
            balance = amount-pay

            return balance

    def save(self,*args,**kwargs):
        if self.pay == None and self.balance == None:
            print("None")
            super().save(*args, **kwargs)
        else:
            self.balance = float(self.calculate())
            super().save(*args, **kwargs)


class BookAppointmentLogs(models.Model):
    reason = models.CharField(max_length=250, verbose_name='reason', null=True)
    fullname = models.CharField(max_length=250, verbose_name='fullname', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    email = models.CharField(max_length=250, verbose_name='email', null=True)
    status = models.CharField(max_length=250, verbose_name='status', null=True)
    date = models.DateField(verbose_name='date', null=True)

class BuyersFormLogs(models.Model):
    lot_type_choices=[('Lawn Lot','Lawn Lot'),
                      ('Mausoleum','Mausoleum'),
                      ('Niche','Niche')]
    
    terms_choices=[('Cash','Cash'),
                   ('1 Year','1 Year'),
                   ('2 Years','2 Years'),
                   ('3 Years','3 Years'),
                   ('Full Down','Full Down'),
                   ('Reservation','Reservation')]

    lot_type = models.CharField(max_length=30, choices=lot_type_choices, verbose_name='lot_type', null=True)
    phase = models.CharField(max_length=30, verbose_name='phase', null=True)
    block = models.CharField(max_length=30, verbose_name='block', null=True)
    lotno = models.CharField(max_length=30, verbose_name='lot_no.', null=True)
    terms = models.CharField(max_length=30, choices=terms_choices, verbose_name='termsofpayment', null=True)
    fullname = models.CharField(max_length=99, verbose_name='fullname', null=True)
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    address = models.CharField(max_length=99, verbose_name='address', null=True)
    email = models.EmailField(max_length=99, verbose_name='email', null=True)
    status = models.CharField(max_length=99, verbose_name='status', null=True)

class ApplicationFormLogs(models.Model):
    date = models.DateField(verbose_name='date', null=True)
    phase = models.CharField(max_length=30, verbose_name='phase', null=True)
    block = models.CharField(max_length=30, verbose_name='block', null=True)
    lotno = models.CharField(max_length=30, verbose_name='lot_no.', null=True)
    fullname = models.CharField(max_length=99, verbose_name='fullname', null=True)
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    address = models.CharField(max_length=99, verbose_name='address', null=True)
    email = models.EmailField(max_length=99, verbose_name='email', null=True)
    status = models.CharField(max_length=99, verbose_name='status', null=True)

class InquiryFormLogs(models.Model):
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

    lot_type = models.CharField(max_length=30, choices=lot_type_choices, verbose_name='lot_type', null=True)
    phase = models.CharField(max_length=30, verbose_name='phase', null=True)
    block = models.CharField(max_length=30, verbose_name='block', null=True)
    lotno = models.CharField(max_length=30, verbose_name='lot_no.', null=True)
    terms = models.CharField(max_length=30, choices=terms_choices, verbose_name='termsofpayment', null=True)
    fullname = models.CharField(max_length=99, verbose_name='fullname', null=True)
    birth = models.DateField(verbose_name='birth', null=True)
    gender_choices=[('Female','Female'),
                      ('Male','Male')]
    gender = models.CharField(max_length=30,choices=gender_choices, verbose_name='gender', null=True)
    contacts = models.CharField(max_length=11, verbose_name='contacts', null=True)
    address = models.CharField(max_length=99, verbose_name='address', null=True)
    email = models.EmailField(max_length=99, verbose_name='email', null=True)
    status = models.CharField(max_length=99, verbose_name='status', null=True)
