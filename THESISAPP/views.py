from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http.response import HttpResponse
from .filters import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from django.http import FileResponse

#EMAIL
from django.core.mail import EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
#MODELS
from .models import *
from .models import InquiryFormModel as inquire
from .models import PaymentHistory as PaymentHistory2
#paginator
from django.core.paginator import Paginator
def Homepage(request):
    return render(request, 'files/Homepage.html')

def Login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect(f'AdminHomepage/{user.pk}')
            elif user is not None and user.is_client:
                login(request, user)
                return redirect(f'Client/{user.pk}')
            elif user is not None and user.is_clerk1:
                login(request,user)
                return redirect(f'Inquiry/{user.pk}/{user.email}')
            elif user is not None and user.is_clerk2:
                login(request,user)
                return redirect(f'AdminHomepage/{user.pk}')
            elif user is not None and user.is_clerk3:
                login(request,user)
                return redirect(f'Application/{user.pk}/{user.email}')
            else:
                msg= 'Invalid Credentials'
        else:
            msg = 'Error Validating Form'
    return render(request, 'files/Login.html',{'form': form, 'msg': msg})

def Signup(request):
    msg = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'User Created'
            return redirect('Login')
        else:
            error_text = '<ul style="display:flex;'\
              'flex-direction:column;list-style-type:none;"'
            for msg_list in form.errors.values():
                for msg in msg_list:
                    error_text += f'<li>{msg}</li>'
            error_text += '</ul>'
            messages.error(request, mark_safe(error_text))
    else:
        form = SignupForm()
    return render(request, 'files/Signup.html', {'form': form, 'msg': msg})

# --------------- CLIENT
@login_required(login_url='/accounts/login/')
def ChangePassword(request, pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.SUCCESS, 'Your password was successfully updated!')
            return redirect('Client', pk=pk)
        else:
            error_text = '<ul style="display:flex;'\
              'flex-direction:column;list-style-type:none;"'
            for msg_list in form.errors.values():
                for msg in msg_list:
                    error_text += f'<li>{msg}</li>'
            error_text += '</ul>'
            messages.error(request, mark_safe(error_text))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'files/ChangePassword.html', {
        'form': form
    })

@login_required(login_url='/accounts/login/')
def Client(request,pk):
    if request.user.is_authenticated and request.user.is_client:
        print("Client Page")
        a = User.objects.get(pk=pk)
        orders = a.lotorder_set.exclude(balance=0)
        no_display = 'N/A'
        new_order = LotOrder.objects.filter(customer_id=pk).exclude(balance=0)
        nn = LotOrder.objects.filter(customer_id=pk).exclude(balance=0).exists()
        print(nn)

        if LotOrder.objects.filter(customer_id=pk).exclude(balance=0).exists() is True:
            new_order = LotOrder.objects.filter(customer_id=pk).exclude(balance=0)
            no_display = ''
        else:
            no_display
            

    else:
        return redirect('Logout')
    return render(request, 'files/Client.html', {'a':a,'orders':orders,'new_order':new_order,'no_display':no_display})

def ApplicationForm(request):
    form = ApplicationFormForm()
    if request.method == 'POST':
        form = ApplicationFormForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success')

    return render(request, 'files/ApplicationForm.html')

def BookAppointment(request):
    form = BookAppointmentForm()
    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success')

    return render(request, 'files/BookAppointment.html')
    
def BuyersForm(request):
    form = BuyersFormForm()
    if request.method == 'POST':
        form = BuyersFormForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success')

    return render(request, 'files/BuyersForm.html')

