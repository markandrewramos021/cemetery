from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
#---------------ADMIN SIDE
    path('Notice/<int:pk>', views.Notice, name='Notice'),
    path('InquiryFormPdf', views.InquiryFormPdf, name='InquiryFormPdf'),
    path('BuyersFormPdf', views.BuyersFormPdf, name='BuyersFormPdf'),
    path('ApplicationFormPdf', views.ApplicationFormPdf, name='ApplicationFormPdf'),
    path('BookAppointmentFormPdf', views.BookAppointmentFormPdf, name='BookAppointmentFormPdf'),
# clerk 1
    path('Inquiry/<int:pk>/<str:email>', views.Inquiry, name='Inquiry'),
    path('InquiryLogs/<int:pk>/<str:email>', views.InquiryLogs, name='InquiryLogs'),
    path('InquiryReject/<int:pk>/<str:email>/<str:lot_type>/<str:phase>/<str:block>/<str:lotno>/<str:fullname>', views.InquiryReject, name='InquiryReject'),
    path('InquiryApprove/<int:pk>/<str:email>/<str:lot_type>/<str:phase>/<str:block>/<str:lotno>/<str:fullname>', views.InquiryApprove, name='InquiryApprove'),
    path('Appointment/<int:pk>/<str:email>', views.Appointment, name='Appointment'),
    path('AppointmentLogs/<int:pk>/<str:email>', views.AppointmentLogs, name='AppointmentLogs'),
    path('AppointmentApprove/<int:pk>/<str:email>/', views.AppointmentApprove, name='AppointmentApprove'),
    path('AppointmentReject/<int:pk>/<str:email>/<str:fullname>', views.AppointmentReject, name='AppointmentReject'),
# clerk 2   
    path('Application/<int:pk>/<str:email>', views.Application, name='Application'),
    path('ApplicationLogs/<int:pk>/<str:email>', views.ApplicationLogs, name='ApplicationLogs'),
    path('ApplicationApprove/<int:pk>/<str:email>/<str:phase>/<str:block>/<str:lotno>/<str:fullname>', views.ApplicationApprove, name='ApplicationApprove'),
    path('ApplicationReject/<int:pk>/<str:email>/<str:phase>/<str:block>/<str:lotno>/<str:fullname>', views.ApplicationReject, name='ApplicationReject'),
    path('BuyersApplication/<int:pk>/<str:email>', views.BuyersApplication, name='BuyersApplication'), 
    path('BuyersApplicationLogs/<int:pk>/<str:email>', views.BuyersApplicationLogs, name='BuyersApplicationLogs'),
    path('BuyersApplicationApprove/<int:pk>/<str:email>/<str:lot_type>/<str:phase>/<str:block>/<str:lotno>/<str:fullname>', views.BuyersApplicationApprove, name='BuyersApplicationApprove'), 
    path('BuyersApplicationReject/<int:pk>/<str:email>/<str:lot_type>/<str:phase>/<str:block>/<str:lotno>/<str:fullname>', views.BuyersApplicationReject, name='BuyersApplicationReject'),  
# clerk 3
    path('ClientPayment/<int:pk>', views.ClientPayment, name='ClientPayment'),
    path('AdminHomepage/<int:pk>', views.AdminHomepage, name='AdminHomepage'),
    path('AddNew/<int:pk>', views.AddNew, name='AddNew'),
    path('AddnewUpdate/<int:pk>', views.AddNewUpdate, name='AddNewUpdate'),
    path('Notifier/<int:pk>', views.Notifier, name='Notifier'),
    path('AddnewDelete/<int:pk>', views.AddNewDelete, name='AddNewDelete'),
    path('AddDeceased/<int:pk>', views.AddDeceased, name='AddDeceased'),
    path('AddDeceasedUpdate/<int:pk>', views.AddDeceasedUpdate, name='AddDeceasedUpdate'),
    path('AddDeceasedDelete/<int:pk>', views.AddDeceasedDelete, name='AddDeceasedDelete'),
    path('LotTable/<int:pk>', views.LotTable, name='LotTable'),
    path('PropertyManagement/<int:pk>', views.PropertyManagement, name='PropertyManagement'),
    path('PropertyManagementUpdate/<int:pk>', views.PropertyManagementUpdate, name='PropertyManagementUpdate'),
    path('PropertyManagementDelete/<int:pk>', views.PropertyManagementDelete, name='PropertyManagementDelete'), 
#---------------END ADMIN SIDE
   
#---------------CLIENT SIDE
    path('', views.Homepage, name='Homepage'),
    path('AboutUs', views.AboutUs, name='AboutUs'),
    path('LotProperty', views.LotProperty, name='LotProperty'),
    path('GraveFinder', views.GraveFinder, name='GraveFinder'),
    path('ContactUs', views.ContactUs, name='ContactUs'),
    path('PrivacyPolicy', views.PrivacyPolicy, name='PrivacyPolicy'),
    path('Help', views.Help, name='Help'),
    path('Login', views.Login, name='Login'),
    path('Signup', views.Signup, name='Signup'),
    path('TermsofPayment', views.TermsofPayment, name='TermsofPayment'),
    path('Logout', views.Logout, name='Logout'),
    path('accounts/login/', views.Logout),
    path('InquiryForm', views.InquiryForm, name='InquiryForm'),
    path('Client/<int:pk>', views.Client, name='Client'),
    path('InstallmentBill/<int:pk>', views.InstallmentBill, name='InstallmentBill'),
    path('PaymentHistory/<int:pk>', views.PaymentHistory, name='PaymentHistory'),
    path('BuyersForm', views.BuyersForm, name='BuyersForm'),
    path('BillSummary/<str:pk>', views.BillSummary, name='BillSummary'),
    path('ApplicationForm', views.ApplicationForm, name='ApplicationForm'),
    path('BookAppointment', views.BookAppointment, name='BookAppointment'),
    path('Property/<int:pk>', views.Property, name='Property'),
    # path('AddDeceasedUpdateClient/<int:pk>', views.AddDeceasedUpdateClient, name='AddDeceasedUpdateClient'),

    #RESET PASSWORD
    path('ResetPassword',
     auth_views.PasswordResetView.as_view(template_name="files/PasswordReset.html"), name="reset_password"),
    path('ResetPasswordSent',
     auth_views.PasswordResetDoneView.as_view(template_name="files/PasswordResetSent.html"), name="password_reset_done"),
    path('Reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="files/PasswordResetForm.html"), name="password_reset_confirm"),
    path('ResetPasswordComplete', 
    auth_views.PasswordResetCompleteView.as_view(template_name="files/PasswordResetDone.html"), name="password_reset_complete"),

    #ChangePass
    path('Password/<int:pk>', views.ChangePassword, name='ChangePassword'),


#---------------END CLIENT SIDE
    
]