@login_required(login_url='/accounts/login/')
def BillSummary(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        print ("Bill Summary Page")
        a = User.objects.get(id=pk)
        orders = a.lotorder_set.all()
    else:
        return redirect('Logout')
    return render(request, 'files/BillSummary.html',{'a':a,'orders':orders})

@login_required(login_url='/accounts/login/')
def InstallmentBill(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        print ("Success")
        a = User.objects.filter(pk=pk)
    else:
        return redirect('Logout')
    return render(request, 'files/InstallmentBill.html',{'a':a})

@login_required(login_url='/accounts/login/')
def PaymentHistory(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        print ("Success")
        a = User.objects.get(pk=pk)
        history = a.paymenthistory_set.all()
    else:
        return redirect('Logout')
    return render(request, 'files/PaymentHistory.html', {'a':a,'history':history})

@login_required(login_url='/accounts/login/')
def Property(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        a = User.objects.get(pk=pk)
        display = a.lotorder_set.filter(balance=0)

    else:
        return redirect('Logout')
    return render(request, 'files/Property.html',{'a':a,'display':display})

# def AddDeceasedUpdateClient(request,pk):
#     if request.user.is_authenticated and request.user.is_client:
#         b = LotOrder.objects.filter(customer_id=request.user.id).values_list('id',flat=True).first()
#         deads = Deads.objects.filter(owner_id=b).values_list('id',flat=True).first()
#         print(deads)
#         dead = Deads.objects.get(pk=deads)
#         user = request.user
#         form = DeceasedForm(user,instance=dead)
#         if request.method == 'POST':
#             form = DeceasedForm(user,request.POST, instance=dead)
#             if form.is_valid():
#                 deceased1 = form.cleaned_data.get('deceased')
#                 born1 = form.cleaned_data.get('born')
#                 died1 = form.cleaned_data.get('died')
#                 Deads.objects.filter(pk=pk).update(deceased=deceased1, born=born1, died=died1)
#                 messages.success(request, 'Successfully Updated'),
#                 fail_silently=True
#                 return redirect('Property', pk=pk)
#             else:
#                 messages.error(request, 'Invalid Input'),
#                 fail_silently=True
#     else:
#         return redirect('Logout')
#     return render(request, 'files/AddDeceased.html',{'form':form,'dead':dead})
# ---------- END CLIENT

# ---------- ADMIN
#-----CLERK1
@login_required(login_url='/accounts/login/')
def Appointment(request, pk,email):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        context= {}
        buyers = BuyersFormModel.objects.all().count()
        inquiries = InquiryFormModel.objects.all().count()
        invitee = BookAppointmentModel.objects.all().count()
        applicants = ApplicationFormModel.objects.all().count()
        overall = buyers+inquiries+invitee+applicants
        
        if overall > 0:
            overall = '!'
        else:
            overall = ''
        
        if invitee > 0:
            invitee = '!'
        else:
            invitee = ''

        if inquiries > 0:
            inquiries = '!'
        else:
            inquiries = ''

        if buyers > 0:
            buyers = '!'
        else:
            buyers = ''

        if applicants > 0:
            applicants = '!'
        else:
            applicants = ''
        context['overall'] = overall
        filter_all = appointmentFilter(request.GET, queryset=BookAppointmentModel.objects.exclude(email=None))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        context['buyers'] = buyers
        context['inquiries'] = inquiries
        context['invitee'] = invitee
        context['applicants'] = applicants
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Appointment Page!')
        return redirect('AdminHomepage',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        messages.add_message(request, messages.ERROR, 'You cannot access Appointment Page!')
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')
    return render(request, 'files/Appointment.html', context=context)

def AppointmentLogs(request, pk,email):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        context= {}
        filter_all = appointmentlogsFilter(request.GET, queryset=BookAppointmentLogs.objects.exclude(email=None))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Appointment Page!')
        return redirect('AdminHomepage',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        messages.add_message(request, messages.ERROR, 'You cannot access Appointment Page!')
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')
    return render(request, 'files/AppointmentLogs.html', context=context)


@login_required(login_url='/accounts/login/')
def AppointmentApprove(request, pk, email):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = BookAppointmentModel.objects.filter(pk=pk).values_list('email', flat=True).first()
        date = BookAppointmentModel.objects.filter(pk=pk).values_list('date', flat=True).first()
        fname = BookAppointmentModel.objects.filter(pk=pk).values_list('fullname', flat=True).first()
        contacts = BookAppointmentModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        reason = BookAppointmentModel.objects.filter(pk=pk).values_list('reason', flat=True).first()
        send_mail(
                'From Himlayang General Trias Management',
                f'Hello {fname},\n\n'+
                f'Thanks for reaching out to us. We appreciate your interest in Himlayang General Trias Cemetery. This is to confirm that we have successfully received your request for Appointment. \n\n'+
                f'We want to inform you that you have been appointed on {date} and at least go between the opening time, 8 am till 5 pm closing, so that the staff will assist you. Please arrive at General Trias City Hall on your scheduled day. Just show this message, so they know you have booked an appointment.\n\n'+
                'If you need immediate assistance or have any further questions, feel free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com\n\n'+
                'Sincerely,\n\nGeneral Trias Managemanent',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        BookAppointmentLogs.objects.create(fullname=fname,contacts=contacts,email=b,reason=reason,date=date,status='Approved')
        BookAppointmentModel.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('Appointment', pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('ClientPayment',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')
 
@login_required(login_url='/accounts/login/')
def AppointmentReject(request,pk,email,fullname):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        a = User.objects.filter(pk=pk)
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = BookAppointmentModel.objects.filter(pk=pk).values_list('email', flat=True).first()
        date = BookAppointmentModel.objects.filter(pk=pk).values_list('date', flat=True).first()
        fname = BookAppointmentModel.objects.filter(pk=pk).values_list('fullname', flat=True).first()
        contacts = BookAppointmentModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        reason = BookAppointmentModel.objects.filter(pk=pk).values_list('reason', flat=True).first()
        send_mail(
                'From Himlayang General Trias Management',
                f'Hello {fname},\n\n'+
                f'Thanks for reaching out to us. We appreciate your interest in Himlayang General Trias Cemetery. After reviewing your request date. It turned out that we were fully booked on that day. We regret to inform you that your appointment request has been denied. \n\n'+
                'If you need immediate assistance or have any further questions, feel free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com\n\n'+
                'Sincerely,\n\nGeneral Trias Managemanent',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        BookAppointmentLogs.objects.create(fullname=fname,contacts=contacts,email=b,reason=reason,date=date,status='Resched')
        BookAppointmentModel.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('Appointment', pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('ClientPayment',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def Inquiry(request, pk, email):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        context= {}
        buyers = BuyersFormModel.objects.all().count()
        inquiries = InquiryFormModel.objects.all().count()
        invitee = BookAppointmentModel.objects.all().count()
        applicants = ApplicationFormModel.objects.all().count()
        overall = buyers+inquiries+invitee+applicants
        
        if overall > 0:
            overall = '!'
        else:
            overall = ''
        
        if invitee > 0:
            invitee = '!'
        else:
            invitee = ''

        if inquiries > 0:
            inquiries = '!'
        else:
            inquiries = ''

        if buyers > 0:
            buyers = '!'
        else:
            buyers = ''

        if applicants > 0:
            applicants = '!'
        else:
            applicants = ''
        context['overall'] = overall
        filter_all = inquiryFilter(request.GET, queryset=inquire.objects.all())
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 10)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        
        #------

        filter_all1 = clientpaymentFilter(request.GET, queryset=LotOrder.objects.filter(terms=None))
        context['filter_all1'] = filter_all1

        paginated_filter_all1 = Paginator(filter_all1.qs, 11)
        page_number1 = request.GET.get('page')
        all_page_obj1 = paginated_filter_all1.get_page(page_number1)

        context['all_page_obj1'] = all_page_obj1
        context['buyers'] = buyers
        context['inquiries'] = inquiries
        context['invitee'] = invitee
        context['applicants'] = applicants
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Inquiry Page!')
        return redirect('AdminHomepage',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        messages.add_message(request, messages.ERROR, 'You cannot access Inquiry Page!')
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')
    return render(request, 'files/Inquiry.html',context=context)

@login_required(login_url='/accounts/login/')
def InquiryLogs(request, pk, email):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        context= {}
        filter_all = inquirylogsFilter(request.GET, queryset=InquiryFormLogs.objects.all())
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 10)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        
    
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Inquiry Page!')
        return redirect('AdminHomepage',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        messages.add_message(request, messages.ERROR, 'You cannot access Inquiry Page!')
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')
    return render(request, 'files/InquiryLogs.html',context=context)

@login_required(login_url='/accounts/login/')
def InquiryApprove(request, pk, email, lot_type,phase,block,lotno,fullname):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = InquiryFormModel.objects.filter(email=email).values_list('email', flat=True).first()
        lot = InquiryFormModel.objects.filter(pk=pk).values_list('lot_type', flat=True).first()
        p = InquiryFormModel.objects.filter(phase=phase).values_list('phase', flat=True).first()
        b1 = InquiryFormModel.objects.filter(block=block).values_list('block', flat=True).first()
        l = InquiryFormModel.objects.filter(lotno=lotno).values_list('lotno', flat=True).first()
        fname = InquiryFormModel.objects.filter(pk=pk).values_list('fullname', flat=True).first()
        terms = InquiryFormModel.objects.filter(pk=pk).values_list('terms', flat=True).first()
        birth = InquiryFormModel.objects.filter(pk=pk).values_list('birth', flat=True).first()
        gender = InquiryFormModel.objects.filter(pk=pk).values_list('gender', flat=True).first()
        contacts = InquiryFormModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        address = InquiryFormModel.objects.filter(pk=pk).values_list('address', flat=True).first()
        print(fname)

        send_mail(
                'From Himlayang General Trias Management',
                f'Dear {fname},\n\nGood day!\n\n' +
                f'After reviewing your request, we want to inform you that it was approved. The lot ({lot} Phase:{p} Block:{b1} Lot No.:{l}) you inquired about is currently available. If you do not get it right away, someone else may. Please sign up or sign in as a client and choose Buyers Form at the Application button if you select one of these choices, Lawn Lot, Mausoleum, and Niche; if not, choose Application Form for Apartment Type. Please fill out the form you select, and in the Location field, put {lot} Phase:{p} Block:{b1} Lot No.:{l}. Thank you!\n\n'+
                'Thank you for inquiring at the Himlayang General Trias Cemetery.\n\n'
                'If you need immediate assistance or have any further questions, you can make an appointment with the Office of Himlayang Gen. Trias and free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com\n\n'+
                'Regards,\nGeneral Trias Management',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        InquiryFormLogs.objects.create(
            lot_type=lot,phase=p,block=b1,lotno=l,terms=terms,fullname=fname,birth=birth,gender=gender,contacts=contacts,address=address,email=b,status='Approved')
        InquiryFormModel.objects.filter(id=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('ClientPayment',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def InquiryReject(request,pk,email,lot_type,phase,block,lotno,fullname):
    if request.user.is_authenticated and request.user.is_clerk1 or request.user.is_admin:
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = InquiryFormModel.objects.filter(email=email).values_list('email', flat=True).first()
        lot = InquiryFormModel.objects.filter(pk=pk).values_list('lot_type', flat=True).first()
        p = InquiryFormModel.objects.filter(phase=phase).values_list('phase', flat=True).first()
        b1 = InquiryFormModel.objects.filter(block=block).values_list('block', flat=True).first()
        l = InquiryFormModel.objects.filter(lotno=lotno).values_list('lotno', flat=True).first()
        fname = InquiryFormModel.objects.filter(fullname=fullname).values_list('fullname', flat=True).first()
        terms = InquiryFormModel.objects.filter(pk=pk).values_list('terms', flat=True).first()
        birth = InquiryFormModel.objects.filter(pk=pk).values_list('birth', flat=True).first()
        gender = InquiryFormModel.objects.filter(pk=pk).values_list('gender', flat=True).first()
        contacts = InquiryFormModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        address = InquiryFormModel.objects.filter(pk=pk).values_list('address', flat=True).first()
        send_mail(
                'From Himlayang General Trias Management',
                f'Dear {fname},\n\nGood day!\n\n' +
                f'We want to inform you that we have declined your request upon checking on it. The lot ({lot} Phase:{p} Block:{b1} Lot No.:{l}) you inquired about is already taken. Try to inquire about other lots. Thank you for inquiring at the Himlayang General Trias Cemetery, and we are sorry for the inconvenience.\n\n'+
                'If you need immediate assistance or have any further questions, you can make an appointment with the Office of Himlayang Gen. Trias and free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com \n\n'+
                'Regards,\nGeneral Trias Management',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        InquiryFormLogs.objects.create(
            lot_type=lot,phase=p,block=b1,lotno=l,terms=terms,fullname=fname,birth=birth,gender=gender,contacts=contacts,address=address,email=b,status='Declined')
        InquiryFormModel.objects.filter(id=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('ClientPayment',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk,email=email)
    else:
        return redirect('Logout')

#-----ENDCLERK1

#---CLERK3
@login_required(login_url='/accounts/login/')
def BuyersApplication(request, pk, email):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk3:
        context= {}
        buyers = BuyersFormModel.objects.all().count()
        inquiries = InquiryFormModel.objects.all().count()
        invitee = BookAppointmentModel.objects.all().count()
        applicants = ApplicationFormModel.objects.all().count()
        overall = buyers+inquiries+invitee+applicants
        
        if overall > 0:
            overall = '!'
        else:
            overall = ''
        
        if invitee > 0:
            invitee = '!'
        else:
            invitee = ''

        if inquiries > 0:
            inquiries = '!'
        else:
            inquiries = ''

        if buyers > 0:
            buyers = '!'
        else:
            buyers = ''

        if applicants > 0:
            applicants = '!'
        else:
            applicants = ''
        context['overall'] = overall
        filter_all = buyersFilter(request.GET, queryset=BuyersFormModel.objects.exclude(fullname=None))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        context['buyers'] = buyers
        context['inquiries'] = inquiries
        context['invitee'] = invitee
        context['applicants'] = applicants
    elif request.user.is_authenticated and request.user.is_clerk1:
        messages.add_message(request, messages.ERROR, 'You cannot access Buyers Page!')
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Buyers Page!')
        return redirect('AdminHomepage',pk=pk)
    else:
        return redirect('Logout')
    return render(request, 'files/BuyersApplication.html',context=context)

@login_required(login_url='/accounts/login/')
def BuyersApplicationLogs(request, pk, email):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk3:
        context= {}
        filter_all = buyerslogsFilter(request.GET, queryset=BuyersFormLogs.objects.exclude(fullname=None))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
    elif request.user.is_authenticated and request.user.is_clerk1:
        messages.add_message(request, messages.ERROR, 'You cannot access Buyers Page!')
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Buyers Page!')
        return redirect('AdminHomepage',pk=pk)
    else:
        return redirect('Logout')
    return render(request, 'files/BuyersApplicationLogs.html',context=context)


@login_required(login_url='/accounts/login/')
def BuyersApplicationApprove(request, pk, email,lot_type,phase,block,lotno,fullname):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk3:
        a = User.objects.filter(pk=pk)
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = BuyersFormModel.objects.filter(email=email).values_list('email', flat=True).first()
        lot = BuyersFormModel.objects.filter(pk=pk).values_list('lot_type', flat=True).first()
        p = BuyersFormModel.objects.filter(phase=phase).values_list('phase', flat=True).first()
        b1 = BuyersFormModel.objects.filter(block=block).values_list('block', flat=True).first()
        l = BuyersFormModel.objects.filter(lotno=lotno).values_list('lotno', flat=True).first()
        fname = BuyersFormModel.objects.filter(pk=pk).values_list('fullname', flat=True).first()
        terms = BuyersFormModel.objects.filter(pk=pk).values_list('terms', flat=True).first()
        birth = BuyersFormModel.objects.filter(pk=pk).values_list('birth', flat=True).first()
        gender = BuyersFormModel.objects.filter(pk=pk).values_list('gender', flat=True).first()
        contacts = BuyersFormModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        address = BuyersFormModel.objects.filter(pk=pk).values_list('address', flat=True).first()
        send_mail(
                'From Himlayang General Trias Management',
                f'Dear {fname},\n\nGood day!\n\n' +
                f'We want to inform you that we have approved your request upon checking on it. The ({lot} Phase:{p} Block:{b1} Lot No.:{l}) is available. Thank you for buying at the Himlayang General Trias Cemetery.\n\n'+
                'If you need immediate assistance or have any further questions, you can make an appointment with the Office of Himlayang Gen. Trias and free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com \n\n'+
                'Regards,\nGeneral Trias Management',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        BuyersFormLogs.objects.create(
            lot_type=lot,phase=p,block=b1,lotno=l,terms=terms,fullname=fname,birth=birth,gender=gender,contacts=contacts,address=address,email=b,status='Approved')
        BuyersFormModel.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('BuyersApplication', pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('AdminHomepage',pk=pk)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def BuyersApplicationReject(request, pk, email,lot_type,phase,block,lotno,fullname):
    if request.user.is_authenticated and request.user.is_clerk3 or request.user.is_admin:
        a = User.objects.filter(pk=pk)
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = BuyersFormModel.objects.filter(email=email).values_list('email', flat=True).first()
        lot = BuyersFormModel.objects.filter(pk=pk).values_list('lot_type', flat=True).first()
        p = BuyersFormModel.objects.filter(phase=phase).values_list('phase', flat=True).first()
        b1 = BuyersFormModel.objects.filter(block=block).values_list('block', flat=True).first()
        l = BuyersFormModel.objects.filter(lotno=lotno).values_list('lotno', flat=True).first()
        fname = BuyersFormModel.objects.filter(fullname=fullname).values_list('fullname', flat=True).first()
        terms = BuyersFormModel.objects.filter(pk=pk).values_list('terms', flat=True).first()
        birth = BuyersFormModel.objects.filter(pk=pk).values_list('birth', flat=True).first()
        gender = BuyersFormModel.objects.filter(pk=pk).values_list('gender', flat=True).first()
        contacts = BuyersFormModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        address = BuyersFormModel.objects.filter(pk=pk).values_list('address', flat=True).first()
        send_mail(
                'From Himlayang General Trias Management',
                f'Dear {fname},\n\nGood day!\n\n' +
                f'We want to inform you that we have declined your request upon checking on it. The ({lot} Phase:{p} Block:{b1} Lot No.:{l}) you are about to buy is already taken. Try to acquire about other lots. Thank you for trying to buy a lot at the Himlayang General Trias Cemetery, and we are sorry for the inconvenience.\n\n'+
                'If you need immediate assistance or have any further questions, you can make an appointment with the Office of Himlayang Gen. Trias and free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com\n\n'+
                'Regards,\nGeneral Trias Management',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        BuyersFormLogs.objects.create(
            lot_type=lot,phase=p,block=b1,lotno=l,terms=terms,fullname=fname,birth=birth,gender=gender,contacts=contacts,address=address,email=b,status='Declined')
        BuyersFormModel.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('BuyersApplication', pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('AdminHomepage',pk=pk)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def Application(request,pk,email):
    if request.user.is_authenticated and request.user.is_clerk3 or request.user.is_admin:
        context= {}
        buyers = BuyersFormModel.objects.all().count()
        inquiries = InquiryFormModel.objects.all().count()
        invitee = BookAppointmentModel.objects.all().count()
        applicants = ApplicationFormModel.objects.all().count()
        overall = buyers+inquiries+invitee+applicants
        
        if overall > 0:
            overall = '!'
        else:
            overall = ''
        
        if invitee > 0:
            invitee = '!'
        else:
            invitee = ''

        if inquiries > 0:
            inquiries = '!'
        else:
            inquiries = ''

        if buyers > 0:
            buyers = '!'
        else:
            buyers = ''

        if applicants > 0:
            applicants = '!'
        else:
            applicants = ''

        filter_all = applicationFilter(request.GET, queryset=ApplicationFormModel.objects.exclude(fullname=None))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        context['buyers'] = buyers
        context['inquiries'] = inquiries
        context['invitee'] = invitee
        context['applicants'] = applicants
        context['overall'] = overall
    elif request.user.is_authenticated and request.user.is_clerk1:
        messages.add_message(request, messages.ERROR, 'You cannot access Application Page!')
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Application Page!')
        return redirect('AdminHomepage',pk=pk)
    else:
        return redirect('Logout')
    return render(request, 'files/Application.html',context=context)

@login_required(login_url='/accounts/login/')
def ApplicationLogs(request,pk,email):
    if request.user.is_authenticated and request.user.is_clerk3 or request.user.is_admin:
        context= {}
        filter_all = applicationlogsFilter(request.GET, queryset=ApplicationFormLogs.objects.exclude(fullname=None))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
    elif request.user.is_authenticated and request.user.is_clerk1:
        messages.add_message(request, messages.ERROR, 'You cannot access Application Page!')
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        messages.add_message(request, messages.ERROR, 'You cannot access Application Page!')
        return redirect('AdminHomepage',pk=pk)
    else:
        return redirect('Logout')
    return render(request, 'files/ApplicationLogs.html',context=context)

@login_required(login_url='/accounts/login/')
def ApplicationApprove(request,pk,email, phase, block, lotno, fullname):
    if request.user.is_authenticated and request.user.is_clerk3 or request.user.is_admin:
        a = User.objects.filter(pk=pk)
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = ApplicationFormModel.objects.filter(email=email).values_list('email', flat=True).first()
        p = ApplicationFormModel.objects.filter(phase=phase).values_list('phase', flat=True).first()
        b1 = ApplicationFormModel.objects.filter(block=block).values_list('block', flat=True).first()
        l= ApplicationFormModel.objects.filter(lotno=lotno).values_list('lotno', flat=True).first()
        fname = ApplicationFormModel.objects.filter(pk=pk).values_list('fullname', flat=True).first()
        birth = ApplicationFormModel.objects.filter(pk=pk).values_list('birth', flat=True).first()
        gender = ApplicationFormModel.objects.filter(pk=pk).values_list('gender', flat=True).first()
        contacts = ApplicationFormModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        address = ApplicationFormModel.objects.filter(pk=pk).values_list('address', flat=True).first()
        date = ApplicationFormModel.objects.filter(pk=pk).values_list('date', flat=True).first()

        send_mail(
                'From Himlayang General Trias Management',
                f'Dear {fname},\n\nGood day!\n\n' +
                f'We want to inform you that we have approved your request upon checking on it. The (Apartment Phase:{p} Block:{b1} Lot No.:{l}) is available. Thank you for buying at the Himlayang General Trias Cemetery. \n\n'+
                'If you need immediate assistance or have any further questions, you can make an appointment with the Office of Himlayang Gen. Trias and free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com\n\n'+
                'Regards,\nGeneral Trias Management',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        ApplicationFormLogs.objects.create(
            email=b,phase=p,block=b1,date=date,lotno=l,fullname=fname,birth=birth,gender=gender,contacts=contacts,address=address,status='Approved')
        ApplicationFormModel.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('Application', pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('ClientPayment',pk=pk)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def ApplicationReject(request,pk,email, phase, block, lotno, fullname):
    if request.user.is_authenticated and request.user.is_clerk3 or request.user.is_admin:
        a = User.objects.filter(pk=pk)
        c = User.objects.filter(pk=pk).values_list('id', flat=True).first()
        b = ApplicationFormModel.objects.filter(email=email).values_list('email', flat=True).first()
        p = ApplicationFormModel.objects.filter(phase=phase).values_list('phase', flat=True).first()
        b1 = ApplicationFormModel.objects.filter(block=block).values_list('block', flat=True).first()
        l= ApplicationFormModel.objects.filter(lotno=lotno).values_list('lotno', flat=True).first()
        fname = ApplicationFormModel.objects.filter(fullname=fullname).values_list('fullname', flat=True).first()
        birth = ApplicationFormModel.objects.filter(pk=pk).values_list('birth', flat=True).first()
        gender = ApplicationFormModel.objects.filter(pk=pk).values_list('gender', flat=True).first()
        contacts = ApplicationFormModel.objects.filter(pk=pk).values_list('contacts', flat=True).first()
        address = ApplicationFormModel.objects.filter(pk=pk).values_list('address', flat=True).first()
        date = ApplicationFormModel.objects.filter(pk=pk).values_list('date', flat=True).first()
        send_mail(
                'From Himlayang General Trias Management',
                f'Dear {fname},\n\nGood day!\n\n' +
                f'We want to inform you that we have declined your request upon checking on it. The (Apartment Phase:{p} Block:{b1} Lot No.:{l}) you are about to buy is already taken. Try to acquire about other lots. Thank you for trying to buy a lot at the Himlayang General Trias Cemetery, and we are sorry for the inconvenience.\n\n'+
                'If you need immediate assistance or have any further questions, you can make an appointment with the Office of Himlayang Gen. Trias and free to call us at Tel. #: (046) 419-8380 to 89 (02) 8779-5980 or visit our website: www.generaltrias.gov.ph and www.himlayangcemeterygentri.com\n\n'+
                'Regards,\nGeneral Trias Management',
                'andrewleilaraqueljustin@gmail.com',
                [b],
                fail_silently=False
            )
        ApplicationFormLogs.objects.create(
            email=b,phase=p,block=b1,date=date,lotno=l,fullname=fname,birth=birth,gender=gender,contacts=contacts,address=address,status='Declined')
        ApplicationFormModel.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully Sent')
        return redirect('Application', pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=email)
    elif request.user.is_authenticated and request.user.is_clerk2:
        return redirect('ClientPayment',pk=pk)
    else:
        return redirect('Logout')
#---ENDCLERK3

#---CLERK2
@login_required(login_url='/accounts/login/')
def AdminHomepage(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        context= {}
        buyers = BuyersFormModel.objects.all().count()
        inquiries = InquiryFormModel.objects.all().count()
        invitee = BookAppointmentModel.objects.all().count()
        applicants = ApplicationFormModel.objects.all().count()
        overall = buyers+inquiries+invitee+applicants
        if overall > 0:
            overall = '!'
        else:
            overall = ''
        
        if invitee > 0:
            invitee = '!'
        else:
            invitee = ''

        if inquiries > 0:
            inquiries = '!'
        else:
            inquiries = ''

        if buyers > 0:
            buyers = '!'
        else:
            buyers = ''

        if applicants > 0:
            applicants = '!'
        else:
            applicants = ''
            
        context['overall'] = overall
        filter_all = deadsFilter(request.GET, queryset=Deads.objects.order_by('-id'))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 10)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        context['buyers'] = buyers
        context['inquiries'] = inquiries
        context['invitee'] = invitee
        context['applicants'] = applicants
    elif request.user.is_authenticated and request.user.is_clerk3:
        messages.add_message(request, messages.ERROR, 'You cannot access Grave Finder Table Page!')
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        messages.add_message(request, messages.ERROR, 'You cannot access Grave Finder Table Page!')
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/AdminHomepage.html', context=context)

@login_required(login_url='/accounts/login/')
def ClientPayment(request, pk):
    if request.user.is_authenticated and request.user.is_clerk2 or request.user.is_admin:
        context= {}
        buyers = BuyersFormModel.objects.all().count()
        inquiries = InquiryFormModel.objects.all().count()
        invitee = BookAppointmentModel.objects.all().count()
        applicants = ApplicationFormModel.objects.all().count()
        filter_all = clientpaymentFilter(request.GET, queryset=LotOrder.objects.order_by('-id'))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 11)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
        context['buyers'] = buyers
        context['inquiries'] = inquiries
        context['invitee'] = invitee
        context['applicants'] = applicants
    elif request.user.is_authenticated and request.user.is_clerk3:
        messages.add_message(request, messages.ERROR, 'You cannot access Client Payment Page!')
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        messages.add_message(request, messages.ERROR, 'You cannot access Client Payment Page!')
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/ClientPayment.html',context=context)

@login_required(login_url='/accounts/login/')
def PropertyManagement(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        print ("PropertyManagement Page")
        a = User.objects.filter(pk=pk)
        form = LotOrderForm()
        form1 = PaymentHistoryForm()
        if request.method == 'POST':
            form = LotOrderForm(request.POST)
            form1 = PaymentHistoryForm(request.POST)
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                messages.success(request, 'Successfully Added')
            else:
                # product1 = form.cleaned_data.get('product')
                # if product1 == LotOrder.objects.filter(product=product1):
                #     form.add_error(None,'This Lot has an owner')
                messages.error(request,'Invalid Input')
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/PropertyManagement.html',{'a':a, 'form':form,'form1':form1})

@login_required(login_url='/accounts/login/')
def PropertyManagementUpdate(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        order = LotOrder.objects.get(id=pk)
        form = LotOrderForm(instance=order)
        form1 = PaymentHistoryForm()
        if request.method == 'POST':
            form = LotOrderForm(request.POST, instance=order)
            form1 = PaymentHistoryForm(request.POST)
            if form.is_valid() and form1.is_valid():
                # balance = form.cleaned_data.get('balance')
                # if balance == 0:
                #     LotOrder.objects.filter(pk=pk).update(status="Fully Paid")
                # else:
                #     LotOrder.objects.filter(pk=pk).update(status="Partially Paid")
                form.save()
                form1.save()
                messages.success(request, 'Successfully Updated')
                return redirect('ClientPayment',pk=pk)
            else:
                messages.error(request, 'Invalid Input')
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/PropertyManagement.html',{'form':form,'order':order, 'form1':form1})

@login_required(login_url='/accounts/login/')
def Notifier(request,pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        form = NotifierForm()
        if request.method == 'POST':
            form = NotifierForm(request.POST)
            if form.is_valid():
                email1 = form.cleaned_data.get('email')
                name = form.cleaned_data.get('name')
                totalamountdue = form.cleaned_data.get('totalamountdue')
                duedate = form.cleaned_data.get('duedate')
                send_mail(
                'Himlayang Cemetery Billing', 
                f'Good day {name}, \n \n You need to pay your monthly fee. Your due date is {duedate} with a total balance of {totalamountdue}. Thank you! \n\n Himlayang Cemetery Marketing Department \n' ,
                'andrewleilaraqueljustin@gmail.com',
                [email1],
                fail_silently=False
            )
                messages.success(request, 'Successfully Sent')
            else:
                print("ERROR")
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/Notifier.html',{'form':form})

@login_required(login_url='/accounts/login/')
def PropertyManagementDelete(request,pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        LotOrder.objects.filter(id=pk).delete()
        return redirect('ClientPayment',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
@login_required(login_url='/accounts/login/')
def AddNew(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        print ("Adding Lots Page")
        a = User.objects.filter(pk=pk)
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                lot = form.cleaned_data.get('lot')
                phase = form.cleaned_data.get('phase')
                block = form.cleaned_data.get('block')
                lotno = form.cleaned_data.get('lotno')
                data = Product.objects.filter(lot=lot,phase=phase,block=block,lotno=lotno).values_list('id',flat=True).first()
                print(data)
                LotOrder.objects.create(product_id=data)
                messages.success(request, 'Successfully Added'),
                fail_silently=True
                return redirect('AddNew', pk=pk)
            else:
                messages.error(request,'Invalid Input')
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/AddNew.html',{'a':a,'form':form})

@login_required(login_url='/accounts/login/')
def AddNewUpdate(request,pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        prod= Product.objects.get(id=pk)
        form = ProductForm(instance=prod)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=prod)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Successfully Updated!'),
                fail_silently=True
                return redirect('LotTable',pk=pk)
            else:
                messages.error(request, 'Invalid Input'),
                fail_silently=True
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/AddNew.html',{'form':form,'prod':prod})

# def AddNewDeceased(request,pk):
#     if request.user.is_authenticated and request.user.is_admin:
#         prod= Product.objects.get(id=pk)
#         form = ProductForm(instance=prod)
#         form1 = ProductForm()
#         if request.method == 'POST':
#             form = ProductForm(request.POST, instance=prod)
#             form1 = ProductForm(request.POST)
#             if form.is_valid():
#                 form1.save()
#                 messages.success(request, 'Successfully Added'),
#                 fail_silently=True
#             else:
#                 messages.error(request, 'Invalid Input'),
#                 fail_silently=True
#     else:
#         return redirect('Logout')
#     return render(request, 'files/AddNew.html',{'form':form,'prod':prod})

@login_required(login_url='/accounts/login/')
def AddNewDelete(request,pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        Product.objects.filter(id=pk).delete()
        return redirect('LotTable',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def AddDeceased(request,pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        a = Deads.objects.all()
        user = request.user
        form = DeceasedForm(user)
        if request.method == 'POST':
            form = DeceasedForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Added'),
                fail_silently=True
                return redirect('AdminHomepage', pk=pk)
            else:
                messages.add_message(request, messages.ERROR, 'Deceased Limit')
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/AddDeceased.html',{'a':a,'form':form})

@login_required(login_url='/accounts/login/')
def AddDeceasedUpdate(request,pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        dead= Deads.objects.get(id=pk)
        user = request.user
        form = DeceasedForm(user,instance=dead)
        if request.method == 'POST':
            form = DeceasedForm(user,request.POST, instance=dead)
            if form.is_valid():
                deceased1 = form.cleaned_data.get('deceased')
                born1 = form.cleaned_data.get('born')
                died1 = form.cleaned_data.get('died')
                Deads.objects.filter(pk=pk).update(deceased=deceased1, born=born1, died=died1)
                messages.success(request, 'Successfully Updated'),
                fail_silently=True
                return redirect('AdminHomepage', pk=pk)
            else:
                messages.error(request, 'Invalid Input'),
                fail_silently=True
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/AddDeceased.html',{'form':form,'dead':dead})

@login_required(login_url='/accounts/login/')
def AddDeceasedDelete(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        Deads.objects.filter(id=pk).delete()
        return redirect('AdminHomepage',pk=pk)
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')

@login_required(login_url='/accounts/login/')
def LotTable(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        context= {}
        filter_all = productFilter(request.GET, queryset=Product.objects.order_by('-id'))
        context['filter_all'] = filter_all

        paginated_filter_all = Paginator(filter_all.qs, 10)
        page_number = request.GET.get('page')
        all_page_obj = paginated_filter_all.get_page(page_number)

        context['all_page_obj'] = all_page_obj
    elif request.user.is_authenticated and request.user.is_clerk3:
        return redirect('Application',pk=pk, email=request.user.email)
    elif request.user.is_authenticated and request.user.is_clerk1:
        return redirect('Inquiry',pk=pk, email=request.user.email)
    else:
        return redirect('Logout')
    return render(request, 'files/LotTable.html', context=context)

@login_required(login_url='/accounts/login/')
def Notice(request, pk):
    if request.user.is_authenticated and request.user.is_admin or request.user.is_clerk2:
        a = User.objects.filter(pk=pk)
        form = NoticeForm()
        if request.method == 'POST':
            form = NoticeForm(request.POST)
            if form.is_valid():
                receiver = form.cleaned_data.get('receiver')
                content = form.cleaned_data.get('content')
                send_mail(
                'From Himlayang General Trias Management',
                content,
                'andrewleilaraqueljustin@gmail.com',
                [receiver],
                fail_silently=False,
            )
            else:
                print("ERROR")
    else:
        return redirect('Logout')
    return render(request, 'files/Notice.html', {'form':form, 'a':a})

# ---------- END ADMIN

# ---------- NO LOGIN
def Niche(request):
    return render(request, 'files/Niche.html')

def AboutUs(request):
    return render(request, 'files/AboutUs.html')

def LotProperty(request):
    return render(request, 'files/LotProperty.html')

def TermsofPayment(request):
    return render(request, 'files/TermsofPayment.html')

def ContactUs(request):
    return render(request, 'files/ContactUs.html')

def PrivacyPolicy(request):
    return render(request, 'files/PrivacyPolicy.html')

def GraveFinder(request):
    q = ""
    if 'q' in request.GET:
        q=request.GET['q']
        prod = Deads.objects.filter(deceased__icontains=q).values_list('deceased', flat=True)
        if q == '' or range(len(prod)==0):
            messages.error(request, 'Name not found!')
            return render(request, 'files/GraveFinder.html',{'q':q})
        else:
            prod = Deads.objects.filter(deceased__icontains=q).order_by('-id')
            p = Paginator(prod, per_page=8)
            page = request.GET.get('page')
            if page == None or page == "":
                page = "1"
            prod = p.get_page(page)
            prod.adjusted_elided_pages = p.get_elided_page_range(page)
            return render(request, 'files/GraveFinder.html',{'prod':prod,'q':q })
    else:
        return render(request, 'files/GraveFinder.html')

    # p = Paginator(prod, per_page=8)
    # page = request.GET.get('page')
    # if page == None or page == "":
    #     page = "1"
    # prod = p.get_page(page)
    # prod.adjusted_elided_pages = p.get_elided_page_range(page)
    # return render(request, 'files/GraveFinder.html',{'prod':prod,'q':q })

def InquiryForm(request):
    form = InquiryFormForm()
    q =''
    if 'lots' in request.GET:
        q=request.GET['lots']
        available = LotOrder.objects.filter(product_id__lot__icontains=q,terms=None).order_by('-product')
    else:
        available = LotOrder.objects.all().filter(terms=None).order_by('-product')
    p = Paginator(available, per_page=14)
    page = request.GET.get('page')
    if page == None or page == "":
        page = "1"
    avail = p.get_page(page)
    avail.adjusted_elided_pages = p.get_elided_page_range(page)
    if request.method == 'POST':
        form = InquiryFormForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success'),
            fail_silently=True,
            return redirect('InquiryForm')
        else:
            messages.error(request, 'Error'),
            fail_silently=True,
            return redirect('InquiryForm')
    return render(request, 'files/InquiryForm.html',{'form':form,'available':available,'avail':avail,'q':q})

def Lawn(request):
    return render(request, 'files/Lawn.html')

def Mausoleum(request):
    return render(request, 'files/Mausoleum.html')

def Apartment(request):
    return render(request, 'files/Apartment.html')

def Help(request):
    return render(request, 'files/Help.html')

def BookAppointmentFormPdf(request):
    #create byteststream buffer
    buf = io.BytesIO()
    #create document template
    pdf = SimpleDocTemplate(buf, pagesize=letter)
    #content
    inquiry_list = BookAppointmentLogs.objects.all()
    data = [['Name','Mobile No.','Email','Date of Appointment','Reason','Status',]]
    for inquiry in inquiry_list:
        data.append([inquiry.fullname,inquiry.contacts,inquiry.email,inquiry.date,inquiry.reason,inquiry.status])
    elems = []
    #table
    elems.append(Table(data))
    pdf.build(elems)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='BookAppointmentLogs.pdf')

def ApplicationFormPdf(request):
    #create byteststream buffer
    buf = io.BytesIO()
    #create document template
    pdf = SimpleDocTemplate(buf, pagesize=letter)
    #content
    application_list = ApplicationFormLogs.objects.all()
    data = [['Name','Mobile No.','Email','Gender','Birthday','Address','Lot Type','Phase','Block','Lot No.','Status']]
    for application in application_list:
        data.append(
            [application.fullname,application.contacts,application.email,application.gender,application.birth,application.address,
            'Apartment',application.phase,application.block,application.lotno,application.status])
    elems = []
    #table
    elems.append(Table(data))
    pdf.build(elems)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='ApplicationLogs.pdf')

def BuyersFormPdf(request):
    #create byteststream buffer
    buf = io.BytesIO()
    #create document template
    pdf = SimpleDocTemplate(buf, pagesize=letter)
    #content
    buyers_list = BuyersFormLogs.objects.all()
    data = [['Name','Mobile No.','Email','Gender','Birthday','Address','Lot Type','Phase','Block','Lot No.','Terms','Status']]
    for buyers in buyers_list:
        data.append(
            [buyers.fullname,buyers.contacts,buyers.email,buyers.gender,buyers.birth,buyers.address,
            buyers.lot_type,buyers.phase,buyers.block,buyers.lotno,buyers.terms,buyers.status])
    elems = []
    #table
    elems.append(Table(data))
    pdf.build(elems)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='BuyersLogs.pdf')

def InquiryFormPdf(request):
    #create byteststream buffer
    buf = io.BytesIO()
    #create document template
    pdf = SimpleDocTemplate(buf, pagesize=letter)
    #content
    inquiry_list = InquiryFormLogs.objects.all()
    data = [['Name','Mobile No.','Email','Gender','Birthday','Address','Lot Type','Phase','Block','Lot No.','Terms','Status']]
    for inquiry in inquiry_list:
        data.append(
            [inquiry.fullname,inquiry.contacts,inquiry.email,inquiry.gender,inquiry.birth,inquiry.address,
            inquiry.lot_type,inquiry.phase,inquiry.block,inquiry.lotno,inquiry.terms,inquiry.status])
    elems = []
    #table
    elems.append(Table(data))
    pdf.build(elems)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='InquiryLogs.pdf')
    
def Logout(request):
    logout(request)
    return redirect ('Login')

# ---------- END NO LOGIN