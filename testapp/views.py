# from automium import schedule
from django.shortcuts import render
import calendar
from datetime import date
from calendar import HTMLCalendar
from testapp.forms import *
from testapp.models import *
from django.http import HttpResponse,HttpResponseRedirect
from OpdManagement.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
from datetime import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from testapp.models import OpdPayment
from testapp.serializers import *
from usermanagementapp.models import *
from encrypt_util import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from OpdManagement import utils as utils_response
from rest_framework import status
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from datetime import datetime as dt
from django.contrib import messages
import random
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import send_mail,EmailMessage
from django.utils import timezone

@login_required(login_url='/user_login')
def change_password(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = PasswordChangeForm(request)
            context = {
                'form': form,
            }
            template_name = 'user_management/change_password.html'
            return render(request, template_name, context)
        else:
            return redirect('login_page')
    elif request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            print('This is valid form')
            form.save()
            # update_session_auth_hash(request,form.user)
            return redirect('dashboard')
        else:
            messages.warning(request, form.errors)
            print('invalid form', form.errors)
            context = {
                'form': form,
            }
            template_name = 'user_management/change_password.html'
            return render(request, template_name, context)

@login_required(login_url='/user_login')
def view_create_userprofile(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or request.user.is_staff:
        try:
            name=request.session['Name']
            records=CreateUser.objects.all()
            return render (request,'user_management/view_create_user.html',{'records':records,'login_name':name})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
# @login_required(login_url='/user_login')
def patient_view(request):
    try:
        return render(request,'testapp/index.html')
    except Exception as error:
           return render(request,'error.html',{'error':error})

def book_appointment(request):
    try:
        form=DoctorTableForm()
        today=date.today()
        yyyy=today.year
        mm=today.month
        nmm=mm+1
        pmm=mm-1
        calendars=HTMLCalendar().formatmonth(yyyy,mm)
        if request.method=='POST':
            doctor_or_speciality=request.POST.get('doctor_or_speciality')
            location=request.POST.get('location')
            records=(DoctorTable.objects.filter(doctor_name__icontains=doctor_or_speciality)|DoctorTable.objects.filter(doctor_department=doctor_or_speciality))&DoctorTable.objects.filter(doctor_location__icontains=location)
            count=0
            if records.exists():
                for data in records:
                    doctor_name=data.doctor_name
                    doctor_id=data.doctor_id
                    doctor_department=data.doctor_department
                    doctor_location=data.doctor_location
                    doctor_profile_image=data.doctor_profile_image
                    doctor_appointment=data.doctor_appointment
                    doctor_fee=data.doctor_fee
                    # doctor_time_slot=data.doctor_time_slot
                    count+=1
                context={'form':form,'doctor':doctor_or_speciality,'location':location,'calendars':calendars,'nmm':nmm,'pmm':pmm,'records':records,'no_of_doctor':count,'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment}
                response=render(request,'testapp/book_appointment.html',context)
                # response.set_cookie(doctor_location,doctor_department)
                request.session['doctor_id']=doctor_id
                request.session['doctor_name']=doctor_name
                request.session['doctor_department']=doctor_department
                request.session['doctor_location']=doctor_location
                request.session['doctor_profile_image']=str(doctor_profile_image)
                request.session['doctor_fee']=str(doctor_fee)
                # request.session['doctor_time_slot']=str(doctor_time_slot)
                return response
            else:
                context={'form':form,'doctor':doctor_or_speciality,'location':location,'calendars':calendars,'nmm':nmm,'pmm':pmm,'records':records,'no_of_doctor':count,}
                response=render(request,'testapp/book_appointment.html',context)
                return response
        return render(request,'testapp/book_appointment.html')
    except Exception as error:
        return render(request,'error.html',{'error':error})

def mobile_register(request):
    try:
        doctor_appointment=request.POST.get('doctor_appointment')
        choose_doctor=request.POST.get('choose_doctor')
        calendars=request.POST.get('calendars')
        if choose_doctor is not None:
            records=DoctorTable.objects.get(doctor_id=choose_doctor)
            doctor_id=records.doctor_id
            doctor_name=records.doctor_name
            doctor_fee=records.doctor_fee
            doctor_department=records.doctor_department
            doctor_location=records.doctor_location
            doctor_profile_image=records.doctor_profile_image
            request.session['doctor_id']=doctor_id
            request.session['doctor_name']=doctor_name
            request.session['doctor_department']=doctor_department
            request.session['doctor_location']=doctor_location
            request.session['doctor_profile_image']=str(doctor_profile_image)
            request.session['doctor_fee']=str(doctor_fee)
        request.session['doctor_appointment']=str(doctor_appointment)
        doctor_name=request.session['doctor_name']
        doctor_department=request.session['doctor_department']
        doctor_location=request.session['doctor_location']
        doctor_profile_image=request.session['doctor_profile_image']
        doctor_appointment=request.session['doctor_appointment']
        doctor_id=request.session['doctor_id']
        doctor_fee=request.session['doctor_fee']
        today=date.today()
        context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'doctor_fee':doctor_fee}
        return render(request,'testapp/mobile_register.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

def date_time(request):
    try:
        doctor_id=request.session['doctor_id']
        mobile_number=request.POST.get('mobile_number')
        first_name=request.POST.get('first_name')
        middle_name=request.POST.get('middle_name')
        last_name=request.POST.get('last_name')
        request.session['mobile_number'] = mobile_number
        request.session['first_name'] = first_name
        request.session['middle_name'] = middle_name
        request.session['last_name'] = last_name
        doctor_name=request.session['doctor_name']
        doctor_department=request.session['doctor_department']
        doctor_location=request.session['doctor_location']
        doctor_profile_image=request.session['doctor_profile_image']
        doctor_appointment=request.session['doctor_appointment']
        mobile_number=request.session['mobile_number']
        # doctor_time_slot=request.session['doctor_time_slot']
        mobile_number=request.session['mobile_number']
        first_name = request.session['first_name']
        middle_name = request.session['middle_name']
        last_name = request.session['last_name']
        doctor_fee=request.session['doctor_fee']
        records=AvailabilityIntradayScheduleMaster.objects.filter(doctor_id=doctor_id)#Getting D_id From
        records2=BookedAppointments.objects.all().only('patient_scheduled_id')
        records3=[]
        records4=[]
        for data in records:
            data=data.time_slot_id
            records3.append(data)
        for data2 in records2:
            print(data2)
            data=data2.patient_scheduled_id
            records4.append(data)
        #Generate Schedule
        fresh_schedule=[]
        for item in records3:
            if item not in records4:
                fresh_schedule.append(item)
        records=AvailabilityIntradayScheduleMaster.objects.filter(Q(time_slot_id__in=fresh_schedule)&Q(time_slot_id__contains=doctor_appointment))

        time_slot_lists='time_slots'
        context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'time_slots':time_slot_lists,'records':records,'doctor_fee':doctor_fee}
        return render(request,'testapp/date_time.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

def appointment_detail(request):
    try:
        scheduled=request.POST.get('scheduled')
        time_slots_name=request.POST.get('time_slots_id')
        get_schedule=AvailabilityIntradayScheduleMaster.objects.get(time_slot_id=time_slots_name)
        scheduled=get_schedule.time_slot_start_time+'-'+get_schedule.time_slot_end_time
        request.session['get_schedule_time_slot_id']=get_schedule.time_slot_id
        request.session['scheduled']=scheduled
        scheduled=request.session['scheduled']
        doctor_name=request.session['doctor_name']
        doctor_department=request.session['doctor_department']
        doctor_location=request.session['doctor_location']
        doctor_profile_image=request.session['doctor_profile_image']
        doctor_appointment=request.session['doctor_appointment']
        mobile_number=request.session['mobile_number']
        first_name = request.session['first_name']
        middle_name = request.session['middle_name']
        last_name = request.session['last_name']
        doctor_fee=request.session['doctor_fee']
        context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'scheduled':scheduled, 'mobile_number':mobile_number,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'doctor_fee':doctor_fee}
        return render(request,'testapp/appointment_detail.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

def booking_detail(request):
    try:
        global records_of_members
        doctor_name=request.session['doctor_name']
        scheduled=request.session['scheduled']
        doctor_department=request.session['doctor_department']
        doctor_location=request.session['doctor_location']
        doctor_profile_image=request.session['doctor_profile_image']
        doctor_appointment=request.session['doctor_appointment']
        mobile_number=request.session['mobile_number']
        first_name = request.session['first_name']
        middle_name = request.session['middle_name']
        last_name = request.session['last_name']
        scheduled=request.session['scheduled']
        doctor_fee=request.session['doctor_fee']
        reference_mobile_number=mobile_number
        base_price=doctor_fee
        without_discount=doctor_fee
        with_discount=630
        if request.method=='POST':
            submit_name=request.POST.get('add_member')
            if 'add_member' in request.POST:
                title_name=request.POST.get('title')

                gender=request.POST.get('gender')
                age=request.POST.get('age')
                mobile_number=request.POST.get('mobile_number')
                email=request.POST.get('email')
                records=AddMembers.objects.get_or_create(
                reference_mobile_number=reference_mobile_number,
                title_name = title_name,
                first_name =first_name,
                middle_name =middle_name,
                last_name =last_name,
                gender=gender,
                age=age,
                mobile_number=mobile_number,
                email=email,
                )
                records_of_members=AddMembers.objects.filter(reference_mobile_number=reference_mobile_number)
                no_of_member=records_of_members.count()

                base_price=doctor_fee
                without_discount=doctor_fee
                with_discount=630
                context={
                'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,
                    'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,
                    'mobile_number':mobile_number,'first_name':first_name,'last_name':last_name,'middle_name':middle_name,'scheduled':scheduled,
                    'records_of_members':records_of_members,'without_discount':without_discount,
                    'with_discount':with_discount,
                }
                return render(request,'testapp/booking_detail.html',context)
        records_of_members=AddMembers.objects.filter(reference_mobile_number=reference_mobile_number)
        no_of_member=records_of_members.count()

        base_price=float(doctor_fee)
        without_discount=float(doctor_fee)
        with_discount=(base_price-(base_price*10)/100)
        context={
        'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'records_of_members':records_of_members, 'mobile_number':mobile_number,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'scheduled':scheduled,'without_discount':without_discount,'with_discount':with_discount,
        }
        return render(request,'testapp/booking_detail.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

from django.contrib.auth.hashers import make_password
@login_required(login_url='/user_login')
def doctor_view(request):
    # try:
        # User.objects.create(username='karan1',password=make_password('1111'),email='abc@gmail.com')
    import datetime
    doctor_name='karan'
    let=doctor_name[0:4].upper()
    datee=datetime.datetime.now().strftime("%d%m%y")
    form=DoctorTableForm()
    userform=CreateUserForm()
    records=DoctorTable.objects.all()
    success='success'
    if request.method=='POST':
        ids=randint(1111,9999)
        dob=request.POST.get('doctor_date_of_birth')
        no_of_doctor_list=DoctorTable.objects.all().count()
        no_of_doctor_list+=1
        if len(str(no_of_doctor_list))==1:
            doc_id='000'+str(no_of_doctor_list)
            doc_reg='R-'+dob+'-'+doc_id
        elif len(str(no_of_doctor_list))==2:
            doc_id='00'+str(no_of_doctor_list)
            doc_reg='R-'+dob+'-'+doc_id
        elif len(str(no_of_doctor_list))==3:
            doc_id='0'+str(no_of_doctor_list)
            doc_reg='R-'+dob+'-'+doc_id
        else:
            doc_id=str(no_of_doctor_list)
            doc_reg='R-'+dob+'-'+doc_id

        no_of_patient_registered=CreateUser.objects.all().count()
        today=date.today()
        today=today.strftime("%y%m%d")
        if len(str(no_of_patient_registered))==1:
            u_id='US'+today+'000'+str(no_of_patient_registered)
        elif len(str(no_of_patient_registered))==2:
            u_id='US'+today+'00'+str(no_of_patient_registered)
        elif len(str(no_of_patient_registered))==3:
            u_id='US'+today+'0'+str(no_of_patient_registered)
        else:
            u_id='US'+today+str(no_of_patient_registered)
        form=DoctorTableForm(request.POST,request.FILES)
        if form.is_valid():
            doctor_id=form.cleaned_data['doctor_id']
            doctor_belogns_to=form.cleaned_data['doctor_belogns_to']
            doctor_email_address=form.cleaned_data['doctor_email_address']
            doctor_name=form.cleaned_data['doctor_name']
            doctor_profile_image=form.cleaned_data['doctor_profile_image']
            doctor_phone_no=form.cleaned_data['doctor_phone_no']
            doctor_appointment=form.cleaned_data['doctor_appointment']
            doctor_address=form.cleaned_data['doctor_address']
            doctor_date_of_birth=form.cleaned_data['doctor_date_of_birth']
            # doctor_department=form.cleaned_data['doctor_department']
            doctor_status=form.cleaned_data['doctor_status']
            doctor_fee=form.cleaned_data['doctor_fee']
            registration_exparing_date=form.cleaned_data['registration_exparing_date']
            doctor_register_by=form.cleaned_data['doctor_register_by']
            doctor_location=form.cleaned_data['doctor_location']
            doctor_sign_image=form.cleaned_data['doctor_sign_image']
            location=request.POST.get('location')
            username=request.POST.get('usename')
            user_profile=request.POST.get('user_profile')
            doctor_department=request.POST.get('doctor_department')
            try:
                import datetime
                let=doctor_name[0:4].upper()
                datee=doctor_date_of_birth.strftime("%d%m%y")
                User.objects.create(username=username,password=make_password(let+str(datee)),email=doctor_email_address,first_name=doctor_name)
                user_id=User.objects.filter(username=username).first()

                DT=DoctorTable(
                    doctor_id=doc_id,doctor_belogns_to=doctor_belogns_to,doctor_email_address=doctor_email_address,doctor_name=doctor_name,doctor_profile_image=doctor_profile_image,doctor_phone_no=doctor_phone_no,doctor_appointment=doctor_appointment,doctor_address=doctor_address,doctor_date_of_birth=doctor_date_of_birth,doctor_department=doctor_department,doctor_status=doctor_status,doctor_fee=doctor_fee,doctor_registration_no=doc_reg,registration_exparing_date=registration_exparing_date,doctor_register_by=doctor_register_by,doctor_location=doctor_location,doctor_sign_image=doctor_sign_image,
                    location_id=location,created_by_id=request.user.id
                )
                DT.save()
                return render(request,'admin1/doctor_view.html',{'form':form,'success':success,'userform':userform})
            except Exception as error:
                messages.warning(request, error)
        else:
            return render(request,'admin1/doctor_view.html',{'form':form,'userform':userform})
    return render(request,'admin1/doctor_view.html',{'form':form,'records':records,'userform':userform})
    # except Exception as error:
    #     return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def doctor_schedule_view(request):
    try:
        form=DoctorScheduleTableForm()
        records=DoctorScheduleTable.objects.all()
        for data in records:
            average_consulting_time=data.average_consulting_time
            doctor_schedule_date=data.doctor_schedule_date
            starts=data.doctor_schedule_start_time
            ends=data.doctor_schedule_end_time
            start_time=datetime.combine(doctor_schedule_date,starts)
            ends_time=datetime.combine(doctor_schedule_date,ends)
            different=ends_time-start_time
        if request.method=='POST':
            form=DoctorScheduleTableForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/doctor-schedule-view')
            else:
                return render(request,'testapp/doctor_schedule_view.html',{'form':form})
        return render(request,'testapp/doctor_schedule_view.html',{'form':form,'records':records})
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def appointment_view(request):
    try:
        form=AppointmentTableForm()
        if request.method=='POST':
            form=AppointmentTableForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("ThanksYOU")
            else:
                return render(request,'testapp/appointment_view.html',{'form':form})
        return render(request,'testapp/appointment_view.html',{'form':form})
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def patient_view_detail(request):
    try:
        form=PatientTableForm()
        if request.method=='POST':
            form=AppointmentTableForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("ThanksYOU")
            else:
                return render(request,'testapp/patient_view.html',{'form':form})
        return render(request,'testapp/patient_view.html',{'form':form})
    except Exception as error:
        return render(request,'error.html',{'error':error})

class DoctorDashbordView(ListView):
    model=DoctorTable
    template_name='admin1/doctortable_list.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['inactive']='inactive'
        return context

class DoctorEditView(UpdateView):
    model=DoctorTable
    fields=('doctor_name','doctor_status','doctor_email_address','doctor_phone_no')
    # template_name='patient/doctortable_confirm_delete.html'

class DoctorDetailView(DetailView):
    model=DoctorTable
    template_name='admin1/doctortable_detail_view.html'
    context_object_name='data'

# Appointment Viewing by Admin...
class AppointmentDeleteView(DeleteView):
    model=BookedAppointments
    template_name='patient/bookedappointment_confirm_delete.html'
    success_url=reverse_lazy('delete-appointment')

class AppointmentDetailView(DetailView):
    model=BookedAppointments
    template_name='admin1/bookedappointment_detail.html'
    context_object_name='data'

@login_required(login_url='/user_login')
def cancel_appointment(request,patient_id):
    try:
        records_patient_id=BookedAppointments.objects.get(patient_id=patient_id)
        form=BookedAppointmentsForm()#instance=records_patient_id
        if request.method=='POST':
            form=BookedAppointmentsForm(request.POST,instance=records_patient_id)
            if form.is_valid():
                form.status = "Canceled"
                form.save()
                return HttpResponseRedirect('/appointment_table')
        return render(request,'admin1/cancel_appointment.html',{'form':form})
    except Exception as error:
        return render(request,'error.html',{'error':error})
    
from datetime import datetime
from django.utils import timezone
@login_required(login_url='/user_login')
def patient_dashboard(request):
    try:
        today = datetime.today().date()
        doctor_records=DoctorTable.objects.all().count()
        appointment_records=BookedAppointments.objects.all()
        today_total_appointment_records1=BookedAppointments.objects.exclude(patient_scheduled_id = "N/A").filter(patient_appointment_date=today)
        canceled_appointment = BookedAppointments.objects.filter(patient_appointment_date=today,patient_scheduled_id = "N/A").count()
        visited_patient = PatientsRegistrationsAllInOne.objects.filter(registration_date_and_time__date = today).count()
        total_appointment=appointment_records.count()
        today_total_appointment_records=today_total_appointment_records1.count()
        
        yearly_cancelled = []
        yearly_appointment = []

        for data in range(1,13):
            yearly_appointment1 = BookedAppointments.objects.exclude(patient_scheduled_id = "N/A").filter(patient_appointment_date__year=today.year,patient_appointment_date__month=data).count()
            yearly_cancelled1 = BookedAppointments.objects.filter(patient_appointment_date__year=today.year,patient_appointment_date__month=data,patient_scheduled_id = "N/A").count()
            yearly_appointment.append(yearly_appointment1)
            yearly_cancelled.append(yearly_cancelled1)
        context={
            'doctor_records':doctor_records,'total_appointment':total_appointment,'today_total_appointment_records':today_total_appointment_records,
            'today_total_appointment_records1':today_total_appointment_records1,"canceled_appointment":canceled_appointment,"visited_patient":visited_patient,
            'yearly_cancelled':yearly_cancelled,'yearly_appointment':yearly_appointment,
        }
        return render(request,'admin1/appointment_dashboard.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def admin_list_table(request):
    try:
        records=User.objects.all()
        context={
        'records':records
        }
        return render(request,'admin1/admin_list_table.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def patient_table(request):
    try:
        return render(request,'admin1/patient_table.html')
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def doctor_table(request):
    try:
        records=DoctorTable.objects.all()
        context={
        'records':records,
        }
        return render(request,'admin1/doctor_table.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
from random import *
@login_required(login_url='/user_login')
def success_booked(request):
    digits='0123456789'
    no_of_appointment=BookedAppointments.objects.all().count()
    today=date.today()
    today=today.strftime("%y%m%d")
    if len(str(no_of_appointment))==1:
        appointment_id='app'+today+'000'+str(no_of_appointment)
        patient_id='pid'+today+'000'+str(no_of_appointment)
    elif len(str(no_of_appointment))==2:
        appointment_id='app'+today+'00'+str(no_of_appointment)
        patient_id='pid'+today+'00'+str(no_of_appointment)
    elif len(str(no_of_appointment))==3:
        appointment_id='app'+today+'0'+str(no_of_appointment)
        patient_id='pid'+today+'0'+str(no_of_appointment)
    else:
        appointment_id='app'+today+str(no_of_appointment)
        patient_id='pid'+today+str(no_of_appointment)
    success='success'
    title_name=request.POST.get('sub')
    first=request.POST.get('first_name')
    middle=request.POST.get('middle_name')
    last=request.POST.get('last_name')
    gender=request.POST.get('gender')
    age=request.POST.get('age')
    phone=request.POST.get('phone')
    email=request.POST.get('email')
    request.session['title_name']=title_name
    request.session['patient_name']=patient_name
    schedule_time=request.POST.get('schedule_time')
    payment=request.POST.get('payment')
    doctor_name=request.session['doctor_name']
    doctor_department=request.session['doctor_department']
    doctor_appointment=request.session['doctor_appointment']
    patient_name=request.session['patient_name']
    title_name=request.session['title_name']
    mobile_number=request.session['mobile_number']
    get_schedule_time_slot_id=request.session['get_schedule_time_slot_id']
    patient_name=title_name + patient_name
    add_this_member=request.POST.get('add_this_member')
    new_members=AddMembers.objects.filter(mobile_number=add_this_member)
    if new_members is not None:
        for data in new_members:
            title_name=data.title_name
            patient_name=data.patient_name
            gender=data.gender
            age=data.age
            mobile_number=data.mobile_number
            email=data.email
            patient_name=title_name + patient_name
            request.session['patient_name']=patient_name
            request.session['gender']=gender
            request.session['mobile_number']=mobile_number
        patient_name=request.session['patient_name']
        title_name=request.session['title_name']
        mobile_number=request.session['mobile_number']

    records=BookedAppointments.objects.get_or_create(
    patient_id=patient_id,
    first_name=first,
    middle_name = middle,
    last_name = last,
    patient_appointment_date=doctor_appointment,
    patient_appointment_id=appointment_id,
    patient_gender=gender,
    patient_age=age,
    patient_mobile_number=phone,
    patient_email_id=email,
    patient_schedule_date_and_time=schedule_time,
    patient_scheduled_id=get_schedule_time_slot_id,
    patient_payment_mode=payment,
    doctor_name=doctor_name,
    doctor_department=doctor_department,
    admin='user',
    created_by_id = request.user.id,
    location_id = request.location,
    )
    if payment=='online_payment':
        On_payment='OnlinePayment'
        order_amount=63000
        order_currency='INR'
        payment_order=client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=1))
        payment_order_id=payment_order['id']
        context={
        'amount':order_amount,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id,'On_payment':On_payment,'email':email,'phone':phone,'patient_name':patient_name,
        }
        return render(request,'testapp/pay.html',context)
    else:
        records_of_members=AddMembers.objects.filter(reference_mobile_number=mobile_number)
        context1={
        'success':success,'appointment_id':appointment_id,'title_name':title_name,'patient_name':patient_name,'gender':gender,'age':age,'phone':phone,'email':email,'schedule_time':schedule_time,'payment':payment,'records_of_members':records_of_members,
        }
        return render(request,'testapp/booking_detail.html',context1)
import datetime
import datetime as dd
def doctor_schedule_view(request):
    print('adssdw')
    form=DoctorScheduleForm()
    if request.method=='POST':
        doctor_name=request.POST.get('doctor_name')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        print(start_date,'+',end_date)
        start = dd.datetime.strptime(start_date, "%Y-%m-%d")
        end = dd.datetime.strptime(end_date, "%Y-%m-%d")
        date_array =(start + timedelta(days=x) for x in range(0, (end-start).days+1))
        date_list=[]
        for date_object in date_array:
            date_object=date_object.strftime("%Y-%m-%d")
            date_list.append(date_object)
        request.session['date_list']=date_list
        request.session['doctor_name']=doctor_name
        context={
        'form':form,'date_list':date_list
        }
        return render(request,'testapp/doctor_scheduled.html',context)
    context={
    'form':form,
    }
    return render(request,'testapp/doctor_scheduled.html',context)

def schedule_date(request):
    if request.method=='POST':
        date_list=request.session['date_list']
        schedule_date_list=[]
        for date_listed in date_list:
            schedule_date=request.POST.get(date_listed)
            schedule_date_list.append(schedule_date)
    scheduled_date_list=[]
    for scheduled_date in schedule_date_list:
        if scheduled_date == None:
            continue
        else:
            scheduled_date_list.append(scheduled_date)
    request.session['scheduled_date_list']=scheduled_date_list
    context={
    'scheduled_date_list':scheduled_date_list,
    }
    return render(request,'testapp/doctor_schedule_time.html',context)

import time as tt
def time_scheduling(request):
    scheduled_date_list=request.session['scheduled_date_list']
    if request.method=='POST':
        select_scheduled=request.POST.get('select_scheduled')
        start_time=request.POST.get('start_time')
        end_time=request.POST.get('end_time')
        average_duration=request.POST.get('average_duration')
        start_time_obj=tt.strptime(start_time,"%H:%M")
        end_time_obj=tt.strptime(end_time,"%H:%M")
        average_duration_obj=tt.strptime(average_duration,"%M")
        # average_duration_obj=tt.strptime(average_duration,"%M")
        average_duration_obj=average_duration_obj.tm_min
        time_hour=end_time_obj.tm_hour-start_time_obj.tm_hour
        time_minuts=end_time_obj.tm_min+start_time_obj.tm_min
        hr=0
        if time_minuts >= 60 and time_minuts < 120:
            hr+=1
            mn=time_minuts-60
            time_hour+=hr
            time_minuts=mn
        # Converting hours in to minuts
        total_minuts=time_hour*60+time_minuts
        #Total Slot
        slots=int(total_minuts/int(average_duration))
        current_start_time=dd.datetime.strptime(start_time,"%H:%M")
        time_mn=00.34
        time_scheduled=[]
        if average_duration_obj==10:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.17)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==15:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.26)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==20:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.34)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==25:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.42)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==30:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.5)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==35:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.59)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==40:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.67)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M %p")
        elif average_duration_obj==45:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.75)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==50:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.84)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==55:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.92)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=dd.datetime.strptime(schedule,"%H:%M")
        time_scheduled.insert(0,start_time)
        actual_time_schedule=[]
        for i in range(0,len(time_scheduled)):
            for j in range(i+1,i+2):
                if time_scheduled[i]==time_scheduled[-1]:
                    break
                else:
                    new_list=time_scheduled[i]+' - '+time_scheduled[j]
                    actual_time_schedule.append(new_list)
        #Generating Slots Id
        count=0
        schedule_id_of_each_slot=[]
        for data in actual_time_schedule:
            count+=1
            schedule_id_of_each_slot.append(count)
        request.session['schedule_id_of_each_slot']=schedule_id_of_each_slot
        request.session['actual_time_schedule']=actual_time_schedule
        request.session['start_time']=start_time
        request.session['end_time']=end_time
        request.session['slots']=str(slots)
        context={
        'scheduled_date_list':scheduled_date_list,'start_time':start_time,'end_time':end_time,'actual_time_schedule':actual_time_schedule,'slots':slots
        }
        return render(request,'testapp/time_scheduling.html',context)
    return render(request,'testapp/time_scheduling.html')

def scheduled_time(request):
    form=AvailableDayScheduleMasterTemp()
    doctor_name=request.session['doctor_name']
    slots=request.session['slots']
    end_time=request.session['end_time']
    start_time=request.session['start_time']
    scheduled_date_list=request.session['scheduled_date_list']
    actual_time_schedule=request.session['actual_time_schedule']
    schedule_id_of_each_slot=request.session['schedule_id_of_each_slot']
    ats_len=len(actual_time_schedule)
    get_time_list=[]
    for data in actual_time_schedule:
        get_time=request.POST.get(data)
        get_time_list.append(get_time)
    for data in range(0,len(get_time_list)):
        if get_time_list[data]==None:
            get_time_list[data]='N/A'
    final_time='final_time'
    form=AvailableDayScheduleMasterTemp(request.POST)
    count=0
    for data in scheduled_date_list:
        count=0
        for times in get_time_list:
            if times =='N/A':
                continue
            print('times',times)
            count+=1
            times=times.split('-')
            start_split_time=times[0]
            end_split_time=times[1]
            time_slot_id=doctor_name+'-'+data+'-'+str(count)
            add_records=AvailabilityIntradayScheduleMaster.objects.create(
            time_slot_id=time_slot_id,
            time_slot_start_time=start_split_time,
            time_slot_end_time=end_split_time,
            doctor_id=doctor_name,
            )
    records=AvailableDayScheduleMasterTemp.objects.get_or_create(
        doctor_id=doctor_name,
        dates_available=scheduled_date_list,
        schedule_id_of_each_slot=schedule_id_of_each_slot,
        time_slots=get_time_list,
        )
    context={
    'get_time_list':get_time_list,'final_time':final_time,'scheduled_date_list':scheduled_date_list,'start_time':start_time,'end_time':end_time,'slots':slots
    }
    return render(request,'testapp/time_scheduling.html',context)

#Appointment_dashboard
def doctor_dash(request):
    today=date.today()
    tomorrow=today+timedelta(1)
    print(tomorrow)
    print(today)
    records=BookedAppointments.objects.all().count()
    today_app=BookedAppointments.objects.filter(patient_appointment_date__contains=today).count()
    tomorrow_app=BookedAppointments.objects.filter(patient_appointment_date__contains=tomorrow).count()

    context={
    'records':records,'today_app':today_app,'tomorrow_app':tomorrow_app,
    }
    return render(request,'doctor/doctor_dash.html',context)
def doctor_appointment(request):
    records=BookedAppointments.objects.all()
    all_app_count=records.count()
    print('all_app_count',all_app_count)
    context={
    'records':records,
    }
    return render(request,'doctor/doctor_appointment.html',context)
def prescription(request):
    return render(request,'doctor/prescription.html')
@login_required(login_url='/user_login')
def appointment_list(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'appointment' in access.user_profile.screen_access or request.user.is_staff:
        try:
            doctor_appointment = BookedAppointments.objects.filter(location=request.location,created_by = request.user,patient_appointment_date=datetime.today())
            context = {
                'doctor_appointment':doctor_appointment
            }
            return render(request,'doctor/appointment_list.html',context)
        except Exception as error:
            return render(request,"error.html",{'error':error})
    else:
        return redirect("dashboard")
def patient_list(request):
    return render(request,'doctor/patient_list.html')
def interface_dashboard(request):
    return render(request,'interface/interface_dashboard.html')
def patient(request):
    return render(request,'interface/patient.html')
#=========================Reports=========================
def reports(request):
    return render(request,'admin1/reports.html')

def cancellation_reports(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    records=BookedAppointments.objects.filter( patient_scheduled_id='N/A',location=request.location)
    if from_date and to_date:
        records=BookedAppointments.objects.filter(patient_schedule_date_and_time__range = [from_date,to_date],patient_scheduled_id='N/A',location=request.location)
    return render(request,'admin1/cancellation_reports.html',{'records':records})

from django.db.models import Q, F, OuterRef
def shorting_filter(request):
    records = BookedAppointments.objects.all()
    consultant_name1 = [data.doctor_name for data in records]
    consultant_name = list(set(consultant_name1))
    department_name1 = [data.doctor_department for data in records]
    department_name = list(set(department_name1))
    if request.method=='POST':
        consultant=request.POST.get('consultant')
        department=request.POST.get('department')
        if 'department'==department:
            filtering_records=BookedAppointments.objects.filter(doctor_department=department,location=request.location)
            filtered='filter'
        else:
            filtering_records=BookedAppointments.objects.filter(doctor_name=consultant,location=request.location)
            filtered='filter'
        context={
        'consultant_name':consultant_name,'department_name':department_name,'filtered':filtered,'filtering_records':filtering_records,
        }
        return render(request,'admin1/shorting_filter.html',context)
    context={
    'consultant_name':consultant_name,'department_name':department_name,
    }
    return render(request,'admin1/shorting_filter.html',context)

def filtering_department(request):
    records = BookedAppointments.objects.all()
    consultant_name1 = [data.doctor_name for data in records]
    consultant_name = list(set(consultant_name1))
    department_name1 = [data.doctor_department for data in records]
    department_name = list(set(department_name1))
    consultant=request.POST.get('consultant')
    department = request.POST.get('department')
    filtered='filter'
    filtering_records=BookedAppointments.objects.filter(doctor_department=department,location=request.location)
    if consultant:
        filtering_records=BookedAppointments.objects.filter(doctor_name=consultant,location=request.location)
        filtered='filter'

    context={
    'consultant_name':consultant_name,'department_name':department_name,'filtered':filtered,'filtering_records':filtering_records,
    }
    return render(request,'admin1/shorting_filter.html',context)

def appointment_detail_reports(request):
    if request.method=='POST':
        start_date = request.POST.get('from_date')
        end_date = request.POST.get('to_date')
        records = None

        if start_date and end_date:
            records = BookedAppointments.objects.filter(patient_appointment_date__range=[start_date,end_date],location=request.location).order_by('-patient_appointment_date')

        elif len(request.POST.get('patient_name')) != 0:
            patient_name = request.POST.get('patient_name').strip()
            patient_name_1 = patient_name.split()
            if len(patient_name_1) == 3:
                records = BookedAppointments.objects.filter(Q(first_name__icontains = patient_name_1[0],location=request.location) | Q(middle_name__icontains = patient_name_1[1],location=request.location) | Q(last_name__icontains = patient_name_1[2],location=request.location))
            elif len(patient_name_1) == 2:
                records = BookedAppointments.objects.filter(Q(first_name = patient_name_1[0],location=request.location) | Q(middle_name__icontains = patient_name_1[1],location=request.location))
            elif len(patient_name_1) == 1:
                records = BookedAppointments.objects.filter(Q(first_name__icontains = patient_name_1[0],location=request.location))
        context={
        'records':records,
        }
        return render(request,'admin1/appointment_detail_reports.html',context)
    return render(request,'admin1/appointment_detail_reports.html')

def table(request):
    return render(request,'interface/table.html')
def doctor_admin_pannel(request):
    return HttpResponseRedirect('/accounts/login')

def sign_up_form(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)#To has password
            user.save()
            return HttpResponseRedirect('/admin_list_table')
    context={
    'form':form
    }
    return render(request,'registration/sign_up_form.html',context)

#++++++++++++++++++++++++++++++++++QMS Process+++++++++++++++++++++++++++++
#QMS Process
class TokenMasterConfiguration:
    def __init__(self,doc_id,doc_name,speciality,status,room_no,max_token_assigned):
        self.doc_id=doc_id
        self.doc_name=doc_name
        self.speciality=speciality
        self.status=status
        self.room_no=room_no
        self.max_token_assigned=max_token_assigned
    def fetch_data(self):
        pass
    def get_data(self):
        pass
class TokenCreation:
    def __init__(self,doc_id,doc_name,speciality,status,room_no,pt_id,is_app,app_id,toekn_no):
        pass
    def fetch_data(self):
        pass
    def get_data(self):
        pass
class TokenSlipGeneration:
    def __init__(self,room_no,pt_id,app_id,toekn_no):
        pass
    def fetch_data(self):
        pass
    def show_data(self):
        pass
class TokenSlipViewDeptWiseOPD:
    def __init__(self,room_no,pt_id,app_id,toekn_no):
        pass
    def fetch_data(self):
        pass
    def get_data(self):
        pass
class TokenSlipViewCentralisedAdmin:
    def __init__(self,room_no,pt_id,app_id,toekn_no):
        pass
    def fetch_data(self):
        pass
#=============date:28/02/2022======================
@login_required(login_url='/user_login')
def titile_master(request):
    title_master=TitleMaster.objects.all()
    context={
    'title_master':title_master
    }
    return render(request,'master_template/title_master.html',context)

@login_required(login_url='/user_login')
def add_new_title(request):
    form=TitleMasterForm()
    add='add'
    if request.method=='POST':
        form=TitleMasterForm(request.POST)
        if form.is_valid():
            form.save()
        context={
        'add':add,'form':form
        }
        return render(request,'master_template/title_master.html',context)
    context={
    'add':add,'form':form
    }
    return render(request,'master_template/title_master.html',context)

@login_required(login_url='/user_login')
def edit_title(request):
    title_master=TitleMaster.objects.all()
    form=TitleMasterForm()
    add='add'
    if request.method=='POST':
        form=TitleMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/title_master')
        context={
        'add':add,'form':form
        }
        return render(request,'general_master/edit_title_master.html',context)
    context={
    'title_master':title_master,'form':form
    }
    return render(request,'general_master/edit_title_master.html',context)

@login_required(login_url='/user_login')
def editing_title(request,pk):
    title_master=TitleMaster.objects.get(id=pk)
    form=TitleMasterForm(instance=title_master)
    editing='editing'
    if request.method=='POST':
        form=TitleMasterForm(request.POST,instance=title_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit-title')
        context={
        'form':form,'editing':editing
        }
        return render(request,'general_master/editing_title_master.html',context)
    context={
    'form':form,'editing':editing
    }
    return render(request,'general_master/editing_title_master.html',context)

@login_required(login_url='/user_login')
def hospital_master(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or request.user.is_staff:
        try:
            hospital_master=HospitalMaster.objects.all()
            form=HospitalMasterForm()
            if request.method=='POST':
                form=HospitalMasterForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/hospital-master')
            context={
            'hospital_master':hospital_master,'form':form,'access':access
            }
            return render(request,'general_master/hospital_master.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')
def add_new_hospital(request):
    form=HospitalMasterForm()
    if request.method=='POST':
        form=HospitalMasterForm(request.POST)
        if form.is_valid():
            form.save()
    add='add'
    context={
    'add':add,'form':form,
    }
    return render(request,'master_template/hospital_master.html',context)

@login_required(login_url='/user_login')
def edit_hospital_master(request):
    hospital_master=HospitalMaster.objects.all()
    editing='editing'
    form=HospitalMasterForm()
    if request.method=='POST':
        form=HospitalMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit-hospital-master')
    context={
    'hospital_master':hospital_master,'form':form
    }
    return render(request,'general_master/edit_hospital_master.html',context)

@login_required(login_url='/user_login')
def editing_hospital_master(request,pk):
    print('...edit...')
    hospital_master=HospitalMaster.objects.get(id=pk)
    form=HospitalMasterForm(instance=hospital_master)
    editing='editing'
    if request.method=='POST':
        form=HospitalMasterForm(request.POST,instance=hospital_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit-hospital-master')
        context={
        'form':form,'editing':editing
        }
        return render(request,'general_master/editing_hospital_master.html',context)
    context={
    'form':form,'editing':editing
    }
    return render(request,'general_master/editing_hospital_master.html',context)

#Master Related Url
# GENERAL_MASTER

@login_required(login_url='/user_login')
def relation(request):
    relation_master=RelationMaster.objects.all()
    form=RelationMasterForm()
    if request.method=='POST':
        form=RelationMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/relation')
    context={
    'relation_master':relation_master,'form':form,
    }
    return render(request,'general_master/relation.html',context)

@login_required(login_url='/user_login')
def edit_relation(request):
    relation_master=RelationMaster.objects.all()
    form=RelationMasterForm()
    if request.method=='POST':
        form=RelationMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/relation')
    context={
    'relation_master':relation_master,'form':form,
    }
    return render(request,'general_master/edit_relation.html',context)

@login_required(login_url='/user_login')
def editing_relation(request,pk):
    relation_master=RelationMaster.objects.get(id=pk)
    form=RelationMasterForm(instance=relation_master)
    if request.method=='POST':
        form=RelationMasterForm(request.POST,instance=relation_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_relation')
    context={
    'relation_master':relation_master,'form':form,
    }
    return render(request,'general_master/editing_relation.html',context)

@login_required(login_url='/user_login')
def city_master(request):
    city_master=CityMaster.objects.all()
    form=CityMasterForm()
    if request.method=='POST':
        form=CityMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/city_master')
    context={
    'city_master':city_master,'form':form
    }
    return render(request,'general_master/city_master.html',context)

@login_required(login_url='/user_login')
def edit_city_master(request):
    city_master=CityMaster.objects.all()
    form=CityMasterForm()
    if request.method=='POST':
        form=CityMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_city_master')
    context={
    'city_master':city_master,'form':form
    }
    return render(request,'general_master/edit_city_master.html',context)

@login_required(login_url='/user_login')
def editing_city_master(request,pk):
    city_master=CityMaster.objects.get(id=pk)
    form=CityMasterForm(instance=city_master)
    if request.method=='POST':
        form=CityMasterForm(request.POST,instance=city_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_city_master')
    context={
    'city_master':city_master,'form':form
    }
    return render(request,'general_master/editing_city_master.html',context)

@login_required(login_url='/user_login')
def country_master(request):
    country_master=CountryMaster.objects.all()
    form=CountryMasterForm()
    if request.method=='POST':
        form=CountryMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/country_master')
    context={
    'country_master':country_master,'form':form
    }
    return render(request,'general_master/country_master.html',context)

@login_required(login_url='/user_login')
def edit_country_master(request):
    country_master=CountryMaster.objects.all()
    form=CountryMasterForm()
    if request.method=='POST':
        form=CountryMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/country_master')
    context={
    'country_master':country_master,'form':form
    }
    return render(request,'general_master/edit_country_master.html',context)

@login_required(login_url='/user_login')
def editing_country_master(request,pk):
    country_master=CountryMaster.objects.get(id=pk)
    form=CountryMasterForm(instance=country_master)
    if request.method=='POST':
        form=CountryMasterForm(request.POST,instance=country_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit-country')
    context={
    'country_master':country_master,'form':form
    }
    return render(request,'general_master/editing_country_master.html',context)

@login_required(login_url='/user_login')
def district(request):
    district_master=DistrictMaster.objects.all()
    form=DistrictMasterForm()
    if request.method=='POST':
        form=DistrictMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/district')
    context={
    'district_master':district_master,'form':form
    }
    return render(request,'general_master/district.html',context)

@login_required(login_url='/user_login')
def edit_district(request):
    district_master=DistrictMaster.objects.all()
    form=DistrictMasterForm()
    if request.method=='POST':
        form=DistrictMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/district')
    context={
    'district_master':district_master,'form':form
    }
    return render(request,'general_master/edit_district.html',context)

@login_required(login_url='/user_login')
def editing_district(request,pk):
    district_master=DistrictMaster.objects.get(id=pk)
    form=DistrictMasterForm(instance=district_master)
    if request.method=='POST':
        form=DistrictMasterForm(request.POST,instance=district_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit-district')
    context={
    'district_master':district_master,'form':form
    }
    return render(request,'general_master/editing_district.html',context)

@login_required(login_url='/user_login')
def gender_master(request):
    gender_master=GenderMater.objects.all()
    form=GenderMaterForm()
    if request.method=='POST':
        form=GenderMaterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gender_master')
    context={
    'gender_master':gender_master,'form':form
    }
    return render(request,'general_master/gender_master.html',context)

@login_required(login_url='/user_login')
def add_new_gender_master(request):
    form=GenderMaterForm()
    if request.method=='POST':
        form=GenderMaterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gender_master')
    add='add'
    context={
    'add':add,'form':form,
    }
    return render(request,'master_template/gender_master.html',context)

@login_required(login_url='/user_login')
def edit_gender_master(request):
    gender_master=GenderMater.objects.all()
    form=GenderMaterForm()
    if request.method=='POST':
        form=GenderMaterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gender_master')
    context={
    'gender_master':gender_master,'form':form
    }
    return render(request,'general_master/edit_gender_master.html',context)

@login_required(login_url='/user_login')
def editing_gender_master(request,pk):
    gender_master=GenderMater.objects.get(id=pk)
    form=GenderMaterForm(instance=gender_master)
    if request.method=='POST':
        form=GenderMaterForm(request.POST,instance=gender_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gender_master')
    context={
    'gender_master':gender_master,'form':form
    }
    return render(request,'general_master/editing_gender_master.html',context)

@login_required(login_url='/user_login')
def holiday_master(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'master' in access.user_profile.screen_access or request.user.is_staff:
        try:
            holiday_master=HolidayMaster.objects.all()
            form=HolidayMasterForm()
            if request.method=='POST':
                form=HolidayMasterForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/holiday_master')
            context={
            'form':form,'holiday_master':holiday_master,'access':access
            }
            return render(request,'general_master/holiday_master.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')
def edit_holiday_master(request):
    holiday_master=HolidayMaster.objects.all()
    form=HolidayMasterForm()
    if request.method=='POST':
        form=HolidayMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_holiday_master')
    context={
    'holiday_master':holiday_master,'form':form
    }
    return render(request,'general_master/edit_holiday_master.html',context)

@login_required(login_url='/user_login')
def editing_holiday_master(request,pk):
    holiday_master=HolidayMaster.objects.get(id=pk)
    form=HolidayMasterForm(instance=holiday_master)
    if request.method=='POST':
        form=HolidayMasterForm(request.POST,instance=holiday_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/holiday_master')
    context={
    'holiday_master':holiday_master,'form':form
    }
    return render(request,'general_master/editing_holiday_master.html',context)

@login_required(login_url='/user_login')
def most_common_document(request):
    most_common_document=MostCommonDocumentTypeMaster.objects.all()
    form=MostCommonDocumentTypeMasterForm()
    if request.method=='POST':
        form=MostCommonDocumentTypeMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/most_common_document')
    context={
    'most_common_document':most_common_document,'form':form
    }
    return render(request,'general_master/most_common_document.html',context)

@login_required(login_url='/user_login')
def edit_most_common_document(request):
    most_common_document=MostCommonDocumentTypeMaster.objects.all()
    form=MostCommonDocumentTypeMasterForm()
    if request.method=='POST':
        form=MostCommonDocumentTypeMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_most_common_document')
    context={
    'most_common_document':most_common_document,'form':form
    }
    return render(request,'general_master/edit_most_common_document.html',context)

@login_required(login_url='/user_login')
def editing_most_common_document(request,pk):
    most_common_document=MostCommonDocumentTypeMaster.objects.get(id=pk)
    form=MostCommonDocumentTypeMasterForm(instance=most_common_document)
    print(form)
    if request.method=='POST':
        form=MostCommonDocumentTypeMasterForm(request.POST,instance=most_common_document)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_most_common_document')
    context={
    'most_common_document':most_common_document,'form':form
    }
    return render(request,'general_master/editing_most_common_document.html',context)

@login_required(login_url='/user_login')
def maritial_status(request):
    martial_status=MaritalStatusMaster.objects.all()
    form=MaritalStatusMasterForm()
    if request.method=='POST':
        form=MaritalStatusMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/maritial_status')

    context={
    'martial_status':martial_status,'form':form
    }
    return render(request,'general_master/maritial_status.html',context)

@login_required(login_url='/user_login')
def edit_maritial_status(request):
    martial_status=MaritalStatusMaster.objects.all()
    form=MaritalStatusMasterForm()
    if request.method=='POST':
        form=MaritalStatusMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_maritial_status')

    context={
    'martial_status':martial_status,'form':form
    }
    return render(request,'general_master/edit_maritial_status.html',context)

@login_required(login_url='/user_login')
def editing_maritial_status(request,pk):
    martial_status=MaritalStatusMaster.objects.get(id=pk)
    form=MaritalStatusMasterForm(instance=martial_status)
    if request.method=='POST':
        form=MaritalStatusMasterForm(request.POST,instance=martial_status)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_maritial_status')

    context={
    'martial_status':martial_status,'form':form
    }
    return render(request,'general_master/editing_maritial_status.html',context)

@login_required(login_url='/user_login')
def title_master(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser  or request.user.is_staff:
        # try:
        title_master=TitleMaster.objects.all()
        form=TitleMasterForm()
        add='add'
        if request.method=='POST':
            form=TitleMasterForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/title_master')
            context={
            'add':add,'form':form
            }
        context={
        'title_master':title_master,'form':form,'access':access
        }
        return render(request,'general_master/title_master.html',context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

#================service Master================
@login_required(login_url='/user_login')
def service_master(request):
    try:
        form=ServiceMasterForm()
        service_cat_obj=ServiceCategory.objects.all()
        service_sub_cat_obj=ServiceSubCategory.objects.all()
        records=None
        if request.method=='POST':
            form=ServiceMasterForm(request.POST)
            search=request.POST.get('searching')
            if search =='Search':
                service_category=request.POST.get('service_category')
                service_sub_category=request.POST.get('service_sub_category')
                records=ServiceMaster.objects.filter(service_category_id=service_category,service_sub_category_id=service_sub_category)
            if form.is_valid():
                form.save()
                print('SAVED SuccessFully')
                return HttpResponseRedirect('/service_master')
        context={
        'form':form,'service_cat_obj':service_cat_obj,'service_sub_cat_obj':service_sub_cat_obj,'records':records,
        }
        return render(request,'general_master/service_master.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def edit_service_master(request,pk):
    service_master=ServiceMaster.objects.get(id=pk)
    form=ServiceMasterForm(instance=service_master)
    if request.method=='POST':
        form=ServiceMasterForm(request.POST,instance=service_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/service_master')
    context={
    'service_master':service_master,'form':form
    }
    return render(request,'general_master/edit_service_master.html',context)

@login_required(login_url='/user_login')
def tariff_master(request):
    tariff_master=TariffMaster.objects.all()
    form=TariffMasterForm()
    if request.method=='POST':
        form=TariffMasterForm(request.POST)
        if form.is_valid():
            print('no no no')
            form.save()
            return HttpResponseRedirect('/tariff_master')
    context={
    'tariff_master':tariff_master,'form':form,
    }
    return render(request,'general_master/tariff_master.html',context)

@login_required(login_url='/user_login')
def edit_tariff_master(request):
    tariff_master=TariffMaster.objects.all()
    form=TariffMasterForm()
    if request.method=='POST':
        form=TariffMasterForm(request.POST)
        if form.is_valid():
            print('no no no')
            form.save()
            return HttpResponseRedirect('/tariff_master')
    context={
    'tariff_master':tariff_master,'form':form,
    }
    return render(request,'general_master/edit_tariff_master.html',context)

@login_required(login_url='/user_login')
def editing_tariff_master(request,pk):
    tariff_master=TariffMaster.objects.get(id=pk)
    form=TariffMasterForm(instance=tariff_master)
    if request.method=='POST':
        form=TariffMasterForm(request.POST,instance=tariff_master)
        if form.is_valid():
            print('no no no')
            form.save()
            return HttpResponseRedirect('/edit_tariff_master')
    context={
    'tariff_master':tariff_master,'form':form,
    }
    return render(request,'general_master/editing_tariff_master.html',context)

@login_required(login_url='/user_login')
def corporate_master(request):
    corporate_master=CorporateMaster.objects.all()
    form=CorporateMasterForm()
    if request.method=='POST':
        form=CorporateMasterForm(request.POST)
        cor_id=randint(101,501)
        corporate_ID=cor_id
        if form.is_valid():
            # CM=CorporateMaster(corporate_ID=cor_id,corporate_Name=corporate_Name,valid_Upto=valid_Upto,contact_No=contact_No,email_ID=email_ID,remark=remark,inactive=inactive,Office_Location_Name=Office_Location_Name,Auth_Person=Auth_Person,designation=Designation,address=address,City=city,PinCode=PinCode,phone_no=phone_no,fax=fax,email=email)
            form.save()
            return HttpResponseRedirect('/corporate_master')
    context={
    'corporate_master':corporate_master,'form':form
    }
    return render(request,'general_master/corporate_master.html',context)

@login_required(login_url='/user_login')
def edit_corporate_master(request):
    form=form=CorporateMasterForm()
    corporate_master = CorporateMaster.objects.all()
    context={
        'form':form,'corporate_master':corporate_master
    }
    return render(request,'general_master/edit_corporate_master.html',context)

@login_required(login_url='/user_login')
def editing_corporate_master(request,pk):
    corporate_master = CorporateMaster.objects.get(id=pk)
    form = form = CorporateMasterForm2(instance=corporate_master)
    if request.method=='POST':
        form = form = CorporateMasterForm2(request.POST,instance=corporate_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_corporate_master')
    context={
        'form':form,'corporate_master':corporate_master
    }
    return render(request,'general_master/editing_corporate_master.html',context)

@login_required(login_url='/user_login')
def billing_master(request):
    form=BillingGroupForm()
    records=BillingGroup.objects.all()
    if request.method=='POST':
        form=BillingGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('billing_master')
    context={
        'form':form,'records':records
    }
    return  render(request,'general_master/billing_master.html',context)

@login_required(login_url='/user_login')
def edit_billing_master(request):
    form=BillingGroupForm()
    records=BillingGroup.objects.all()
    if request.method=='POST':
        form=BillingGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('billing_master')
    context={
        'form':form,'records':records
    }
    return  render(request,'general_master/edit_billing_master.html',context)

@login_required(login_url='/user_login')
def editing_billing_master(request,id):
    records=BillingGroup.objects.get(id=id)
    form=BillingGroupForm(instance=records)
    if request.method=='POST':
        form=BillingGroupForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_billing_master')
    context={
        'form':form,'records':records
    }
    return  render(request,'general_master/editing_billing_master.html',context)

# ========================Service Charge Master For OPD By mantu======================
@login_required(login_url='/user_login')
def service_charge_master(request):
    try:
        service_charge_master=ServiceChargeMaster.objects.all()
        tariff_master=TariffMaster.objects.all()
        # ward_type=WardType.objects.all()
        # ward_category=WardCategory.objects.all()
        ward_type=AdmissionWardType.objects.all()
        ward_category=AdmissionWardCate.objects.all()
        service_category=ServiceCategory.objects.all()
        service_sub_category=ServiceSubCategory.objects.all()
        service_department=ServiceDepartment.objects.all()
        service_sub_department=ServiceSubDepartment.objects.all()
        form=ServiceChargeMaster()
        sd=service_department
        ssd=service_sub_department
        records=None
        if request.method=='POST':
            form=ServiceChargeMaster(request.POST)
            searching=request.POST.get('search')
            submit=request.POST.get('submit')
            if searching=='Search':
                service_department=request.POST.get('service_department')
                service_sub_department=request.POST.get('service_sub_department')
                records=ServiceMaster.objects.filter(service_department=service_department,ServiceSubDepartment_id=service_sub_department)
                s_d = ServiceDepartment.objects.get(id=service_department)
                s_s_d = ServiceSubDepartment.objects.get(id=service_sub_department)
                ser_dep=s_d.service_department
                ser_sub_dep=s_s_d.service_sub_department
                ser_dep_id=s_d.id
                ser_sub_dep_id=s_s_d.id
                context = {
                    'service_charge_master': service_charge_master, 'form': form, 'tariff_master': tariff_master,
                    'service_department': sd, 'service_sub_department': ssd,'service_category':service_category,'service_sub_category':service_sub_category,
                    'records': records,'s_d':ser_dep,'s_s_d':ser_sub_dep,'ser_dep_id':ser_dep_id,'ser_sub_dep_id':ser_sub_dep_id,'ward_type':ward_type,
                    'ward_category':ward_category,
                }
                return render(request, 'general_master/service_charge_master.html', context)
            elif submit=='Save':
                tariff_id = request.POST.get('tariff_id')
                service_id = request.POST.getlist('service_id')
                service_charge = request.POST.getlist('service_charge')
                applicable_date = request.POST.get('applicable_date')
                service_category = request.POST.getlist('service_category')
                service_sub_category = request.POST.getlist('service_sub_category')
                ward_type = request.POST.get('ward_type')
                ward_category = request.POST.get('ward_category')
                ipd_opd = request.POST.get('ipd_opd')
                print('alldata',ward_type,ward_category,ipd_opd)
                service_check = ''
                for d in range(len(service_id)):
                    var_tariff_id=tariff_id
                    var_service_id=service_id[d]
                    var_service_charge=service_charge[d]
                    var_applicable_date=applicable_date
                    var_service_category=service_category[d]
                    var_ward_type=ward_type
                    var_ward_category=ward_category
                    var_ipd_opd=ipd_opd
                    var_service_sub_category=service_sub_category[d]
                    if ipd_opd == 'OPD':
                        service_check=ServiceChargeMaster.objects.filter(tariff_id=var_tariff_id,service_id=var_service_id,ipd_opd='OPD')
                    else:
                        service_check=ServiceChargeMaster.objects.filter(tariff_id=var_tariff_id,service_id=var_service_id,ward_type=var_ward_type,ward_category=var_ward_category,ipd_opd='IPD')
                    if not service_check.exists():
                        data =ServiceChargeMaster(
                            tariff_id_id=var_tariff_id,
                            service_id_id=var_service_id,
                            service_charge=var_service_charge,
                            applicable_date=var_applicable_date,
                            service_category_id=var_service_category,
                            service_sub_category_id=var_service_sub_category,
                            ward_type_id=var_ward_type,
                            ward_category_id=var_ward_category,
                            # inactive=var_inactive,
                            ipd_opd=var_ipd_opd,
                            created_by_id = request.user.id,
                            location_id = request.location,
                        )
                        data.save()
                        print('data saved..............',data)
                    else:
                        print('data allready there-------------...')
                return HttpResponseRedirect('/service_charge_master')
        context={
            'service_charge_master':service_charge_master,'form':form,'tariff_master':tariff_master,'service_category':service_category,'service_sub_category':service_sub_category,
            'service_department':service_department,'service_sub_department':service_sub_department,'records':records,'ward_category':ward_category,'ward_type':ward_type,
        }
        return render(request,'general_master/service_charge_master.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})
#============================End Service Charge Master=====================

@login_required(login_url='/user_login')
def tariff_charge_master(request):
    try:
        print('This is tariff charge master...')
        tariff_charge_master=TariffChargeMaster.objects.all()
        tariff_master=TariffMaster.objects.all()
        service_department=ServiceDepartment.objects.all()
        service_sub_department=ServiceSubDepartment.objects.all()
        form=TariffChargeMasterForm()
        sd=service_department
        ssd=service_sub_department
        records=None
        if request.method=='POST':
            form=TariffChargeMasterForm(request.POST)
            searching=request.POST.get('search')
            submit=request.POST.get('submit')
            if searching=='Search':
                print('Im searching data...')
                service_department=request.POST.get('service_department')
                service_sub_department=request.POST.get('service_sub_department')
                records=ServiceMaster.objects.filter(service_department__in=service_department)&ServiceMaster.objects.filter(ServiceSubDepartment_id__in=service_sub_department)
                # return HttpResponseRedirect('/tariff_charge_master')
                s_d = ServiceDepartment.objects.get(id=service_department)
                s_s_d = ServiceSubDepartment.objects.get(id=service_sub_department)
                ser_dep=s_d.service_department
                ser_sub_dep=s_s_d.service_sub_department
                ser_dep_id=s_d.id
                ser_sub_dep_id=s_s_d.id
                context = {
                    'tariff_charge_master': tariff_charge_master, 'form': form, 'tariff_master': tariff_master,
                    'service_department': sd, 'service_sub_department': ssd,
                    'records': records,'s_d':ser_dep,'s_s_d':ser_sub_dep,'ser_dep_id':ser_dep_id,'ser_sub_dep_id':ser_sub_dep_id,
                }
                return render(request, 'general_master/tariff_charge_master.html', context)
            elif submit=='Save':
                print('Im ready to save your data')
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/tariff_charge_master')
        context={
        'tariff_charge_master':tariff_charge_master,'form':form,'tariff_master':tariff_master,
            'service_department':service_department,'service_sub_department':service_sub_department,'records':records
        }
        return render(request,'general_master/tariff_charge_master.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def edit_tariff_charge_master(request):
    form = TariffChargeMasterForm()
    tariff_charge_master = TariffChargeMaster.objects.all()
    context={
        'form': form, 'tariff_charge_master': tariff_charge_master,
    }
    return render(request,'general_master/edit_tariff_charge_master.html',context)

@login_required(login_url='/user_login')
def editing_tariff_charge_master(request,pk):
    tariff_charge_master = TariffChargeMaster.objects.get(id=pk)
    form = TariffChargeMasterForm(instance=tariff_charge_master)
    if request.method=='POST':
        form=TariffChargeMasterForm(request.POST,instance=tariff_charge_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_tariff_charge_master')
    context={
        'form':form,'tariff_charge_master':tariff_charge_master,
    }
    return render(request,'general_master/editing_tariff_charge_master.html',context)

@login_required(login_url='/user_login')
def add_charge(request):
    if request.method=='POST':
        qdict=request.POST
        print('Our Dict = ',qdict)
        sample_dict=dict(qdict.lists())
        service_id=sample_dict.get('service_id')
        charges=sample_dict.get('charges')
        print('service_id= ',service_id)
        print('charges= ',charges)
        if service_id is  None and charges is None:
            return HttpResponseRedirect('/service_charge_master')
        service_master=ServiceMaster.objects.filter(id__in=service_id)
        if service_master.exists():
            for id in range(service_master.count()):
                if charges[id]=='':
                    continue
                adding_charge = ServiceMaster.objects.get(id=service_id[id])
                adding_charge.Charges = charges[id]  # updating
                adding_charge.save()  # Saving
                # print(f'id =  {service_id[id]} Charges = {charges[id]}')

        # return HttpResponseRedirect('/service_charge_master')
    return HttpResponseRedirect('/service_charge_master')

@login_required(login_url='/user_login')
def billing_group_tariff(request):
    billing_gtl=BillingGroupTariffLink.objects.all()
    form=BillingGroupTariffLinkForm()
    if request.method=='POST':
        form=BillingGroupTariffLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/billing_group_tariff')
    context={
    'form':form,'billing_gtl':billing_gtl
    }
    return render(request,'general_master/billing_group_tariff.html',context)
#master dashboard

@login_required(login_url='/user_login')
def master_dashboard(request):
    return render(request,'general_master/master_dashboard.html')
#=================QMS========================
@login_required(login_url='/user_login')
def qms_dashboard(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'qms' in access.user_profile.screen_access or request.user.is_staff:
        today = datetime.today().date()
        today_token = TokenMasterConf.objects.filter(Date = today)
        token_created = TokenCreationDone.objects.filter(Date = today,location=request.location)   
        token_created1 = token_created.count()
        today_token1 = 0
        avail_dr_count = 0
        available_doctor = []
        for data in today_token:
            dict = {}
            today_token1+=data.Max_Token_Assigned
            avail_dr_count+=1
            dict["Doctor_name"] = data.Doct_Name
            dict["specialist"] = data.Doct_Name.doctor_department
            dict["room_no"] = data.Room_No
            dict["profile"] = data.Doct_Name.doctor_profile_image
            available_doctor.append(dict)   
        context = {
            'today_token1':today_token1,'access':access,'avail_dr_count':avail_dr_count,"available_doctor":available_doctor,
            'token_created1':token_created1,'token_created':token_created
        }
        return render(request,'qms/qms_dashboard.html',context)
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')
def token_master_configuration(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'token_master_configuration' in access.user_profile.screen_access or request.user.is_staff:
        try:
            form=TokenMasterConfigurationForm()
            form2=ReplicatedForm()
            if request.method == 'POST':
                replicate = request.POST.get('replicate')
                if replicate == 'ReplicatedSave':
                    start_date = request.POST.get('start_date')
                    end_date = request.POST.get('end_date')
                    Doct_Name = request.POST.get('Doct_Name')
                    doct_id = Doct_Name
                    status = request.POST.get('status')
                    Room_No = request.POST.get('Room_No')
                    Max_Token_Assigned = request.POST.get('Max_Token_Assigned')
                    # Spliting date
                    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                    date_array = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1))
                    date_list=[]
                    for date_object in date_array:
                        date_object=date_object.strftime("%Y-%m-%d")
                        date_list.append(date_object)
                    for data in range(0,len(date_list)):
                        Doct_Name=doct_id
                        doctor_name=DoctorTable.objects.get(doctor_id=Doct_Name)
                        Doct_Name=doctor_name.doctor_name
                        replicated_tmc=ReplicatedTokenMasterConf(Date=date_list[data],Doct_Name=Doct_Name,status=status,Room_No=Room_No,Max_Token_Assigned=Max_Token_Assigned)
                        replicated_tmc.save()
                else:
                    form=TokenMasterConfigurationForm(request.POST)
                    if form.is_valid():
                        data=form.save(commit=False)
                        data.created_by_id=request.user.id
                        data.location_id=request.location
                        data.save()
                        return HttpResponseRedirect('/token_master_configuration')
                    context={
                    'form':form
                    }
                    return render(request,'qms/token_master_configuration.html',context)
            tmc = TokenMasterConf.objects.filter(Date=date.today(),location=request.location)
            context={
            'form':form,'tmc':tmc,'form2':form2
            }
            return render(request,'qms/token_master_configuration.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

#==========Token Master Conf Edit=========================
@login_required(login_url='/user_login')
def token_master_configuration_update(request,pk):
    tmc=TokenMasterConf.objects.get(id=pk)
    form=TokenMasterConfigurationForm(instance=tmc)
    if request.method=='POST':
        form=TokenMasterConfigurationForm(request.POST,instance=tmc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/token_master_configuration')
        print('Invalid Data')
    context={
    'form':form,
    }
    return render(request,'qms/token_master_configuration_update.html',context)
from django.contrib import messages#import Messages
# ========= Token Creation====================

@login_required(login_url='/user_login')
def token_creation2(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'token_creation' in access.user_profile.screen_access or request.user.is_staff:
        try:
            form=TokenCreationForm2()
            if request.method=='POST':
                form=TokenCreationForm2(request.POST)
                if form.is_valid():
                    Date = request.POST.get('Date').strip()
                    Doct_Name = request.POST.get('Doct_Name').strip()
                    D_Name = form.cleaned_data['Doct_Name']
                    Pt_Id = request.POST.get('Patient_Id').strip()
                    searching_patient_id = BookedAppointments.objects.filter(patient_id__iexact=Pt_Id)
                    searching_doctor_id = DoctorTable.objects.filter(doctor_id__iexact=Doct_Name)

                    for data in searching_doctor_id:
                        doc_id = data.doctor_id
                        doc_name = data.doctor_name
                        doc_speciality = data.doctor_department

                        request.session['Date'] = Date
                        request.session['doc_id'] = doc_id
                        request.session['doc_name'] = doc_name
                        request.session['doc_speciality'] = doc_speciality
                    doc_id = request.session['doc_id']
                    doc_name = request.session['doc_name']
                    doc_speciality = request.session['doc_speciality']
                    if searching_patient_id.exists():
                        for data in searching_patient_id:
                            patient_name = f'{data.first_name} {data.middle_name} {data.last_name}'
                            request.session['pt_id']=data.patient_id
                            request.session['pt_name']=patient_name
                        form = TokenCreationForm3()
                        pt_id = request.session['pt_id']
                        pt_name = request.session['pt_name']
                        get_max_token = TokenMasterConf.objects.filter(Date=date.today())&TokenMasterConf.objects.filter(Doct_Name=doc_id)
                        get_booked_token = TokenCreationDone.objects.filter(Date=date.today(),location=request.location)&TokenCreationDone.objects.filter(Doct_id=doc_id,location=request.location)
                        booked_token = []
                        if get_booked_token.exists():
                            for data in get_booked_token:
                                booked_token.append(int(data.Token_No))
                        tokens = None
                        if get_max_token.exists():
                            for data in get_max_token:
                                assigned_token=data.Max_Token_Assigned
                            tokens = []
                            for data in range(1,assigned_token+1):
                                tokens.append(data)
                            #Login to removing item from two dirrent list
                            res = list(set(tokens)^set(booked_token))
                            tokens = res
                        tc = TokenCreationDone.objects.filter(Date=date.today(),location=request.location)
                        context={
                        'doc_id':doc_id, 'doc_name':doc_name,'doc_speciality':doc_speciality,'pt_id':pt_id,'pt_name':pt_name,'form':form,'token':tokens,'tc':tc,
                        }
                        return render(request,'qms/token_creation3.html',context)
            tc=TokenCreationDone.objects.filter(Date=date.today(),location=request.location)
            context={
            'form':form,'tc':tc,
            }
            return render(request,'qms/token_creation2.html',context)
        except Exception as error:
            return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def token_creation(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'token_creation' in access.user_profile.screen_access or request.user.is_staff:
        try:
            if request.method=='POST':
                Date=request.session['Date']
                doc_id=request.session['doc_id']
                Doct_Name=request.session['doc_name']
                doc_speciality=request.session['doc_speciality']
                pt_id=request.session['pt_id']
                pt_name=request.session['pt_name']
                Token_No=request.POST.get('token')
                Room_No=request.POST.get('Room_No')
                print(f'Room No {Room_No}, Token No {Token_No}, Doctor name {Doct_Name}')
                tcd=TokenCreationDone(Date=Date,Doct_id=doc_id,Doct_Name=Doct_Name,speciality=doc_speciality,Pt_Id=pt_id,Pt_Name=pt_name,Token_No=Token_No,Room_No=Room_No,created_by_id=request.user.id,location_id=request.location,)
                tcd.save()
                return HttpResponseRedirect('/token_creation2')
            # doc_id=request.session['doc_id']
            tc=TokenCreationDone.objects.filter(Date=date.today(),location=request.location)
            # mtc=TokenMasterConf.objects.filter(Date=date.today())&TokenMasterConf.objects.filter(Doct_Name=doc_id)
            context={
            'tc':tc,'access':access
            }
            return render(request,'qms/token_creation2.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

# ======department View=================================
@login_required(login_url='/user_login')
def opd_reception_view(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'token_admin_view' in access.user_profile.screen_access or request.user.is_staff:
        try:
            records2=TokenMasterConf.objects.filter(Q(Date=date.today(),location=request.location)&Q(status='Out'),location=request.location)
            out_list=[]
            for data in records2:
                doct=data.Doct_Name
                out_list.append(doct)
            if request.method=='POST':
                capture_time=request.POST.get('save')
                next_save = request.POST.get('missing_button')
                inside_room = request.POST.get('Inside')
                if capture_time == "Patient_Out":
                    patient_id = request.POST.get('patient_id')
                    doctor_name = request.POST.get('doctor_name')
                    start_time = request.POST.get('start_time')
                    end_time = request.POST.get('end_time')
                    commonid = request.POST.get('commonid')
                    records=TokenCreationDone.objects.exclude(Doct_Name__in=out_list,status = "Waiting" ).get(id=commonid,Date=date.today(),location=request.location)
                    records.status = "Patient Out"
                    records.save()
                    tt=TimeTaken(patient_id=patient_id,doctor_name=doctor_name,start_time=start_time,end_time=end_time)
                    tt.save()
                elif next_save:
                    ids = next_save.split('.')
                    records=TokenCreationDone.objects.get(id=ids[1],Date=date.today(),status__in = ["Waiting","Missed Patient"],location=request.location)
                    records.status = "Missed Patient"
                    records.save()
                elif inside_room:
                    ids = inside_room.split('.')
                    records = TokenCreationDone.objects.get(id=ids[1],Date=date.today(),status__in = ["Waiting","Missed Patient","Inside"],location=request.location)
                    records.status = "Inside"
                    records.save() 
            records = TokenCreationDone.objects.exclude(Doct_Name__in=out_list).filter(Date=date.today(),status__in = ["Waiting","Missed Patient","Inside"],location=request.location)
            context={
                'records':records,'access':access
            }
            return render(request,'qms/opd_reception_view.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
# ============Centralised view=========================

@login_required(login_url='/user_login')
def centralised_admin_view(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'centralized_view' in access.user_profile.screen_access or request.user.is_staff:
        try:
            cav=TokenCreationDone.objects.filter(Date=date.today(),location=request.location)
            return render(request,'qms/centralised_admin_view.html',{'cav':cav})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def token_slip_generation(request,pk):
    tc=TokenCreationDone.objects.get(id=pk)
    context={
    'tc':tc,
    }
    return render(request,'qms/token_slip_generation.html',context)

@login_required(login_url='/user_login')
def token_slip_generations(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'token_slip_generation' in access.user_profile.screen_access or request.user.is_staff:
        try:
            tc=TokenCreationDone.objects.filter(Date=date.today(),location=request.location)
            context={
            'tc':tc,'access':access
            }
            return render(request,'qms/token_slip_gen.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

# Clinical Dashboard
@login_required(login_url='/user_login')
def dashboard(request):
    request.session['Name']='karan'
    request.session['doctor']='karan'
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    context={
        'access':access
    }
    return render(request,'clinical/dashboard.html',context)

def partially_dashboard(request):
    return render(request,'clinical/partially_dashboard.html')
# =============Start Patient Registration==================
def calculateAge(birthDate):
    birthDate = datetime.strptime(birthDate, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))

    return age

# registeration for appointment patient
@login_required(login_url='/user_login')
def appoint_patient_register(request,pk):
    appointment_patient = BookedAppointments.objects.get(patient_appointment_id = pk)
    import random
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'patient_registration' in access.user_profile.screen_access or request.user.is_staff:
        i = 0
        refered_bymaster = ''
        if i == 0:
            refered_bymaster = Refered_by_Master.objects.all()
            current_date=date.today()
            registration_date_and_time=''
            mobile_number = ''
            patient_name = ''
            first_name = ''
            middle_name = ''
            last_name = ''
            uhid=''
            appointment_id=''
            emergency_contact_person=''
            search_app_id=request.GET.get('search_app_id')
            search_uhid=request.GET.get('search_uhid')
            form_visit=PatientVisitMainForm()
            if search_app_id == 'IsAppointmentId':
                appointment_id = request.GET.get('appointment_id').strip()
                try:
                    app_related_records=BookedAppointments.objects.get(patient_appointment_id = appointment_id)
                    first_name=app_related_records.first_name
                    middle_name=app_related_records.middle_name
                    last_name=app_related_records.last_name
                    registration_date_and_time = app_related_records.patient_schedule_date_and_time
                except:
                    pass
            if search_uhid=='IsUHID':
                uhid=request.GET.get('uhid')
                try:
                    uhid_related_records=PatientRegistrationMains.objects.get(uhid=uhid)
                    uhid_related_records2=PatientRegistrationSub.objects.get(uhid=uhid)
                    registration_date_and_time=uhid_related_records2.registration_date_and_time
                    mobile_number=uhid_related_records2.mobile_number
                    first_name=uhid_related_records.first_name
                    middle_name=uhid_related_records.middle_name
                    last_name=uhid_related_records.last_name
                except:
                    pass

            # form=PatientRegistrationForm()
            if request.method=='POST':
                appointment_id=request.POST.get('appointment_id')
                uhid=request.POST.get('uhid')
                patient_profile=request.FILES.get('patient_profile')
                registration_date_and_time=request.POST.get('registration_date_and_time')
                patient_name=request.POST.get('patient_name')
                mobile_number=request.POST.get('mobile_number')
                title=request.POST.get('title')
                first_name=request.POST.get('first_name')
                middle_name=request.POST.get('middle_name')
                last_name=request.POST.get('last_name')
                dob=request.POST.get('dob')
                #== here some thing ===========
                age=calculateAge(dob)
                gender=request.POST.get('gender')
                blood_group=request.POST.get('blood_group')
                marital_status=request.POST.get('marital_status')
                father_or_husband_name=request.POST.get('father_or_husband_name')
                mother_name=request.POST.get('mother_name')
                mobile_number=request.POST.get('mobile_number')
                address=request.POST.get('address')
                referred_by=request.POST.get('referred_by')
                city=request.POST.get('city')
                state=request.POST.get('state')
                country=request.POST.get('country')
                pin_code=request.POST.get('pin_code')
                aadhar_number=request.POST.get('aadhar_number')
                pan_number=request.POST.get('pan_number')
                emergency_contact_person=request.POST.get('emergency_contact_person')
                emergency_contact_num=request.POST.get('emergency_contact_num')
                alternate_contact_number=request.POST.get('alternate_contact_number')
                nationality=request.POST.get('nationality')
                email_id=request.POST.get('email_id')
                staff_member=request.POST.get('staff_member')
                relationship=request.POST.get('relationship')
                allow_photo=request.POST.get('allow_photo')
                notable=request.POST.get('notable')
                cash=request.POST.get('cash')
                senior_citizen=request.POST.get('senior_citizen')
                billing_group=request.POST.get('billing_group')
                corporate_name=request.POST.get('corporate_name')
                cardholder_name=request.POST.get('nhif_ins_cor_id')
                card_number=request.POST.get('card_number')
                relation=request.POST.get('relation')
                ins_doc_upload=request.FILES.get('ins_doc_upload')
                choose_ins_doc=request.POST.getlist('choose_ins_doc')
                ins_id_upload = request.FILES.get('ins_id_upload')

                """
                'uhid':uhid,'registration_date_and_time':registration_date_and_time,'patient_name':patient_name,'mobile_number':mobile_number,'title':title,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'dob':dob,'gender':gender,'blood_group':blood_group,'marital_status':marital_status,'father_or_husband_name':father_or_husband_name,
                'mother_name':mother_name,'address':address,'address':address,'referred_by':referred_by,'city':city,'state':state,
                'country':country,'pin_code':pin_code,'aadhar_number':aadhar_number,'pan_number':pan_number,'emergency_contact_person':emergency_contact_person,'emergency_contact_num':emergency_contact_num,'alternate_contact_number':alternate_contact_number,'nationality':nationality,'email_id':email_id,'staff_member':staff_member,'relationship':relationship,'allow_photo':allow_photo,'notable':notable,'cash':cash,'senior_citizen':senior_citizen,'billing_group':billing_group,
                'corporate_name':corporate_name,'cardholder_name':cardholder_name,'card_number':card_number,'relation':relation,
                'valid_upto':valid_upto,'sum_insured_amount':sum_insured_amount,'InActive':InActive,'first_name':first_name,"middle_name":middle_name,'last_name':last_name,
                """
                valid_upto=request.POST.get('valid_upto')
                sum_insured_amount=request.POST.get('sum_insured_amount')
                if not valid_upto:
                    valid_upto = None
                InActive=request.POST.get('InActive')

                # Start Generating UHID In Some Format
                no_of_patient_registered = PatientRegistrationMains.objects.all().count()
                today = date.today()
                today = today.strftime("%y%m%d")
                if len(str(no_of_patient_registered)) == 1:
                    uhid = 'UHID' + today + '000' + str(no_of_patient_registered)
                elif len(str(no_of_patient_registered)) == 2:
                    uhid = 'UHID' + today + '00' + str(no_of_patient_registered)
                elif len(str(no_of_patient_registered)) == 3:
                    uhid = 'UHID' + today + '0' + str(no_of_patient_registered)
                else:
                    uhid = 'UHID' + today + str(no_of_patient_registered)
                otp= str(random.randint(100000, 999999))
                request.session['otp']=otp
                request.session['email_id']=email_id
                # End Generating UHID In Some Format
                mail1 = EmailMessage('this is for verification',otp, settings.EMAIL_HOST_USER, [email_id])
                mail1.send()
                patient_regist_main=PatientRegistrationMains(
                uhid=uhid,title=title,first_name=first_name,middle_name=middle_name,last_name=last_name,age=age,dob=dob,gender=gender,
                    created_by_id=request.user.id, location_id=request.location,
                )
                patient_regist_sub=PatientRegistrationSub(
                uhid=uhid,registration_date_and_time=registration_date_and_time,blood_group=blood_group,marital_status=marital_status,father_or_husband_name=father_or_husband_name,mother_name=mother_name,address=address,referred_by=referred_by,city=city,state=state,country=country,pin_code=pin_code,aadhar_card=aadhar_number,pan_card=pan_number,emergency_contact_person=emergency_contact_person,emergency_contact_num=emergency_contact_num,alternate_contact_number=alternate_contact_number,nationality=nationality,email=email_id,staff_member=staff_member,mobile_number=mobile_number,relationship=relationship,allow_photo_at_nursing_station=allow_photo,notable=notable,
                    created_by_id=request.user.id, location_id=request.location,
                )
                patient_billing_info=PatientBillingInfos(
                uhid=uhid,in_cash=cash,is_senior_citizen=senior_citizen,billing_group=billing_group,nhif_ins_cor_name=corporate_name,nhif_ins_cor_id=cardholder_name,relation=relation,card_number=card_number,valid_upto=valid_upto,sum_insured_amount=sum_insured_amount,
                is_inactive=InActive,created_by_id=request.user.id,location_id=request.location,
                )
                pr_single_table=PatientsRegistrationsAllInOne(
                uhid=uhid,title=title,first_name=first_name,middle_name=middle_name,last_name=last_name,age=age,dob=dob,gender=gender,patient_profile=patient_profile,registration_date_and_time=registration_date_and_time,blood_group=blood_group,marital_status=marital_status,father_or_husband_name=father_or_husband_name,mother_name=mother_name,address=address,referred_by=referred_by,city=city,state=state,country=country,pin_code=pin_code,aadhar_card=aadhar_number,pan_card=pan_number,next_of_kin=emergency_contact_person,next_of_kin_mob_no=emergency_contact_num,alternate_contact_number=alternate_contact_number,nationality=nationality,email=email_id,staff_member=staff_member,mobile_number=mobile_number,relationship=relationship,allow_photo_at_nursing_station=allow_photo,notable=notable,in_cash=cash,is_senior_citizen=senior_citizen,billing_group=billing_group,nhif_ins_cor_name=corporate_name,nhif_ins_cor_id=cardholder_name,relation=relation,card_number=card_number,valid_upto=valid_upto,sum_insured_amount=sum_insured_amount,ins_doc_upload=ins_doc_upload,
                ins_id_upload=ins_id_upload,created_by_id=request.user.id,location_id=request.location,
                is_inactive=InActive,appointment_id = pk
                )
                patient_bar_code=PatientBarCode(uhid=uhid)
                patient_profile=PatientProfile(uhid=uhid,p_images=patient_profile)
                patient_regist_main.save()
                patient_regist_sub.save()
                patient_billing_info.save()
                patient_bar_code.save()
                patient_profile.save()
                pr_single_table.save()
                for dt in range(len(choose_ins_doc)):
                    dt_doc=choose_ins_doc[dt]

                    patiet_doct = PatientInsDocType(uhid=uhid,billing_group=billing_group,nhif_ins_corp_name=corporate_name,doc_type=dt_doc)
                    patiet_doct.save()
                # request.session['visit_uhid']=uhid
                capturing_dt=PatientRegistrationSub.objects.get(uhid=uhid)
                registration_date_and_time=capturing_dt.registration_date_and_time
                context={
                    'uhid':uhid,'registration_date_and_time':registration_date_and_time,'patient_name':patient_name,'mobile_number':mobile_number,'title':title,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'dob':dob,'gender':gender,'blood_group':blood_group,'marital_status':marital_status,'father_or_husband_name':father_or_husband_name,
                    'mother_name':mother_name,'address':address,'address':address,'referred_by':referred_by,'city':city,'state':state,
                    'country':country,'pin_code':pin_code,'aa dhar_number':aadhar_number,'pan_number':pan_number,'emergency_contact_person':emergency_contact_person,'emergency_contact_num':emergency_contact_num,'alternate_contact_number':alternate_contact_number,'nationality':nationality,'email_id':email_id,'staff_member':staff_member,'relationship':relationship,'allow_photo':allow_photo,'notable':notable,'cash':cash,'senior_citizen':senior_citizen,'billing_group':billing_group,
                    'corporate_name':corporate_name,'cardholder_name':cardholder_name,'card_number':card_number,'relation':relation,
                    'valid_upto':valid_upto,'sum_insured_amount':sum_insured_amount,'InActive':InActive,'access':access,'first_name':first_name,"middle_name":middle_name,'last_name':last_name,
                }
                return HttpResponseRedirect('/veryf_otp',context)
            visited = PatientVisitMains.objects.all().order_by('-id')
            corporate=CorporateMaster.objects.all()
            billing=BillingGroup.objects.all()
            ins_records=Ins_Document.objects.all()
            relation_master = RelationMaster.objects.all
            relation_nhif = Relation.objects.all()
            context={
            'registration_date_and_time':registration_date_and_time,'form_visit':form_visit,'relation_nhif':relation_nhif,
            'mobile_number':mobile_number,'first_name':patient_name,'uhid':uhid,'visited':visited,'appointment_id':appointment_id,
            'corporate':corporate,'billing':billing,'ins_records':ins_records,'relation_master':relation_master,'access':access,'first_name':first_name,"middle_name":middle_name,'last_name':last_name,"refered_bymaster":refered_bymaster,
            'appointment_patient':appointment_patient }
            return render(request,'clinical/appoint_patient_register.html',context)

    else:
        return redirect('dashboard')


# Patient Registration

@login_required(login_url='/user_login')
def patient_registration(request):
    import random
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'patient_registration' in access.user_profile.screen_access or request.user.is_staff:
        i = 0
        refered_bymaster = ''
        if i == 0:
            refered_bymaster = Refered_by_Master.objects.all()
            current_date=date.today()
            registration_date_and_time=''
            mobile_number=''
            patient_name=''
            first_name=''
            middle_name = ''
            last_name = ''
            uhid=''
            appointment_id=''
            emergency_contact_person=''
            search_app_id=request.GET.get('search_app_id')
            search_uhid=request.GET.get('search_uhid')
            form_visit=PatientVisitMainForm()
            if search_app_id == 'IsAppointmentId':
                appointment_id = request.GET.get('appointment_id').strip()
                try:
                    app_related_records=BookedAppointments.objects.get(patient_appointment_id = appointment_id)
                    first_name=app_related_records.first_name
                    middle_name=app_related_records.middle_name
                    last_name=app_related_records.last_name
                    registration_date_and_time = app_related_records.patient_schedule_date_and_time
                except:
                    pass
            if search_uhid=='IsUHID':
                uhid=request.GET.get('uhid')
                try:
                    uhid_related_records=PatientRegistrationMains.objects.get(uhid=uhid)
                    uhid_related_records2=PatientRegistrationSub.objects.get(uhid=uhid)
                    registration_date_and_time=uhid_related_records2.registration_date_and_time
                    mobile_number=uhid_related_records2.mobile_number
                    first_name=uhid_related_records.first_name
                    middle_name=uhid_related_records.middle_name
                    last_name=uhid_related_records.last_name
                except:
                    pass

            # form=PatientRegistrationForm()
            if request.method=='POST':
                appointment_id=request.POST.get('appointment_id')
                uhid=request.POST.get('uhid')
                patient_profile=request.FILES.get('patient_profile')
                registration_date_and_time=request.POST.get('registration_date_and_time')
                patient_name=request.POST.get('patient_name')
                mobile_number=request.POST.get('mobile_number')
                title=request.POST.get('title')
                first_name=request.POST.get('first_name')
                middle_name=request.POST.get('middle_name')
                last_name=request.POST.get('last_name')
                dob=request.POST.get('dob')
                #== here some thing ===========
                age=calculateAge(dob)
                gender=request.POST.get('gender')
                blood_group=request.POST.get('blood_group')
                marital_status=request.POST.get('marital_status')
                father_or_husband_name=request.POST.get('father_or_husband_name')
                mother_name=request.POST.get('mother_name')
                mobile_number=request.POST.get('mobile_number')
                address=request.POST.get('address')
                referred_by=request.POST.get('referred_by')
                city=request.POST.get('city')
                state=request.POST.get('state')
                country=request.POST.get('country')
                pin_code=request.POST.get('pin_code')
                aadhar_number=request.POST.get('aadhar_number')
                pan_number=request.POST.get('pan_number')
                emergency_contact_person=request.POST.get('emergency_contact_person')
                emergency_contact_num=request.POST.get('emergency_contact_num')
                alternate_contact_number=request.POST.get('alternate_contact_number')
                nationality=request.POST.get('nationality')
                email_id=request.POST.get('email_id')
                staff_member=request.POST.get('staff_member')
                relationship=request.POST.get('relationship')
                allow_photo=request.POST.get('allow_photo')
                notable=request.POST.get('notable')
                cash=request.POST.get('cash')
                senior_citizen=request.POST.get('senior_citizen')
                billing_group=request.POST.get('billing_group')
                corporate_name=request.POST.get('corporate_name')
                cardholder_name=request.POST.get('nhif_ins_cor_id')
                card_number=request.POST.get('card_number')
                relation=request.POST.get('relation')
                ins_doc_upload=request.FILES.get('ins_doc_upload')
                choose_ins_doc=request.POST.getlist('choose_ins_doc')
                ins_id_upload = request.FILES.get('ins_id_upload')

                """
                'uhid':uhid,'registration_date_and_time':registration_date_and_time,'patient_name':patient_name,'mobile_number':mobile_number,'title':title,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'dob':dob,'gender':gender,'blood_group':blood_group,'marital_status':marital_status,'father_or_husband_name':father_or_husband_name,
                'mother_name':mother_name,'address':address,'address':address,'referred_by':referred_by,'city':city,'state':state,
                'country':country,'pin_code':pin_code,'aadhar_number':aadhar_number,'pan_number':pan_number,'emergency_contact_person':emergency_contact_person,'emergency_contact_num':emergency_contact_num,'alternate_contact_number':alternate_contact_number,'nationality':nationality,'email_id':email_id,'staff_member':staff_member,'relationship':relationship,'allow_photo':allow_photo,'notable':notable,'cash':cash,'senior_citizen':senior_citizen,'billing_group':billing_group,
                'corporate_name':corporate_name,'cardholder_name':cardholder_name,'card_number':card_number,'relation':relation,
                'valid_upto':valid_upto,'sum_insured_amount':sum_insured_amount,'InActive':InActive,'first_name':first_name,"middle_name":middle_name,'last_name':last_name,
                """
                valid_upto=request.POST.get('valid_upto')
                sum_insured_amount=request.POST.get('sum_insured_amount')
                if not valid_upto:
                    valid_upto = None
                InActive=request.POST.get('InActive')

                # Start Generating UHID In Some Format
                no_of_patient_registered = PatientRegistrationMains.objects.all().count()
                today = date.today()
                today = today.strftime("%y%m%d")
                if len(str(no_of_patient_registered)) == 1:
                    uhid = 'UHID' + today + '000' + str(no_of_patient_registered)
                elif len(str(no_of_patient_registered)) == 2:
                    uhid = 'UHID' + today + '00' + str(no_of_patient_registered)
                elif len(str(no_of_patient_registered)) == 3:
                    uhid = 'UHID' + today + '0' + str(no_of_patient_registered)
                else:
                    uhid = 'UHID' + today + str(no_of_patient_registered)
                otp= str(random.randint(100000, 999999))
                request.session['otp']=otp
                request.session['email_id']=email_id
                # End Generating UHID In Some Format
                mail1 = EmailMessage('this is for verification',otp, settings.EMAIL_HOST_USER, [email_id])
                mail1.send()
                patient_regist_main=PatientRegistrationMains(
                uhid=uhid,title=title,first_name=first_name,middle_name=middle_name,last_name=last_name,age=age,dob=dob,gender=gender,
                    created_by_id=request.user.id, location_id=request.location,
                )
                patient_regist_sub=PatientRegistrationSub(
                uhid=uhid,registration_date_and_time=registration_date_and_time,blood_group=blood_group,marital_status=marital_status,father_or_husband_name=father_or_husband_name,mother_name=mother_name,address=address,referred_by=referred_by,city=city,state=state,country=country,pin_code=pin_code,aadhar_card=aadhar_number,pan_card=pan_number,emergency_contact_person=emergency_contact_person,emergency_contact_num=emergency_contact_num,alternate_contact_number=alternate_contact_number,nationality=nationality,email=email_id,staff_member=staff_member,mobile_number=mobile_number,relationship=relationship,allow_photo_at_nursing_station=allow_photo,notable=notable,
                    created_by_id=request.user.id, location_id=request.location,
                )
                patient_billing_info=PatientBillingInfos(
                uhid=uhid,in_cash=cash,is_senior_citizen=senior_citizen,billing_group=billing_group,nhif_ins_cor_name=corporate_name,nhif_ins_cor_id=cardholder_name,relation=relation,card_number=card_number,valid_upto=valid_upto,sum_insured_amount=sum_insured_amount,
                is_inactive=InActive,created_by_id=request.user.id,location_id=request.location,
                )
                pr_single_table=PatientsRegistrationsAllInOne(
                uhid=uhid,title=title,first_name=first_name,middle_name=middle_name,last_name=last_name,age=age,dob=dob,gender=gender,patient_profile=patient_profile,registration_date_and_time=registration_date_and_time,blood_group=blood_group,marital_status=marital_status,father_or_husband_name=father_or_husband_name,mother_name=mother_name,address=address,referred_by=referred_by,city=city,state=state,country=country,pin_code=pin_code,aadhar_card=aadhar_number,pan_card=pan_number,next_of_kin=emergency_contact_person,next_of_kin_mob_no=emergency_contact_num,alternate_contact_number=alternate_contact_number,nationality=nationality,email=email_id,staff_member=staff_member,mobile_number=mobile_number,relationship=relationship,allow_photo_at_nursing_station=allow_photo,notable=notable,in_cash=cash,is_senior_citizen=senior_citizen,billing_group=billing_group,nhif_ins_cor_name=corporate_name,nhif_ins_cor_id=cardholder_name,relation=relation,card_number=card_number,valid_upto=valid_upto,sum_insured_amount=sum_insured_amount,ins_doc_upload=ins_doc_upload,
                ins_id_upload=ins_id_upload,created_by_id=request.user.id,location_id=request.location,
                is_inactive=InActive,
                )
                patient_bar_code=PatientBarCode(uhid=uhid)
                patient_profile=PatientProfile(uhid=uhid,p_images=patient_profile)
                patient_regist_main.save()
                patient_regist_sub.save()
                patient_billing_info.save()
                patient_bar_code.save()
                patient_profile.save()
                pr_single_table.save()
                for dt in range(len(choose_ins_doc)):
                    dt_doc=choose_ins_doc[dt]

                    patiet_doct = PatientInsDocType(uhid=uhid,billing_group=billing_group,nhif_ins_corp_name=corporate_name,doc_type=dt_doc)
                    patiet_doct.save()
                # request.session['visit_uhid']=uhid
                capturing_dt=PatientRegistrationSub.objects.get(uhid=uhid)
                registration_date_and_time=capturing_dt.registration_date_and_time
                context={
                    'uhid':uhid,'registration_date_and_time':registration_date_and_time,'patient_name':patient_name,'mobile_number':mobile_number,'title':title,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'dob':dob,'gender':gender,'blood_group':blood_group,'marital_status':marital_status,'father_or_husband_name':father_or_husband_name,
                    'mother_name':mother_name,'address':address,'address':address,'referred_by':referred_by,'city':city,'state':state,
                    'country':country,'pin_code':pin_code,'aa dhar_number':aadhar_number,'pan_number':pan_number,'emergency_contact_person':emergency_contact_person,'emergency_contact_num':emergency_contact_num,'alternate_contact_number':alternate_contact_number,'nationality':nationality,'email_id':email_id,'staff_member':staff_member,'relationship':relationship,'allow_photo':allow_photo,'notable':notable,'cash':cash,'senior_citizen':senior_citizen,'billing_group':billing_group,
                    'corporate_name':corporate_name,'cardholder_name':cardholder_name,'card_number':card_number,'relation':relation,
                    'valid_upto':valid_upto,'sum_insured_amount':sum_insured_amount,'InActive':InActive,'access':access,'first_name':first_name,"middle_name":middle_name,'last_name':last_name,
                }
                return HttpResponseRedirect('/veryf_otp',context)
            visited = PatientVisitMains.objects.all().order_by('-id')
            corporate=CorporateMaster.objects.all()
            billing=BillingGroup.objects.all()
            ins_records=Ins_Document.objects.all()
            relation_master = RelationMaster.objects.all
            relation_nhif = Relation.objects.all()
            context={
            'registration_date_and_time':registration_date_and_time,'form_visit':form_visit,'relation_nhif':relation_nhif,
                'mobile_number':mobile_number,'first_name':patient_name,'uhid':uhid,'visited':visited,'appointment_id':appointment_id,
                'corporate':corporate,'billing':billing,'ins_records':ins_records,'relation_master':relation_master,'access':access,'first_name':first_name,"middle_name":middle_name,'last_name':last_name,"refered_bymaster":refered_bymaster
            }
            return render(request,'clinical/patient_registration.html',context)

    else:
        return redirect('dashboard')

#========================== To Veryfied OTP =================================
def veryf_otp(request):
    otp=request.session['otp']
    resend_otp=request.POST.get('resnd_otp')
    if resend_otp == 'resnd_otp':
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp
        email_id=request.session['email_id']
        mail1 = EmailMessage('this is for resend OTP', otp, settings.EMAIL_HOST_USER, [email_id])
        mail1.send()
        otp=request.session['otp']

    if request.method=="POST":
        enter_otp=request.POST.get('enter_otp')
        if otp == enter_otp:
            return HttpResponseRedirect('/patient_registration')
        else:
            messages.success(request, 'OTP Not Match.......')
            return HttpResponseRedirect('/veryf_otp')

    return render(request,'clinical/otp.html')

# Editing Patient Registration
@login_required(login_url='/user_login')
def patient_registration_edit(request,uhid):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'visitor_add' in access.user_profile.screen_access:
        try:
            refered_bymaster = Refered_by_Master.objects.all()
            request.session['visit_uhid']=uhid
            emergency_contact_person=''
            alternate_contact_number=''
            emergency_contact_num=''
            email=''
            records=''
            nationality=''
            staff_member=''
            relationship=''
            allow_photo_at_nursing_station=''
            notable=''
            in_cash=''
            is_senior_citizen=''
            billing_group=''
            corporate_name=''
            cardholder_name=''
            card_number=''
            relation=''
            valid_upto=''
            sum_insured_amount=''
            is_inactive=''
            city=''
            try:
                corporate = CorporateMaster.objects.all()
                billing = BillingGroup.objects.all()
                records = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
                title=records.title
                first_name = records.first_name
                middle_name = records.middle_name
                last_name = records.last_name
                dob = records.dob
                gender = records.gender
                registration_date_and_time = records.registration_date_and_time
                blood_group = records.blood_group
                marital_status = records.marital_status
                father_or_husband_name = records.father_or_husband_name
                mother_name = records.mother_name
                mobile_number = records.mobile_number
                address = records.address
                referred_by = records.referred_by
                city = records.city
                state = records.state
                country = records.country
                pin_code = records.pin_code
                aadhar_card = records.aadhar_card
                pan_card = records.pan_card
                emergency_contact_person = records.emergency_contact_person
                emergency_contact_num = records.emergency_contact_num
                alternate_contact_number = records.alternate_contact_number
                nationality = records.nationality
                email = records.email
                staff_member = records.staff_member
                relationship = records.relationship
                allow_photo_at_nursing_station = records.allow_photo_at_nursing_station
                notable = records.notable
                in_cash = records.in_cash
                is_senior_citizen = records.is_senior_citizen
                billing_group = records.billing_group
                corporate_name = records.corporate_name
                cardholder_name = records.cardholder_name
                card_number = records.card_number
                relation = records.relation
                valid_upto = records.valid_upto
                sum_insured_amount = records.sum_insured_amount
                is_inactive = records.is_inactive
              
            except:
                pass

            form_visit = PatientVisitMainForm()
            doctor_table=DoctorTable.objects.all()
            visited = PatientVisitMains.objects.filter(uhid__exact=uhid).order_by('-id')
            #========== Changing Billing Group 18/06/2023 ================================
            records = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
            if records.nhif_ins_cor_name == 'Cash':
                pat_ins_name= 'CASH'
            else:
                pat_ins_namess = CorporateMaster.objects.get(id=records.nhif_ins_cor_name)
                pat_ins_name=pat_ins_namess.corporate_Name
            pat_bill_id = BillingGroup.objects.get(id=records.billing_group)
            #====================== END ===============================================
            context={
                'title':title,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,
                'dob':dob,'gender':gender,'registration_date_and_time':registration_date_and_time,'blood_group':blood_group,
                'blood_group':blood_group,'marital_status':marital_status,'father_or_husband_name':father_or_husband_name,
                'mother_name':mother_name,'mobile_number':mobile_number,'address':address,'referred_by':referred_by,
                'state':state,'country':country,'pin_code':pin_code,'aadhar_card':aadhar_card,'pan_card':pan_card,
                'emergency_contact_person':emergency_contact_person,'emergency_contact_num':emergency_contact_num,
                'alternate_contact_number':alternate_contact_number,'nationality':nationality,'email':email,'staff_member':staff_member,
                'relationship':relationship,'allow_photo_at_nursing_station':allow_photo_at_nursing_station,'notable':notable,
                'in_cash':in_cash,'is_senior_citizen':is_senior_citizen,'billing_group':billing_group,'corporate_name':corporate_name,
                'cardholder_name':cardholder_name,'card_number':card_number,'relation':relation,'valid_upto':valid_upto,
                'sum_insured_amount':sum_insured_amount,'is_inactive':is_inactive,'city':city,'uhid':uhid,'doctor_table':doctor_table,
                'form_visit':form_visit,'visited':visited,'corporate':corporate,'billing':billing,'records':records,'doctor_table':doctor_table,
                'refered_bymaster':refered_bymaster,'pat_ins_name':pat_ins_name,'pat_bill_id':pat_bill_id
                }
            return render(request,'clinical/patient_registration_edit.html',context)

        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

#=============Patient Search=============
@login_required(login_url='/user_login')
def patient_search(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'patient_registration' in access.user_profile.screen_access or request.user.is_staff:
        try:
            records1=PatientsRegistrationsAllInOne.objects.filter(location=request.location).order_by('-id')
            if request.method=='POST':
                uhid=request.POST.get('uhid').strip()
                patient_name=request.POST.get('patient_name')
                get_dob=request.POST.get('dob')
                mobile_number=request.POST.get('mobile_number').strip()
                patient_name=request.POST.get('patient_name').strip()
                patient_name_1 = patient_name.split(" ")
                if patient_name == '':
                    patient_name="Not Provided"
                if get_dob == '':
                    get_dob=date.today()
                try:
                    if uhid:
                        records = PatientsRegistrationsAllInOne.objects.filter(uhid__icontains = uhid)
                    elif mobile_number != "+254":
                        records = PatientsRegistrationsAllInOne.objects.filter(mobile_number__icontains = mobile_number)
                    elif len(patient_name_1) == 3:
                        records = PatientsRegistrationsAllInOne.objects.filter(Q(uhid__exact=uhid)|Q(first_name__icontains=patient_name_1[0],middle_name__icontains=patient_name_1[1],last_name__icontains=patient_name_1[2])|Q(mobile_number__exact=mobile_number))
                    elif len(patient_name_1) == 2:
                        records = PatientsRegistrationsAllInOne.objects.filter(Q(uhid__exact=uhid)|Q(first_name__icontains=patient_name_1[0],last_name__icontains=patient_name_1[2])|Q(first_name__icontains=patient_name_1[0],middle_name__icontains=patient_name_1[1]) | Q(mobile_number__exact=mobile_number))
                    elif len(patient_name_1) == 1:
                        records = PatientsRegistrationsAllInOne.objects.filter(Q(first_name__icontains=patient_name_1[0],location=request.location)|Q(middle_name__icontains=patient_name_1[0],location=request.location)|Q(last_name__icontains=patient_name_1[0],location=request.location)|Q(uhid=uhid,location=request.location)|Q(mobile_number=mobile_number))
                    success_search = 'success'
                    context={
                    'records':records,'success_search':success_search,
                    }
                    return render(request,'clinical/patient_search.html',context)
                except Exception as e:
                    pass
            context={
            'records1':records1,
            }
            return render(request,'clinical/patient_search.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
# OPD CARD
@login_required(login_url='/user_login')
def register_card_generation(request,uhid):
    try:
        barcode=PatientBarCode.objects.get(uhid=uhid)
        p_r_m=PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
        barcode=barcode.barcode
        title=p_r_m.title
        first_name=p_r_m.first_name
        middle_name=p_r_m.middle_name
        last_name=p_r_m.last_name
        dob=p_r_m.dob
        gender=p_r_m.gender
        mobile_number=p_r_m.mobile_number
        if middle_name is None:
            middle_name=''
        name=str(title)+''+str(first_name)+''+str(middle_name)+''+str(last_name)
        context={
        'barcode':barcode,'name':name,'dob':dob,'gender':gender,'mobile_number':mobile_number,'uhid':uhid,
        }
        return render(request,'clinical/register_card.html',context)

    except Exception as error:
        return render(request,'error.html',{'error':error})

# Visit Creations
@login_required(login_url='/user_login')
def out_paient_visit(request):
        current_local_time = timezone.localtime(timezone.now())
        print('This is out patinet ')
        # visit_uhid=request.session['visit_uhid']
        form_visit = PatientVisitMainForm()
        if request.method == 'POST':
            print('This is post method')
            form_visit = PatientVisitMainForm(request.POST)
            if form_visit.is_valid():
                print('Form Validating')
                uhid = form_visit.cleaned_data['uhid']
                visit_type = form_visit.cleaned_data['visit_type']
                visit_type_name = request.POST.get('visit_type')
                description = form_visit.cleaned_data['description']
                nurse_doctor = form_visit.cleaned_data['doctor']
                clinical_department = form_visit.cleaned_data['clinical_department']
                billing_groups=request.POST.get('billing_group_id')
                insurances=request.POST.get('insurance_id')
                visit_uhid = request.session['visit_uhid']
                checking = PatientsRegistrationsAllInOne.objects.filter(uhid__exact=visit_uhid)
                if not checking.exists():
                    form_visit = PatientVisitMainForm()
                    error = "Not Find UHID"
                    context = {
                        'form_visit': form_visit, 'error': error,
                    }
                    # return render(request,'clinical/out_patient_visit.html',context)
                    return HttpResponseRedirect('/patient_registration')
                else:
                    #======================== Table count uniqe id generate =============================
                    no_of_visit = PatientVisitMains.objects.all().count()
                    if len(str(no_of_visit)) == 1:
                        pat_visit_no = 'VI' + '00000' + str(no_of_visit)
                    elif len(str(no_of_visit)) == 2:
                        pat_visit_no = 'VI' + '0000' + str(no_of_visit)
                    elif len(str(no_of_visit)) == 3:
                        pat_visit_no = 'VI' + '000' + str(no_of_visit)
                    elif len(str(no_of_visit)) == 4:
                        pat_visit_no = 'VI' + '00' + str(no_of_visit)
                    elif len(str(no_of_visit)) == 5:
                        pat_visit_no = 'VI' + '0' + str(no_of_visit)
                    else:
                        pat_visit_no = 'VI' + str(no_of_visit)
                    #======================== For Serial visit id against uhid ==========================
                    creating_visit_id = PatientVisitMains.objects.filter(uhid__exact=visit_uhid).count()
                    today = date.today()
                    today = today.strftime("%y%m%d")
                    print('today---->,',today)
                    if len(str(creating_visit_id)) == 1:
                        visit_id = 'V.ID' + today + '00' + str(creating_visit_id)
                    elif len(str(creating_visit_id)) == 2:
                        visit_id = 'V.ID' + today + '0' + str(creating_visit_id)
                    else:
                        visit_id = 'V.ID' + today + str(creating_visit_id)

                    #================= For Unique Visit ID 20/06/2023==========================
                    year=today[0:2]
                    last_three_characters_visit_id = visit_id[10:]
                    last_four_characters_uhid = visit_uhid[10:]
                    mix_id='VI'+year+''+last_four_characters_uhid+''+last_three_characters_visit_id
                    #========================== END ==================================
                    
                    visit_ids=PatientVisitMains.objects.filter(uhid=visit_uhid)
                    if not visit_ids.exists():
                        update_patient_status=PatientsRegistrationsAllInOne.objects.filter(uhid=visit_uhid).last()
                        update_patient_status.update_status=timezone.localtime(timezone.now())
                        if billing_groups == None:
                            billing_groups=update_patient_status.billing_group
                        if insurances == None:
                            insurances=update_patient_status.nhif_ins_cor_name
                        patien_visit_creation = PatientVisitMains(
                            uhid=visit_uhid, visit_type=visit_type, description=description, doctor=nurse_doctor,
                            clinical_department=clinical_department, visit_id=pat_visit_no, batch_no=visit_type,
                            created_by_id=request.user.id,location_id=request.location,uv_id=visit_id,
                            billing_group_id=billing_groups,insurance_name=insurances,
                        )
                        patien_visit_creation.save()
                        if billing_groups != None:
                            update_patient_status.billing_group=billing_groups
                        if insurances != None:
                            update_patient_status.nhif_ins_cor_name=insurances
                        update_patient_status.save()
                        return HttpResponseRedirect(f'/patient_registration/{visit_uhid}')
                    elif visit_ids.last().status== 'processing' or visit_ids.last().status== 'close':
                        update_patient_status=PatientsRegistrationsAllInOne.objects.filter(uhid=visit_uhid).last()
                        update_patient_status.update_status=timezone.localtime(timezone.now())
                        if billing_groups == None:
                            billing_groups=update_patient_status.billing_group
                        if insurances == None:
                            insurances=update_patient_status.nhif_ins_cor_name
                        patien_visit_creation = PatientVisitMains(
                            uhid=visit_uhid, visit_type=visit_type, description=description, doctor=nurse_doctor,
                            clinical_department=clinical_department, visit_id=pat_visit_no, batch_no=visit_type,
                            created_by_id=request.user.id,location_id=request.location,uv_id=visit_id,
                            billing_group_id=billing_groups, insurance_name=insurances,
                        )
                        patien_visit_creation.save()
                        if billing_groups != None:
                            update_patient_status.billing_group=billing_groups
                        if insurances != None:
                            update_patient_status.nhif_ins_cor_name=insurances
                        update_patient_status.save()
                        update=PatientVisitMains.objects.filter(uhid=visit_uhid,status__in=['processing','close']).last()
                        update.status='completed'
                        update.save()
                        return HttpResponseRedirect(f'/patient_registration/{visit_uhid}')
            else:
                print('This is invalid form',form_visit.errors)
        visited = PatientVisitMains.objects.all().order_by('-id')
        context = {
            'form_visit': form_visit, 'visited': visited
        }
        return render(request, 'clinical/patient_registration.html', context)
    # except Exception as error:
    #     return render(request, 'error.html', {'error': error})


@login_required(login_url='/user_login')
def patient_search_edit(request,uhid):
    try:
        records=PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
        request.session['visit_uhid']=uhid
        form=PatientsRegistrationsAllInOneForm(instance=records)
        if request.method=='POST':
            form=PatientsRegistrationsAllInOneForm(request.POST,request.FILES,instance=records)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/patient_search')
        context={
        'form':form,
        }
        return render(request,'clinical/patient_search_edit.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def patient_search_delete(request,uhid):
    records=PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
    records.delete()
    return  HttpResponseRedirect('/patient_search')

# register_card
@login_required(login_url='/user_login')
def register_card(request):
    try:
        uhid='UHID2204130000'
        barcode=PatientBarCode.objects.get(uhid=uhid)
        p_r_m=PatientRegistrationMains.objects.get(uhid=uhid)
        p_r_s=PatientRegistrationSub.objects.get(uhid=uhid)
        barcode=barcode.barcode
        title=p_r_m.title
        first_name=p_r_m.first_name
        middle_name=p_r_m.middle_name
        last_name=p_r_m.last_name
        dob=p_r_m.dob
        gender=p_r_m.gender
        mobile_number=p_r_s.mobile_number
        name=title+''+first_name+''+middle_name+''+last_name
        context={
        'barcode':barcode,'name':name,'dob':dob,'gender':gender,'mobile_number':mobile_number,'uhid':uhid,
        }
        return render(request,'clinical/register_card.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

@login_required(login_url='/user_login')
def patient_visit(request):
    return render(request,'clinical/patient_visit.html')
@login_required(login_url='/user_login')
def nursing_assessment(request):
    return render(request,'clinical/nursing_assessment.html')

# Implementing Messages..
#====================== Searching Sevices =============================
def search_address(request):
    service_name=request.GET.get('service_name')
    payload=[]
    tariff_names=request.session['tariff_names']
    if service_name and len(service_name)>0:
        fake_address_objs=ServiceChargeMaster.objects.filter(service_id__service_name__icontains=service_name,tariff_id__in=tariff_names,ipd_opd='OPD')
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.service_id))
        fake_address_objs=ProfileChargeMaster.objects.filter(profile_id__profile_name__icontains=service_name,tariff_id__in=tariff_names,ipd_opd='OPD')
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.profile_id))
        fake_address_objs=PackageChargeMaster.objects.filter(package_id__package_name__icontains=service_name,tariff_id__in=tariff_names)
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.package_id))

    return JsonResponse({'status':200,'data':payload})

from django.db.models import Sum
import random
@login_required(login_url='/user_login')
def opd_billing(request,uhid=None): #By Mantu=====================================
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'opd_billing' in access.user_profile.screen_access:
        # try:
            now = datetime.now()
            date_new = now.strftime("%Y-%m-%d")
            records_today = OpdBillingMain.objects.filter(bill_date_time__date=date_new,location=request.location).order_by('-id')
            # records_today=OpdBillingMain.objects.all()
            search_uhid = uhid
            data = request.GET.get('search')
            data_insert = request.GET.get('insert')
            data_save = request.GET.get('save')
            request.session['pay_m_uhid'] = search_uhid
            request.session['search_datas'] = data
            visit_no_temp_main = ''
            temp_bill_nou = ''
            temp_bill_no = ''
            if request.method == 'POST':
                service_name = request.POST.getlist('service_name')
                uhid = request.POST.get('uhid')
                if request.session['visit_id_temp']:
                    temp_visit = request.session['visit_id_temp']
                    visit_id = temp_visit
                else:
                    visit_id = request.POST.get('visit_id')
                temp_bill_no = request.POST.get('temp_bill_nos')
                package_profile_id = request.POST.get('package_profile_id')
                package_profile_amt = request.POST.get('package_profile_amt')
                amount = request.POST.getlist('amount')
                discount = request.POST.getlist('discount')
                unit = request.POST.getlist('unit')
                net_amount = request.POST.getlist('net_amount')
                outstanding_amount = request.POST.getlist('outstanding_amount')
                total_amount = request.POST.getlist('total_amount')
                service_category = request.POST.getlist('service_category')
                service_sub_category = request.POST.getlist('service_sub_category')
                receive_amount = request.POST.getlist('receive_amount')
                request.session['searched_uhid'] = uhid
                request.session['visit_id'] = visit_id
                # OPD id payment
                request.session['pay_m_receive_amount'] = receive_amount
                request.session['pay_m_uhids'] = uhid
                request.session['pay_m_visit_id'] = visit_id
                request.session['service_name'] = service_name
                temp_bill = OpdBillingTemper.objects.filter(uhid=uhid, visit_no=visit_id)
                temp_bill_id = OpdBillingTemper.objects.filter(uhid=uhid, visit_no=visit_id)
                id_bill_temp = [*set(data.visit_no for data in temp_bill_id)]
                if package_profile_id:
                    yy = date.today().year
                    current_yy = str(yy)[2:]
                    previous_yy = str(yy - 1)[2:]
                    finance_year = previous_yy + current_yy
                    b_no = str(random.randint(1000, 9999))
                    op_bill_no = 'OP' + finance_year + b_no
                    request.session['op_bill_no'] = op_bill_no
                else:
                    yy = date.today().year
                    current_yy = str(yy)[2:]
                    previous_yy = str(yy - 1)[2:]
                    finance_year = previous_yy + current_yy
                    b_no = str(random.randint(1000, 9999))
                    op_bill_no = 'ISR' + finance_year + b_no
                    request.session['op_bill_no'] = op_bill_no
                for i in range(len(service_name)):
                    ind_service_name = service_name[i]
                    ind_uhid = uhid
                    ind_visit_id = visit_id
                    ind_temp_bill_no = temp_bill_no
                    ind_Pr_Opd_sr_bill_no = op_bill_no
                    ind_package_profile_id = package_profile_id
                    ind_package_profile_amt = package_profile_amt
                    ind_amount = amount[i]
                    ind_discount = discount[i]
                    ind_unit = unit[i]
                    ind_net_amount = net_amount[i]
                    ind_outstanding_amount = outstanding_amount[i]
                    ind_total_amount = total_amount[i]
                    ind_service_category = service_category[i]
                    ind_service_sub_category = service_sub_category[i]
                    ind_receive_amount = receive_amount[i]
                    print('=-------=====',service_name[i])
                    temp_opd_billing = OpdBillingTemper(
                        uhid=ind_uhid,
                        visit_no=ind_visit_id,
                        temp_bill_no=ind_temp_bill_no,
                        Pr_Opd_sr_bill_no=ind_Pr_Opd_sr_bill_no,
                        package_profile_id=package_profile_id,
                        package_profile_amt=package_profile_amt,
                        service_name=ind_service_name,
                        rate=ind_amount,
                        discount=ind_discount,
                        unit=ind_unit,
                        net_ammount=ind_net_amount,
                        outstanding_amount=ind_outstanding_amount,
                        total_amount=ind_total_amount,
                        service_category_id=ind_service_category,
                        service_sub_category_id=ind_service_sub_category,
                        receive_amount=ind_receive_amount,created_by_id=request.user.id,location_id=request.location,
                    )
                    temp_opd_billing.save()
                    #  lab module
                    get_uhid_data = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
                    if get_uhid_data.billing_group != '1':
                        profile_record=ProfileService.objects.all()
                        profile_name_list=[data.profile_name for data in profile_record]
                        pen_inv=PendingInvestigation_main.objects.filter(uhid=ind_uhid,visit_no=ind_visit_id).last()
                        if pen_inv:
                            PTID=pen_inv.PTID
                        else:
                            PID = str(random.randint(100000, 999999))
                            PTID = 'PTID' + PID
                        te_id = str(random.randint(100000, 999999))
                        test_id = 'TST' + te_id
                        bill_no=temp_bill_no

                        if ind_service_name in profile_name_list:
                            profile_pac_record = ProfileService.objects.filter(profile_name=ind_service_name).first()
                            pending_inv = PendingInvestigation_main(
                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                profile_id='', profile_name=ind_service_name, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                sub_department=profile_pac_record.service_sub_department
                            )
                            pending_inv.save()

                            profile_rec_filter=ProfileService.objects.filter(profile_name=ind_service_name)
                            for data in profile_rec_filter:
                                print('age',get_uhid_data.age)
                                if data.service_name == 'Age':
                                    rangee=get_uhid_data.age
                                elif get_uhid_data.gender == 'Male':
                                    rangee=data.male_range
                                elif get_uhid_data.gender == 'Female':
                                    rangee=data.female_range
                                else:
                                    rangee=data.male_range
                                pending_inv_sub=LabResultEntry(
                                    test_id=test_id,profile_id='',profile_name=ind_service_name,service_name=data.service_name,
                                    range=rangee,units=' ',created_by_id=request.user.id,location_id=request.location,
                                    outsource=data.outsource,
                                )
                                pending_inv_sub.save()
                        else:
                            lab_record=ServiceMaster.objects.filter(service_name=ind_service_name,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')
                            print('lab_record',lab_record,ind_service_name)
                            serivce_test=Service_Test.objects.filter(test_name__service_name__contains=ind_service_name).first()
                            opd_package=OpdPackageService.objects.filter(package_name__package_name__contains=ind_service_name)
                            if opd_package:

                                for data in opd_package:
                                    te_id = str(random.randint(100000, 999999))
                                    test_id = 'TST' + te_id
                                    print('=======================karannnn',data.service_name,data.profile_name)
                                    if data.service_name:
                                        lab_records=ServiceMaster.objects.filter(service_name=data.service_name,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')

                                        if lab_records:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=lab_records.last().service_name, date_time=datetime.now(),
                                                department=lab_records.last().service_department,outsource=lab_records.last().outsource,
                                                sub_department=lab_records.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                            )
                                            pending_inv.save()
                                            pending_inv_sub = LabResultEntry(
                                                test_id=test_id, profile_id='', profile_name=lab_records.last().service_name, service_name=lab_records.last().service_name,
                                                units=' ',created_by_id=request.user.id,location_id=request.location,outsource=lab_records.last().outsource,
                                            )
                                            pending_inv_sub.save()
                                    elif data.profile_name:
                                        profile_pac_record = ProfileService.objects.filter(profile_name=data.profile_name.profile_name).last()
                                        if profile_pac_record:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=profile_pac_record.profile_name, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                                sub_department=profile_pac_record.service_sub_department
                                            )
                                            pending_inv.save()
                                            profile_rec_filter=ProfileService.objects.filter(profile_name=profile_pac_record.profile_name)
                                            for data in profile_rec_filter:
                                                if data.service_name == 'Age':
                                                    rangee=get_uhid_data.age
                                                elif get_uhid_data.gender == 'Male':
                                                    rangee=data.male_range
                                                elif get_uhid_data.gender == 'Female':
                                                    rangee=data.female_range
                                                else:
                                                    rangee=data.male_range
                                                pending_inv_sub=LabResultEntry(
                                                    test_id=test_id,profile_id='',profile_name=profile_pac_record.profile_name,service_name=data.service_name,
                                                    range=rangee,units=data.units,created_by_id=request.user.id,location_id=request.location,
                                                    outsource=data.outsource,
                                                )
                                                pending_inv_sub.save()
                            elif lab_record:
                                pending_inv = PendingInvestigation_main(
                                    test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                    profile_id='', profile_name=ind_service_name, date_time=datetime.now(),
                                    department=lab_record.last().service_department,outsource=lab_record.last().outsource,
                                    sub_department=lab_record.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                )
                                pending_inv.save()
                                pending_inv_sub = LabResultEntry(
                                    test_id=test_id, profile_id='', profile_name=ind_service_name, service_name=lab_record.last().service_name,
                                    units='',created_by_id=request.user.id,location_id=request.location,outsource=lab_record.last().outsource,
                                )
                                pending_inv_sub.save()
                messages.success(request, 'Successfully Populated Your Services..')
                name = request.session['patient_name']
                dob = request.session['dob']
                mobile_number = request.session['mobile_number']
                billing_group = request.session['billing_group']
                corporate_names = request.session['corporate_name']
                gender = request.session['gender']
                visit_id = request.session['pay_m_visit_id']
                request.session['searched_uhid'] = uhid
                # request.session['visit_id']=visit_id
                if corporate_names == 'Cash':
                    corp_name = 'Cash'
                else:
                    corp_all = CorporateMaster.objects.get(id=corporate_names)
                    corp_name = corp_all.corporate_Name
                tariff = BillingGroupTariffLink.objects.filter(Billing_Group_Name_id=billing_group)
                billing_groups1 = [*set(data.Billing_Group_Name for data in tariff)]
                temp_records = OpdBillingTemper.objects.filter(Q(uhid=uhid) & Q(visit_no=visit_id))
                #========================= For Discount ==============================================
                ttl_rate = OpdBillingTemper.objects.filter(visit_no=visit_id, uhid=uhid).aggregate(Sum('rate'))
                ttl_rate = ttl_rate['rate__sum']
                ttl_qty = OpdBillingTemper.objects.filter(visit_no=visit_id, uhid=uhid).aggregate(Sum('unit'))
                ttl_qty = ttl_qty['unit__sum']
                ttl_dics = OpdBillingTemper.objects.filter(visit_no=visit_id, uhid=uhid).aggregate(Sum('discount'))
                ttl_dics = ttl_dics['discount__sum']
                ttl_net_amt = OpdBillingTemper.objects.filter(visit_no=visit_id, uhid=uhid).aggregate(Sum('net_ammount'))
                ttl_net_amt = ttl_net_amt['net_ammount__sum']
                ttl_amt = OpdBillingTemper.objects.filter(visit_no=visit_id, uhid=uhid).aggregate(Sum('total_amount'))
                ttl_amt = ttl_amt['total_amount__sum']
                #================================= END =============================================================
                # return HttpResponseRedirect('/opd_billing/')
                context = {
                    'temp_records': temp_records,'corp_name': corp_name,'corporate_names': corporate_names,
                    'ttl_rate': ttl_rate, 'ttl_qty': ttl_qty, 'ttl_amt': ttl_amt, 'ttl_dics': ttl_dics,'ttl_net_amt': ttl_net_amt,
                    'mobile_number': mobile_number, 'billing_groups1': billing_groups1, 'name': name,
                    'gender': gender, 'dob': dob, 'searched_uhid': uhid, 'visit_id': visit_id,
                    'visit_no_temp_main': visit_no_temp_main,'records_today':records_today,'access':access
                }
                return render(request, 'clinical/opd_billing.html', context)
            billing_form = BillingCreationForm()

            billing_search = request.GET.get('billing_search')
            print('billing_search', billing_search)
            # billing_search=None
            uhid_searching = request.GET.get('uhid_searching')
            if uhid_searching == 'is_uhid':
                uhid = request.GET.get('uhid')
                request.session['pay_m_uhidss'] = uhid
                print('--==-=-=-uhid,----',uhid)
                # records=PatientVisitMains.objects.filter(uhid=uhid)
                records = PatientVisitMains.objects.filter(uhid__exact=uhid,status='open')
                services = ServiceChargeMaster.objects.all()
                service_master = ServiceChargeMaster.objects.all()
                # visit_id=request.session['pay_m_visit_id']
                request.session['searched_uhid'] = uhid

                context = {
                    'records': records, 'searched_uhid': uhid, 'services': services, 'service_master': service_master,
                    'records_today':records_today,
                    # 'pay_m_visit_id':visit_id,
                }
                return render(request, 'clinical/opd_billing.html', context)
            if billing_search == 'is_opd_billing':
                visit_no = request.GET.get('visit_no')
                selected_service = request.GET.get('selected_service')
                if visit_no is not '':
                    finding_uhid = PatientVisitMains.objects.get(id=visit_no)
                    uhid = finding_uhid.uhid
                    visit_id = finding_uhid.visit_id
                    request.session['visit_id_temp'] = visit_id
                    request.session['pay_m_visit_id']=visit_id
                    clinical_departments = finding_uhid.clinical_department
                    doctor_name = finding_uhid.doctor
                    departments_name = str(clinical_departments)
                    dr_name = str(doctor_name)
                    print('doctor name=======,',dr_name)
                    request.session['clinical_department'] = departments_name
                    request.session['nurse_doctor'] = dr_name
                    temp_records = OpdBillingTemper.objects.filter(Q(uhid=uhid) & Q(visit_no=visit_id))
                    get_uhid_data = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
                    title = get_uhid_data.title
                    title_uhid = get_uhid_data.uhid
                    first_name = get_uhid_data.first_name
                    middle_name = get_uhid_data.middle_name
                    last_name = get_uhid_data.last_name
                    dob = get_uhid_data.dob
                    gender = get_uhid_data.gender
                    mobile_number = get_uhid_data.mobile_number
                    billing_group = get_uhid_data.billing_group
                    corporate_names = get_uhid_data.nhif_ins_cor_name
                    print('corporate_name:----',corporate_names)
                    current_year = date.today().year
                    dob_year = dob.year
                    dob = current_year - dob_year
                    if middle_name == None :
                        name = title + '. ' + first_name + ' ' + last_name
                    else:
                        name = title + '. ' + first_name + ' ' + middle_name + ' ' + last_name
                    request.session['patient_name'] = name
                    request.session['dob'] = dob
                    request.session['mobile_number'] = mobile_number
                    request.session['billing_group'] = billing_group
                    request.session['corporate_name'] = corporate_names
                    print('corporate_names:-----=============',corporate_names)
                    request.session['gender'] = gender
                    request.session['uhid'] = uhid
                    request.session['searched_uhid'] = uhid
                    request.session['visit_id'] = visit_id
                    service_master = ServiceChargeMaster.objects.all()
                    # corporate = BillingGroupCorporateMaster.objects.get(id=corporate_names)
                    if corporate_names == 'Cash':
                        corp_name='Cash'
                    else:
                        corp_all = CorporateMaster.objects.get(id=corporate_names)
                        corp_name = corp_all.corporate_Name
                    # corporate_names = corporate.Corporate_Name
                    # corporate_billing_groups = corporate.Biiling_Group_id
                    tariff = BillingGroupTariffLink.objects.filter(Billing_Group_Name_id=billing_group)
                    billing_groups = [data.Billing_Group_Name_id for data in tariff]
                    billing_gp = [data.Billing_Group_Name for data in tariff]
                    # billing_groups1=[data.Billing_Group_Name for data in tariff]
                    billing_groups1 = [*set(billing_gp)]
                    print('billing_groups1', billing_groups1)
                    tariff_names = [data.Tariff_id for data in tariff]
                    # billing_groups=tariff. Billing_Group_Name_id
                    # billing_groups1=tariff. Billing_Group_Name
                    # tariff_names=tariff.Tariff_id
                    for data in tariff_names:
                        service = ServiceChargeMaster.objects.all().filter(tariff_id__exact=data)
                    request.session['tariff_names'] = tariff_names
                    # print('tariff_names==123123=============',tariff_names)
                    service_id = 0
                    service_charge = 0
                    default_unit = 1
                    default_discount = 0
                    default_out_standing_amount = 0
                    request.session['service_id'] = service_id
                    request.session['service_charge'] = service_charge

                context = {
                    'name': name, 'dob': dob, 'mobile_number': mobile_number, 'billing_group': billing_group,
                    'corporate_names': corporate_names,
                    'gend er': gender, 'searched_uhid': uhid, 'visit_id': visit_id, 'service_master': service_master,
                    'service_id': service_id,
                    'service_charge': service_charge, 'default_unit': default_unit, 'default_discount': default_discount,
                    'temp_bill_no': temp_bill_no,
                    'default_out_standing_amount': default_out_standing_amount, 'corp_name': corp_name,
                    'billing_groups1': billing_groups1, 'service': service, 'visit_no_temp_main': visit_no_temp_main,
                    'records_today': records_today,'access':access,'temp_records':temp_records,
                }
                return render(request, 'clinical/opd_billing.html', context)
            package_id=''
            package_amt=''
            intell_search = request.GET.get('search')
            print('intell_search-----new,',intell_search)
            intell_search_view = request.GET.get('search')
            request.session['intell_search'] = intell_search
            print('intell_search_view', intell_search_view)
            service_charge = ServiceChargeMaster.objects.filter(ipd_opd='OPD')
            service_charge_list = [data.service_id.service_name for data in service_charge]
            print('service_charge_list---new',service_charge_list)

            profile_data = OpdPackageMaster.objects.all()
            profile_list = [data.package_name for data in profile_data]
            if 'tariff_names' in request.session:
                tariff_names=request.session['tariff_names']
            else:
                tariff_names=[]
            service_test_data = ServiceTest.objects.all()
            get_service=''
            test_list = [data.test_name for data in service_test_data]
            if intell_search:
                print('abc--------new', str(intell_search) in service_charge_list)
                if str(intell_search) in service_charge_list:
                    print(f"{intell_search} is present in the service_charge_list.")
                    # intell_search = intell_search.split('-')
                    service_ids = intell_search
                    service_name = intell_search
                    get_service = ServiceChargeMaster.objects.filter(service_id__service_name=service_ids,tariff_id__in=tariff_names,ipd_opd='OPD' )
                    intell_search_ser_name = [data.service_id for data in get_service]
                    intell_search_ser_charges = [data.service_charge for data in get_service]
                    intell_search_ser_cate = [data.service_category for data in get_service]
                    intell_search_ser_sub_cat = [data.service_sub_category for data in get_service]
                    intell_search_ser_qty = ['1']
                    intell_search_ser_disc = ['0']
                    intell_search_ser_total_amt = [data.service_charge for data in get_service]
                elif str(intell_search) in profile_list:
                    # get_services = OpdPackageService.objects.filter(package_name__icontains=intell_search)
                    get_services1 = PackageChargeMaster.objects.filter(package_id__package_name__icontains=intell_search,tariff_id__in=tariff_names)
                    package_id = [data.id for data in get_services1]
                    package_amt = [data.package_charge for data in get_services1]
                    print('package_id================', package_id, package_amt)
                    intell_search_ser_name = [data.package_id for data in get_services1]
                    intell_search_ser_charges = [data.package_charge for data in get_services1]
                    intell_search_ser_qty = '1'  # [data.quantity for data in get_services]
                    intell_search_ser_disc = '0'  # [data.discount for data in get_services]
                    intell_search_ser_total_amt = [data.package_charge for data in get_services1]
                    intell_search_ser_cate = [data.ward_type for data in get_services1]
                    intell_search_ser_sub_cat = [data.ward_category for data in get_services1]
                elif str(intell_search) in test_list:
                    get_services = ServiceTest.objects.filter(test_name__icontains=intell_search)
                    print('get_services', get_services)
                    intell_search_ser_name = [data.test_name for data in get_services]
                    intell_search_ser_charges = [data.test_charges for data in get_services]
                    intell_search_ser_qty = '1'
                    intell_search_ser_disc = '0'
                    intell_search_ser_total_amt = [data.test_charges for data in get_services]
                else:
                    # get_services = ProfileMaster.objects.filter(profile_name__icontains=intell_search)
                    # print('get_services', get_services)
                    get_services1 = ProfileChargeMaster.objects.filter(profile_id__profile_name__icontains=intell_search,tariff_id__in=tariff_names,ipd_opd='OPD')
                    package_id = [data.id for data in get_services1]
                    package_amt = [data.profile_charge for data in get_services1]
                    intell_search_ser_name = [data.profile_id for data in get_services1]
                    intell_search_ser_charges = [data.profile_charge for data in get_services1]
                    intell_search_ser_cate = [data.service_category for data in get_services1]
                    intell_search_ser_sub_cat = [data.service_sub_category for data in get_services1]
                    intell_search_ser_qty = '1'
                    intell_search_ser_disc = '0'
                    print('intell_search_ser_name', intell_search_ser_cate, intell_search_ser_sub_cat)
                    print(f"{intell_search} is not present in the service_charge_list.")
                    # intell_search_ser_qty = [data.quantity for data in get_services]
                    # intell_search_ser_disc = [data.discount for data in get_services]
                    intell_search_ser_total_amt = [data.profile_charge for data in get_services1]
                all_data = zip(intell_search_ser_name, intell_search_ser_charges, intell_search_ser_qty, intell_search_ser_disc,
                            intell_search_ser_total_amt,intell_search_ser_sub_cat,intell_search_ser_cate)
                name = request.session['patient_name']
                dob = request.session['dob']
                mobile_number = request.session['mobile_number']
                billing_group = request.session['billing_group']
                corporate_name = request.session['corporate_name']
                searched_uhid = request.session['uhid']
                gender = request.session['gender']
                visit_id = request.session['visit_id']
                default_unit = 1
                default_discount = 0
                default_out_standing_amount = 0
                search_datas = request.session['search_datas']
                search_url_data = '?search=' + search_datas
                request.session['search_urls'] = search_url_data
                context = {
                    'intell_search_ser_name': intell_search_ser_name, 'intell_search_ser_charges': intell_search_ser_charges,
                    'name': name, 'dob': dob, 'mobile_number': mobile_number, 'billing_group': billing_group,
                    'gender': gender, 'searched_uhid': searched_uhid, 'unit': default_unit, 'discount': default_discount,
                    'OutStandingAmount': default_out_standing_amount, 'visit_id': visit_id,
                    'visit_no_temp_main': visit_no_temp_main,'intell_search_ser_sub_cat':intell_search_ser_sub_cat,
                    'intell_search_ser_cate':intell_search_ser_cate,
                    'search_url_data': search_url_data, 'corporate_name': corporate_name, 'all_data': all_data,
                    'intell_search': intell_search_view,'package_id':package_id,'package_amt':package_amt,
                    'records_today':records_today,'access':access
                }
                return render(request, 'clinical/opd_billing.html', context)
            uhid = ''
            services = ''
            service_master = ServiceChargeMaster.objects.all()
            context = {
                'billing_form': billing_form, 'searched_uhid': uhid, 'services': services, 'searched_uhid': search_uhid,
                'service_master': service_master,'records_today':records_today,'access':access
            }
            return render(request, 'clinical/opd_billing.html', context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

#       NEW OPD BILLING BY MANTU ============
def delete_everything(request):
    temp_record=OpdBillingTemper.objects.all().delete()
    return HttpResponseRedirect('/main_opd')

from datetime import datetime

@login_required(login_url='/user_login')
def main_opd(request):
    # try:
        save_data = request.POST.get('save')
        delete_data = request.POST.get('delete')
        patient_name = request.session['patient_name']
        dob = request.session['dob']
        mobile_number = request.session['mobile_number']
        billing_group = request.session['billing_group']
        corporate_names = request.session['corporate_name']
        gender = request.session['gender']
        pay_m_uhid = request.session['pay_m_uhidss']
        pay_m_visit_id = request.session['pay_m_visit_id']
        print('pay_m_uhid data---------,',pay_m_uhid)
        print('pay_m_visit_id data---------,',pay_m_visit_id)
        billing_groups=request.session['billing_group']
        corporate_names=request.session['corporate_name']
        departments_name=request.session['clinical_department']
        dr_name=request.session['nurse_doctor']
        if corporate_names == 'Cash':
            corp_name = 'Cash'
        else:
            corp_all = CorporateMaster.objects.get(id=corporate_names)
            corp_name = corp_all.corporate_Name
        bill_all = BillingGroup.objects.get(id=billing_groups)
        billing_name = bill_all.billing_group
        # corporate_nam = corp_all.Corporate_Name
        mode_of_payment=OpdPaymentMode.objects.all()
        users=AuthorizedPerson.objects.all()
        records=OpdBillingTemper.objects.filter(visit_no__exact=pay_m_visit_id,uhid=pay_m_uhid)
        print('records==========,',records)
        #========================== For total calculation main table ============================
        ttl_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('total_amount'))
        ttl_amt = ttl_amt['total_amount__sum']
        rate_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('rate'))
        rate_amt = rate_amt['rate__sum']
        rcv_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('receive_amount'))
        rcv_amt = rcv_amt['receive_amount__sum']
        nt_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('net_ammount'))
        nt_amt = nt_amt['net_ammount__sum']
        nt_disc = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('discount'))
        nt_disc = nt_disc['discount__sum']
        ttl_outstanding_amount = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('outstanding_amount'))
        ttl_outstanding_amount = ttl_outstanding_amount['outstanding_amount__sum']
        ttl_unit = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('unit'))
        ttl_unit = ttl_unit['unit__sum']
        #===================================== END ====================================================
        ttl_unit = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('unit'))
        ttl_unit = ttl_unit['unit__sum']
        if request.method == 'POST' and 'save' in request.POST:
            print('for main opd table')
            service = request.POST.getlist('service')
            uhid = request.POST.get('uhid')
            visit_id = request.POST.get('visit_id')
            temp_bill_no = request.POST.get('temp_bill_no')
            package_profile_id = request.POST.getlist('package_profile_id')
            package_profile_amt = request.POST.getlist('package_profile_amt')
            Pr_Opd_sr_bill_no = request.POST.getlist('Pr_Opd_sr_bill_no')
            print('Pr_Opd_sr_bill_no',Pr_Opd_sr_bill_no)
            corporate_id = request.POST.get('corporate_id')
            billing_group_id = request.POST.get('billing_group_id')
            net_amount = request.POST.getlist('net_amount')
            discount = request.POST.getlist('discount')
            pay_amount = request.POST.getlist('pay_amount')
            request.session['pay_m_receive_amount']=pay_amount
            paid_amount = request.POST.getlist('paid_amount')
            outstanding_amount = request.POST.getlist('outstanding_amount')
            unit = request.POST.getlist('unit')
            update_status = request.POST.getlist('update_status')
            total_net_amt = request.POST.get('total_net_amt')
            total_disc = request.POST.get('total_disc')
            total_payable_amt = request.POST.get('total_payable_amt')
            total_paid_amt = request.POST.get('total_paid_amt')
            total_outstanding_amt = request.POST.get('total_outstanding_amt')
            payment_mode = request.POST.get('payment_mode')
            lou_no = request.POST.get('lou_no')
            print('lou_no-----',lou_no)
            claim_no = request.POST.get('claim_no')
            service_category = request.POST.getlist('service_category')
            service_sub_category = request.POST.getlist('service_sub_category')
            order_id = request.POST.getlist('order_id')
            insurance_amt = request.POST.get('insurance_amt')
            auth_pesrson = request.POST.get('auth_pesrson') #== FOR giving discount ==
            remark = request.POST.get('remark')#== FOR giving discount ==
            print('auth_pesrson,',auth_pesrson)
            print('remark,',remark)
            request.session['searched_uhid'] = uhid
            request.session['visit_id'] = visit_id
            # search_urls = request.session['search_urls']
            # Start Generating Bill no & Bill Id In Some Format
            no_of_patient_registered = OpdBillingMain.objects.all().count()
            today = date.today()
            today = today.strftime("%y%m%d")
            if len(str(no_of_patient_registered)) == 1:
                bill_no = 'OP' + '00000' + str(no_of_patient_registered)
            elif len(str(no_of_patient_registered)) == 2:
                bill_no = 'OP' + '0000' + str(no_of_patient_registered)
            elif len(str(no_of_patient_registered)) == 3:
                bill_no = 'OP' + '000' + str(no_of_patient_registered)
            elif len(str(no_of_patient_registered)) == 4:
                bill_no = 'OP' + '00' + str(no_of_patient_registered)
            elif len(str(no_of_patient_registered)) == 5:
                bill_no = 'OP' + '0' + str(no_of_patient_registered)
            else:
                bill_no = 'OP' + str(no_of_patient_registered)

            # # Generating Bill No and Bil Id Generation Start
            # yy = date.today().year
            # current_yy = str(yy)[2:]
            # previous_yy = str(yy - 1)[2:]
            # finance_year = previous_yy + current_yy
            b_no = str(random.randint(100000, 999999))
            # bill_no = 'OP' + finance_year + b_no
            today = date.today()
            today = str(today).replace('-', '')
            prefix = today[2:]
            bill_id = prefix + b_no
            # patient id generating
            PID = str(random.randint(100000, 999999))
            PTID = 'PTID' + PID
            get_uhid_data=PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
            profile_record=ProfileService.objects.all()
            profile_name_list=[data.profile_name for data in profile_record]
            request.session['pay_m_uhid'] = uhid
            request.session['pay_m_visit_id'] = visit_id
            request.session['pay_m_bill_no'] = bill_no
            # print('pay_m_bill_no', bill_no)
            one_service=set(Pr_Opd_sr_bill_no)
            package_id=set(package_profile_id)
            con =zip(one_service,package_id)
            if 'closed_bill' in update_status:
                yy = date.today().year
                current_yy = str(yy)[2:]
                previous_yy = str(yy - 1)[2:]
                finance_year = previous_yy + current_yy
                b_no = str(random.randint(1000, 9999))
                temp_bill_nos = 'OPENID' + finance_year + b_no
                for i in range(len(service)):
                    ind_service = service[i]
                    ind_uhid = uhid
                    ind_visit_id = visit_id
                    ind_temp_bill_no = temp_bill_nos
                    ind_package_profile_id = package_profile_id[i]
                    ind_package_profile_amt = package_profile_amt[i]
                    ind_corporate_id = corporate_id
                    ind_billing_group_id = billing_group_id
                    ind_department = departments_name
                    ind_dr_name = dr_name
                    ind_net_amount = net_amount[i]
                    ind_discount = discount[i]
                    ind_pay_amount = pay_amount[i]
                    ind_paid_amount = paid_amount[i]
                    ind_outstanding_amount = outstanding_amount[i]
                    ind_unit = unit[i]
                    ind_payment_mode = payment_mode
                    ind_service_category=service_category[i]
                    ind_service_sub_category=service_sub_category[i]
                    ind_order_id=order_id[i]
                    # test id generating
                    te_id = str(random.randint(100000, 999999))
                    test_id = 'TST' + te_id
                    opd_billing_sub = OpdBillingSub(
                        bill_id=bill_id,
                        bill_no=bill_no,
                        temp_bill_no=ind_temp_bill_no,
                        package_profile_id=ind_package_profile_id,
                        package_profile_amt=ind_package_profile_amt,
                        uhid=ind_uhid,
                        department=ind_department,
                        doctor_name=ind_dr_name,
                        visit_no=ind_visit_id,
                        corporate_id=ind_corporate_id,
                        billing_group_id=ind_billing_group_id,
                        service_id=ind_service,
                        charges=ind_net_amount,
                        unit=ind_unit,
                        pay_amount=ind_pay_amount,
                        paid_amount=ind_paid_amount,
                        outstanding_amount=ind_outstanding_amount,
                        payment_mode=ind_payment_mode,
                        total_amount=ind_pay_amount,
                        discount=ind_discount,
                        service_category=ind_service_category,
                        service_sub_category=ind_service_sub_category,
                        order_id=ind_order_id,
                        status='closed_bill',created_by_id=request.user.id,location_id=request.location,
                    )
                    opd_billing_sub.save()

                    # ============ 29/12/22 ==========================
                    if ind_service in profile_name_list:
                        print('sucess=====================', ind_service)
                        packages = OPDBillingPackage(
                            uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no,
                            package_id='', package_name=ind_service, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                        )
                        packages.save()
                    # === karan {16-12-2022} =============
                    if get_uhid_data.billing_group == '1':
                        if ind_service in profile_name_list:
                            profile_pac_record = ProfileService.objects.filter(profile_name=ind_service).first()
                            pending_inv = PendingInvestigation_main(
                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                profile_id='', profile_name=ind_service, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                sub_department=profile_pac_record.service_sub_department
                            )
                            pending_inv.save()

                            profile_rec_filter=ProfileService.objects.filter(profile_name=ind_service)
                            for data in profile_rec_filter:
                                print('age',get_uhid_data.age)
                                if data.service_name == 'Age':
                                    rangee=get_uhid_data.age
                                elif get_uhid_data.gender == 'Male':
                                    rangee=data.male_range
                                elif get_uhid_data.gender == 'Female':
                                    rangee=data.female_range
                                else:
                                    rangee=data.male_range
                                pending_inv_sub=LabResultEntry(
                                    test_id=test_id,profile_id='',profile_name=ind_service,service_name=data.service_name,
                                    range=rangee,units=' ',created_by_id=request.user.id,location_id=request.location,
                                    outsource=data.outsource,
                                )
                                pending_inv_sub.save()
                        else:
                            lab_record=ServiceMaster.objects.filter(service_name=ind_service,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')
                            print('lab_record',lab_record,ind_service)
                            serivce_test=Service_Test.objects.filter(test_name__service_name__contains=ind_service).first()
                            opd_package=OpdPackageService.objects.filter(package_name__package_name__contains=ind_service)
                            if opd_package:

                                for data in opd_package:
                                    te_id = str(random.randint(100000, 999999))
                                    test_id = 'TST' + te_id
                                    print('=======================karannnn',data.service_name,data.profile_name)
                                    if data.service_name:
                                        lab_records=ServiceMaster.objects.filter(service_name=data.service_name,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')

                                        if lab_records:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=lab_records.last().service_name, date_time=datetime.now(),
                                                department=lab_records.last().service_department,outsource=lab_records.last().outsource,
                                                sub_department=lab_records.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                            )
                                            pending_inv.save()
                                            pending_inv_sub = LabResultEntry(
                                                test_id=test_id, profile_id='', profile_name=lab_records.last().service_name, service_name=lab_records.last().service_name,
                                                units=' ',created_by_id=request.user.id,location_id=request.location,outsource=lab_records.last().outsource,
                                            )
                                            pending_inv_sub.save()
                                    elif data.profile_name:
                                        profile_pac_record = ProfileService.objects.filter(profile_name=data.profile_name.profile_name).last()
                                        if profile_pac_record:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=profile_pac_record.profile_name, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                                sub_department=profile_pac_record.service_sub_department
                                            )
                                            pending_inv.save()

                                            profile_rec_filter=ProfileService.objects.filter(profile_name=profile_pac_record.profile_name)
                                            for data in profile_rec_filter:
                                                if data.service_name == 'Age':
                                                    rangee=get_uhid_data.age
                                                elif get_uhid_data.gender == 'Male':
                                                    rangee=data.male_range
                                                elif get_uhid_data.gender == 'Female':
                                                    rangee=data.female_range
                                                else:
                                                    rangee=data.male_range
                                                pending_inv_sub=LabResultEntry(
                                                    test_id=test_id,profile_id='',profile_name=profile_pac_record.profile_name,service_name=data.service_name,
                                                    range=rangee,units=' ',created_by_id=request.user.id,location_id=request.location,
                                                    outsource=data.outsource,
                                                )
                                                pending_inv_sub.save()
                            elif lab_record:
                                pending_inv = PendingInvestigation_main(
                                    test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                    profile_id='', profile_name=ind_service, date_time=datetime.now(),
                                    department=lab_record.last().service_department,outsource=lab_record.last().outsource,
                                    sub_department=lab_record.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                )
                                pending_inv.save()

                                # if get_uhid_data.gender == 'Male':
                                #     rangee = serivce_test.male_range
                                # elif get_uhid_data.gender == 'Female':
                                #     rangee = serivce_test.female_range
                                # else:
                                #     rangee = serivce_test.male_range
                                pending_inv_sub = LabResultEntry(
                                    test_id=test_id, profile_id='', profile_name=ind_service, service_name=lab_record.last().service_name,
                                    units='',created_by_id=request.user.id,location_id=request.location,outsource=lab_record.last().outsource,
                                )
                                pending_inv_sub.save()

                    service_master=ServiceMaster.objects.select_related('service_sub_category').filter(service_name=ind_service).first()
                    if service_master:
                        dis_id = str(random.randint(100000, 999999))
                        test_id = 'DID' + dis_id
                        if service_master.service_sub_category.service_sub_category == 'Radiology investigation':
                            uhid_id=PatientsRegistrationsAllInOne.objects.filter(uhid=ind_uhid).first()
                            RIS_PendingInvestigation_main.objects.create(
                                bill_no=bill_no,test_id=test_id,uhid_id=uhid_id.id,visit_no=ind_visit_id,service_id=service_master.id,
                                created_by_id=request.user.id,location_id=request.location,
                            )

                if payment_mode == '':
                    main_opd_billing = OpdBillingMain(
                        bill_no=bill_no,
                        bill_id=bill_id,
                        uhid=uhid,
                        temp_bill_no=temp_bill_nos,
                        package_profile_id=package_profile_id,
                        visit_no=visit_id,
                        department=departments_name,
                        doctor_name=dr_name,
                        corporate_id=corporate_id,
                        billing_group_id=billing_group_id,
                        net_amount=total_paid_amt,
                        discount=total_disc,
                        pay_amount=total_payable_amt,
                        paid_amount=total_paid_amt,
                        outstanding_amount=total_paid_amt,
                        payment_mode=payment_mode,
                        lou_no=lou_no,
                        claim_no=claim_no,
                        insurance_amt=insurance_amt,
                        status='closed_bill',created_by_id=request.user.id,location_id=request.location,
                    )
                    main_opd_billing.save()
                else:
                    main_opd_billing = OpdBillingMain(
                        bill_no=bill_no,
                        bill_id=bill_id,
                        uhid=uhid,
                        temp_bill_no=temp_bill_nos,
                        package_profile_id=package_profile_id,
                        visit_no=visit_id,
                        department=departments_name,
                        doctor_name=dr_name,
                        corporate_id=corporate_id,
                        billing_group_id=billing_group_id,
                        net_amount=total_paid_amt,
                        discount=total_disc,
                        pay_amount=total_payable_amt,
                        paid_amount=total_paid_amt,
                        outstanding_amount=total_outstanding_amt,
                        payment_mode=payment_mode,
                        lou_no=lou_no,
                        claim_no=claim_no,
                        insurance_amt=insurance_amt,
                        checklist_status='',
                        claim_status='',
                        claim_amt='',
                        status='closed_bill',created_by_id=request.user.id,location_id=request.location,
                    )
                    main_opd_billing.save()
            else:
                for i in range(len(service)):
                    ind_service = service[i]
                    ind_uhid = uhid
                    ind_visit_id = visit_id
                    ind_temp_bill_no = temp_bill_no
                    ind_package_profile_id = package_profile_id[i]
                    ind_package_profile_amt = package_profile_amt[i]
                    ind_corporate_id = corporate_id
                    ind_billing_group_id = billing_group_id
                    ind_department = departments_name
                    ind_dr_name = dr_name
                    ind_net_amount = net_amount[i]
                    ind_discount = discount[i]
                    ind_pay_amount = pay_amount[i]
                    ind_paid_amount = paid_amount[i]
                    ind_outstanding_amount = outstanding_amount[i]
                    ind_unit = unit[i]
                    ind_payment_mode = payment_mode
                    ind_service_category=service_category[i]
                    ind_order_id=order_id[i]
                    print('ind_service_category ',ind_service_category)
                    # get_ids=OpdBillingTemper.object.get(service_category=ind_service_category)
                    # get_ids_id=
                    ind_service_sub_category=service_sub_category[i]
                    # test id generating
                    te_id = str(random.randint(100000, 999999))
                    test_id = 'TST' + te_id
                    opd_billing_sub = OpdBillingSub(
                        bill_id=bill_id,
                        bill_no=bill_no,
                        temp_bill_no=ind_temp_bill_no,
                        package_profile_id=ind_package_profile_id,
                        package_profile_amt=ind_package_profile_amt,
                        uhid=ind_uhid,
                        department=ind_department,
                        doctor_name=ind_dr_name,
                        visit_no=ind_visit_id,
                        corporate_id=ind_corporate_id,
                        billing_group_id=ind_billing_group_id,
                        service_id=ind_service,
                        charges=ind_net_amount,
                        unit=ind_unit,
                        pay_amount=ind_pay_amount,
                        paid_amount=ind_paid_amount,
                        outstanding_amount=ind_outstanding_amount,
                        payment_mode=ind_payment_mode,
                        total_amount=ind_pay_amount,
                        service_category=ind_service_category,
                        service_sub_category=ind_service_sub_category,
                        order_id=ind_order_id,
                        discount=ind_discount,created_by_id=request.user.id,location_id=request.location,
                    )
                    print('test_id ',test_id)
                    opd_billing_sub.save()
                    print('SAved...')

                    #============ 29/12/22 ==========================
                    if ind_service in profile_name_list:
                        print('sucess=====================',ind_service)
                        packages=OPDBillingPackage(
                            uhid=ind_uhid,visit_no=ind_visit_id,bill_no=bill_no,
                            package_id='',package_name=ind_service,date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                        )
                        packages.save()
                    # === karan {16-12-2022} =============
                    if get_uhid_data.billing_group == '1':
                        if ind_service in profile_name_list:
                            profile_pac_record = ProfileService.objects.filter(profile_name=ind_service).first()
                            pending_inv = PendingInvestigation_main(
                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                profile_id='', profile_name=ind_service, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                sub_department=profile_pac_record.service_sub_department
                            )
                            pending_inv.save()

                            profile_rec_filter=ProfileService.objects.filter(profile_name=ind_service)
                            for data in profile_rec_filter:
                                print('age',get_uhid_data.age)
                                if data.service_name == 'Age':
                                    rangee=get_uhid_data.age
                                elif get_uhid_data.gender == 'Male':
                                    rangee=data.male_range
                                elif get_uhid_data.gender == 'Female':
                                    rangee=data.female_range
                                else:
                                    rangee=data.male_range
                                pending_inv_sub=LabResultEntry(
                                    test_id=test_id,profile_id='',profile_name=ind_service,service_name=data.service_name,
                                    range=rangee,units=' ',created_by_id=request.user.id,location_id=request.location,
                                    outsource=data.outsource,
                                )
                                pending_inv_sub.save()
                        else:
                            lab_record=ServiceMaster.objects.filter(service_name=ind_service,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')
                            print('lab_record',lab_record,ind_service)
                            serivce_test=Service_Test.objects.filter(test_name__service_name__contains=ind_service).first()
                            opd_package=OpdPackageService.objects.filter(package_name__package_name__contains=ind_service)
                            if opd_package:

                                for data in opd_package:
                                    te_id = str(random.randint(100000, 999999))
                                    test_id = 'TST' + te_id
                                    print('=======================karannnn',data.service_name,data.profile_name)
                                    if data.service_name:
                                        lab_records=ServiceMaster.objects.filter(service_name=data.service_name,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')

                                        if lab_records:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=lab_records.last().service_name, date_time=datetime.now(),
                                                department=lab_records.last().service_department,outsource=lab_records.last().outsource,
                                                sub_department=lab_records.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                            )
                                            pending_inv.save()
                                            pending_inv_sub = LabResultEntry(
                                                test_id=test_id, profile_id='', profile_name=lab_records.last().service_name, service_name=lab_records.last().service_name,
                                                units=' ',created_by_id=request.user.id,location_id=request.location,outsource=lab_records.last().outsource,
                                            )
                                            pending_inv_sub.save()
                                    elif data.profile_name:
                                        profile_pac_record = ProfileService.objects.filter(profile_name=data.profile_name.profile_name).last()
                                        if profile_pac_record:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=profile_pac_record.profile_name, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                                sub_department=profile_pac_record.service_sub_department
                                            )
                                            pending_inv.save()

                                            profile_rec_filter=ProfileService.objects.filter(profile_name=profile_pac_record.profile_name)
                                            for data in profile_rec_filter:
                                                if data.service_name == 'Age':
                                                    rangee=get_uhid_data.age
                                                elif get_uhid_data.gender == 'Male':
                                                    rangee=data.male_range
                                                elif get_uhid_data.gender == 'Female':
                                                    rangee=data.female_range
                                                else:
                                                    rangee=data.male_range
                                                pending_inv_sub=LabResultEntry(
                                                    test_id=test_id,profile_id='',profile_name=profile_pac_record.profile_name,service_name=data.service_name,
                                                    range=rangee,units=' ',created_by_id=request.user.id,location_id=request.location,
                                                    outsource=data.outsource,
                                                )
                                                pending_inv_sub.save()
                            elif lab_record:
                                pending_inv = PendingInvestigation_main(
                                    test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                    profile_id='', profile_name=ind_service, date_time=datetime.now(),
                                    department=lab_record.last().service_department,outsource=lab_record.last().outsource,
                                    sub_department=lab_record.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                )
                                pending_inv.save()
                                pending_inv_sub = LabResultEntry(
                                    test_id=test_id, profile_id='', profile_name=ind_service, service_name=lab_record.last().service_name,
                                    units='',created_by_id=request.user.id,location_id=request.location,outsource=lab_record.last().outsource,
                                )
                                pending_inv_sub.save()

                    service_master=ServiceMaster.objects.select_related('service_sub_category').filter(service_name=ind_service).first()
                    if service_master:
                        dis_id = str(random.randint(100000, 999999))
                        test_id = 'DID' + dis_id
                        if service_master.service_sub_category.service_sub_category == 'Radiology investigation':
                            uhid_id=PatientsRegistrationsAllInOne.objects.filter(uhid=ind_uhid).first()
                            RIS_PendingInvestigation_main.objects.create(
                                bill_no=bill_no,test_id=test_id,uhid_id=uhid_id.id,visit_no=ind_visit_id,service_id=service_master.id,
                                created_by_id=request.user.id,location_id=request.location,
                            )
                if payment_mode == '':
                    main_opd_billing = OpdBillingMain(
                        bill_no=bill_no,
                        bill_id=bill_id,
                        uhid=uhid,
                        temp_bill_no=temp_bill_no,
                        package_profile_id=package_profile_id,
                        visit_no=visit_id,
                        department=departments_name,
                        doctor_name=dr_name,
                        corporate_id=corporate_id,
                        billing_group_id=billing_group_id,
                        net_amount=total_paid_amt,
                        discount=total_disc,
                        pay_amount=total_payable_amt,
                        paid_amount=total_paid_amt,
                        outstanding_amount=total_paid_amt,
                        payment_mode=payment_mode,
                        lou_no=lou_no,
                        claim_no=claim_no,
                        insurance_amt=insurance_amt,
                        created_by_id=request.user.id,location_id=request.location,
                    )
                    main_opd_billing.save()
                else:
                    main_opd_billing = OpdBillingMain(
                        bill_no=bill_no,
                        bill_id=bill_id,
                        uhid=uhid,
                        temp_bill_no=temp_bill_no,
                        package_profile_id=package_profile_id,
                        visit_no=visit_id,
                        department=departments_name,
                        doctor_name=dr_name,
                        corporate_id=corporate_id,
                        billing_group_id=billing_group_id,
                        net_amount=total_paid_amt,
                        discount=total_disc,
                        pay_amount=total_payable_amt,
                        paid_amount=total_paid_amt,
                        outstanding_amount=total_outstanding_amt,
                        payment_mode=payment_mode,
                        lou_no=lou_no,
                        claim_no=claim_no,
                        insurance_amt=insurance_amt,
                        checklist_status='',
                        claim_status = '',
                        claim_amt = '',created_by_id=request.user.id,location_id=request.location,
                    )
                    main_opd_billing.save()
            data = OpdBillingTemper.objects.filter(uhid__exact=uhid,visit_no__exact=pay_m_visit_id).delete()
            update_status=PatientVisitMains.objects.filter(uhid__exact=uhid,visit_id__exact=pay_m_visit_id).last()
            update_status.status='processing'
            update_status.save()
            if total_disc != '0':
                data=OPDBillDiscountRemark(
                    authorised_by_id=auth_pesrson,
                    bill_no=bill_no,
                    remark=remark,
                    created_by_id = request.user.id,
                    location_id = request.location,
                )
                data.save()
            if corp_name == 'Cash':
                return  HttpResponseRedirect('/opd_payment_mode')
            else:
                return  HttpResponseRedirect('/opd_payment_credit')
            # return  HttpResponseRedirect('/main_opd')
        patient_name = request.session['patient_name']
        dob = request.session['dob']
        mobile_number = request.session['mobile_number']
        billing_group = request.session['billing_group']
        corporate_names = request.session['corporate_name']
        gender = request.session['gender']
        pay_m_uhid = request.session['pay_m_uhidss']
        pay_m_visit_id = request.session['pay_m_visit_id']
        billing_group=request.session['billing_group']
        corporate_names=request.session['corporate_name']
        main_table = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)|Q(visit_no=pay_m_visit_id)).last()
        print(f'main_table',main_table)

        return render(request,'clinical/main_opd.html',{'records':records,'mode_of_payment':mode_of_payment,'pay_m_visit_id':pay_m_visit_id,'pay_m_uhid':pay_m_uhid,
                                                        'billing_group':billing_group,'corporate_names':corporate_names,'users':users,
                                                    'patient_name':patient_name,'dob':dob,'mobile_number':mobile_number,'gender':gender,'corp_name':corp_name,
                                                        'billing_name':billing_name,'ttl_amt':ttl_amt,'rcv_amt':rcv_amt,'nt_amt':nt_amt,'nt_disc':nt_disc,
                                                        'ttl_outstanding_amount':ttl_outstanding_amount,'ttl_unit':ttl_unit,'rate_amt':rate_amt})

    # except Exception as error:
    #     return render(request,'error.html',{'error':error})


#========================= for open bill ============================

@login_required(login_url='/user_login')
def for_open_bill_main_opd(request):
    try:
        pay_m_uhid = request.session['pay_m_uhid']
        pay_m_visit_id = request.session['pay_m_visit_id']
        billing_groups=request.session['billing_group']
        corporate_names=request.session['corporate_name']
        departments_name=request.session['clinical_department']
        dr_name=request.session['nurse_doctor']
        if corporate_names == 'Cash':
            corp_name = 'Cash'
        else:
            corp_all = CorporateMaster.objects.get(id=corporate_names)
            corp_name = corp_all.corporate_Name
        bill_all = BillingGroup.objects.get(id=billing_groups)
        billing_name = bill_all.billing_group
        # corporate_nam = corp_all.Corporate_Name
        mode_of_payment=OpdPaymentMode.objects.all()
        records=OpdBillingTemper.objects.filter(visit_no__exact=pay_m_visit_id,uhid=pay_m_uhid)
        ttl_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('total_amount'))
        ttl_amt = ttl_amt['total_amount__sum']
        rcv_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('receive_amount'))
        rcv_amt = rcv_amt['receive_amount__sum']
        nt_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('net_ammount'))
        nt_amt = nt_amt['net_ammount__sum']
        nt_disc = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('discount'))
        nt_disc = nt_disc['discount__sum']
        ttl_outstanding_amount = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('outstanding_amount'))
        ttl_outstanding_amount = ttl_outstanding_amount['outstanding_amount__sum']
        ttl_unit = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('unit'))
        ttl_unit = ttl_unit['unit__sum']
        if request.method == 'POST' and 'save' in request.POST:
            print('for main opd table')
            service = request.POST.getlist('service')
            uhid = request.POST.get('uhid')
            visit_id = request.POST.get('visit_id')
            temp_bill_no = request.POST.get('temp_bill_no')
            package_profile_id = request.POST.getlist('package_profile_id')
            package_profile_amt = request.POST.getlist('package_profile_amt')
            Pr_Opd_sr_bill_no = request.POST.getlist('Pr_Opd_sr_bill_no')
            print('Pr_Opd_sr_bill_no',Pr_Opd_sr_bill_no)
            corporate_id = request.POST.get('corporate_id')
            billing_group_id = request.POST.get('billing_group_id')
            net_amount = request.POST.getlist('net_amount')
            discount = request.POST.getlist('discount')
            pay_amount = request.POST.getlist('pay_amount')
            paid_amount = request.POST.getlist('paid_amount')
            outstanding_amount = request.POST.getlist('outstanding_amount')
            unit = request.POST.get('unit')
            total_net_amt = request.POST.get('total_net_amt')
            total_disc = request.POST.get('total_disc')
            total_payable_amt = request.POST.get('total_payable_amt')
            total_paid_amt = request.POST.get('total_paid_amt')
            total_outstanding_amt = request.POST.get('total_outstanding_amt')
            payment_mode = request.POST.get('payment_mode')
            request.session['searched_uhid'] = uhid
            request.session['visit_id'] = visit_id
            search_urls = request.session['search_urls']
            # Generating Bill No and Bil Id Generation Start
            yy = date.today().year
            current_yy = str(yy)[2:]
            previous_yy = str(yy - 1)[2:]
            finance_year = previous_yy + current_yy
            b_no = str(random.randint(100000, 999999))
            bill_no = 'OP' + finance_year + b_no
            today = date.today()
            today = str(today).replace('-', '')
            prefix = today[2:]
            bill_id = prefix + b_no
            # patient id generating
            PID = str(random.randint(100000, 999999))
            PTID = 'PTID' + PID
            get_uhid_data=PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
            profile_record=ProfileService.objects.all()
            profile_name_list=[data.profile_name for data in profile_record]
            request.session['pay_m_uhid'] = uhid
            request.session['pay_m_visit_id'] = visit_id
            request.session['pay_m_bill_no'] = bill_no
            # print('pay_m_bill_no', bill_no)
            one_service=set(Pr_Opd_sr_bill_no)
            package_id=set(package_profile_id)
            con =zip(one_service,package_id)
            # print('con=---------', con)
            # for d,d1 in con:
            #     if d.startwith('OP'):
            #         package=OpdPackageMaster.objects.get(id=d1)
            #         p_na=package.package_name
            #         p_amt=package.package_amount
            #         data = OpdBillingSub(
            #             bill_no=bill_no,
            #             uhid=uhid,
            #             temp_bill_no=temp_bill_no,
            #             bill_id=bill_id,
            #             service_id=p_na,
            #             charges=p_amt,
            #             visit_no=visit_id,
            #             department=departments_name,
            #             doctor_name=dr_name,
            #             corporate_id=corporate_id,
            #             billing_group_id=billing_group_id,
            #             discount=total_disc,
            #             pay_amount=total_payable_amt,
            #             paid_amount=total_paid_amt,
            #             outstanding_amount=total_outstanding_amt,
            #             unit='0',
            #             payment_mode=payment_mode,
            #             total_amount=total_paid_amt,
            #         )
            #         data.save()
            #         for i in range(len(package_profile_id)):
            #             print('i',i)
            #             ind_service = service[i]
            #             ind_uhid = uhid
            #             ind_visit_id = visit_id
            #             ind_net_amount = net_amount[i]
            #             ind_pay_amount = pay_amount[i]
            #             ind_paid_amount = paid_amount[i]
            #             ind_outstanding_amount = outstanding_amount[i]
            #             ind_unit = unit
            #             opd_billing_sub=OpdBillingSub(
            #                 bill_id='0',
            #                 bill_no='0',
            #                 temp_bill_no='0',
            #                 package_profile_id=ind_service,
            #                 package_profile_amt=ind_net_amount,
            #                 uhid='0',
            #                 department='0',
            #                 doctor_name='0',
            #                 visit_no='0',
            #                 corporate_id='0',
            #                 billing_group_id='0',
            #                 charges='0',
            #                 unit=ind_unit,
            #                 pay_amount=ind_pay_amount,
            #                 paid_amount=ind_paid_amount,
            #                 outstanding_amount=ind_outstanding_amount,
            #                 payment_mode='0',
            #                 total_amount='0',
            #                 discount='0'
            #             )
            #             opd_billing_sub.save()
            #     else:
            yy = date.today().year
            current_yy = str(yy)[2:]
            previous_yy = str(yy - 1)[2:]
            finance_year = previous_yy + current_yy
            b_no = str(random.randint(1000, 9999))
            temp_bill_nos = 'OPENID' + finance_year + b_no
            request.session['temp_bill_no'] = temp_bill_nos
            print('temp_bill_no', temp_bill_nos)
            for i in range(len(service)):
                ind_service = service[i]
                ind_uhid = uhid
                ind_visit_id = visit_id
                ind_temp_bill_no = temp_bill_nos
                ind_package_profile_id = package_profile_id[i]
                ind_package_profile_amt = package_profile_amt[i]
                ind_corporate_id = corporate_id
                ind_billing_group_id = billing_group_id
                ind_department = departments_name
                ind_dr_name = dr_name
                ind_net_amount = net_amount[i]
                ind_discount = discount[i]
                ind_pay_amount = pay_amount[i]
                ind_paid_amount = paid_amount[i]
                ind_outstanding_amount = outstanding_amount[i]
                ind_unit = unit
                ind_payment_mode = payment_mode
                # test id generating
                te_id = str(random.randint(100000, 999999))
                test_id = 'TST' + te_id
                opd_billing_sub = OpdBillingSub(
                    bill_id=bill_id,
                    bill_no=bill_no,
                    temp_bill_no=ind_temp_bill_no,
                    package_profile_id=ind_package_profile_id,
                    package_profile_amt=ind_package_profile_amt,
                    uhid=ind_uhid,
                    department=ind_department,
                    doctor_name=ind_dr_name,
                    visit_no=ind_visit_id,
                    corporate_id=ind_corporate_id,
                    billing_group_id=ind_billing_group_id,
                    service_id=ind_service,
                    charges=ind_net_amount,
                    unit=ind_unit,
                    pay_amount=ind_pay_amount,
                    paid_amount=ind_paid_amount,
                    outstanding_amount=ind_outstanding_amount,
                    payment_mode=ind_payment_mode,
                    total_amount=ind_pay_amount,
                    discount=ind_discount
                )
                opd_billing_sub.save()

                #============ 29/12/22 ==========================
                if ind_service in profile_name_list:
                    print('sucess=====================',ind_service)
                    packages=OPDBillingPackage(
                        uhid=ind_uhid,visit_no=ind_visit_id,bill_no=bill_no,
                        package_id='',package_name=ind_service,date_time=datetime.now()
                    )
                    packages.save()
                # === karan {16-12-2022} =============
                if ind_service in profile_name_list:
                    print('sucess=====================',ind_service)
                    profile_pac_record = ProfileService.objects.filter(profile_name=ind_service)[0]
                    pending_inv = PendingInvestigation_main(
                        test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                        profile_id='', profile_name=ind_service, date_time=datetime.now(),
                        department=profile_pac_record.service_department,
                        sub_department=profile_pac_record.service_sub_department
                    )
                    pending_inv.save()

                    profile_rec_filter=ProfileService.objects.filter(profile_name=ind_service)
                    for data in profile_rec_filter:
                        print('age',get_uhid_data.age)
                        if get_uhid_data.age is range(0, 5):
                            rangee=data.infant_range
                        elif get_uhid_data.age is range(6, 15):
                            rangee=data.chield_range
                        elif get_uhid_data.age is range(16, 99) and get_uhid_data.gender == 'Male':
                            rangee=data.male_range
                        elif get_uhid_data.age is range(6, 99) and get_uhid_data.gender == 'Female':
                            rangee=data.female_range
                        else:
                            rangee=data.male_range
                        pending_inv_sub=LabResultEntry(
                            test_id=test_id,profile_id='',profile_name=ind_service,service_name=data.service_name,
                            range=rangee,units=data.units
                        )
                        pending_inv_sub.save()
                    # ===================================
            if payment_mode == '':
                main_opd_billing = OpdBillingMain(
                    bill_no=bill_no,
                    bill_id=bill_id,
                    uhid=uhid,
                    temp_bill_no=temp_bill_no,
                    package_profile_id=package_profile_id,
                    visit_no=visit_id,
                    department=departments_name,
                    doctor_name=dr_name,
                    corporate_id=corporate_id,
                    billing_group_id=billing_group_id,
                    net_amount=total_net_amt,
                    discount=total_disc,
                    pay_amount=total_payable_amt,
                    paid_amount=total_paid_amt,
                    outstanding_amount=total_paid_amt,
                    payment_mode=payment_mode,
                )
                main_opd_billing.save()
            else:
                main_opd_billing = OpdBillingMain(
                    bill_no=bill_no,
                    bill_id=bill_id,
                    uhid=uhid,
                    temp_bill_no=temp_bill_no,
                    package_profile_id=package_profile_id,
                    visit_no=visit_id,
                    department=departments_name,
                    doctor_name=dr_name,
                    corporate_id=corporate_id,
                    billing_group_id=billing_group_id,
                    net_amount=total_net_amt,
                    discount=total_disc,
                    pay_amount=total_payable_amt,
                    paid_amount=total_paid_amt,
                    outstanding_amount=total_outstanding_amt,
                    payment_mode=payment_mode,
                    checklist_status='',
                    claim_status = '',
                    claim_amt = '',
                )
                main_opd_billing.save()
            data = OpdBillingTemper.objects.filter(uhid__exact=uhid,visit_no__exact=pay_m_visit_id).delete()
            return  HttpResponseRedirect('/main_opd')
        patient_name = request.session['patient_name']
        print('patient_name',patient_name)
        dob = request.session['dob']
        mobile_number = request.session['mobile_number']
        gender = request.session['gender']
        pay_m_uhid = request.session['pay_m_uhid']
        pay_m_visit_id = request.session['pay_m_visit_id']
        billing_group=request.session['billing_group']
        corporate_names=request.session['corporate_name']
        main_table = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)|Q(visit_no=pay_m_visit_id)).last()
        print(f'main_table',main_table)
        return render(request,'clinical/opd_bill/for_open_opd_main.html',{'records':records,'mode_of_payment':mode_of_payment,'pay_m_visit_id':pay_m_visit_id,'pay_m_uhid':pay_m_uhid,
                                                        'billing_group':billing_group,'corporate_names':corporate_names,
                                                    'patient_name':patient_name,'dob':dob,'mobile_number':mobile_number,'gender':gender,'corp_name':corp_name,
                                                        'billing_name':billing_name,'ttl_amt':ttl_amt,'rcv_amt':rcv_amt,'nt_amt':nt_amt,'nt_disc':nt_disc,
                                                        'ttl_outstanding_amount':ttl_outstanding_amount,'ttl_unit':ttl_unit})
    except Exception as error:
        return render(request,'error.html',{'error':error})

#========================= for open bill ============================

@login_required(login_url='/user_login')
def for_open_bill_main_opd(request):
    try:
        pay_m_uhid = request.session['pay_m_uhid']
        pay_m_visit_id = request.session['pay_m_visit_id']
        billing_groups=request.session['billing_group']
        corporate_names=request.session['corporate_name']
        departments_name=request.session['clinical_department']
        dr_name=request.session['nurse_doctor']
        if corporate_names == 'Cash':
            corp_name = 'Cash'
        else:
            corp_all = CorporateMaster.objects.get(id=corporate_names)
            corp_name = corp_all.corporate_Name
        bill_all = BillingGroup.objects.get(id=billing_groups)
        billing_name = bill_all.billing_group
        # corporate_nam = corp_all.Corporate_Name
        mode_of_payment=OpdPaymentMode.objects.all()
        records=OpdBillingTemper.objects.filter(visit_no__exact=pay_m_visit_id,uhid=pay_m_uhid)
        ttl_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('total_amount'))
        ttl_amt = ttl_amt['total_amount__sum']
        rcv_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('receive_amount'))
        rcv_amt = rcv_amt['receive_amount__sum']
        nt_amt = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('net_ammount'))
        nt_amt = nt_amt['net_ammount__sum']
        nt_disc = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id,uhid=pay_m_uhid).aggregate(Sum('discount'))
        nt_disc = nt_disc['discount__sum']
        ttl_outstanding_amount = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('outstanding_amount'))
        ttl_outstanding_amount = ttl_outstanding_amount['outstanding_amount__sum']
        ttl_unit = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id).aggregate(Sum('unit'))
        ttl_unit = ttl_unit['unit__sum']
        if request.method == 'POST' and 'save' in request.POST:
            print('for main opd table')
            service = request.POST.getlist('service')
            uhid = request.POST.get('uhid')
            visit_id = request.POST.get('visit_id')
            temp_bill_no = request.POST.get('temp_bill_no')
            package_profile_id = request.POST.getlist('package_profile_id')
            package_profile_amt = request.POST.getlist('package_profile_amt')
            Pr_Opd_sr_bill_no = request.POST.getlist('Pr_Opd_sr_bill_no')
            print('Pr_Opd_sr_bill_no',Pr_Opd_sr_bill_no)
            corporate_id = request.POST.get('corporate_id')
            billing_group_id = request.POST.get('billing_group_id')
            net_amount = request.POST.getlist('net_amount')
            discount = request.POST.getlist('discount')
            pay_amount = request.POST.getlist('pay_amount')
            paid_amount = request.POST.getlist('paid_amount')
            outstanding_amount = request.POST.getlist('outstanding_amount')
            unit = request.POST.get('unit')
            total_net_amt = request.POST.get('total_net_amt')
            total_disc = request.POST.get('total_disc')
            total_payable_amt = request.POST.get('total_payable_amt')
            total_paid_amt = request.POST.get('total_paid_amt')
            total_outstanding_amt = request.POST.get('total_outstanding_amt')
            payment_mode = request.POST.get('payment_mode')
            request.session['searched_uhid'] = uhid
            request.session['visit_id'] = visit_id
            search_urls = request.session['search_urls']
            # Generating Bill No and Bil Id Generation Start
            yy = date.today().year
            current_yy = str(yy)[2:]
            previous_yy = str(yy - 1)[2:]
            finance_year = previous_yy + current_yy
            b_no = str(random.randint(100000, 999999))
            bill_no = 'OP' + finance_year + b_no
            today = date.today()
            today = str(today).replace('-', '')
            prefix = today[2:]
            bill_id = prefix + b_no
            # patient id generating
            PID = str(random.randint(100000, 999999))
            PTID = 'PTID' + PID
            get_uhid_data=PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
            profile_record=ProfileService.objects.all()
            profile_name_list=[data.profile_name for data in profile_record]
            request.session['pay_m_uhid'] = uhid
            request.session['pay_m_visit_id'] = visit_id
            request.session['pay_m_bill_no'] = bill_no
            # print('pay_m_bill_no', bill_no)
            one_service=set(Pr_Opd_sr_bill_no)
            package_id=set(package_profile_id)
            con =zip(one_service,package_id)
            # print('con=---------', con)
            # for d,d1 in con:
            #     if d.startwith('OP'):
            #         package=OpdPackageMaster.objects.get(id=d1)
            #         p_na=package.package_name
            #         p_amt=package.package_amount
            #         data = OpdBillingSub(
            #             bill_no=bill_no,
            #             uhid=uhid,
            #             temp_bill_no=temp_bill_no,
            #             bill_id=bill_id,
            #             service_id=p_na,
            #             charges=p_amt,
            #             visit_no=visit_id,
            #             department=departments_name,
            #             doctor_name=dr_name,
            #             corporate_id=corporate_id,
            #             billing_group_id=billing_group_id,
            #             discount=total_disc,
            #             pay_amount=total_payable_amt,
            #             paid_amount=total_paid_amt,
            #             outstanding_amount=total_outstanding_amt,
            #             unit='0',
            #             payment_mode=payment_mode,
            #             total_amount=total_paid_amt,
            #         )
            #         data.save()
            #         for i in range(len(package_profile_id)):
            #             print('i',i)
            #             ind_service = service[i]
            #             ind_uhid = uhid
            #             ind_visit_id = visit_id
            #             ind_net_amount = net_amount[i]
            #             ind_pay_amount = pay_amount[i]
            #             ind_paid_amount = paid_amount[i]
            #             ind_outstanding_amount = outstanding_amount[i]
            #             ind_unit = unit
            #             opd_billing_sub=OpdBillingSub(
            #                 bill_id='0',
            #                 bill_no='0',
            #                 temp_bill_no='0',
            #                 package_profile_id=ind_service,
            #                 package_profile_amt=ind_net_amount,
            #                 uhid='0',
            #                 department='0',
            #                 doctor_name='0',
            #                 visit_no='0',
            #                 corporate_id='0',
            #                 billing_group_id='0',
            #                 charges='0',
            #                 unit=ind_unit,
            #                 pay_amount=ind_pay_amount,
            #                 paid_amount=ind_paid_amount,
            #                 outstanding_amount=ind_outstanding_amount,
            #                 payment_mode='0',
            #                 total_amount='0',
            #                 discount='0'
            #             )
            #             opd_billing_sub.save()
            #     else:
            yy = date.today().year
            current_yy = str(yy)[2:]
            previous_yy = str(yy - 1)[2:]
            finance_year = previous_yy + current_yy
            b_no = str(random.randint(1000, 9999))
            temp_bill_nos = 'OPENID' + finance_year + b_no
            request.session['temp_bill_no'] = temp_bill_nos
            print('temp_bill_no', temp_bill_nos)
            for i in range(len(service)):
                ind_service = service[i]
                ind_uhid = uhid
                ind_visit_id = visit_id
                ind_temp_bill_no = temp_bill_nos
                ind_package_profile_id = package_profile_id[i]
                ind_package_profile_amt = package_profile_amt[i]
                ind_corporate_id = corporate_id
                ind_billing_group_id = billing_group_id
                ind_department = departments_name
                ind_dr_name = dr_name
                ind_net_amount = net_amount[i]
                ind_discount = discount[i]
                ind_pay_amount = pay_amount[i]
                ind_paid_amount = paid_amount[i]
                ind_outstanding_amount = outstanding_amount[i]
                ind_unit = unit
                ind_payment_mode = payment_mode
                # test id generating
                te_id = str(random.randint(100000, 999999))
                test_id = 'TST' + te_id
                opd_billing_sub = OpdBillingSub(
                    bill_id=bill_id,
                    bill_no=bill_no,
                    temp_bill_no=ind_temp_bill_no,
                    package_profile_id=ind_package_profile_id,
                    package_profile_amt=ind_package_profile_amt,
                    uhid=ind_uhid,
                    department=ind_department,
                    doctor_name=ind_dr_name,
                    visit_no=ind_visit_id,
                    corporate_id=ind_corporate_id,
                    billing_group_id=ind_billing_group_id,
                    service_id=ind_service,
                    charges=ind_net_amount,
                    unit=ind_unit,
                    pay_amount=ind_pay_amount,
                    paid_amount=ind_paid_amount,
                    outstanding_amount=ind_outstanding_amount,
                    payment_mode=ind_payment_mode,
                    total_amount=ind_pay_amount,
                    discount=ind_discount
                )
                opd_billing_sub.save()

                #============ 29/12/22 ==========================
                if ind_service in profile_name_list:
                    print('sucess=====================',ind_service)
                    packages=OPDBillingPackage(
                        uhid=ind_uhid,visit_no=ind_visit_id,bill_no=bill_no,
                        package_id='',package_name=ind_service,date_time=datetime.now()
                    )
                    packages.save()
                # === karan {16-12-2022} =============
                if ind_service in profile_name_list:
                    print('sucess=====================',ind_service)
                    profile_pac_record = ProfileService.objects.filter(profile_name=ind_service)[0]
                    pending_inv = PendingInvestigation_main(
                        test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                        profile_id='', profile_name=ind_service, date_time=datetime.now(),
                        department=profile_pac_record.service_department,
                        sub_department=profile_pac_record.service_sub_department
                    )
                    pending_inv.save()

                    profile_rec_filter=ProfileService.objects.filter(profile_name=ind_service)
                    for data in profile_rec_filter:
                        print('age',get_uhid_data.age)
                        if get_uhid_data.age is range(0, 5):
                            rangee=data.infant_range
                        elif get_uhid_data.age is range(6, 15):
                            rangee=data.chield_range
                        elif get_uhid_data.age is range(16, 99) and get_uhid_data.gender == 'Male':
                            rangee=data.male_range
                        elif get_uhid_data.age is range(6, 99) and get_uhid_data.gender == 'Female':
                            rangee=data.female_range
                        else:
                            rangee=data.male_range
                        pending_inv_sub=LabResultEntry(
                            test_id=test_id,profile_id='',profile_name=ind_service,service_name=data.service_name,
                            range=rangee,units=data.units
                        )
                        pending_inv_sub.save()
                    # ===================================
            if payment_mode == '':
                main_opd_billing = OpdBillingMain(
                    bill_no=bill_no,
                    bill_id=bill_id,
                    uhid=uhid,
                    temp_bill_no=temp_bill_no,
                    package_profile_id=package_profile_id,
                    visit_no=visit_id,
                    department=departments_name,
                    doctor_name=dr_name,
                    corporate_id=corporate_id,
                    billing_group_id=billing_group_id,
                    net_amount=total_net_amt,
                    discount=total_disc,
                    pay_amount=total_payable_amt,
                    paid_amount=total_paid_amt,
                    outstanding_amount=total_paid_amt,
                    payment_mode=payment_mode,
                )
                main_opd_billing.save()
            else:
                main_opd_billing = OpdBillingMain(
                    bill_no=bill_no,
                    bill_id=bill_id,
                    uhid=uhid,
                    temp_bill_no=temp_bill_no,
                    package_profile_id=package_profile_id,
                    visit_no=visit_id,
                    department=departments_name,
                    doctor_name=dr_name,
                    corporate_id=corporate_id,
                    billing_group_id=billing_group_id,
                    net_amount=total_net_amt,
                    discount=total_disc,
                    pay_amount=total_payable_amt,
                    paid_amount=total_paid_amt,
                    outstanding_amount=total_outstanding_amt,
                    payment_mode=payment_mode,
                    checklist_status='',
                    claim_status = '',
                    claim_amt = '',
                )
                main_opd_billing.save()
            data = OpdBillingTemper.objects.filter(uhid__exact=uhid,visit_no__exact=pay_m_visit_id).delete()
            return  HttpResponseRedirect('/main_opd')
        patient_name = request.session['patient_name']
        print('patient_name',patient_name)
        dob = request.session['dob']
        mobile_number = request.session['mobile_number']
        gender = request.session['gender']
        pay_m_uhid = request.session['pay_m_uhid']
        pay_m_visit_id = request.session['pay_m_visit_id']
        billing_group=request.session['billing_group']
        corporate_names=request.session['corporate_name']
        main_table = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)|Q(visit_no=pay_m_visit_id)).last()
        print(f'main_table',main_table)
        return render(request,'clinical/opd_bill/for_open_opd_main.html',{'records':records,'mode_of_payment':mode_of_payment,'pay_m_visit_id':pay_m_visit_id,'pay_m_uhid':pay_m_uhid,
                                                        'billing_group':billing_group,'corporate_names':corporate_names,
                                                    'patient_name':patient_name,'dob':dob,'mobile_number':mobile_number,'gender':gender,'corp_name':corp_name,
                                                        'billing_name':billing_name,'ttl_amt':ttl_amt,'rcv_amt':rcv_amt,'nt_amt':nt_amt,'nt_disc':nt_disc,
                                                        'ttl_outstanding_amount':ttl_outstanding_amount,'ttl_unit':ttl_unit})
    except Exception as error:
        return render(request,'error.html',{'error':error})

#===================================== END ===============================
@login_required(login_url='/user_login')
def opd_billing_search(request):
    try:
        aaaa = PatientsRegistrationsAllInOne.objects.all()
        if aaaa:
            visit_list=[]
            records2 = PatientsRegistrationsAllInOne.objects.extra(select={
            'pat_tariff_name':'Select billing_group from testapp_billinggroup where id=testapp_patientsregistrationsallinone.billing_group',
            'pat_insurance':'Select corporate_Name from testapp_CorporateMaster where id=testapp_patientsregistrationsallinone.nhif_ins_cor_name',
            'pat_visit_id':'Select visit_id from testapp_PatientVisitMains where uhid=testapp_patientsregistrationsallinone.uhid',
            }).filter(location=request.location).order_by('-update_status')
            print("patient_name_1",records2)
            list_uhis=[data.uhid for data in records2]
            for vi in list_uhis:
                visit=PatientVisitMains.objects.filter(uhid=vi).last()
                if not visit:
                    visit_list.append(' ')
                else:
                    visit_list.append(visit)
            records1=zip(records2,visit_list)
            if request.method == 'POST':
                uhid = request.POST.get('uhid').strip()
                get_dob = request.POST.get('dob')
                mobile_number = request.POST.get('mobile_number').strip()
                patient_name = request.POST.get('patient_name').strip()
                patient_name_1 = patient_name.split(" ")
                
                if patient_name == '':
                    patient_name="Not Provided"
                if get_dob == '':
                    get_dob=date.today()

                if uhid:
                    records2 = PatientsRegistrationsAllInOne.objects.extra(select={
                        'pat_tariff_name': 'Select billing_group from testapp_BillingGroup where id=testapp_patientsregistrationsallinone.billing_group',
                        'pat_insurance': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_patientsregistrationsallinone.nhif_ins_cor_name',
                        'pat_visit_id': 'Select visit_id from testapp_PatientVisitMains where uhid=testapp_patientsregistrationsallinone.uhid',
                    }).filter(uhid__iexact = uhid)
                    list_uhis = [data.uhid for data in records2]
                    for vi in list_uhis:
                        visit = PatientVisitMains.objects.filter(uhid=vi).last()
                        if not visit:
                            visit_list.append(' ')
                        else:
                            visit_list.append(visit)
                    print('visit', len(visit_list))
                    records1 = zip(records2, visit_list)
                elif mobile_number != "+254":
                    print("mbl no")
                    records2 = PatientsRegistrationsAllInOne.objects.extra(select={
                        'pat_tariff_name': 'Select billing_group from testapp_BillingGroup where id=testapp_patientsregistrationsallinone.billing_group',
                        'pat_insurance': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_patientsregistrationsallinone.nhif_ins_cor_name',
                        'pat_visit_id': 'Select visit_id from testapp_PatientVisitMains where uhid=testapp_patientsregistrationsallinone.uhid',
                    }).filter(mobile_number__icontains = mobile_number)
                    list_uhis = [data.uhid for data in records2]
                    for vi in list_uhis:
                        visit = PatientVisitMains.objects.filter(uhid=vi).last()
                        if not visit:
                            visit_list.append(' ')
                        else:
                            visit_list.append(visit)
                    print('visit', len(visit_list))
                    records1 = zip(records2, visit_list)
                elif len(patient_name_1) == 2:
                    records2 = PatientsRegistrationsAllInOne.objects.extra(select={
                        'pat_tariff_name': 'Select billing_group from testapp_BillingGroup where id=testapp_patientsregistrationsallinone.billing_group',
                        'pat_insurance': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_patientsregistrationsallinone.nhif_ins_cor_name',
                        'pat_visit_id': 'Select visit_id from testapp_PatientVisitMains where uhid=testapp_patientsregistrationsallinone.uhid',
                    }).filter(Q(uhid__exact=uhid)|Q(first_name__icontains=patient_name_1[0],last_name__icontains=patient_name_1[2])|Q(first_name__icontains=patient_name_1[0],middle_name__icontains=patient_name_1[1]) | Q(mobile_number__exact=mobile_number))
                    list_uhis = [data.uhid for data in records2]
                    for vi in list_uhis:
                        visit = PatientVisitMains.objects.filter(uhid=vi).last()
                        if not visit:
                            visit_list.append(' ')
                        else:
                            visit_list.append(visit)
                    print('visit', len(visit_list))
                    records1 = zip(records2, visit_list)
                elif len(patient_name_1) == 1:
                    records2 = PatientsRegistrationsAllInOne.objects.extra(select={
                        'pat_tariff_name': 'Select billing_group from testapp_BillingGroup where id=testapp_patientsregistrationsallinone.billing_group',
                        'pat_insurance': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_patientsregistrationsallinone.nhif_ins_cor_name',
                        'pat_visit_id': 'Select visit_id from testapp_PatientVisitMains where uhid=testapp_patientsregistrationsallinone.uhid',
                    }).filter(Q(first_name__icontains=patient_name_1[0],location=request.location)|Q(middle_name__icontains=patient_name_1[0],location=request.location)|Q(last_name__icontains=patient_name_1[0],location=request.location)|Q(uhid=uhid,location=request.location)|Q(mobile_number__exact=mobile_number))
                    list_uhis = [data.uhid for data in records2]
                    for vi in list_uhis:
                        visit = PatientVisitMains.objects.filter(uhid=vi).last()
                        if not visit:
                            visit_list.append(' ')
                        else:
                            visit_list.append(visit)
                    print('visit', len(visit_list))
                    records1 = zip(records2, visit_list)
                elif len(patient_name_1) == 3:
                    records2 = PatientsRegistrationsAllInOne.objects.extra(select={
                        'pat_tariff_name': 'Select billing_group from testapp_BillingGroup where id=testapp_patientsregistrationsallinone.billing_group',
                        'pat_insurance': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_patientsregistrationsallinone.nhif_ins_cor_name',
                        'pat_visit_id': 'Select visit_id from testapp_PatientVisitMains where uhid=testapp_patientsregistrationsallinone.uhid',
                    }).filter(Q(uhid__exact=uhid)|Q(first_name__icontains=patient_name_1[0],middle_name__icontains=patient_name_1[1],last_name__icontains=patient_name_1[2])|Q(mobile_number__exact=mobile_number))
                    list_uhis = [data.uhid for data in records2]
                    for vi in list_uhis:
                        visit = PatientVisitMains.objects.filter(uhid=vi).last()
                        if not visit:
                            visit_list.append(' ')
                        else:
                            visit_list.append(visit)
                    print('visit', len(visit_list))
                    records1 = zip(records2, visit_list)
                context = {
                    'records1': records1
                }
                return render(request,'clinical/opd_billing_search.html',context)
            service_master=ServiceChargeMaster.objects.all()
            context = {
                'records1': records1,'service_master':service_master,
            }
            return render(request,'clinical/opd_billing_search.html',context)
            
        else:
            return render(request,'clinical/opd_billing_search.html')
    except Exception as error:
        return render(request,'error.html',{'error':error})
import re

@login_required(login_url='/user_login')
def opd_payment_mode(request):
    # try:
        # form=OpdPaymentForm()
        tatol_package_amt=0
        package_deatils=''
        intell_search=''
        # intell_search = request.session['intell_search']
        data1=OpdPackageMaster.objects.all()
        p_name=[data.package_name for data in data1]
        if request.method=='POST':
            messages.success(request,'')
            pay_m_uhid=request.POST.get('pay_m_uhid')
            bill_no=request.POST.get('bill_no')
            pay_m_visit_id=request.POST.get('pay_m_visit_id')
            amount=request.POST.get('net_amount')
            mode_type=request.POST.get('mode_type')
             # ================== fields ===========
            # cash
            cash_paid_by=request.POST.get('cash_paid_by')
            cash_pay_amount=request.POST.get('cash_pay_amount')
            remaing_amount=request.POST.get('remaing_amount')
            # m-pesa
            mpesa_paid_by=request.POST.get('mpesa_paid_by')
            mpesa_ref_no=request.POST.get('mpesa_ref_no')
            mpesa_card_holder_name=request.POST.get('mpesa_card_holder_name')
            mpesa_mobile_no=request.POST.get('mpesa_mobile_no')
            mpesa_pay_amount=request.POST.get('mpesa_pay_amount')
            # card
            card_ref_no=request.POST.get('card_ref_no')
            card_paid_by=request.POST.get('card_paid_by')
            card_pay_amount=request.POST.get('card_pay_amount')
            card_bank_no=request.POST.get('card_bank_no')
            # bank
            bank=request.POST.get('bank')
            bank_ref_no=request.POST.get('bank_ref_no')
            bank_card_holder_name=request.POST.get('bank_card_holder_name')
            bank_pay_amount=request.POST.get('bank_pay_amount')
            # eft
            eft_ref_no=request.POST.get('eft_ref_no')
            eft_bank_no=request.POST.get('eft_bank_no')
            eft_paid_by=request.POST.get('eft_paid_by')
            eft_pay_amount=request.POST.get('eft_pay_amount')
            # cheque
            cheque_ref_no=request.POST.get('cheque_ref_no')
            cheque_bank_no=request.POST.get('cheque_bank_no')
            cheque_paid_by=request.POST.get('cheque_paid_by')
            cheque_pay_amount=request.POST.get('cheque_pay_amount')

            pay_m_receive_amount = request.session['pay_m_receive_amount']
            pay_m_uhid = request.session['pay_m_uhid']
            pay_m_visit_id = request.session['pay_m_visit_id']
            pay_m_bill_nos = request.session['pay_m_bill_no']
            print('====',mode_type)
            receipt_no_count = OpdPayment.objects.all().count()
            today = date.today()
            today_date = today.strftime("%d%m%y")
            receipt_no = 'RC' + today_date + str(receipt_no_count)
            types='Bill Now'
            print('receipt_no--------->,', receipt_no)
            if mode_type == 'cash':
                if float(amount) == float(cash_pay_amount):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                print('status', status)
                OpdPayment.objects.create(
                    uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id, mode_type=mode_type,
                    paid_by=cash_paid_by, net_amount=amount, paid_amount=cash_pay_amount, status=status,
                    created_by_id = request.user.id, location_id = request.location,receipt_no=receipt_no,type=types,
                )
                update_pay_amt = OpdBillingMain.objects.filter(uhid=pay_m_uhid, bill_no=pay_m_bill_nos,
                                                               visit_no=pay_m_visit_id).last()
                update_pay_amt.paid_amount = cash_pay_amount
                update_pay_amt.outstanding_amount = remaing_amount
                update_pay_amt.save()
            elif mode_type == 'debit_credit_card':
                if float(amount) == float(card_pay_amount):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                OpdPayment.objects.create(
                    uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id, mode_type=mode_type,
                    paid_by=card_paid_by, net_amount=amount, paid_amount=card_pay_amount, ref_number=card_ref_no,
                    status=status, bank_no=card_bank_no,receipt_no=receipt_no,type=types,
                    created_by_id=request.user.id, location_id=request.location,
                )
                update_pay_amt = OpdBillingMain.objects.filter(uhid=pay_m_uhid, bill_no=pay_m_bill_nos,
                                                               visit_no=pay_m_visit_id).last()
                update_pay_amt.paid_amount = card_pay_amount
                update_pay_amt.outstanding_amount = remaing_amount
                update_pay_amt.save()
            elif mode_type == 'm_pesa':
                if float(amount) == float(mpesa_pay_amount):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                OpdPayment.objects.create(
                    uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id, mode_type=mode_type,
                    paid_by=mpesa_paid_by, net_amount=amount, paid_amount=mpesa_pay_amount, ref_number=mpesa_ref_no,
                    status=status, card_holder_name=mpesa_card_holder_name, mobile_nummber=mpesa_mobile_no,
                    created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no,type=types,
                )
                update_pay_amt = OpdBillingMain.objects.filter(uhid=pay_m_uhid, bill_no=pay_m_bill_nos,
                                                               visit_no=pay_m_visit_id).last()
                update_pay_amt.paid_amount = mpesa_pay_amount
                update_pay_amt.outstanding_amount = remaing_amount
                update_pay_amt.save()
            elif mode_type == 'bank':
                if float(amount) == float(bank_pay_amount):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                OpdPayment.objects.create(
                    uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id, mode_type=mode_type,
                    bank_no=bank, net_amount=amount, paid_amount=bank_pay_amount, ref_number=bank_ref_no, status=status,
                    card_holder_name=bank_card_holder_name,
                    created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no,type=types,
                )
                update_pay_amt = OpdBillingMain.objects.filter(uhid=pay_m_uhid, bill_no=pay_m_bill_nos,
                                                               visit_no=pay_m_visit_id).last()
                update_pay_amt.paid_amount = bank_pay_amount
                update_pay_amt.outstanding_amount = remaing_amount
                update_pay_amt.save()
            elif mode_type == 'eft':
                if float(amount) == float(eft_pay_amount):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                OpdPayment.objects.create(
                    uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id, mode_type=mode_type,
                    paid_by=eft_paid_by, net_amount=amount, paid_amount=eft_pay_amount, ref_number=eft_ref_no,
                    status=status, bank_no=eft_bank_no,
                    created_by_id = request.user.id, location_id = request.location,receipt_no=receipt_no,type=types,
                )
                update_pay_amt = OpdBillingMain.objects.filter(uhid=pay_m_uhid, bill_no=pay_m_bill_nos,
                                                               visit_no=pay_m_visit_id).last()
                update_pay_amt.paid_amount = eft_pay_amount
                update_pay_amt.outstanding_amount = remaing_amount
                update_pay_amt.save()
            elif mode_type == 'cheque':
                if float(amount) == float(cheque_pay_amount):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                OpdPayment.objects.create(
                    uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id, mode_type=mode_type,
                    paid_by=cheque_paid_by, net_amount=amount, paid_amount=cheque_pay_amount, ref_number=cheque_ref_no,
                    status=status, bank_no=cheque_bank_no,
                    created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no,type=types,
                )
                update_pay_amt = OpdBillingMain.objects.filter(uhid=pay_m_uhid, bill_no=pay_m_bill_nos,
                                                               visit_no=pay_m_visit_id).last()
                update_pay_amt.paid_amount = cheque_pay_amount
                update_pay_amt.outstanding_amount = remaing_amount
                update_pay_amt.save()
            elif mode_type == 'all':
                total = float('0' + cash_pay_amount) + float('0' + card_pay_amount) + float(
                    '0' + mpesa_pay_amount) + float('0' + bank_pay_amount) + float('0' + eft_pay_amount) + float(
                    '0' + cheque_pay_amount)
                if float(amount) == float(total):
                    status = 'fully_paid'
                else:
                    status = 'partially_paid'
                if cash_pay_amount:
                    receipt_no_count = OpdPayment.objects.all().count()
                    today = date.today()
                    today_date = today.strftime("%d%m%y")
                    receipt_no_cash = 'RC' + today_date + str(receipt_no_count)
                    OpdPayment.objects.create(
                        uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id,mode_type='cash',
                        paid_by=cash_paid_by,net_amount=amount,paid_amount=cash_pay_amount,status=status,
                        created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no_cash,type=types,
                    )
                if card_pay_amount:
                    receipt_no_count = OpdPayment.objects.all().count()
                    today = date.today()
                    today_date = today.strftime("%d%m%y")
                    receipt_no_debit = 'RC' + today_date + str(receipt_no_count)
                    OpdPayment.objects.create(
                        uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id,mode_type='debit_credit_card',
                        paid_by=card_paid_by,net_amount=amount,paid_amount=card_pay_amount,ref_number=card_ref_no,status=status,bank_no=card_bank_no,
                        created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no_debit,type=types,
                    )
                if mpesa_pay_amount:
                    receipt_no_count = OpdPayment.objects.all().count()
                    today = date.today()
                    today_date = today.strftime("%d%m%y")
                    receipt_no_m_pesa = 'RC' + today_date + str(receipt_no_count)
                    OpdPayment.objects.create(
                        uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id,mode_type='m_pesa',
                        bank_no=mpesa_paid_by,net_amount=amount,paid_amount=mpesa_pay_amount,ref_number=mpesa_ref_no,status=status,card_holder_name=mpesa_card_holder_name,
                        mobile_nummber=mpesa_mobile_no,created_by_id = request.user.id, location_id = request.location,receipt_no=receipt_no_m_pesa,type=types,
                    )
                if bank_pay_amount:
                    receipt_no_count = OpdPayment.objects.all().count()
                    today = date.today()
                    today_date = today.strftime("%d%m%y")
                    receipt_no_bank = 'RC' + today_date + str(receipt_no_count)
                    OpdPayment.objects.create(
                        uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id,mode_type='bank',
                        bank_no=bank,net_amount=amount,paid_amount=bank_pay_amount,ref_number=bank_ref_no,status=status,card_holder_name=bank_card_holder_name,
                        created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no_bank,type=types,
                    )
                if eft_pay_amount:
                    receipt_no_count = OpdPayment.objects.all().count()
                    today = date.today()
                    today_date = today.strftime("%d%m%y")
                    receipt_no_eft = 'RC' + today_date + str(receipt_no_count)
                    OpdPayment.objects.create(
                        uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id,mode_type='eft',
                        paid_by=eft_paid_by,net_amount=amount,paid_amount=eft_pay_amount,ref_number=eft_ref_no,status=status,bank_no=eft_bank_no,
                        created_by_id=request.user.id, location_id=request.location,receipt_no=receipt_no_eft,type=types,
                    )
                if cheque_pay_amount:
                    receipt_no_count = OpdPayment.objects.all().count()
                    today = date.today()
                    today_date = today.strftime("%d%m%y")
                    receipt_no_cheque = 'RC' + today_date + str(receipt_no_count)
                    OpdPayment.objects.create(
                        uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id,mode_type='cheque',
                        paid_by=cheque_paid_by,net_amount=amount,paid_amount=cheque_pay_amount,ref_number=cheque_ref_no,status=status,bank_no=cheque_bank_no,
                        created_by_id = request.user.id, location_id = request.location,receipt_no=receipt_no_cheque,type=types,
                    )
            #  not completed
            patient_detail=PatientsRegistrationsAllInOne.objects.get(uhid=pay_m_uhid)
            title=patient_detail.title
            first_name=patient_detail.first_name
            middle_name=patient_detail.middle_name
            last_name=patient_detail.last_name
            mobile_number=patient_detail.mobile_number
            address=patient_detail.address
            if middle_name== None:
                patinet_name = title + ' ' + first_name + ' ' + last_name
            else:
                patinet_name = title + ' ' + first_name + ' ' + middle_name + ' ' + last_name
            billing_groups = BillingGroup.objects.get(id=patient_detail.billing_group)
            if patient_detail.nhif_ins_cor_name == 'Cash':
                sponsors = 'Self'
            else:
                sponsorss = CorporateMaster.objects.get(id=patient_detail.nhif_ins_cor_name)
                sponsors=sponsorss.corporate_Name
            list_d=['Walked By','AAA ','BBB']
            if patient_detail.referred_by in list_d:
                reffered_by = 'Walked By'
                print('reffered_by----,',reffered_by)
            else:
                reffered_bys = Refered_by_Master.objects.get(id=patient_detail.referred_by)
                reffered_by=reffered_bys.Staff_name
            #========Card no some field *********1234 like this ===============
            pay_m_receive_amount = request.session['pay_m_receive_amount']
            pay_m_uhid = request.session['pay_m_uhid']
            pay_m_visit_id = request.session['pay_m_visit_id']
            pay_m_bill_nos = request.session['pay_m_bill_no']
            default_unit=2
            default_discount=10.0
            payment_details=OpdPayment.objects.filter(uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id)
            print('payment_details---------------------->,',payment_details)
            visit_detail=PatientVisitMains.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_id=pay_m_visit_id))
            visit_date_time=''
            temp_record = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_no=pay_m_visit_id)).last()
            ser_name = OpdBillingSub.objects.filter(uhid=pay_m_uhid, visit_no=pay_m_visit_id, bill_no=pay_m_bill_nos)
            services_name = [data.service_id for data in ser_name]
            inv_name = [data.service_category for data in ser_name]
            print('inv_name------>,',inv_name)
            ins_records = ServiceCategory.objects.filter(service_category__in=inv_name).order_by('id')
            services_que = ServiceChargeMaster.objects.filter(service_id__service_name__in=services_name)
            ttl_amt = OpdBillingSub.objects.filter(uhid=pay_m_uhid, visit_no=pay_m_visit_id, bill_no=pay_m_bill_nos,
                                                   service_category__in=inv_name).aggregate(Sum('paid_amount'))
            ttl_amt = ttl_amt['paid_amount__sum']
            exact_bill_id=temp_record.bill_no
            date_time=temp_record.bill_date_time
            mode_of_payment = OpdPaymentMode.objects.all()
            mode_of_bank = BankMaster.objects.all()
            temp_reco = OpdBillingMain.objects.filter(bill_no__exact=exact_bill_id).last()
            exact_bill_no=temp_reco.bill_no
            temp_records = OpdBillingSub.objects.filter(bill_no=exact_bill_no)
            # =================== Here To calculate sub total in invoice =======================
            sub_list = []
            for inv in ins_records:
                ttl_amt = OpdBillingSub.objects.filter(bill_no=exact_bill_no,
                                                       service_category=inv.service_category).aggregate(Sum('charges'))
                net_amount = ttl_amt['charges__sum']
                sub_list.append(net_amount)
            # ============================ Here total Amount  ==============================
            net_amount = OpdBillingSub.objects.filter(bill_no=exact_bill_no).aggregate(Sum('charges'))
            net_amount = net_amount['charges__sum']
            # ================= END =================================================
            for visit_detail in visit_detail:
                visit_date_time = visit_detail.visit_date_time
            all_data = zip(ins_records,sub_list)

            context = {
                'pay_m_visit_id': pay_m_visit_id,'amount':amount,'pay_m_uhid':pay_m_uhid,'bill_no':bill_no,
                'patinet_name':patinet_name,'mobile_number':mobile_number,'address':address,'visit_detail':visit_detail,
                'default_unit':default_unit,'default_discount':default_discount,'patient_detail':patient_detail,'all_data':all_data,
                'visit_date_time':visit_date_time,'temp_records':temp_records,'temp_record':temp_record,
                'net_amount':net_amount,'date_time':date_time,'exact_bill_no':exact_bill_no,'mode_of_payment':mode_of_payment,
                'mode_of_bank':mode_of_bank,'intell_search':intell_search,'tatol_package_amt':tatol_package_amt,
                'billing_groups':billing_groups,'sponsors':sponsors,'payment_details':payment_details,'reffered_by':reffered_by,
                'sponsors':sponsors,
            }
            # return render(request, 'clinical/opdbillrecipte.html', context)
            return render(request, 'clinical/opd_billing_receipt_cash.html', context)
        pay_m_receive_amount=request.session['pay_m_receive_amount']
        pay_m_uhid=request.session['pay_m_uhid']
        pay_m_visit_id=request.session['pay_m_visit_id']
        # temp_visit=request.session['temp_visit']
        pay_m_bill_nos=request.session['pay_m_bill_no']

        # temp_records = OpdBillingTemper.objects.filter(visit_no=pay_m_visit_id)
        temp_record = OpdBillingMain.objects.filter(uhid__exact=pay_m_uhid).last()
        exact_visit_id = temp_record.bill_no
        # temp_reco = OpdBillingMain.objects.filter(visit_no__exact=exact_visit_id)
        net_amount = OpdBillingMain.objects.filter(bill_no__exact=exact_visit_id).aggregate(Sum('paid_amount'))
        net_amount = net_amount['paid_amount__sum']
        context={
            'pay_m_receive_amount':pay_m_receive_amount,'pay_m_uhid':pay_m_uhid,
            'pay_m_visit_id':pay_m_visit_id,'net_amount':net_amount,
        }
        return render(request,'clinical/opd_payment_mode.html',context)
    # except Exception as error:
    #     return render(request,'error.html',{'error':error})

def opd_payment_credit(request):
    # form=OpdPaymentForm()
    tatol_package_amt=0
    intell_search = request.session['intell_search']
    data1=OpdPackageMaster.objects.all()
    p_name=[data.package_name for data in data1]

    if request.method=='POST':
        # service_name=request.session['service_name']
        messages.success(request,'')
        pay_m_uhid=request.POST.get('pay_m_uhid')
        bill_no=request.POST.get('bill_no')
        pay_m_visit_id=request.POST.get('pay_m_visit_id')
        patient_paid_amts=request.POST.get('patient_paid_amts')
        amount=request.POST.get('amount')
        paid_amt=request.POST.get('paid_amt')
        mode_type=request.POST.get('mode_type')
        bank=request.POST.get('bank')
        card_no=request.POST.get('card_no')
        utr_id=request.POST.get('utr_id')
        patient_detail=PatientsRegistrationsAllInOne.objects.get(uhid=pay_m_uhid)
        title=patient_detail.title
        first_name=patient_detail.first_name
        middle_name=patient_detail.middle_name
        last_name=patient_detail.last_name
        mobile_number=patient_detail.mobile_number
        address=patient_detail.address
        print('names====,',title,first_name,middle_name,last_name)
        if middle_name == None:
            patinet_name = title + ' ' + first_name + ' ' + last_name
        else:
            patinet_name=title+' '+first_name+' '+middle_name+' '+last_name
        billing_groups=BillingGroup.objects.get(id=patient_detail.billing_group)
        if patient_detail.nhif_ins_cor_name == 'Cash':
            sponsors='Cash'
        else:
            sponsors=CorporateMaster.objects.get(id=patient_detail.nhif_ins_cor_name)
        list_d=['Walked By','AAA ','BBB']
        if patient_detail.referred_by in list_d:
            reffered_by = 'Walked By'
            print('reffered_by----,',reffered_by)
        else:
            reffered_bys = Refered_by_Master.objects.get(id=patient_detail.referred_by)
            reffered_by=reffered_bys.Staff_name
        # reffered_by=Refered_by_Master.objects.get(id=patient_detail.referred_by)
        pay_m_receive_amount = request.session['pay_m_receive_amount']
        pay_m_uhid = request.session['pay_m_uhid']
        pay_m_visit_id = request.session['pay_m_visit_id']
        pay_m_bill_nos = request.session['pay_m_bill_no']
        # pay_m_bill_no=101
        print('pay_m_bill_no==========>>>>',pay_m_bill_nos)
        opd_pay=Credit(
            uhid=pay_m_uhid,
            bill_no=pay_m_bill_nos,
            visit_no=pay_m_visit_id,
            patient_paid_amt=patient_paid_amts,
            net_payable_amt=amount,
            paid_amt=paid_amt,created_by_id=request.user.id,location_id=request.location,
        )
        opd_pay.save()
        default_unit=2
        default_discount=10.0
        visit_detail=PatientVisitMains.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_id=pay_m_visit_id))
        visit_date_time=''
        temp_record = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_no=pay_m_visit_id,bill_no=pay_m_bill_nos)).last()
        ser_name=OpdBillingSub.objects.filter(uhid=pay_m_uhid,visit_no=pay_m_visit_id,bill_no=pay_m_bill_nos)
        services_name=[data.service_id for data in ser_name]
        inv_name=[data.service_category for data in ser_name]
        ins_records = ServiceCategory.objects.filter(service_category__in=inv_name).order_by('id')
        services_que=ServiceChargeMaster.objects.filter(service_id__service_name__in=services_name)
        ttl_amt = OpdBillingSub.objects.filter(uhid=pay_m_uhid,visit_no=pay_m_visit_id,bill_no=pay_m_bill_nos,service_category__in=inv_name).aggregate(Sum('paid_amount'))
        ttl_amt = ttl_amt['paid_amount__sum']
        # temp_record = OpdBillingMain.objects.filter(uhid__exact=pay_m_uhid).last()
        exact_bill_id=temp_record.bill_no
        exact_visit_id=temp_record.visit_no
        date_time=temp_record.bill_date_time
        mode_of_payment = OpdPaymentMode.objects.all()
        mode_of_bank = BankMaster.objects.all()
        temp_reco = OpdBillingMain.objects.filter(bill_no__exact=exact_bill_id).last()
        temp_visit=temp_reco.visit_no
        exact_bill_no=temp_reco.bill_no
        temp_records = OpdBillingSub.objects.filter(bill_no=exact_bill_no)
        # bill_No=temp_records.bill_no
        # =================== Here To calculate sub total in invoice =======================
        sub_list = []
        for inv in ins_records:
            ttl_amt = OpdBillingSub.objects.filter(bill_no=exact_bill_no,
                                                   service_category=inv.service_category).aggregate(Sum('charges'))
            net_amount = ttl_amt['charges__sum']
            sub_list.append(net_amount)
        # ============================ Here total Amount  ==============================
        net_amount = OpdBillingSub.objects.filter(bill_no=exact_bill_no).aggregate(Sum('charges'))
        net_amount = net_amount['charges__sum']
        net_amount_main = OpdBillingMain.objects.filter(bill_no__exact=exact_bill_id).aggregate(Sum('paid_amount'))
        net_amount_main = net_amount_main['paid_amount__sum']
        net_disc_main = OpdBillingMain.objects.filter(bill_no__exact=exact_bill_id).aggregate(Sum('discount'))
        net_disc_main = net_disc_main['discount__sum']
        # ================= END =================================================
        for visit_detail in visit_detail:
            visit_date_time = visit_detail.visit_date_time
        all_data=zip(ins_records,sub_list)
        context = {
            'pay_m_visit_id': pay_m_visit_id,'amount':amount,'pay_m_uhid':pay_m_uhid,'bill_no':bill_no,
            'patinet_name':patinet_name,'mobile_number':mobile_number,'address':address,'visit_detail':visit_detail,
            'default_unit':default_unit,'default_discount':default_discount,'patient_detail':patient_detail,
            'visit_date_time':visit_date_time,'temp_records':temp_records,
            'net_amount':net_amount,'date_time':date_time,'exact_bill_no':exact_bill_no,'mode_of_payment':mode_of_payment,
            'mode_of_bank':mode_of_bank,'tatol_package_amt':tatol_package_amt,"intell_search":intell_search,
            'temp_record':temp_record,'billing_groups':billing_groups,'sponsors':sponsors,'all_data':all_data,
            'reffered_by':reffered_by,'services_que':services_que,'ins_records':ins_records,'ttl_amt':ttl_amt,
            'net_amount_main':net_amount_main,'net_disc_main':net_disc_main,
        }
        # return render(request, 'clinical/opdbillreciptecash.html', context)
        return render(request, 'clinical/opd_billiing_receipt_insurance.html', context)

    pay_m_receive_amount=request.session['pay_m_receive_amount']
    pay_m_uhid=request.session['pay_m_uhid']
    pay_m_visit_id=request.session['pay_m_visit_id']
    pay_m_bill_nos=request.session['pay_m_bill_no']
    temp_record = OpdBillingMain.objects.filter(uhid__exact=pay_m_uhid).last()
    exact_visit_id = temp_record.bill_no
    net_amount = OpdBillingMain.objects.filter(bill_no__exact=exact_visit_id).aggregate(Sum('paid_amount'))
    net_amount = net_amount['paid_amount__sum']
    paid_amt=0
    context={
        'pay_m_receive_amount':pay_m_receive_amount,'pay_m_uhid':pay_m_uhid,
        'pay_m_visit_id':pay_m_visit_id,'net_amount':net_amount,'paid_amt':paid_amt
    }
    return render(request,'clinical/opd_payment_credit.html',context)

def opd_invoice(request):
    pass
def visit_dashboard1(request):
    return render(request,'clinical/visit_dashboard.html')
def opdbillrecipte(request):
    return render(request,'clinical/opdbillrecipte.html')

# Images Uploading.....
def image_uploading(request):
    images=request.GET.get('patient_profile')
    img_saving=PatientImages(p_images=images)
    img_saving.save()
    print('images ',images)
    return HttpResponse('Images')

# date 13/04/20222
# Nurser Station
@login_required(login_url='/user_login')
def nurse_dashboard(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'clinical_management' in access.user_profile.screen_access:
        today=datetime.today()
        monday = today - timedelta(days=today.weekday())  # assuming start of week is Monday
        week_dates = []
        for i in range(7):
            week_dates.append((monday + timedelta(days=i)).strftime("%Y-%m-%d"))
        consultant_patient = VitalSign.objects.extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        }).filter(location=request.location).order_by("-id").exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','completed',]))
        total_p = consultant_patient.count()
        Doctor = DoctorTable.objects.all().count()

        pat = PatientVisitMains.objects.filter(status='processing')
        idd = []
        for data in pat:
            bill = OpdBillingMain.objects.filter(visit_no=data.visit_id,uhid=data.uhid).last()
            if bill:
                idd.append(bill.id)
        records = OpdBillingMain.objects.extra(select={
            'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        }).filter(location=request.location, id__in=idd).order_by("-id").exclude(bill_id__in=VitalSign.objects.values('bill_id')).count()

        pending_visited_list = OpdBillingMain.objects.extra(select={
            'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        }).filter(location=request.location, id__in=idd,bill_date_time__date= today).order_by("-id").exclude(bill_id__in=VitalSign.objects.values('bill_id'))

        
        discharged_patient = PatientVisitMains.objects.filter(visit_type=2,claim_no='discharged',location=request.location).count()

        date_visited_lst = []
        for data in week_dates:
            dates_visit = OpdBillingMain.objects.filter(location=request.location, id__in=idd,bill_date_time__date = data ).exclude(bill_id__in=VitalSign.objects.values('bill_id')).count()
            date_visited_lst.append(dates_visit)

        # Monthly Counts

        Monthly_visited = OpdBillingMain.objects.filter(location=request.location,bill_date_time__month = today.month).count()
        
        pending_visited_count = OpdBillingMain.objects.filter(location=request.location, id__in=idd,bill_date_time__month= today.month).exclude(bill_id__in=VitalSign.objects.values('bill_id')).count()
        monthly_consultant = VitalSign.objects.filter(location=request.location,date__month = today.month).order_by("-id").exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','completed',])).count()
        monthly_discharged_patient = PatientVisitMains.objects.filter(visit_type=2,claim_no='discharged',visit_date_time__month = today.month,location=request.location).count()
        print("monthly_consultant",monthly_discharged_patient)
        context = {
            'access':access,"week_dates":week_dates,"records":records,"total_p":total_p,"Doctor":Doctor,
            'discharged_patient':discharged_patient,"date_visited_lst":date_visited_lst,"pending_visited_list":pending_visited_list,"Monthly_visited":Monthly_visited,
            'pending_visited_count':pending_visited_count,"monthly_consultant":monthly_consultant,"monthly_discharged_patient":monthly_discharged_patient
        }
        return render(request,'nurse_station/nurse_dashboard.html',context)
    else:
        return redirect('dashboard')

# def visit_dashboard(request):
#     searching_uhid = request.GET.get('uhid')
#     records=OpdBillingMain.objects.all()
#     pending_patient=records.count()
#     if searching_uhid != None:
#         search_records = OpdBillingMain.objects.filter(uhid=searching_uhid)
#         context={
#             'search_records':search_records,
#         }
#         return render(request,'nurse_station/visit_dashboard.html',context)
#     context={
#         'records':records,'pending_patient':pending_patient
#     }
#     return render(request,'nurse_station/visit_dashboard.html',context)

@login_required(login_url='/user_login')
def visit_dashboard(request):
    searching_uhid = request.GET.get('uhid')
    pat_name = request.GET.get('name')
    pat=PatientVisitMains.objects.filter(status='processing')
    idd=[]
    for data in pat:
        bill=OpdBillingMain.objects.filter(visit_no=data.visit_id,uhid=data.uhid).last()
        if bill:
            idd.append(bill.id)
    records = OpdBillingMain.objects.extra(select={
        'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
    }).filter(location=request.location, id__in=idd).order_by("-id").exclude(bill_id__in=VitalSign.objects.values('bill_id'))
    print('record1',records,records)
    pending_patient=records.count()

    if searching_uhid:
        records = OpdBillingMain.objects.filter(Q(uhid__exact=searching_uhid)|Q(bill_no__exact=searching_uhid)).extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
    }).filter(location=request.location,id__in=idd).order_by("-id").exclude(bill_id__in=VitalSign.objects.values('bill_id'))
    if pat_name:
        pat_record=PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=pat_name,location=request.location)
        list_uhid=[data.uhid for data in pat_record]
        records = OpdBillingMain.objects.filter(uhid__in=list_uhid).extra(
            select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            }).filter(location=request.location,id__in=idd).order_by("-id").exclude(
            bill_id__in=VitalSign.objects.values('bill_id'))
    context={
        'records':records,'pending_patient':pending_patient
    }
    return render(request,'nurse_station/kennedy/visit_dashboard.html',context)
# =====================Clinical Management====================

@login_required(login_url='/user_login')
def clinical_managements(request,data):
    global url_data
    url_data=data
    search_data=data.split('~')
    print('Search Data :- ',search_data)
    search_uhid=search_data[0]
    search_vid=search_data[1]
    patient_details=PatientsRegistrationsAllInOne.objects.get(uhid=search_uhid)
    patient_visit_details= PatientVisitMains.objects.get(Q(uhid=search_uhid) & Q(visit_id=search_vid))
    # admission_info= PatientVisitMains.objects.get(Q(uhid=search_uhid) & Q(visit_id=search_vid))
    uhid=search_uhid
    visit_id=search_vid
    patient_name=patient_details.title+' '+patient_details.first_name+' '+patient_details.last_name
    dob=patient_details.dob
    patient_byear=dob.year
    gender=patient_details.gender
    current_year=date.today().year
    years_old=current_year-patient_byear
    records = VitalSign.objects.filter(Q(uhid=search_uhid) & Q(visit_id=search_vid))
    allergies = PatientAllergy.objects.filter(Q(uhid=search_uhid) & Q(visit_id=search_vid))
    emr_records1 = EmrInfo.objects.filter(Q(uhid=search_uhid)).prefetch_related('emrinfo_record')
    # admission_info=AdmissionInfos.objects.filter(Q(uhid=search_uhid))
    form = VitalSignForm()
    allergy_form = PatientAllergyForm()
    triage_info_form= TriageInfoForm()
    emr_info_records_form = EmrInfoRecordForm()
    emr_info_form = EmrInfoForm()
    if request.method == 'POST':
        if request.POST.get('vital_sign') =='vital':
            form = VitalSignForm(request.POST)
            finding_bill_id=OpdBillingMain.objects.filter(Q(uhid=uhid)&Q(visit_no=visit_id))
            for data in finding_bill_id:
                bill_id=data.bill_id
            request.session['bill_id'] = bill_id
            if form.is_valid():
                uhid = uhid
                bill_id = bill_id
                visit_id =visit_id
                sys_bp = request.POST.get('sys_bp')
                dia_bp = request.POST.get('dia_bp')
                temp = request.POST.get('temp')
                weight = request.POST.get('weight')
                height = request.POST.get('height')
                bmi = request.POST.get('bmi')
                resp_rate =  request.POST.get('resp_rate')
                heart_rate =  request.POST.get('heart_rate')
                urine_output = request.POST.get('urine_output')
                blood_sugar_r = request.POST.get('blood_sugar_r')
                blood_sugar_f = request.POST.get('blood_sugar_f')
                spo2 = request.POST.get('spo2')
                avpu = request.POST.get('avpu')
                trauma = request.POST.get('trauma')
                mobility = request.POST.get('mobility')
                oxygen_supplementation = request.POST.get('oxygen_supplementation')
                comments = request.POST.get('comments')
                gcs = request.POST.get('gcs')
                print(f'blood_sugar_f : - {blood_sugar_f}')
                print('This form form validation')
                # Saving Process in DB
                vital_sign=VitalSign(
                    uhid=uhid,bill_id=bill_id,visit_id=visit_id,
                    sys_bp=sys_bp,dia_bp=dia_bp,temp=temp,weight=weight,height=height,bmi=bmi,resp_rate=resp_rate,
                    heart_rate=heart_rate,urine_output=urine_output,blood_sugar_r=blood_sugar_r,
                    blood_sugar_f=blood_sugar_f,spo2=spo2,avpu=avpu,trauma=trauma,mobility=mobility,
                    oxygen_supplementation=oxygen_supplementation,comments=comments,created_by_id=request.user.id,location_id=request.location,
                    gcs = gcs,
                )
                vital_sign.save()
                print('url data',url_data)
                return HttpResponseRedirect(f'/cm/{url_data}')
            else:
                print('INVALID FORM')
        elif request.POST.get('allergy') =='allergy':
            form_allergy = PatientAllergyForm(request.POST)
            finding_bill_id = OpdBillingMain.objects.filter(Q(uhid=uhid) & Q(visit_no=visit_id))
            for data in finding_bill_id:
                bill_id = data.bill_id
            if form_allergy.is_valid():
                uhid = uhid
                bill_id = bill_id
                visit_id = visit_id
                type = request.POST.get('type')
                allergen = request.POST.get('allergen')
                reaction = request.POST.get('reaction')
                # Saving Process in DB
                patient_allergy = PatientAllergy(
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id, type=type, allergen=allergen, reaction=reaction,
                )
                patient_allergy.save()
                return HttpResponseRedirect(f'/cm/{url_data}')
            else:
                print('INVALID FORM for allergy')
        elif request.POST.get('triage') =='triage':
            triage_info_form = TriageInfoForm(request.POST)
            triage_info_form_save = triage_info_form.save(commit=False)
            triage_info_form_save.uhid = uhid
            triage_info_form_save.visit_id = visit_id
            triage_info_form_save.patient_name = patient_name
            triage_info_form_save.save()
            messages.success(request, 'Triage Info Saved Successfully')
        elif request.POST.get('print_pdf') =='print_pdf':
            from django.http import HttpResponse
            from django.template.loader import render_to_string
            triage_info= TriageInfo.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)).first()
            context={
                'triage_info': triage_info,
                'emr_records': emr_records1,
            }
            return render(request, 'nurse_station/triage_pdf.html', context)
            # html = render_to_string('nurse_station/triage_pdf.html',{'triage_info': triage_info})
            # response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'filename="triage_info.pdf"'
            # weasyprint.HTML(string=html).write_pdf(response,stylesheets=[
            #     weasyprint.CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")
            #         ])
            # return response
        elif request.POST.get('emr_record_id') =='emr_record_id':
            emr_info_records_form = EmrInfoRecordForm(request.POST,request.FILES)
            emr_info_form = EmrInfoForm(request.POST)
            files = request.FILES.getlist('medical_record_file')
            # save emr info data
            if request.POST.get('record_type') == 'OPD':
                if not EmrInfo.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)).exists():
                    emr_info= EmrInfo(
                        uhid=uhid,visit_id=visit_id,patient_name=patient_name,record_type=request.POST.get('record_type'),
                        visit_date=patient_visit_details.visit_date_time,age=years_old,gender=gender
                    )
                    emr_info.save()
                    # save emr record data last pk
                    emr_info_id = EmrInfo.objects.latest('id')

                    # save the emr record file
                    if emr_info_records_form.is_valid():
                        for f in files:
                            emr_info_records = EmrInfoRecord(
                                emrinfo=emr_info_id,medical_record_file=f,medical_record_type=request.POST.get('medical_record_type'),
                            )
                            emr_info_records.save()
                    messages.success(request, 'EMR Info Saved Successfully')
                else:
                    # get the pk of emr info
                    emr_info_id = EmrInfo.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)).first()
                    if emr_info_records_form.is_valid():
                        for f in files:
                            emr_info_records = EmrInfoRecord(
                                emrinfo=emr_info_id,medical_record_file=f,medical_record_type=request.POST.get('medical_record_type'),
                            )
                            emr_info_records.save()
                    messages.success(request, 'EMR Info Saved Successfully')
            else:
                # the record is IPD
                admission_id = request.POST.get('admission_id')
                if not EmrInfo.objects.filter(Q(uhid=uhid) & Q(visit_id=admission_id)).exists():
                    emr_info = EmrInfo(
                        uhid=uhid, visit_id=admission_id, patient_name=patient_name,
                        record_type=request.POST.get('record_type'),
                        visit_date=patient_visit_details.visit_date_time, age=years_old, gender=gender
                    )
                    emr_info.save()
                    # save emr record data last pk
                    emr_info_id = EmrInfo.objects.latest('id')

                    # save the emr record file
                    if emr_info_records_form.is_valid():
                        for f in files:
                            emr_info_records = EmrInfoRecord(
                                emrinfo=emr_info_id, medical_record_file=f,
                                medical_record_type=request.POST.get('medical_record_type'),
                            )
                            emr_info_records.save()
                    messages.success(request, 'EMR Info Saved Successfully')
                else:
                    # get the pk of emr info
                    emr_info_id = EmrInfo.objects.filter(Q(uhid=uhid) & Q(visit_id=admission_id)).first()
                    if emr_info_records_form.is_valid():
                        for f in files:
                            emr_info_records = EmrInfoRecord(
                                emrinfo=emr_info_id, medical_record_file=f,
                                medical_record_type=request.POST.get('medical_record_type'),
                            )
                            emr_info_records.save()
                    messages.success(request, 'EMR Info Saved Successfully')
        else:
            print('No Form')
    request.session['uhid']=uhid
    request.session['vid']=visit_id
    request.session['patient_name']=patient_name
    request.session['dob']=years_old
    request.session['gender']=gender
    context = {
        'form': form, 'records': records,'uhid':uhid,'patient_name':patient_name,'emr_info_records_form' :emr_info_records_form,'emr_records':emr_records1,
        'dob':years_old,'gender':gender,'allergy_form':allergy_form,'allergies':allergies,'triage_info_form':triage_info_form,'emr_info_form':emr_info_form,
    }
    return render(request,'nurse_station/kennedy/patient_visit.html',context)


def emr_records(request):
    # api for getting emr info
    if request.method == 'GET':
        uhid = request.GET.get('uhid', None)
        record_type = request.GET.get('record_type', None)
        emr_info_records= EmrInfo.objects.filter(Q(uhid=uhid) & Q(record_type=record_type)).prefetch_related('emrinfo_record')
        serializer = EmrInfoSerializer(emr_info_records, many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)


def emr_records_uhid(request):
    if request.method == 'GET':
        # uhids = EmrInfo.objects.values_list('uhid', flat=True).distinct()
        uhids = EmrInfo.objects.values('uhid').distinct()
        serializer = EmrInfoRecordsUhidSerializer(uhids, many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def emr_records_type(request):
    if request.method == 'GET':
        records_type = EmrInfo.objects.values('medical_record_type').distinct()
        serializer = EmrInfoRecordsTypeSerializer(records_type, many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)
# =====================Clinical Management=============================

@login_required(login_url='/user_login')
def patient_visit(request):
    print('This is patient Visit')
    records=VitalSign.objects.all()
    form=VitalSignForm()
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/patient_visit')
    context={
        'form':form,'records':records,
    }
    return render(request,'nurse_station/patient_visit.html',context)
@login_required(login_url='/user_login')
def nurse_login(request):
    return render(request,'nurse_station/nurse_login.html')
@login_required(login_url='/user_login')
def diagnosis_master(request):
    records=DiagnosisMaster.objects.all()
    form=DiagnosisMasterForm()
    if request.method=='POST':
        form=DiagnosisMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/diagnosis_master')
    context={
        'form':form,'records':records,
    }
    return render(request,'general_master/diagnosis_master.html',context)

def consultant_tab_cancel(request,pk):
    aa = pk.split("~")
    print(aa)
    records = PreMedicine.objects.get(id=aa[0])
    records.delete()
    return redirect(f"/nursing_assessment/{aa[1]}~{aa[2]}~{aa[3]}")

def investigation_cancel(request,pk):
    aa = pk.split("~")
    records = InvestigationProcedure.objects.get(id=aa[0])
    records.delete()
    return redirect(f"/nursing_assessment/{aa[1]}~{aa[2]}~{aa[3]}")

#========================== Kennedy code 13/03/2023 =====================================
@login_required(login_url='/user_login')
#========================== Kennedy code 13/03/2023 =====================================
def nursing_assessment(request,data):
    from django.shortcuts import get_object_or_404
    Active='nurse_assessment'
    primary_key = data
    search_data=data.split('~')
    search_uhid=search_data[0]
    search_vid=search_data[1]
    search_bill_id=search_data[2]
    diagnosis_form = DiagnosisForm()
    uhid = search_uhid
    visit_id = search_vid
    bill_id = search_bill_id
    medical_list=Inventory_ItemMaster.objects.filter(assets='0').order_by('item_name')
    patient_details = PatientsRegistrationsAllInOne.objects.get(uhid=search_uhid)
    patient_name = patient_details.first_name+' '+patient_details.last_name
    dob = patient_details.age
    gender = patient_details.gender

    #======= for investigation and procedure ============================
    billing_g=patient_details.billing_group
    tariff=BillingGroupTariffLink.objects.filter(Billing_Group_Name=billing_g).last()
    tariff_name=tariff.Tariff
    service_cat=ServiceCategory.objects.filter(service_category__in=['Investigation','TBD','Service category'])
    service_lt = ServiceMaster.objects.filter(service_category__in=service_cat)
    serv_list=[data.id for data in service_lt]
    service_list = ServiceChargeMaster.objects.filter(service_id__in=serv_list, tariff_id=tariff_name)
    profile_list = ProfileChargeMaster.objects.filter(tariff_id=tariff_name)
    package_list=PackageChargeMaster.objects.filter(tariff_id=tariff_name)
    #================================ END =====================================

    # get initial data for nursing operations
    present_complains = PresentingComplaintTemp.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    present_sub = PresentingComplaintSub.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    examination_diagnosis = HistoryAndExamination.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    history_diagnosis = History.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    diagnosis = DiagnosisTemp.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    diagnosis_sub = DiagnosisSub.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    advice = Advice.objects.filter(uhid=uhid,visit_id=visit_id,bill_id=bill_id)
    recordsss = PreMedicine.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    vital_records = VitalSign.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    pre_medicine = PreMedicine.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id)).values()
    if pre_medicine:
        pre_medicine = pre_medicine[0]
    else:
        pre_medicine = {}
    # advice = Advice.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id))
    srevice_name = ''
    charge = ''
    category = ''
    sub_category = ''
    pm_form = PrescriptionMedicineForm()
    history_diagnosis_form = HistoryAndExaminationForm()
    if request.method == 'POST':
        diagnosis_main_b = request.POST.get('diagnosis_main_b')
        diagno = request.POST.get('diagno')
        His_and_exam = request.POST.get('His_and_exam')
        examination = request.POST.get('examination')
        inves_proce_Temp = request.POST.get('inves_proce_Temp')
        inves_proce = request.POST.get('inves_proce')
        presenting_complaint_temp = request.POST.get('presenting_complaint_temp')
        presenting_complaint_main = request.POST.get('presenting_complaint_main')
        advice = request.POST.get('advice')
        medical_certificate = request.POST.get('medical_certificate')
        pre_medicine_btn = request.POST.get('pre_medicine_btn')
        to_opd = request.POST.get('to_opd')
        #======================================= Data Save into Diagnosis Table 27/03/2023 =====================================
        if diagno == 'DiagnosisTemp':
            Active='diagnosis'
            print('This is dia form data ')
            diagnosiss = request.POST.get('diagnosis')
            D_GRG_Code = request.POST.get('diagnosis_id')
            data1=DiagnosisTemp(
                uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                diagnosis=diagnosiss,D_GRG_Code=D_GRG_Code,
            )
            data1.save()
            messages.success(request, 'Diagnosis Added Successfully')
            # return HttpResponseRedirect(f'/nursing_assessment/{data}')
        elif diagnosis_main_b == 'DiagnosisMain':
            Active='diagnosis'
            present_count = Diagnosis.objects.filter(
                Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).aggregate(count=Count('diagnosis'))['count']
            print('This is dia form data----------- ',present_count)
            diagnosiss_m = request.POST.getlist('diagnosis_main')
            D_GRG_Code_m = request.POST.getlist('D_GRG_Codes_main')
            present_counts = Diagnosis.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id))
            if not present_counts.exists():
                data1=Diagnosis(
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    diagnosis=present_count,D_GRG_Code=present_count,
                )
                data1.save()
                messages.success(request, 'Diagnosis Added Successfully SUB and Main table')
            main_rec = Diagnosis.objects.filter(bill_id=bill_id).first()
            for sub_data in range(len(diagnosiss_m)):
                sub_diagnosiss_m_sub=diagnosiss_m[sub_data]
                sub_D_GRG_Code_msub=D_GRG_Code_m[sub_data]
                data_sub= DiagnosisSub(
                    main_id_id=main_rec.id,
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    diagnosis=sub_diagnosiss_m_sub,D_GRG_Code=sub_D_GRG_Code_msub,
                )
                data_sub.save()
            else:
                present_counts = DiagnosisTemp.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).aggregate(count=Count('diagnosis'))['count']
                updated=Diagnosis.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).last()
                updated.diagnosis=int(updated.diagnosis)+int(present_counts)
                updated.D_GRG_Code=int(updated.D_GRG_Code)+int(present_counts)
                updated.save()
                messages.success(request, 'Data Update Successfully')
            DiagnosisTemp.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).delete()
            # return HttpResponseRedirect(f'/nursing_assessment/{data}')
        elif His_and_exam == 'HistoryAndExamination':
            Active='history_exam'

            history_exists = History.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id)).exists()
            if not history_exists:
                data1 = History(
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    Past_Medical_Surgical= request.POST.get("past_medical"),
                    Family_History= request.POST.get("Family_History"),
                    Paediatric_History= request.POST.get("Paediatric_History"),
                    Gynaec_Obstetric_History= request.POST.get("Gynaec_Obstetric_History"),
                    socioeconomic_history =  request.POST.get("Socioeconomic_Examination"),
                )
                data1.save()
                messages.success(request, 'Data Saved Successfully')
                # return HttpResponseRedirect(f'/nursing_assessment/{data}')
            else:
                messages.warning(request, 'Data Already Exists')

        elif examination == 'HistoryAndExamination1':
            Active='history_exam1'
            history_exists = HistoryAndExamination.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id)).exists()
            if not history_exists:
                data1 = HistoryAndExamination(
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    general_examination=request.POST.get("general_examination"),
                    # systemetic_examination=request.POST.get("systemtic_examination"),
                    Cardiovascular=request.POST.get("Cardiovascular"),
                    Respiration=request.POST.get("Respiration"),
                    gastrointestinal_system = request.POST.get("gastrointestinal"),
                    genitourinary_system = request.POST.get("genitourinary"),
                    Musculoskeletal=request.POST.get("masculoskeletal"),
                    integumentary = request.POST.get("integumentary"),
                    central_nervous_system = request.POST.get("central_nervous_system"),
                    ENT = request.POST.get("ENT"),
                )
                data1.save()
                messages.success(request, 'Data Saved Successfully')
                # return HttpResponseRedirect(f'/nursing_assessment/{data}')
            else:
                messages.warning(request, 'Data Already Exists')

        elif inves_proce == 'InvestigationAndProcedure':
            Active="investigation"
            investigation_and_procedure = request.POST.get('investigation_and_procedure')
            status = request.POST.get('status')
            if status == 'on':
                status = True
            else:
                status = False
            # investigationprocedure = InvestigationProcedure.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id)).exists()
            # if not investigationprocedure:
            data1 = InvestigationProcedure(
                uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                investigation_and_procedure=investigation_and_procedure,
                status=status,
            )
            data1.save()
            messages.success(request, 'Data Saved Successfully')
        elif to_opd == 'OPD_Billing':
            Active="investigation"
            takedata=InvestigationProcedure.objects.filter(uhid=uhid, visit_id=visit_id)
            order = str(random.randint(1000, 9999))
            order_id = order
            invest_list=[data.investigation_and_procedure for data in takedata]
            investigation_list = ServiceChargeMaster.objects.filter(service_id__service_name__in=invest_list, tariff_id=tariff_name)
            for inves in takedata:
                service_record = ServiceChargeMaster.objects.filter(service_id__service_name=inves.investigation_and_procedure).last()
                profiles_record = ProfileChargeMaster.objects.filter(profile_id__profile_name__exact=inves.investigation_and_procedure).last()
                package_record = PackageChargeMaster.objects.filter(package_id__package_name__exact=inves.investigation_and_procedure).last()
                if service_record:
                    srevice_name=service_record.service_id
                    charge=service_record.service_charge
                    category=service_record.service_category.id
                    sub_category=service_record.service_sub_category.id
                elif profiles_record:
                    srevice_name=profiles_record.profile_id
                    charge=profiles_record.profile_charge
                    category=profiles_record.service_category.id
                    sub_category=profiles_record.service_sub_category.id
                elif package_record:
                    srevice_name=package_record.package_id
                    charge=package_record.package_charge
                    category=package_record.ward_type.id
                    sub_category=package_record.ward_category.id
                check_duplicate=OpdBillingTemper.objects.filter(uhid=uhid, visit_no=visit_id,service_name=srevice_name)
                if not check_duplicate.exists():
                    OpdBillingTemper.objects.create(
                        uhid=uhid,
                        visit_no=visit_id,
                        order_id=order_id,
                        service_name=srevice_name,
                        rate=charge,
                        net_ammount=charge,
                        outstanding_amount='0',
                        receive_amount=charge,
                        discount='0',
                        total_amount=charge,
                        unit='1',
                        service_category_id=category,
                        service_sub_category_id=sub_category,
                    )
                    #  lab module
                    get_uhid_data = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
                    if get_uhid_data.billing_group != '1':
                        ind_uhid=uhid
                        ind_visit_id=visit_id
                        ind_service_name = srevice_name
                        profile_record=ProfileService.objects.all()
                        profile_name_list=[data.profile_name for data in profile_record]
                        pen_inv=PendingInvestigation_main.objects.filter(uhid=ind_uhid,visit_no=ind_visit_id).last()
                        if pen_inv:
                            PTID=pen_inv.PTID
                        else:
                            PID = str(random.randint(100000, 999999))
                            PTID = 'PTID' + PID
                        te_id = str(random.randint(100000, 999999))
                        test_id = 'TST' + te_id
                        bill_no=order_id

                        if ind_service_name in profile_name_list:
                            profile_pac_record = ProfileService.objects.filter(profile_name=ind_service_name).first()
                            pending_inv = PendingInvestigation_main(
                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                profile_id='', profile_name=ind_service_name, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                sub_department=profile_pac_record.service_sub_department
                            )
                            pending_inv.save()

                            profile_rec_filter=ProfileService.objects.filter(profile_name=ind_service_name)
                            for data in profile_rec_filter:
                                print('age',get_uhid_data.age)
                                if data.service_name == 'Age':
                                    rangee=get_uhid_data.age
                                elif get_uhid_data.gender == 'Male':
                                    rangee=data.male_range
                                elif get_uhid_data.gender == 'Female':
                                    rangee=data.female_range
                                else:
                                    rangee=data.male_range
                                pending_inv_sub=LabResultEntry(
                                    test_id=test_id,profile_id='',profile_name=ind_service_name,service_name=data.service_name,
                                    range=rangee,units=data.units,created_by_id=request.user.id,location_id=request.location,
                                    outsource=data.outsource,
                                )
                                pending_inv_sub.save()
                        else:
                            lab_record=ServiceMaster.objects.filter(service_name=ind_service_name,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')
                            serivce_test=Service_Test.objects.filter(test_name__service_name__contains=ind_service_name).first()
                            opd_package=OpdPackageService.objects.filter(package_name__package_name__contains=ind_service_name)
                            if opd_package:

                                for data in opd_package:
                                    te_id = str(random.randint(100000, 999999))
                                    test_id = 'TST' + te_id
                                    if data.service_name:
                                        lab_records=ServiceMaster.objects.filter(service_name=data.service_name,service_category__service_category__contains='investigation',service_sub_category__service_sub_category__contains='lab investigation')

                                        if lab_records:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=lab_records.last().service_name, date_time=datetime.now(),
                                                department=lab_records.last().service_department,outsource=lab_records.last().outsource,
                                                sub_department=lab_records.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                            )
                                            pending_inv.save()
                                            pending_inv_sub = LabResultEntry(
                                                test_id=test_id, profile_id='', profile_name=lab_records.last().service_name, service_name=lab_records.last().service_name,
                                                units=' ',created_by_id=request.user.id,location_id=request.location,outsource=lab_records.last().outsource,
                                            )
                                            pending_inv_sub.save()
                                    elif data.profile_name:
                                        profile_pac_record = ProfileService.objects.filter(profile_name=data.profile_name.profile_name).last()
                                        if profile_pac_record:
                                            pending_inv = PendingInvestigation_main(
                                                test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                                profile_id='', profile_name=profile_pac_record.profile_name, date_time=datetime.now(),created_by_id=request.user.id,location_id=request.location,
                                                department=profile_pac_record.service_department,outsource=profile_pac_record.outsource,
                                                sub_department=profile_pac_record.service_sub_department
                                            )
                                            pending_inv.save()

                                            profile_rec_filter=ProfileService.objects.filter(profile_name=profile_pac_record.profile_name)
                                            for data in profile_rec_filter:
                                                if data.service_name == 'Age':
                                                    rangee=get_uhid_data.age
                                                elif get_uhid_data.gender == 'Male':
                                                    rangee=data.male_range
                                                elif get_uhid_data.gender == 'Female':
                                                    rangee=data.female_range
                                                else:
                                                    rangee=data.male_range
                                                pending_inv_sub=LabResultEntry(
                                                    test_id=test_id,profile_id='',profile_name=profile_pac_record.profile_name,service_name=data.service_name,
                                                    range=rangee,units=data.units,created_by_id=request.user.id,location_id=request.location,
                                                    outsource=data.outsource,
                                                )
                                                pending_inv_sub.save()
                            elif lab_record:
                                pending_inv = PendingInvestigation_main(
                                    test_id=test_id, uhid=ind_uhid, visit_no=ind_visit_id, bill_no=bill_no, PTID=PTID,
                                    profile_id='', profile_name=ind_service_name, date_time=datetime.now(),
                                    department=lab_record.last().service_department,outsource=lab_record.last().outsource,
                                    sub_department=lab_record.last().ServiceSubDepartment,created_by_id=request.user.id,location_id=request.location,
                                )
                                pending_inv.save()
                                pending_inv_sub = LabResultEntry(
                                    test_id=test_id, profile_id='', profile_name=ind_service_name, service_name=lab_record.last().service_name,
                                    units='',created_by_id=request.user.id,location_id=request.location,outsource=lab_record.last().outsource,
                                )
                                pending_inv_sub.save()
                    messages.success(request, 'Data Saved Successfully')
                else:
                    messages.warning(request, 'Data All Ready There')
            update_status=PatientVisitMains.objects.filter(uhid=uhid, visit_id=visit_id).last()
            update_status.status='open'
            update_status.save()
            update_patient_status = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid).last()
            update_patient_status.update_status = timezone.localtime(timezone.now())
            update_patient_status.save()
            messages.success(request, 'Data Saved Successfully')
            # return HttpResponseRedirect(f'/nursing_assessment/{data}')

        elif advice == 'Advices':
            Active='Advices'
            advice = request.POST.get('advice')
            follow_up_date = request.POST.get('follow_up_date')
            refer_to_emergency = request.POST.get('refer_to_emergency')
            refer_to_admission = request.POST.get('refer_to_admission')
            visit_complete = request.POST.get('visit_complete')
            refer_to_mental_health = request.POST.get('refer_to_mental_health')
            # print(f'{advice},{follow_up_date},{refer_to_emergency},{refer_to_mental_health}')
            try:
                data1 = Advice.objects.create(
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    advice=advice,
                    follow_up_date=follow_up_date,
                    follow_check_box=str(refer_to_emergency) + str(refer_to_admission) + str(visit_complete) + str(
                        refer_to_mental_health)
                )
                messages.success(request, 'Data Saved Successfully')
            except:
                messages.warning(request, 'Data already Saved')
        #======================= PresentingComplaintTemp Table save data ===================================
        elif presenting_complaint_temp == 'PresentingComplaintTemp':
            Active='presenting_com'
            presenting_comp = request.POST.get('presenting_comp')
            initial_comp = request.POST.get('initial_comp')
            data1 = PresentingComplaintTemp(
                uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                presenting_comp=presenting_comp,
                initial_comp=initial_comp,
            )
            data1.save()
            messages.success(request, 'Data Saved Successfully')
            # messages.error(request, 'Data Already Exists')
        #========================= PresentingComplaint Table save data ===================================
        elif presenting_complaint_main == 'PresentingComplaintMain':
            Active='presenting_com'
            present_count = PresentingComplaintTemp.objects.filter(
                Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).aggregate(count=Count('initial_comp'))['count']

            # count = Person.objects.filter(age__gte=18).aggregate(count=Count('id'))['count']
            presenting_comp_sub = request.POST.getlist('presenting_comp_sub')
            initial_comp_sub = request.POST.getlist('initial_comp_sub')
            present_counts = PresentingComplaint.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id))
            if not present_counts.exists():
                data1= PresentingComplaint(
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    presenting_comp=present_count,
                    initial_comp=present_count,
                )
                data1.save()
                messages.success(request, 'Data Saved Successfully')
            main_rec=PresentingComplaint.objects.filter(bill_id=bill_id).first()
            for sub_data in range(len(presenting_comp_sub)):
                sub_presenting_comp_sub=presenting_comp_sub[sub_data]
                sub_initial_comp_sub_sub=initial_comp_sub[sub_data]
                data_sub= PresentingComplaintSub(
                    main_id_id=main_rec.id,
                    uhid=uhid, bill_id=bill_id, visit_id=visit_id,
                    presenting_comp=sub_presenting_comp_sub,
                    initial_comp=sub_initial_comp_sub_sub,
                )
                data_sub.save()
            else:
                present_counts = PresentingComplaintTemp.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).aggregate(count=Count('presenting_comp'))['count']
                updated=PresentingComplaint.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).first()
                updated.presenting_comp=int(updated.presenting_comp)+int(present_counts)
                updated.initial_comp=int(updated.initial_comp)+int(present_counts)
                updated.save()
                messages.success(request, 'Data Update Successfully')
            PresentingComplaintTemp.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id) & Q(bill_id=bill_id)).delete()
            # return HttpResponseRedirect(f'/nursing_assessment/{data}')
        # ================================== END Presenting Complaint ==============================================
        #================================
        elif medical_certificate == 'MedicalCertificate':
            Active='MedicalCertificate'
            template = request.POST.get('template')
            authorize_dr = request.POST.get('authorize_dr')
            finalized = request.POST.get('finalized')
            if finalized == 'on':
                finalized = True
            else:
                finalized = False
            data1 = MedicalCertificates(
                mc_templates=template,
                authorize_dr=authorize_dr,
                finalized=finalized,
            )
            data1.save()
            messages.success(request, 'Data Saved Successfully')
            # return HttpResponseRedirect(f'/nursing_assessment/{data}')
        elif pre_medicine_btn == 'Prescription_medicine':
            medical_list=Inventory_ItemMaster.objects.filter(assets='0').order_by('item_name')
            pm_form = PrescriptionMedicineForm(request.POST)
            medical_listt=request.POST.get('medicine')
            Active='pre_medication'
            if pm_form.is_valid():
                pre_form = pm_form.save(commit=False)
                # check if uhid exist
                # uhidaa = PreMedicine.objects.filter(Q(uhid=uhid) & Q(visit_id=visit_id)& Q(bill_id=bill_id)).exists()
                # if not uhidaa:
                pre_form.uhid = uhid
                pre_form.visit_id = visit_id
                pre_form.bill_id = bill_id
                pre_form.medicine_id = medical_listt
                pre_form.created_by_id = request.user.id
                pre_form.location_id = request.location
                pre_form.save()
                update_status = PatientVisitMains.objects.filter(uhid=uhid, visit_id=visit_id).last()
                update_status.status = 'open'
                update_status.save()
                update_patient_status = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid).last()
                import datetime
                update_patient_status.update_status = datetime.datetime.now()
                update_patient_status.save()
                messages.success(request,'Prescription Medicine Added Successfully')
                # return HttpResponseRedirect(f'/nursing_assessment/{data}')
                # print('data saved in table')
                # else:
                #     messages.error(request, 'Prescription Medicine Already Added')
                #     print('data not save in table ')
            else:
                print(pm_form.errors)
                messages.warning(request, 'Invalid form, Prescription Medicine Not Added')
                # return HttpResponseRedirect(f'/nursing_assessment/{data}')
        elif request.POST.get('prescription_report') == 'report':
            from django.conf import settings
            from django.http import HttpResponse
            from django.template.loader import render_to_string
            import weasyprint

            vitals = VitalSign.objects.filter(uhid=uhid, visit_id=visit_id).first()
            patient_allergy = PatientAllergy.objects.filter(uhid=uhid, visit_id=visit_id).first()
            triage_info = TriageInfo.objects.filter(uhid=uhid, visit_id=visit_id).first()
            complaints = PresentingComplaint.objects.filter(uhid=uhid, visit_id=visit_id).first()

            context = {
                'vitals': vitals,
                'patient_allergy': patient_allergy,
                'triage_info': triage_info,
                'complaints': complaints,
                'patient_name': patient_name,
                'uhid': uhid,
                'visit_id': visit_id,
            }

            # order = get_object_or_404(Order, id=order_id)
            html = render_to_string('pdf/prescription.html', context=context)
            print('html,',html)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'filename=patient.pdf'
            weasyprint.HTML(string=html).write_pdf(response,
                                                   stylesheets=[
                                                       weasyprint.CSS(settings.STATIC_ROOT / 'css/bootstrap.css')])
            return response

    records = PreMedicine.objects.filter(uhid=uhid, visit_id=visit_id,)
    diagnosis_records = Diagnosis.objects.filter(uhid=uhid, visit_id=visit_id,)
    invest_and_proce_records = InvestigationProcedure.objects.filter(uhid=uhid, visit_id=visit_id,)
    context = {
        'pm_form': pm_form, 'records': records, 'diagnosis_form': diagnosis_form,'medical_list':medical_list,'service_list':service_list,
        'diagnosis_records': diagnosis_records, 'invest_and_proce_records': invest_and_proce_records,'present_sub':present_sub,
        'uhid': uhid, 'patient_name': patient_name, 'dob': dob, 'gender': gender,'recordsss':recordsss,'diagnosis_sub':diagnosis_sub,
        'present_complains': present_complains, 'examination_diagnosis': examination_diagnosis, 'diagnosis': diagnosis,
        'pre_medicine': pre_medicine, 'advice': advice, 'history_diagnosis_form': history_diagnosis_form,'history_diagnosis':history_diagnosis,'vital_records':vital_records,'Active':Active,
        'profile_list':profile_list,'package_list':package_list,"primary_key":primary_key
    }
    return render(request, 'nurse_station/kennedy/nursing_assessment.html', context)

def emergency(request):
    return render(request,'nurse_station/emergency.html')
def in_patient_management(request):
    return render(request,'nurse_station/in_patient_management.html')
def procedure_room(request):
    return render(request,'nurse_station/procedure_room.html')
def system_control(request):
    return render(request,'nurse_station/system_control.html')

@login_required(login_url='/user_login')
def billing_group_corporate(request):
    form=BillingGroupCorporateForm1()
    records=BillingGroupCorporateMaster.objects.all()
    if request.method=='POST':
        form = BillingGroupCorporateForm1(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/billing_group_corporate')
    context={
        'form':form,'records':records
    }
    return render(request,'general_master/billing_group_corporate.html',context)

@login_required(login_url='/user_login')
def ward_category(request):
    form=WardCategoryForm()
    records=WardCategory.objects.all()
    ward_category='ward_category'
    if request.method=='POST':
        form=WardCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ward_category')
    context={
    'form':form,'ward_category':ward_category,'records':records,
    }
    return render(request,'general_master/ward_category.html',context)

@login_required(login_url='/user_login')
def edit_wardcategory(request):
    records=WardCategory.objects.all()
    context={
    'ward_category':ward_category,'records':records,
    }
    return render(request,'general_master/edit_wardcategory.html',context)

@login_required(login_url='/user_login')
def editing_wardcategory(request,pk):
    records=WardCategory.objects.get(id=pk)
    form=WardCategoryForm()
    ward_category='ward_category'
    if request.method=='POST':
        form=WardCategoryForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ward_category')
    context={
    'ward_category':ward_category,'records':records,'form':form,
    }

    return render(request,'general_master/editing_wardcategory.html',context)


@login_required(login_url='/user_login')
def intelligence_search(request):
    return render(request,'testapp/error.html')


#=================================IPD and Pharmacy==========================
# Pharmacy


@login_required(login_url='/user_login')
def issue_inbox(request):
    form=IssueInboxForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/issue_inbox.html',context)
def challan_bill(request):
    form=ChallanBillForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/challan_bill.html',context)
def stock_entry(request):
    form=StockEntryForm()
    context={
        'form':form,
    }

    return render(request,'pharmacy/stock_entry.html',context)
# 21-04-22
def item_detail(request):
    form=ItemDetailForm()
    context={
        'form':form,
    }

    return render(request,'pharmacy/item_detail.html',context)

def sba(request):
    form=SoaForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/sba.html',context)

def vendors_name(request):
    form=VendorForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/vendors_name.html',context)

def po(request):
    form=PoForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/po.html',context)
def gatepass(request):
    form=GatePassForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/gatepass.html',context)
def details_of_receiver(request):
    form=DetailsOfReceiverForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/details_of_receiver.html',context)
def due_bill(request):
    form=DueBillForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/due_bill.html',context)
def indent_detail(request):
    form=IndentDetailForm()
    context={
        'form':form,
    }
    return render(request,'pharmacy/indent_detail.html',context)
    # IPD
#============================Inventry Screen Start==========================
# def item_category_master(request):
#     form = ItemCategoryMasterForm()
#     item_category_master = ItemCategoryMaster.objects.all()
#     if request.method == 'POST':
#         form = ItemCategoryMasterForm(request.POST)
#         if form.is_valid():
#             form.save()
#     return render(request, 'inventory_master/item_category_master.html',
#                   {'form': form, 'item_category_master': item_category_master})


# Item Category master

@login_required(login_url='/user_login')
def item_category_master(request):
    form = ItemCategoryMasterForm()
    item_category_master = ItemCategoryMaster.objects.all()
    if request.method == 'POST':
        form = ItemCategoryMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/item_category_master.html',
                  {'form': form, 'item_category_master': item_category_master})



@login_required(login_url='/user_login')
def edit_item_category_master(request):
    form = ItemCategoryMasterForm()
    item_category_master = ItemCategoryMaster.objects.all()
    if request.method == 'POST':
        form = ItemCategoryMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_item_category_master.html',
                  {'form': form, 'item_category_master': item_category_master})



@login_required(login_url='/user_login')
def editing_item_category_master(request, id):
    item_category_master = ItemCategoryMaster.objects.get(id=id)
    form = ItemCategoryMasterForm(instance=item_category_master)
    if request.method == 'POST':
        form = ItemCategoryMasterForm(request.POST, instance=item_category_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_item_category_master')
    return render(request, 'inventory_master/editing_item_category_master.html',
                  {'form': form, 'item_category_master': item_category_master})



@login_required(login_url='/user_login')
def deleting_item_category_master(request, id):
    item_category_master = ItemCategoryMaster.objects.get(id=id)
    item_category_master.delete()
    return HttpResponseRedirect('/item_category_master')


# Ends Item Category Master
# Item Belongs To Master
# Item Category master

@login_required(login_url='/user_login')
def belongs_to_master(request):
    form = ItemBelongsToMasterForm()
    belongs_to_master = ItemBelongsToMaster.objects.all()
    if request.method == 'POST':
        form = ItemBelongsToMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/belongs_to_master.html',
                  {'form': form, 'belongs_to_master': belongs_to_master})



@login_required(login_url='/user_login')
def edit_belongs_to_master(request):
    form = ItemBelongsToMasterForm()
    belongs_to_master = ItemBelongsToMaster.objects.all()
    if request.method == 'POST':
        form = ItemBelongsToMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_belongs_to_master.html',
                  {'form': form, 'belongs_to_master': belongs_to_master})



@login_required(login_url='/user_login')
def editing_belongs_to_master(request, id):
    belongs_to_master = ItemBelongsToMaster.objects.get(id=id)
    form = ItemBelongsToMasterForm(instance=belongs_to_master)
    if request.method == 'POST':
        form = ItemBelongsToMasterForm(request.POST, instance=belongs_to_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_belongs_to_master')
    return render(request, 'inventory_master/editing_belongs_to_master.html',
                  {'form': form, 'belongs_to_master': belongs_to_master})



@login_required(login_url='/user_login')
def deleting_belongs_to_master(request, id):
    belongs_to_master = ItemBelongsToMaster.objects.get(id=id)
    belongs_to_master.delete()
    return HttpResponseRedirect('/belongs_to_master')


# Packaging Master Start

@login_required(login_url='/user_login')
def packaging_master(request):
    form = PackagigMasterForm()
    packaging_master = PackagigMaster.objects.all()
    if request.method == 'POST':
        form = PackagigMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/packaging_master')
    return render(request, 'inventory_master/packaging_master.html',
                  {'form': form, 'packaging_master': packaging_master})



@login_required(login_url='/user_login')
def edit_packaging_master(request):
    form = PackagigMasterForm()
    packaging_master = PackagigMaster.objects.all()
    if request.method == 'POST':
        form = PackagigMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_packaging_master.html',
                  {'form': form, 'packaging_master': packaging_master})



@login_required(login_url='/user_login')
def editing_packaging_master(request, id):
    packaging_master = PackagigMaster.objects.get(id=id)
    form = PackagigMasterForm(instance=packaging_master)
    if request.method == 'POST':
        form = PackagigMasterForm(request.POST, instance=packaging_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_packaging_master')
    return render(request, 'inventory_master/editing_packaging_master.html',
                  {'form': form, 'packaging_master': packaging_master})



@login_required(login_url='/user_login')
def deleting_packaging_master(request, id):
    packaging_master = PackagigMaster.objects.get(id=id)
    packaging_master.delete()
    return HttpResponseRedirect('/packaging_master')


# Ends Packaging Master
# Start Item Unit Master

@login_required(login_url='/user_login')
def item_unit_master(request):
    form = ItemUnitMasterForm()
    item_unit_master = ItemUnitMaster.objects.all()
    if request.method == 'POST':
        form = ItemUnitMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/item_unit_master')
    return render(request, 'inventory_master/item_unit_master.html',
                  {'form': form, 'item_unit_master': item_unit_master})



@login_required(login_url='/user_login')
def edit_item_unit_master(request):
    form = ItemUnitMasterForm()
    item_unit_master = ItemUnitMaster.objects.all()
    if request.method == 'POST':
        form = ItemUnitMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_item_unit_master.html',
                  {'form': form, 'item_unit_master': item_unit_master})



@login_required(login_url='/user_login')
def editing_item_unit_master(request, id):
    item_unit_master = ItemUnitMaster.objects.get(id=id)
    form = ItemUnitMasterForm(instance=item_unit_master)
    if request.method == 'POST':
        form = ItemUnitMasterForm(request.POST, instance=item_unit_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_item_unit_master')
    return render(request, 'inventory_master/editing_item_unit_master.html',
                  {'form': form, 'item_unit_master': item_unit_master})



@login_required(login_url='/user_login')
def deleting_item_unit_master(request, id):
    item_unit_master = ItemUnitMaster.objects.get(id=id)
    item_unit_master.delete()
    return HttpResponseRedirect('/item_unit_master')

    # Ends Item Unit Master


# Start Item Manufacturer

@login_required(login_url='/user_login')
def item_manufacturer(request):
    form = ItemManufacturerForm()
    item_manufacturer = ItemManufacturer.objects.all()
    if request.method == 'POST':
        form = ItemManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/item_manufacturer')
    return render(request, 'inventory_master/item_manufacturer.html',
                  {'form': form, 'item_manufacturer': item_manufacturer})



@login_required(login_url='/user_login')
def edit_item_manufacturer(request):
    form = ItemManufacturerForm()
    item_manufacturer = ItemManufacturer.objects.all()
    if request.method == 'POST':
        form = ItemManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_item_manufacturer.html',
                  {'form': form, 'item_manufacturer': item_manufacturer})



@login_required(login_url='/user_login')
def editing_item_manufacturer(request, id):
    item_manufacturer = ItemManufacturer.objects.get(id=id)
    form = ItemManufacturerForm(instance=item_manufacturer)
    if request.method == 'POST':
        form = ItemManufacturerForm(request.POST, instance=item_manufacturer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_item_manufacturer')
    return render(request, 'inventory_master/editing_item_manufacturer.html',
                  {'form': form, 'item_manufacturer': item_manufacturer})



@login_required(login_url='/user_login')
def deleting_item_manufacturer(request, id):
    item_manufacturer = ItemManufacturer.objects.get(id=id)
    item_manufacturer.delete()
    return HttpResponseRedirect('/item_manufacturer')
    # Item Master


@login_required(login_url='/user_login')
def item_master(request):
    form = ItemMasterForm()
    item_manufact = ItemManufact.objects.all()
    supplier = ItemSupplier.objects.all()
    item_manufact_form=''
    if request.method == 'POST':
        manufacture = request.POST.get('manufacture')
        supplier = request.POST.get('supplier')
        item_master = request.POST.get('item_master')
        if manufacture == 'Manufacture':
            manufacture = request.POST.get('manufacturers')
            data = ManufactureTempTable(
                manufacture=manufacture
            )
            data.save()
            return HttpResponseRedirect('/item_master')
        elif supplier=="supplier":
            print('midle')
            item_manufact_form = ItemManufacturerForm(request.POST)
            if item_manufact_form.is_valid():
                item_manufact_form.save()
                return HttpResponseRedirect('/item_master')
        elif item_master == 'item_master':
            print('last')
            form=ItemMasterForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/item_master')
            else:
                print(form.errors)
    manu_temp = ManufactureTempTable.objects.all()
    context = {
        'form': form, 'item_manufact': item_manufact, 'manu_temp': manu_temp, 'item_manufact_form':item_manufact_form
    }
    return render(request, 'inventory_master/item_master.html', context)




@login_required(login_url='/user_login')
def edit_store_master(request):
    form = StoreMasterForm()
    store_master = StoreMaster.objects.all()
    if request.method == 'POST':
        form = StoreMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_store_master.html', {'form': form, 'store_master': store_master})



@login_required(login_url='/user_login')
def editing_store_master(request, id):
    store_master = StoreMaster.objects.get(id=id)
    form = StoreMasterForm(instance=store_master)
    if request.method == 'POST':
        form = StoreMasterForm(request.POST, instance=store_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_store_master')
    return render(request, 'inventory_master/editing_store_master.html', {'form': form, 'store_master': store_master})



@login_required(login_url='/user_login')
def deleting_store_master(request, id):
    store_master = StoreMaster.objects.get(id=id)
    store_master.delete()
    return HttpResponseRedirect('/store_master')



@login_required(login_url='/user_login')
def store_nursing_counter_mapping(request):
    form = StoreNursingCounterForm()
    store_nursing_counter_mapping = StoreNursingCounter.objects.all()
    if request.method == 'POST':
        form = StoreNursingCounterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/store_nursing_counter_mapping')
    return render(request, 'inventory_master/store_nursing_counter_mapping.html',
                  {'form': form, 'store_nursing_counter_mapping': store_nursing_counter_mapping})


@login_required(login_url='/user_login')
def edit_store_nursing_counter_mapping(request):
    form = StoreNursingCounterForm()
    store_nursing_counter_mapping = StoreNursingCounter.objects.all()
    if request.method == 'POST':
        form = StoreNursingCounterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_store_nursing_counter_mapping.html',
                  {'form': form, 'store_nursing_counter_mapping': store_nursing_counter_mapping})


@login_required(login_url='/user_login')
def editing_store_nursing_counter_mapping(request, id):
    store_nursing_counter_mapping = StoreNursingCounter.objects.get(id=id)
    form = StoreNursingCounterForm(instance=store_nursing_counter_mapping)
    if request.method == 'POST':
        form = StoreNursingCounterForm(request.POST, instance=store_nursing_counter_mapping)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_store_nursing_counter_mapping')
    return render(request, 'inventory_master/editing_store_nursing_counter_mapping.html',
                  {'form': form, 'store_nursing_counter_mapping': store_nursing_counter_mapping})


@login_required(login_url='/user_login')
def deleting_store_nursing_counter_mapping(request, id):
    store_nursing_counter_mapping = StoreNursingCounter.objects.get(id=id)
    store_nursing_counter_mapping.delete()
    return HttpResponseRedirect('/store_nursing_counter_mapping')


# End Store Nursing Counter Mapping
# Start Item Location Master
@login_required(login_url='/user_login')
def item_location_master(request):
    form = ItemLocationForm()
    item_location_master = ItemLocation.objects.all()
    if request.method == 'POST':
        form = ItemLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/item_location_master')
    return render(request, 'inventory_master/item_location_master.html',
                  {'form': form, 'item_location_master': item_location_master})


@login_required(login_url='/user_login')
def edit_item_location_master(request):
    form = ItemLocationForm()
    item_location_master = ItemLocation.objects.all()
    if request.method == 'POST':
        form = ItemLocationForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_item_location_master.html',
                  {'form': form, 'item_location_master': item_location_master})


@login_required(login_url='/user_login')
def editing_item_location_master(request, id):
    item_location_master = ItemLocation.objects.get(id=id)
    form = ItemLocationForm(instance=item_location_master)
    if request.method == 'POST':
        form = ItemLocationForm(request.POST, instance=item_location_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_item_location_master')
    return render(request, 'inventory_master/editing_item_location_master.html',
                  {'form': form, 'item_location_master': item_location_master})


@login_required(login_url='/user_login')
def deleting_item_location_master(request, id):
    item_location_master = ItemLocation.objects.get(id=id)
    item_location_master.delete()
    return HttpResponseRedirect('/item_location_master')


# Ends Item Location Master
#============================Inventry Screen End============================
def multi_row(request):
    if request.method=='POST':
        qdict=request.POST
        print('Our Dict = ', qdict)
        sample_dict = dict(qdict.lists())
        name = sample_dict.get('name[]')
        email = sample_dict.get('email[]')
        print('name= ', name)
        print('email= ', email)
        print(request.POST.get('name[]'))
        name=request.POST.get('name[]')
        email=request.POST.get('email[]')
        print(f'name {name} , email {email}')
        return HttpResponseRedirect('/multi_row')
    return render(request,'clinical/adding_multiple_data.html')

# ===================Master=====================

@login_required(login_url='/user_login')
def group_master(request):
    form=GroupMasterForm()
    if request.method=='POST':
        form=GroupMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group_master')

    return render(request,'testapp/group_master.html',{'form':form})
@login_required(login_url='/user_login')
def branch_master(request):
    form=BranchMasterForm()
    if request.method=='POST':
        form=BranchMasterForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/branch_master')
    return render(request,'testapp/branch_master.html',{'form':form})
@login_required(login_url='/user_login')
def clinical_department(request):
    form=ClinicalOrDepartmentForm()
    clinical_department=ClinicalOrDepartment.objects.all()
    if request.method=='POST':
        form=ClinicalOrDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/clinical_department')
    return render(request,'general_master/clinical_department.html',{'form':form,'clinical_department':clinical_department})

@login_required(login_url='/user_login')
def edit_clinical_department(request):
    form=ClinicalOrDepartmentForm()
    clinical_department=ClinicalOrDepartment.objects.all()
    if request.method=='POST':
        form=ClinicalOrDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'general_master/edit_clinical_department.html',{'form':form,'clinical_department':clinical_department})

@login_required(login_url='/user_login')
def editing_clinical_department(request,id):
    clinical_department=ClinicalOrDepartment.objects.get(id=id)
    form=ClinicalOrDepartmentForm(instance=clinical_department)
    if request.method=='POST':
        form=ClinicalOrDepartmentForm(request.POST,instance=clinical_department)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_clinical_department')
    return render(request,'general_master/editing_clinical_department.html',{'form':form,'clinical_department':clinical_department})

@login_required(login_url='/user_login')
def visit_type_master(request):
    form=VisitTyoeMasterForm()
    visit_type_master=VisitTyoeMaster.objects.all()
    if request.method=='POST':
        form=VisitTyoeMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'general_master/visit_type_master.html',{'form':form,'visit_type_master':visit_type_master})

@login_required(login_url='/user_login')
def edit_visit_type_master(request):
    form=VisitTyoeMasterForm()
    visit_type_master=VisitTyoeMaster.objects.all()
    if request.method=='POST':
        form=VisitTyoeMasterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'general_master/edit_visit_type_master.html',{'form':form,'visit_type_master':visit_type_master})

@login_required(login_url='/user_login')
def editing_visit_type_master(request,id):
    visit_type_master=VisitTyoeMaster.objects.get(id=id)
    form=VisitTyoeMasterForm(instance=visit_type_master)
    if request.method=='POST':
        form=VisitTyoeMasterForm(request.POST,instance=visit_type_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_visit_type_master')
    return render(request,'general_master/editing_visit_type_master.html',{'form':form,'visit_type_master':visit_type_master})

@login_required(login_url='/user_login')
def add_service_master(request):
    form=ServiceCategoryForm()
    service_category=ServiceCategory.objects.all()
    if request.method=='POST':
        form=ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/service-master')
    context={
    'form':form,'service_category':service_category
    }
    return render(request,'general_master/service_category.html',context)


@login_required(login_url='/user_login')
def add_sub_service_master(request):
    form=ServiceSubCategoryForm()
    service_sub_category='service_sub_category'
    service_subb_category1=ServiceSubCategory.objects.all()
    if request.method=='POST':
        form=ServiceSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_sub_service_master')
    context={
    'form':form,'service_sub_category':service_sub_category,'service_subb_category1':service_subb_category1
    }
    return render(request,'general_master/sub_service_category.html',context)

@login_required(login_url='/user_login')
def edit_add_sub_service_master(request):
    form=ServiceSubCategoryForm()
    service_sub_category='service_sub_category'
    service_subb_category1=ServiceSubCategory.objects.all()
    if request.method=='POST':
        form=ServiceSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_sub_service_master')
    context={
    'form':form,'service_category':service_sub_category,'service_subb_category1':service_subb_category1
    }
    return render(request,'general_master/edit_sub_service_category.html',context)

@login_required(login_url='/user_login')
def editing_add_sub_service_master(request,id):
    service_su_category1=ServiceSubCategory.objects.get(id=id)
    form=ServiceSubCategoryForm(instance=service_su_category1)
    service_sub_category='service_sub_category'
    if request.method=='POST':
        form=ServiceSubCategoryForm(request.POST,instance=service_su_category1)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_sub_service_master')
    context={
    'form':form,'service_category':service_sub_category,'service_su_category1':service_su_category1
    }
    return render(request,'general_master/editing_sub_service_category.html',context)


@login_required(login_url='/user_login')
def add_service_department(request):
    form=ServiceDepartmentForm()
    service_department1=ServiceDepartment.objects.all()
    service_department='service_department'
    if request.method=='POST':
        form=ServiceDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_department')
    context={
    'form':form,'service_department':service_department,'service_department1':service_department1
    }
    return render(request,'general_master/service_department.html',context)

@login_required(login_url='/user_login')
def edit_add_service_department(request):
    form=ServiceDepartmentForm()
    service_department1=ServiceDepartment.objects.all()
    service_department='service_department'
    if request.method=='POST':
        form=ServiceDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_service_department')
    context={
    'form':form,'service_department':service_department,'service_department1':service_department1
    }
    return render(request,'general_master/edit_service_department.html',context)

@login_required(login_url='/user_login')
def editing_add_service_department(request,id):
    service_department1=ServiceDepartment.objects.get(id=id)
    form=ServiceDepartmentForm(instance=service_department1)
    service_department='service_department'
    if request.method=='POST':
        form=ServiceDepartmentForm(request.POST,instance=service_department1)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_department')
    context={
    'form':form,'service_department':service_department,'service_department1':service_department1
    }
    return render(request,'general_master/editing_service_department.html',context)


@login_required(login_url='/user_login')
def add_service_sub_department(request):
    service_sub_department1=ServiceSubDepartment.objects.all()
    form=ServiceSubDepartmentForm()
    service_sub_department='service_sub_department'
    if request.method=='POST':
        form=ServiceSubDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_sub_department')
    context={
    'form':form,'service_sub_department':service_sub_department,'service_sub_department1':service_sub_department1
    }
    return render(request,'general_master/sub_service_department.html',context)

@login_required(login_url='/user_login')
def edit_add_service_sub_department(request):
    service_sub_department1=ServiceSubDepartment.objects.all()
    form=ServiceSubDepartmentForm()
    service_sub_department='service_sub_department'
    if request.method=='POST':
        form=ServiceSubDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_sub_department')
    context={
    'form':form,'service_sub_department':service_sub_department,'service_sub_department1':service_sub_department1
    }
    return render(request,'general_master/edit_sub_service_department.html',context)

@login_required(login_url='/user_login')
def editing_add_service_sub_department(request,id):
    service_sub_department1=ServiceSubDepartment.objects.get(id=id)
    form=ServiceSubDepartmentForm(instance=service_sub_department1)
    service_sub_department='service_sub_department'
    if request.method=='POST':
        form=ServiceSubDepartmentForm(request.POST,instance=service_sub_department1)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_sub_department')
    context={
    'form':form,'service_sub_department':service_sub_department,'service_sub_department1':service_sub_department1
    }
    return render(request,'general_master/editing_sub_service_department.html',context)



@login_required(login_url='/user_login')
def ward_type(request):
    form=WardTypeForm()
    ward_type='ward_type'
    ward_type=WardType.objects.all()
    if request.method=='POST':
        form=WardTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ward_type')
    context={
    'form':form,'ward_type':ward_type
    }
    return render(request,'general_master/ward_type.html',context)

@login_required(login_url='/user_login')
def edit_ward_type(request):
    form=WardTypeForm()
    ward_type='ward_type'
    ward_type=WardType.objects.all()
    if request.method=='POST':
        form=WardTypeForm(request.POST)
        if form.is_valid():
            form.save()
    context={
    'form':form,'ward_type':ward_type
    }
    return render(request,'general_master/edit_ward_type.html',context)

@login_required(login_url='/user_login')
def editing_ward_type(request,id):
    ward_type='ward_type'
    ward_type=WardType.objects.get(id=id)
    form=WardTypeForm(instance=ward_type)
    if request.method=='POST':
        form=WardTypeForm(request.POST,instance=ward_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_ward_type')
    context={
    'form':form,'ward_type':ward_type
    }
    return render(request,'general_master/editing_ward_type.html',context)

@login_required(login_url='/user_login')
def blood_master(request):
    form=BloodMasterForm()
    blood_master='blood_master'
    blood_master=BloodMaster.objects.all()
    if request.method=='POST':
        form=BloodMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blood_master')
    context={
    'form':form,'blood_master':blood_master
    }
    return render(request,'general_master/blood_master.html',context)

@login_required(login_url='/user_login')
def edit_blood_master(request):
    form=BloodMasterForm()
    blood_master='blood_master'
    blood_master=BloodMaster.objects.all()
    if request.method=='POST':
        form=BloodMasterForm(request.POST)
        if form.is_valid():
            form.save()
    context={
    'form':form,'blood_master':blood_master
    }
    return render(request,'general_master/edit_blood_master.html',context)

@login_required(login_url='/user_login')
def editing_blood_master(request,id):
    blood_master='blood_master'
    blood_master=BloodMaster.objects.get(id=id)
    form=BloodMasterForm(instance=blood_master)
    if request.method=='POST':
        form=BloodMasterForm(request.POST,instance=blood_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_blood_master')
    context={
    'form':form,'blood_master':blood_master
    }
    return render(request,'general_master/editing_blood_master.html',context)

@login_required(login_url='/user_login')
def designation(request):
    records=Designation.objects.all()
    form=DesignationForm()
    ward_type='ward_type'
    if request.method=='POST':
        form=DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/designation')
    context={
    'form':form,'ward_type':ward_type,'records':records
    }
    return render(request,'general_master/designation.html',context)

@login_required(login_url='/user_login')
def edit_designation(request):
    records=Designation.objects.all()
    form=DesignationForm()
    ward_type='ward_type'
    if request.method=='POST':
        form=DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/designation')
    context={
    'form':form,'ward_type':ward_type,'records':records
    }
    return render(request,'general_master/edit_designation.html',context)

@login_required(login_url='/user_login')
def editing_designation(request,id):
    records=Designation.objects.get(id=id)
    form=DesignationForm(instance=records)
    ward_type='ward_type'
    if request.method=='POST':
        form=DesignationForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/designation')
    context={
    'form':form,'ward_type':ward_type,'records':records
    }
    return render(request,'general_master/editing_designation.html',context)

@login_required(login_url='/user_login')
def create_room(request):
    create_room1=RoomNumber.objects.all()
    form=RoomNumberForm()
    if request.method=='POST':
        form=RoomNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create-room')
    create_room='create_room'
    context={
    'form':form,'create_room':create_room,'create_room1':create_room1
    }
    return render(request,'general_master/create_room.html',context)

@login_required(login_url='/user_login')
def edit_create_room(request):
    create_room1=RoomNumber.objects.all()
    form=RoomNumberForm()
    if request.method=='POST':
        form=RoomNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create-room')
    create_room='create_room'
    context={
    'form':form,'create_room':create_room,'create_room1':create_room1
    }
    return render(request,'general_master/edit_create_room.html',context)

@login_required(login_url='/user_login')
def editing_create_room(request,id):
    create_room1=RoomNumber.objects.get(id=id)
    form=RoomNumberForm(instance=create_room1)
    if request.method=='POST':
        form=RoomNumberForm(request.POST,instance=create_room1)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create-room')
    create_room='create_room'
    context={
    'form':form,'create_room':create_room,'create_room1':create_room1
    }
    return render(request,'general_master/editing_create_room.html',context)

# ================End Master View=================================
from django.shortcuts import redirect
def temp_service_removing(request,id):
    temp_service=OpdBillingTemper.objects.get(id=id)
    temp_service.delete()
    search_urls=request.session['search_urls']
    print('Search URL',search_urls)
    return HttpResponseRedirect(f'/opd_billing/{search_urls}')

def opd_trasaction(request):
    form1=CashForm()
    if request.method=='POST':
        form1=CashForm(request.POST)
        if form1.is_valid():
            form1.save()
        return HttpResponseRedirect('/opd_trasaction')

    context={
        'form1':form1,
    }
    return render(request,'clinical/opd_trasaction.html',context)

def ipd_list(request):
    get_data=PatientsRegistrationsAllInOne.objects.all()
    record=ClinicalOrDepartment.objects.all()
    print('records',record)
    # print('get_data',get_data)
    if request.method=='POST':
        adm_date=request.POST.get('adm_date')
        ward=request.POST.get('ward')
        department=request.POST.get('department')
        print('department',department)
        floor=request.POST.get('floor')
        print('adm_date',adm_date)
        filtering_records = PatientVisitMains.objects.filter(clinical_department=department)
        print('filtering_records======================',filtering_records)

        return render(request,'admin/depart.html',{'filtering_records':filtering_records,'record':record})
    return render(request,'clinical/ipd.html',{'get_data':get_data,'record':record})

def summerize_bill(request):
    return render(request,'clinical/summerize_bill.html')

def details_bill(request):
    return render(request,'clinical/summerize_bill.html')

@login_required(login_url='/user_login')
def payment_mode(request):
    records=OpdPaymentMode.objects.all()
    form=OpdPaymentModeForm()
    if request.method=='POST':
        form=OpdPaymentModeForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/payment_mode')
    context={
        'form':form,'records':records
    }
    return render(request,'general_master/payment_mode.html',context)

@login_required(login_url='/user_login')
def edit_payment_mode(request):
    records=OpdPaymentMode.objects.all()
    form=OpdPaymentModeForm()
    if request.method=='POST':
        form=OpdPaymentModeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/payment_mode')
    create_room='create_room'
    context={
    'form':form,'create_room':create_room,'records':records
    }
    return render(request,'general_master/edit_payment_mode.html',context)


@login_required(login_url='/user_login')
def editing_payment_mode(request,pk):
    records=OpdPaymentMode.objects.get(id=pk)
    form=OpdPaymentModeForm(instance=records)
    if request.method=='POST':
        form=OpdPaymentModeForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/payment_mode')
    context={
        'form':form,'records':records
    }
    return render(request,'general_master/editing_payment_mode.html',context)

@login_required(login_url='/user_login')
def bank_master(request):
    records=BankMaster.objects.all()
    form=BankMasterForm()
    if request.method=='POST':
        form=BankMasterForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/bank_master')
    context={
        'form':form,'records':records
    }
    return render(request,'general_master/bank_master.html',context)

@login_required(login_url='/user_login')
def edit_bank_master(request):
    records=BankMaster.objects.all()
    form=BankMasterForm()
    if request.method=='POST':
        form=BankMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bank_master')
    create_room='create_room'
    context={
    'form':form,'create_room':create_room,'records':records
    }
    return render(request,'general_master/edit_bank_master.html',context)

@login_required(login_url='/user_login')
def editing_bank_master(request,pk):
    records=BankMaster.objects.get(id=pk)
    form=BankMasterForm(instance=records)
    if request.method=='POST':
        form=BankMasterForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/bank_master')
    context={
        'form':form,'records':records
    }
    return render(request,'general_master/editing_bank_master.html',context)
def investigation_view(request):
    return render(request,'clinical/investigation_view.html')
def consultant_view(request):
    return render(request,'clinical/consultant_view.html')
def medicine_view(request):
    return render(request,'clinical/medicine_view.html')
def room_charge_view(request):
    return render(request,'clinical/investigation_view.html')


@login_required(login_url='/user_login')
def for_create_adv_visit(request,uhid):
    request.session['visit_uhid']=uhid
    try:
        corporate = CorporateMaster.objects.all()
        billing = BillingGroup.objects.all()
        records = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
        title=records.title
        first_name = records.first_name
        middle_name = records.middle_name
        last_name = records.last_name
        dob = records.dob
        gender = records.gender
        registration_date_and_time = records.registration_date_and_time
        blood_group = records.blood_group
        marital_status = records.marital_status
        father_or_husband_name = records.father_or_husband_name
        mother_name = records.mother_name
        mobile_number = records.mobile_number
        address = records.address
        referred_by = records.referred_by
        city = records.city
        state = records.state
        country = records.country
        pin_code = records.pin_code
        aadhar_card = records.aadhar_card
        pan_card = records.pan_card
        emergency_contact_person = records.emergency_contact_person
        emergency_contact_num = records.emergency_contact_num
        alternate_contact_number = records.alternate_contact_number
        nationality = records.nationality
        email = records.email
        staff_member = records.staff_member
        relationship = records.relationship
        allow_photo_at_nursing_station = records.allow_photo_at_nursing_station
        notable = records.notable
        in_cash = records.in_cash
        is_senior_citizen = records.is_senior_citizen
        billing_group = records.billing_group
        corporate_name = records.corporate_name
        cardholder_name = records.cardholder_name
        card_number = records.card_number
        relation = records.relation
        valid_upto = records.valid_upto
        sum_insured_amount = records.sum_insured_amount
        is_inactive = records.is_inactive
        print('valid_upto',valid_upto)
    except:
        pass

    form_visit = PatientVisitMainForm()
    visited = PatientVisitMains.objects.filter(uhid__exact=uhid).order_by('-id')
    context={
        'title':title,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,
        'dob':dob,'gender':gender,'registration_date_and_time':registration_date_and_time,'blood_group':blood_group,
        'blood_group':blood_group,'marital_status':marital_status,'father_or_husband_name':father_or_husband_name,
        'mother_name':mother_name,'mobile_number':mobile_number,'address':address,'referred_by':referred_by,
        'state':state,'country':country,'pin_code':pin_code,'aadhar_card':aadhar_card,'pan_card':pan_card,
        'emergency_contact_person':emergency_contact_person,'emergency_contact_num':emergency_contact_num,
        'alternate_contact_number':alternate_contact_number,'nationality':nationality,'email':email,'staff_member':staff_member,
        'relationship':relationship,'allow_photo_at_nursing_station':allow_photo_at_nursing_station,'notable':notable,
        'in_cash':in_cash,'is_senior_citizen':is_senior_citizen,'billing_group':billing_group,'corporate_name':corporate_name,
        'cardholder_name':cardholder_name,'card_number':card_number,'relation':relation,'valid_upto':valid_upto,
        'sum_insured_amount':sum_insured_amount,'is_inactive':is_inactive,'city':city,'uhid':uhid,
        'form_visit':form_visit,'visited':visited,'corporate':corporate,'billing':billing
    }
    return render(request,'clinical/patient_registration_edit.html',context)

@login_required(login_url='/user_login')
def get_list_patient(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'opd_advance' in access.user_profile.screen_access:
        try:
            records = PatientsRegistrationsAllInOne.objects.filter(location=request.location)
            context={
                'records':records,'access':access
            }
            return render(request,'clinical/get_list_patient.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def get_list_patient_edit(request,uhid):
    request.session['adv_visit_uhid']=uhid
    print('uhid===========',uhid)
    pay_details = Adv_Visit_Creation.objects.all().order_by('-id')

    records = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
    if request.method == 'POST' and 'adv_pay' in request.POST:
        advance_pay=request.POST.get('advance_pay')
        print('advance_pay',advance_pay)
        in_uhid=uhid
        print('in_uhid===========', in_uhid)
        datas=Adv_Visit_Creation(
            uhid=in_uhid,
            advance_pay=advance_pay,
        )
        datas.save()
        return HttpResponseRedirect('#')
    context={
        'records':records,'pay_details':pay_details,
    }
    return render(request,'clinical/get_list_patient_edit.html',context)



@login_required(login_url='/user_login')
def avd_pay_paient_visit(request):
    uhids=request.session['adv_visit_uhid']

    form_visit=AdvPatientVisitMainForm()
    if request.method=='POST':
        form_visit = AdvPatientVisitMainForm(request.POST)
        if form_visit.is_valid():

            visit_type = form_visit.cleaned_data['visit_type']
            print('visit_type',visit_type)
            description = form_visit.cleaned_data['description']
            print('description', description)
            nurse_doctor = form_visit.cleaned_data['nurse_doctor']
            clinical_department = form_visit.cleaned_data['clinical_department']
            # if visit_type=='Dialysis':
            creating_visit_id = AdvPatientVisitMains.objects.filter(uhid__exact=uhids).count()
            adv_payment = Adv_Visit_Creation.objects.filter(uhid__exact=uhids).last()
            paid_amt=adv_payment.advance_pay
            rate_dialysis=100
            no_visit=int(paid_amt)/int(rate_dialysis)
            no_actual_visit=str(no_visit)[:1]

            today = date.today()
            today = today.strftime("%y%m%d")
            list = []
            for i in range(10):
                visit_ids = 'V.ID' + today + '00' +str(creating_visit_id)+str(i)
                list.append(visit_ids)
                print('visit_id',visit_ids)
            print('list',list)
            for d in range(len(list)):
               data_visit_id=list[d]
               data_uhid=uhids
               data_visit_type=visit_type
               data_description=description
               data_nurse_doctor=nurse_doctor
               data_clinical_department=clinical_department
               patien_visit_creation = AdvPatientVisitMains(
                   uhid=data_uhid,  visit_type=data_visit_type, description=data_description, nurse_doctor=data_nurse_doctor,
                   clinical_department=data_clinical_department,visit_id=data_visit_id,
               )
               patien_visit_creation.save()
        # else:
                #     creating_visit_id = AdvPatientVisitMains.objects.filter(uhid__exact=uhids).count()
                #     today = date.today()
                #     today = today.strftime("%y%m%d")
                #     if len(str(creating_visit_id)) == 1:
                #         visit_id = 'V.ID' + today + '00' + str(creating_visit_id)
                #     elif len(str(creating_visit_id)) == 2:
                #         visit_id = 'V.ID' + today + '0' + str(creating_visit_id)
                #     else:
                #         visit_id = 'V.ID' + today + str(creating_visit_id)
                #     print('visit_id', visit_id)
                # print(f'Visiting ... {visit_type},{description},{nurse_doctor},{clinical_department}')
                # patien_visit_creation = AdvPatientVisitMains(
                #     uhid=uhids, visit_type=visit_type, description=description, nurse_doctor=nurse_doctor,
                #     clinical_department=clinical_department, visit_id=visit_id,
                # )
                # patien_visit_creation.save()
                # print('hello world')
            return HttpResponseRedirect(f'/avd_pay_paient_visit')
    visited=AdvPatientVisitMains.objects.filter(uhid=uhids).order_by('-id')
    context={
        'form_visit':form_visit,'visited':visited
    }
    return render(request,'clinical/avd_pay_paient_visit.html',context)
# Date 10/11/22 ===========================Start=========================



@login_required(login_url='/user_login')
def hospital_report_revenue(request):
    get_data = PatientsRegistrationsAllInOne.objects.all()
    record = ClinicalOrDepartment.objects.all()
    if request.method == 'POST':
        # department = request.POST.get('department')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        print(f'Start Date {start_date}, end date {end_date}')
        main_table_data=OpdBillingMain.objects.filter(bill_date_time__range=[start_date,end_date])
        print('department_data',main_table_data)
        # filtering_records = PatientVisitMains.objects.filter(clinical_department=department)
        return render(request, 'clinical/hospital_report_revenue.html', {'record': record,'main_table_data':main_table_data,'start_date':start_date,'end_date':end_date})
    return render(request, 'clinical/hospital_report_revenue.html', {'get_data': get_data, 'record': record})
    # return render(request,'clinical/hospital_report_revenue.html')

@login_required(login_url='/user_login')
def department_wise_reports(request):
    if request.method=='POST':
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        print(f'Start Date {start_date}, end date {end_date}')
        department_records = PatientVisitMains.objects.filter(visit_date_time__range=[start_date,end_date])
        print('department_records',department_records)
        context={
        'department_records':department_records,
        }
        return render(request,'clinical/department_report.html',context)
    return render(request,'clinical/department_report.html')

@login_required(login_url='/user_login')
def patient_details(request):
    if request.method=='POST':
        uhids=request.POST.get('uhid_data')
        patient_records = PatientsRegistrationsAllInOne.objects.filter(uhid__exact=uhids)
        billing_records = OpdBillingMain.objects.filter(uhid__exact=uhids)
        payment_records = OpdPayment.objects.filter(uhid__exact=uhids)
        payment_visit = OpdPayment.objects.filter(uhid__exact=uhids)
        payment_record=payment_visit.visit_id
        department_records = PatientVisitMains.objects.filter(Q(visit_id__exact=payment_record)&Q(uhid__exact=uhids))
        print('payment_visit_id',payment_record)
        print('billing_records',billing_records)
        print('department_records',department_records)
        context={
            'patient_records':patient_records,'billing_records':billing_records,'department_records':department_records,
            'payment_records':payment_records,
        }
        return render(request,'clinical/patient_details.html',context)
    return render(request,'clinical/patient_details.html')


@login_required(login_url='/user_login')
def detail_revenue_report(request):
    doctorr = PatientsRegistrationsAllInOne.objects.all()
    doctor_list = [data.first_name for data in doctorr]
    if request.method=='POST':
        bill_start_date=request.POST.get('b_start_date')
        bill_end_date=request.POST.get('b_end_date')
        billing_records = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date])
        billing_record = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date]).order_by('uhid')
        sample_ids = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date]).values_list('uhid', flat=True)
        print('sample_ids',sample_ids)
        uhidss=PatientsRegistrationsAllInOne.objects.filter(uhid__in=sample_ids)
        # queryset = OpdBillingMain.objects.all().select_related('first_name').select_related('age')
        print('uhidss',uhidss)
        # print('total',total_uhid)
        print('billing_record',billing_record)
        uhid_list = []
        list1=[]
        all_list=[]
        for data11 in billing_record:
            for x in uhidss:
                dict1 = data11
                dict2 = x
                dict1.append(dict2)
                all_list.append(dict1)
        for x in uhidss:
            list1.append(x)
        # for d in uhid_list:
        #     list1.append(d)
        list2=[]
        list2=list1+uhid_list
        print('list2-------------',list2)
        new_var=list(set(list2))
        print('new_var================',new_var)
        all_list_api = []
        for patient in sample_ids:
            for admissionin in uhidss:
                if patient['uhid'] == admissionin['uhid']:
                    dict1 = patient
                    dict2 = admissionin
                    dict1.update(dict2)
                    all_list_api.append(dict1)
        print('uhidss new connection',uhidss)
        context={
            'billing_records':billing_records,
            'list2':list2,'uhidss':uhidss,'new_var':new_var,
        }
        return render(request,'clinical/details_revenue_report.html',context)
    return render(request,'clinical/details_revenue_report.html')



@login_required(login_url='/user_login')
def hospital_department_report(request):
    if request.method=='POST':
        start_date=request.POST.get('b_start_date')
        end_date=request.POST.get('b_end_date')
        doctorr = ClinicalOrDepartment.objects.all()
        depart_list = [data.clinical_department for data in doctorr]
        renenue_records = OpdBillingMain.objects.filter(bill_date_time__range=[start_date,end_date],location=request.location).order_by('bill_date_time').distinct()
        list2 = []
        list2=depart_list
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        list7 = []
        list8 = []
        all_one=zip(list2,list3,list4,list5,list6,list8)
        # queryset = OpdBillingMain.objects.filter('department').distinct()
        # print('queryset-------------------------',queryset)
        for i in range(len(depart_list)):
            ind_department_list=depart_list[i]
            # print('ind_uhid_list',ind_uhid_list)
            total_count = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(department__exact=ind_department_list,location=request.location)).count()
            total_revenue = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('net_amount'))
            total_revenue = total_revenue['net_amount__sum']
            total_revenue_net = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(department__exact=ind_department_list,location=request.location)).aggregate(
                Sum('net_amount'))
            total_revenue_net = total_revenue_net['net_amount__sum']
            total_revenue_disc = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(department__exact=ind_department_list,location=request.location)).aggregate(
                Sum('discount'))
            total_revenue_disc = total_revenue_disc['discount__sum']
            total_revenue_payable = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(department__exact=ind_department_list,location=request.location)).aggregate(
                Sum('pay_amount'))
            total_revenue_payable = total_revenue_payable['pay_amount__sum']
            total_revenue_paid = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(department__exact=ind_department_list,location=request.location)).aggregate(
                Sum('paid_amount'))
            total_revenue_paid = total_revenue_paid['paid_amount__sum']
            list3.append(total_revenue_net)
            list4.append(total_revenue_disc)
            list5.append(total_revenue_payable)
            list6.append(total_revenue_paid)
            list7.append(total_count)
            if total_revenue_net != None and total_revenue != None :
                liat_E=total_revenue_net/total_revenue*100
                list8.append(liat_E)
            total_net = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('net_amount'))
            total_net = total_net['net_amount__sum']
            total_disc = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('discount'))
            total_disc = total_disc['discount__sum']
            total_payable = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('pay_amount'))
            total_payable = total_payable['pay_amount__sum']
            total_paid = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('paid_amount'))
            total_paid = total_paid['paid_amount__sum']
            chart=zip(list2,list8)
        context={
            'renenue_records':renenue_records,'total_revenue_net':total_revenue_net,'total_revenue_disc':total_revenue_disc,
            'total_revenue_payable':total_revenue_payable,'total_revenue_paid':total_revenue_paid,'start_date':start_date,'end_date':end_date,
            'depart_list':depart_list,'list2':list2,'list3':list3,'list4':list4,'list5':list5,'list6':list6,'all_one':all_one,
            'total_net':total_net,'total_payable':total_payable,'total_disc':total_disc,'total_paid':total_paid,
            'chart':chart
        }
        return render(request,'clinical/hospital_department_report.html',context)
    return render(request,'clinical/hospital_department_report.html')

from testapp.serializers import PatienDetailSerializer,OpdBillingMainSerializer
@login_required(login_url='/user_login')
def all_details_report(request):
    bill_start_date=request.POST.get('b_start_date')
    bill_end_date=request.POST.get('b_end_date')
    if bill_start_date and bill_end_date:
        bill_start_date=request.POST.get('b_start_date').split("T")[0]
        bill_end_date=request.POST.get('b_end_date').split("T")[0]
        records = OpdBillingMain.objects.extra(select={
            'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
            'pat_gender':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        }).filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel').order_by('-uhid')
        net_amt = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('net_amount'))
        net_amt = net_amt['net_amount__sum']
        net_disc = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('discount'))
        net_disc = net_disc['discount__sum']
        amt_pay = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('pay_amount'))
        amt_pay = amt_pay['pay_amount__sum']
        amt_paid = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('paid_amount'))
        amt_paid = amt_paid['paid_amount__sum']
        context={
            'records_1':records,'net_amt':net_amt,'net_disc':net_disc,'amt_pay':amt_pay,'amt_paid':amt_paid,"bill_start_date":bill_start_date,
            "bill_end_date":bill_end_date
        }
        return render(request,'clinical/details_revenue_report.html',context)
    return render(request,'clinical/details_revenue_report.html')

@login_required(login_url='/user_login')
def doctor_wise_revenue_report(request):
    if request.method=='POST':
        start_date=request.POST.get('b_start_date')
        end_date=request.POST.get('b_end_date')
        doctorr = DoctorTable.objects.all()
        depart_list = [data.doctor_name for data in doctorr]
        renenue_records = OpdBillingMain.objects.filter(bill_date_time__range=[start_date,end_date],location=request.location).order_by('bill_date_time').distinct()
        list2 = []
        list2=depart_list
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        list7 = []
        list8 = []
        liat_E=''
        all_one=zip(list2,list3,list4,list5,list6,list8)
        for i in range(len(depart_list)):
            ind_department_list=depart_list[i]
            total_count = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date]) & Q(department__exact=ind_department_list),location=request.location).count()
            total_revenue = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('net_amount'))
            total_revenue = total_revenue['net_amount__sum']
            departmenttt = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(doctor_name__exact=ind_department_list,location=request.location))
            total_revenue_net = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(doctor_name__exact=ind_department_list,location=request.location)).aggregate(
                Sum('net_amount'))
            total_revenue_net = total_revenue_net['net_amount__sum']
            total_revenue_disc = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(doctor_name__exact=ind_department_list,location=request.location)).aggregate(
                Sum('discount'))
            total_revenue_disc = total_revenue_disc['discount__sum']
            total_revenue_payable = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(doctor_name__exact=ind_department_list,location=request.location)).aggregate(
                Sum('pay_amount'))
            total_revenue_payable = total_revenue_payable['pay_amount__sum']
            total_revenue_paid = OpdBillingMain.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(doctor_name__exact=ind_department_list,location=request.location)).aggregate(
                Sum('paid_amount'))
            total_revenue_paid = total_revenue_paid['paid_amount__sum']
            list3.append(total_revenue_net)
            list4.append(total_revenue_disc)
            list5.append(total_revenue_payable)
            list6.append(total_revenue_paid)
            list7.append(total_count)
            if total_revenue_net != None:
                liat_E = total_revenue_net / total_revenue * 100
                list8.append(liat_E)
            elif total_revenue_net == None and total_revenue != None :
                liat_E = 0 / total_revenue * 100
                list8.append(liat_E)
            total_net = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('net_amount'))
            total_net = total_net['net_amount__sum']
            total_disc = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('discount'))
            total_disc = total_disc['discount__sum']
            total_payable = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('pay_amount'))
            total_payable = total_payable['pay_amount__sum']
            total_paid = OpdBillingMain.objects.filter(bill_date_time__range=[start_date, end_date],location=request.location).aggregate(
                Sum('paid_amount'))
            total_paid = total_paid['paid_amount__sum']
            chart=zip(list2,list8)

        context={
            'renenue_records':renenue_records,'total_net':total_net,'total_payable':total_payable,
            'total_disc':total_disc,'total_paid':total_paid,'start_date':start_date,'end_date':end_date,
            'depart_list':depart_list,'list3':list3,'list4':list4,'list5':list5,'list6':list6,'list2':list2,'all_one':all_one,
            'chart':chart,
        }
        return render(request,'clinical/doctor_wise_revenue_report.html',context)
    return render(request,'clinical/doctor_wise_revenue_report.html')
from testapp.serializers import PatienDetailSerializer,OpdBillingMainSerializer


@login_required(login_url='/user_login')
def service_analysis_report(request):
    list1=[]
    list2=[]
    all_one=zip(list1,list2)
    service_department=ServiceDepartment.objects.all()
    service_sub_department=ServiceSubDepartment.objects.all()
    services=ServiceMaster.objects.all()
    depart_list = [data.service_department for data in services]
    sub_depart_list = [data.ServiceSubDepartment for data in services]
    list1.append(depart_list)
    list2.append(sub_depart_list)

    services1=ServiceMaster.objects.all().only('service_department')
    services2=ServiceMaster.objects.all().only('ServiceSubDepartment')
    context={
        'services':services,'services2':services2,'all_one':all_one,
    }
    return render(request,'clinical/service_analysis_report.html',context)

@login_required(login_url='/user_login')
def detail_doctor_report(request):
    if request.method=='POST':
        all_records =''
        start_date=request.POST.get('b_start_date')
        end_date=request.POST.get('b_end_date')
        doctor_detail = OpdBillingMain.objects.filter(bill_date_time__range=[start_date,end_date],location=request.location).order_by('bill_date_time')
        Temporary_Table.objects.all().delete()
        records2 = [data.doctor_name for data in doctor_detail]
        res = [*set(records2)]
        list4=[]
        for data in res:
            records = OpdBillingMain.objects.filter(doctor_name=data)
            reco = [data.uhid for data in doctor_detail]
            doctor_name = [data.doctor_name for data in doctor_detail]
            doct_names=set(doctor_name)
            doct_names2=list(doct_names)
            legnth = len(records)
            list4.append(reco)
            for data in records:
                data = Temporary_Table(
                    uhid=data.uhid, visit_no=data.visit_no, bill_date_time=data.bill_date_time,
                    department=data.department, doctor_name=data.doctor_name, net_amount=data.net_amount,
                    discount=data.discount, pay_amount=data.pay_amount, paid_amount=data.paid_amount,
                    payment_mode=data.payment_mode,
                )
                data.save()
            all_records = Temporary_Table.objects.all()
        return render(request,'clinical/detail_doctor_report.html',{'all_records':all_records})
    return render(request,'clinical/detail_doctor_report.html')

@login_required(login_url='/user_login')
def today_report(request):
    pay_mode_id=''
    pay_mode=''
    now = datetime.now()
    date_new = now.strftime("%Y-%m-%d")
    today_details = OpdBillingMain.objects.filter(bill_date_time__date=date_new,location=request.location).order_by('bill_date_time')
    mode_name=[data.payment_mode for data in today_details]
    mode_names = set(mode_name)
    for pay_data in mode_name:
        mode_pay=OpdPaymentMode.objects.filter(id__icontains=pay_data)
        pay_mode_id=[data.id for data in mode_pay]
        pay_mode = [data.payment_mode for data in mode_pay]
    list=[]
    for dat in pay_mode_id:
        payment_mode = OpdBillingMain.objects.filter(Q(bill_date_time__date=date_new,location=request.location)&Q(payment_mode=dat,location=request.location)).aggregate(Sum('net_amount'))
        payment_mode = payment_mode['net_amount__sum']
        list.append(payment_mode)
    list_all=zip(pay_mode,list)
#=============================== For New Collection Report 24/04/2023 ===================================
    users = CreateUser.objects.all()
    if request.method=="POST":
        bill_start_date = request.POST.get('b_start_date')
        bill_end_date = request.POST.get('b_end_date')
        mode_type = request.POST.get('mode_type')
        users_id = request.POST.get('users')
        #====================== Only Date Range ===================================================
        if bill_start_date != '' and bill_end_date !='' and mode_type=='' and users_id =='' :
            records=OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location).extra(select={
                                'f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'm_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                'disc':'Select discount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                'payable':'Select pay_amount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                }).order_by("-uhid").exclude(status='cancel')
            users=[data.created_by for data in records]
            # user_details=CreateUser.objects.filter(login_id__in=users)
            pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash').extra(select={
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
                                }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel').aggregate(Sum('net_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_ttl_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash').aggregate(Sum('total_taxable_amount'))
            p_rcv_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash').aggregate(Sum('paid_amount'))
            sub_tot_amt = p_ttl_amt['total_taxable_amount__sum']
            sub_paid_amt = p_rcv_amt['paid_amount__sum']
            opd_tot_amt = ttl_amt['net_amount__sum']
            opd_paid_amt = rcv_amt['paid_amount__sum']
            if sub_tot_amt is None:
                sub_tot_amt = 0
            if sub_paid_amt is None :
                sub_paid_amt = 0
            if opd_tot_amt is None :
                opd_tot_amt = 0
            if opd_paid_amt is None :
                opd_paid_amt = 0
            ttl_net = opd_tot_amt + sub_tot_amt
            paid_amt = opd_paid_amt +sub_paid_amt
            #=========================== Modes Wise Toatal AMT ====================
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='cash').exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_amt_cash = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type__startswith='cash',panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_cash['paid_amount__sum']:
                amt_cash = amt_cash['paid_amount__sum'] + p_amt_cash['paid_amount__sum']
            else:
                amt_cash = amt_cash['paid_amount__sum']
            amt_debit = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='debit_credit_card').exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_amt_debit = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type__startswith='debit_credit_card',panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_debit['paid_amount__sum']:
                amt_debit = amt_debit['paid_amount__sum'] + p_amt_debit['paid_amount__sum']
            else:
                amt_debit = amt_debit['paid_amount__sum']
            amt_m_pesa = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='m_pesa').exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_amt_m_pesa = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type__startswith='m_pesa',panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_m_pesa['paid_amount__sum']:
                amt_m_pesa = amt_m_pesa['paid_amount__sum'] + p_amt_m_pesa['paid_amount__sum']
            else:
                amt_m_pesa = amt_m_pesa['paid_amount__sum']
            amt_bank = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='bank').exclude(status='cancel').aggregate(Sum('paid_amount'))
            amt_bank = amt_bank['paid_amount__sum']
            amt_eft = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='eft').exclude(status='cancel').aggregate(Sum('paid_amount'))
            amt_eft = amt_eft['paid_amount__sum']
            amt_cheque = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='cheque').exclude(status='cancel').aggregate(Sum('paid_amount'))
            amt_cheque = amt_cheque['paid_amount__sum']
            if amt_cash is None:
                amt_cash = 0
            if amt_debit is None :
                amt_debit = 0
            if amt_m_pesa is None :
                amt_m_pesa = 0
            if amt_bank is None:
                amt_bank = 0
            if amt_eft is None :
                amt_eft = 0
            if amt_cheque is None:
                amt_cheque = 0
            total_paments= amt_cash+amt_debit+amt_m_pesa+amt_bank+amt_eft+amt_cheque
            context = {
                'today_details': today_details, 'date_new': date_new, 'list_all': list_all,
                'records': records, 'ttl_net': ttl_net, 'paid_amt': paid_amt, 'amt_cash': amt_cash,
                'amt_debit': amt_debit, 'amt_m_pesa': amt_m_pesa, 'amt_bank': amt_bank,
                'amt_eft': amt_eft, 'amt_cheque': amt_cheque, 'total_paments': total_paments,
                'pharmacy_records': pharmacy_records, 'sub_tot_amt': sub_tot_amt, 'sub_paid_amt': sub_paid_amt,
                'opd_tot_amt': opd_tot_amt, 'opd_paid_amt': opd_paid_amt, 'users': users,'bill_start_date':bill_start_date,'bill_end_date':bill_end_date,
            }
            return render(request, 'clinical/today_report.html', context)
        #================================ Date range with payment mode =============================================
        elif bill_start_date != '' and bill_end_date !='' and mode_type != '' and users_id=='':
            records=OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,location=request.location).extra(select={
                                'f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'm_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                'disc':'Select discount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                'payable':'Select pay_amount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                }).order_by("-uhid").exclude(status='cancel')
            users=[data.created_by for data in records]
            pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,panel='Cash').extra(select={
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
                                }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,location=request.location).exclude(status='cancel').aggregate(Sum('net_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,location=request.location).exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_ttl_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,panel='Cash').aggregate(Sum('total_taxable_amount'))
            p_rcv_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,panel='Cash').aggregate(Sum('paid_amount'))
            sub_tot_amt = p_ttl_amt['total_taxable_amount__sum']
            sub_paid_amt = p_rcv_amt['paid_amount__sum']
            opd_tot_amt = ttl_amt['net_amount__sum']
            opd_paid_amt = rcv_amt['paid_amount__sum']
            if sub_tot_amt is None:
                sub_tot_amt=0
            if sub_paid_amt is None:
                sub_paid_amt=0
            if opd_tot_amt is None:
                opd_tot_amt=0
            if opd_paid_amt is None:
                opd_paid_amt=0
            ttl_net = opd_tot_amt + sub_tot_amt
            if sub_paid_amt:
                paid_amt = rcv_amt['paid_amount__sum'] + p_rcv_amt['paid_amount__sum']
            else:
                paid_amt = rcv_amt['paid_amount__sum']
            #=========================== Modes Wise Toatal AMT ====================
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type=mode_type).exclude(status='cancel').aggregate(Sum('paid_amount'))
            amt_cash = amt_cash['paid_amount__sum']
            p_amt_cash = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,panel='Cash').aggregate(Sum('paid_amount'))
            p_amt_cash=p_amt_cash['paid_amount__sum']
            if amt_cash is None:
                amt_cash = 0
            if p_amt_cash is None :
                p_amt_cash = 0
            mode_wise_total_paments= amt_cash+p_amt_cash
            context = {
                'today_details': today_details, 'date_new': date_new, 'list_all': list_all,
                'records': records, 'ttl_net': ttl_net, 'paid_amt': paid_amt, 'amt_cash': amt_cash,
                'mode_wise_total_paments': mode_wise_total_paments,'mode_type':mode_type,
                'pharmacy_records': pharmacy_records, 'sub_tot_amt': sub_tot_amt, 'sub_paid_amt': sub_paid_amt,
                'opd_tot_amt': opd_tot_amt, 'opd_paid_amt': opd_paid_amt, 'users': users,'bill_start_date':bill_start_date,'bill_end_date':bill_end_date,
            }
            return render(request, 'clinical/today_report.html', context)
        #========================= Date Range With Payment Mode and users =================================
        elif bill_start_date != '' and bill_end_date !='' and mode_type != '' and users_id != '':
            records=OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,created_by=users_id,location=request.location).extra(select={
                                'f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'm_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                'disc':'Select discount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                'payable':'Select pay_amount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                                }).order_by("-uhid").exclude(status='cancel')
            users=[data.created_by for data in records]
            user_details=CreateUser.objects.filter(login_id__in=users)
            pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,created_by=users_id,panel='Cash').extra(select={
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
                                }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,created_by=users_id,location=request.location).exclude(status='cancel').aggregate(Sum('net_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,created_by=users_id,location=request.location).exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_ttl_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,created_by=users_id,panel='Cash').aggregate(Sum('total_taxable_amount'))
            p_rcv_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,created_by=users_id,panel='Cash').aggregate(Sum('paid_amount'))
            sub_tot_amt = p_ttl_amt['total_taxable_amount__sum']
            sub_paid_amt = p_rcv_amt['paid_amount__sum']
            opd_tot_amt = ttl_amt['net_amount__sum']
            opd_paid_amt = rcv_amt['paid_amount__sum']
            if sub_tot_amt is None:
                sub_tot_amt=0
            if sub_paid_amt is None:
                sub_paid_amt=0
            if opd_tot_amt is None:
                opd_tot_amt=0
            if opd_paid_amt is None:
                opd_paid_amt=0
            ttl_net = opd_tot_amt + sub_tot_amt
            if sub_paid_amt:
                paid_amt = rcv_amt['paid_amount__sum'] + p_rcv_amt['paid_amount__sum']
            else:
                paid_amt = rcv_amt['paid_amount__sum']
            #=========================== Modes Wise Toatal AMT ====================
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type=mode_type,created_by=users_id).exclude(status='cancel').aggregate(Sum('paid_amount'))
            amt_cash = amt_cash['paid_amount__sum']
            p_amt_cash = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,created_by=users_id,panel='Cash').aggregate(Sum('paid_amount'))
            p_amt_cash=p_amt_cash['paid_amount__sum']
            if amt_cash is None:
                amt_cash = 0
            if p_amt_cash is None :
                p_amt_cash = 0
            mode_wise_total_paments= amt_cash+p_amt_cash
            context = {
                'today_details': today_details, 'date_new': date_new, 'list_all': list_all,
                'records': records, 'ttl_net': ttl_net, 'paid_amt': paid_amt, 'amt_cash': amt_cash,
                'mode_wise_total_paments': mode_wise_total_paments,'mode_type':mode_type,
                'pharmacy_records': pharmacy_records, 'sub_tot_amt': sub_tot_amt, 'sub_paid_amt': sub_paid_amt,
                'opd_tot_amt': opd_tot_amt, 'opd_paid_amt': opd_paid_amt, 'users': users,'bill_start_date':bill_start_date,'bill_end_date':bill_end_date,
            }
            return render(request, 'clinical/today_report.html', context)
        #==================== Date Range With Users ====================================
        elif bill_start_date != '' and bill_end_date != '' and mode_type == '' and users_id != '':
            print('bill_end_date---->,', bill_end_date, bill_start_date, mode_type, users_id)
            records = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location).extra(select={
                'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                'disc': 'Select discount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                'payable': 'Select pay_amount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
            }).order_by("-uhid").exclude(status='cancel')
            users = [data.created_by for data in records]
            pharmacy_records = PS_CounterSale_Parent.objects.filter(
                sales_date__range=[bill_start_date, bill_end_date],created_by=users_id, panel='Cash').extra(select={
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
            }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location).exclude(status='cancel').aggregate(Sum('paid_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location).exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_ttl_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                             panel='Cash').aggregate(Sum('total_taxable_amount'))
            p_rcv_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                             panel='Cash').aggregate(Sum('paid_amount'))
            sub_tot_amt = p_ttl_amt['total_taxable_amount__sum']
            sub_paid_amt = p_rcv_amt['paid_amount__sum']
            opd_tot_amt = ttl_amt['paid_amount__sum']
            opd_paid_amt = rcv_amt['paid_amount__sum']
            if sub_tot_amt is None:
                sub_tot_amt=0
            if sub_paid_amt is None:
                sub_paid_amt=0
            if opd_tot_amt is None:
                opd_tot_amt=0
            if opd_paid_amt is None:
                opd_paid_amt=0
            ttl_net = opd_tot_amt + sub_tot_amt
            if sub_paid_amt:
                paid_amt = rcv_amt['paid_amount__sum'] + p_rcv_amt['paid_amount__sum']
            else:
                paid_amt = rcv_amt['paid_amount__sum']
            # =========================== Modes Wise Toatal AMT ====================
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                 location=request.location, mode_type__startswith='cash').exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            p_amt_cash = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                              type__startswith='cash', panel='Cash').aggregate(
                Sum('paid_amount'))
            if p_amt_cash['paid_amount__sum']:
                amt_cash = amt_cash['paid_amount__sum'] + p_amt_cash['paid_amount__sum']
            else:
                amt_cash = amt_cash['paid_amount__sum']
            amt_debit = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                  location=request.location,
                                                  mode_type__startswith='debit_credit_card').exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            p_amt_debit = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                               type__startswith='debit_credit_card',
                                                               panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_debit['paid_amount__sum']:
                amt_debit = amt_debit['paid_amount__sum'] + p_amt_debit['paid_amount__sum']
            else:
                amt_debit = amt_debit['paid_amount__sum']
            amt_m_pesa = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                   location=request.location,
                                                   mode_type__startswith='m_pesa').exclude(status='cancel').aggregate(Sum('paid_amount'))
            p_amt_m_pesa = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                                type__startswith='m_pesa', panel='Cash').aggregate(
                Sum('paid_amount'))
            if p_amt_m_pesa['paid_amount__sum']:
                amt_m_pesa = amt_m_pesa['paid_amount__sum'] + p_amt_m_pesa['paid_amount__sum']
            else:
                amt_m_pesa = amt_m_pesa['paid_amount__sum']
            amt_bank = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],
                                                 location=request.location,created_by=users_id, mode_type__startswith='bank').exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            amt_bank = amt_bank['paid_amount__sum']
            amt_eft = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location, mode_type__startswith='eft').exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            amt_eft = amt_eft['paid_amount__sum']
            amt_cheque = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                   location=request.location,
                                                   mode_type__startswith='cheque').exclude(status='cancel').aggregate(Sum('paid_amount'))
            amt_cheque = amt_cheque['paid_amount__sum']
            if amt_cash is None:
                amt_cash = 0
            if amt_debit is None:
                amt_debit = 0
            if amt_m_pesa is None:
                amt_m_pesa = 0
            if amt_bank is None:
                amt_bank = 0
            if amt_eft is None:
                amt_eft = 0
            if amt_cheque is None:
                amt_cheque = 0
            total_paments = amt_cash + amt_debit + amt_m_pesa + amt_bank + amt_eft + amt_cheque
            context = {
                'today_details': today_details, 'date_new': date_new, 'list_all': list_all,
                'records': records, 'ttl_net': ttl_net, 'paid_amt': paid_amt, 'amt_cash': amt_cash,
                'amt_debit': amt_debit, 'amt_m_pesa': amt_m_pesa, 'amt_bank': amt_bank,
                'amt_eft': amt_eft, 'amt_cheque': amt_cheque, 'total_paments': total_paments,
                'pharmacy_records': pharmacy_records, 'sub_tot_amt': sub_tot_amt, 'sub_paid_amt': sub_paid_amt,
                'opd_tot_amt': opd_tot_amt, 'opd_paid_amt': opd_paid_amt, 'users': users,'bill_start_date':bill_start_date,'bill_end_date':bill_end_date,
            }
            return render(request, 'clinical/today_report.html', context)
    context={
        'users':users,
    }
    return render(request,'clinical/today_report.html',context)

@login_required(login_url='/user_login')
def credit_bill(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'opd_bill_settlement' in access.user_profile.screen_access:
        try:
            list_patient = []
            list_opd_main_records = []
            opd_records = Credit.objects.filter(location=request.location)
            # main_records_opd=OpdBillingMain.objects.all()
            opd_data = [data.uhid for data in opd_records]
            opd_bill = [data.bill_no for data in opd_records]
            # print('opd_bill',opd_bill)
            all_data = zip(opd_data, opd_bill)
            for opd_data,opd_bill in all_data:
                patient_records = PatientsRegistrationsAllInOne.objects.get(uhid=opd_data)
                main_records_opd = OpdBillingMain.objects.filter(Q(uhid__exact=opd_data) & Q(bill_no__exact=opd_bill))
                list_patient.append(patient_records)
                list_opd_main_records.append(main_records_opd)
                print('list_opd_main_records',list_opd_main_records)
            var_received_amt=0
            if request.method=="POST":
                uhid=request.POST.getlist('uhid')
                visit_no=request.POST.getlist('visit_no')
                bill_no=request.POST.getlist('bill_no')
                print("bill_no",bill_no)
                bill_date=request.POST.getlist('bill_date')
                p_name=request.POST.getlist('p_name')
                p_payer=request.POST.getlist('p_payer')
                bill_amt=request.POST.getlist('bill_amt')
                tax=request.POST.getlist('tax')
                receivable_amt=request.POST.getlist('receivable_amt')
                received_amt=request.POST.getlist('received_amt')
                outstanding_amt=request.POST.getlist('outstanding_amt')
                paymennt_mode=request.POST.getlist('paymennt_mode')
                cheque_no=request.POST.getlist('cheque_no')
                claim_no=request.POST.getlist('claim_no')
                batch_no=request.POST.getlist('batch_no')
                refrence_id=request.POST.getlist('refrence_id')
                status=request.POST.getlist('status')
                # status2=request.POST.getlist('status2')
                checkbox=request.POST.getlist('checkbox')
                paid_amt=request.POST.getlist('paid_amt')
                current_date_time = datetime.now()
                for ind in range(len(bill_no)):
                    var_uhid=uhid[ind]
                    var_visit_no=visit_no[ind]
                    var_bill_no=bill_no[ind]
                    var_bill_date=bill_date[ind]
                    var_claim_no=claim_no[ind]
                    var_batch_no=batch_no[ind]
                    var_refrence_id=refrence_id[ind]
                    var_p_payer=p_payer[ind]
                    var_bill_amt=bill_amt[ind]
                    var_tax=tax[ind]
                    var_receivable_amt=receivable_amt[ind]
                    var_received_amt=received_amt[ind]
                    var_outstanding_amt=outstanding_amt[ind]
                    var_cheque_no=cheque_no[ind]
                    var_paymennt_mode=paymennt_mode[ind]
                    if var_outstanding_amt=='0':
                        var_status2='Fully'
                    else:
                        var_status2='Partially'
                    if var_bill_no in checkbox:
                        data=OPDBillSettlementTemp(
                            uhid=var_uhid,
                            visit_id=var_visit_no,
                            bill_no=var_bill_no,
                            bill_date=var_bill_date,
                            bill_amt=var_bill_amt,
                            claim_no=var_claim_no,
                            batch_no=var_batch_no,
                            refrence_id=var_refrence_id,
                            payer=var_p_payer,
                            tax=var_tax,
                            receivable_amt=var_receivable_amt,
                            received_amt=var_received_amt,
                            outstanding_amt=var_outstanding_amt,
                            paymennt_mode=var_paymennt_mode,
                            cheque_no=var_cheque_no,
                            status2=var_status2,created_by_id=request.user.id,location_id=request.location,
                        )
                        data.save()
                        main_table=OpdBillingMain.objects.get(bill_no=var_bill_no)
                        main_table.paid_amt=var_received_amt
                        main_table.paid_amt_update_date=current_date_time
                        main_table.save()
                        Credit.objects.filter(bill_no=var_bill_no).delete()
                        return HttpResponseRedirect('/credit_bill')
            else:
                all_in_one = zip(opd_records,list_patient,list_opd_main_records)
                context = {
                    'opd_records': opd_records, 'all_in_one': all_in_one,'var_received_amt':var_received_amt,'access':access
                }
                return render(request, 'clinical/credit_bill.html',context)
            return render(request,'clinical/credit_bill.html')
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

def credit_patient(request):
    dob = request.session['dob']
    mobile_number = request.session['mobile_number']
    billing_group = request.session['billing_group']
    corporate_names = request.session['corporate_name']
    gender = request.session['gender']
    pay_m_uhid = request.session['pay_m_uhid']
    pay_m_visit_id = request.session['pay_m_visit_id']
    billing_groups = request.session['billing_group']
    corporate_names = request.session['corporate_name']
    departments_name = request.session['clinical_department']
    pay_m_receive_amount = request.session['pay_m_receive_amount']
    pay_m_bill_nos = request.session['pay_m_bill_no']
    if request.method=='POST':
        # bill_no=request.POST.get('bill_no')
        # bill_date_time=request.POST.get('bill_date_time')
        # uhid=request.POST.get('uhid')
        # department=request.POST.get('department')
        # visit_no=request.POST.get('visit_no')
        # discount=request.POST.get('discount')
        net_payable_amt=request.POST.get('pay_m_receive_amount')
        paid_amt=request.POST.get('pay_m_receive_amount')

        dob = request.session['dob']
        mobile_number = request.session['mobile_number']
        billing_group = request.session['billing_group']
        corporate_names = request.session['corporate_name']
        gender = request.session['gender']
        pay_m_uhid = request.session['pay_m_uhid']
        pay_m_visit_id = request.session['pay_m_visit_id']
        billing_groups = request.session['billing_group']
        corporate_names = request.session['corporate_name']
        departments_name = request.session['clinical_department']
        pay_m_receive_amount = request.session['pay_m_receive_amount']
        pay_m_bill_nos = request.session['pay_m_bill_no']
        discount=00
        dr_name = request.session['nurse_doctor']
        print('pay_m_receive_amount',pay_m_receive_amount)
        data=Credit(
            bill_no=pay_m_bill_nos,
            uhid=pay_m_uhid,
            department=departments_name,
            visit_no=pay_m_visit_id,
            discount=discount,
            net_payable_amt=net_payable_amt,
            paid_amt=paid_amt,created_by_id=request.user.id,location_id=request.location,

        )
        data.save()
    return render(request,'clinical/credit_patient.html')


@login_required(login_url='/user_login')
def outstannding_amt_register(request):
    all_records = OPDBillSettlementTemp.objects.exclude(outstanding_amt='0').filter(location=request.location).order_by('-uhid')
    all_record = Credit.objects.filter(paid_amt__exact='0',location=request.location).order_by('-uhid')
    outstanding=[data.outstanding_amt for data in all_records]
    list = []
    for data in outstanding:
        if data != 0:
            all_ots_amt = OPDBillSettlementTemp.objects.filter(outstanding_amt=data)
            list.append(all_ots_amt)
    context={
        'all_records':all_records,'all_record':all_record
    }
    return render(request,'clinical/outstannding_amt_registe.html',context)

@login_required(login_url='/user_login')
def payer_by_report(request):
    payer_by = BillingGroup.objects.all()
    all = 0
    all_in = ''
    net_amt = 0
    net_disc = 0
    amt_pay = 0
    amt_paid = 0
    payer_name_all2=0
    list_opdbs=[]
    payer_names=[]
    payer_id = request.POST.get('payer_id')
    from_date = request.POST.get('b_start_date')
    to_date = request.POST.get('b_end_date')
    if request.method=="POST":
        if from_date and to_date and len(payer_id) != 0:
            from_date = request.POST.get('b_start_date').split("T")[0]
            to_date = request.POST.get('b_end_date').split("T")[0]
            payer_name = BillingGroup.objects.filter(id=payer_id)
            payer_nam = [data.billing_group for data in payer_name]
            payer_name_all = set(payer_nam)
            payer_name_all2 = list(payer_name_all)
        all=OpdBillingMain.objects.extra(select={
        'insurance_name': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',}).filter(billing_group_id=payer_id,location=request.location,bill_date_time__range=[from_date,to_date]).exclude(status='cancel')
        list_opdbs.append(all)
        payer_names.append(payer_name)
        all_in=zip(list_opdbs,payer_names)
        net_amt = OpdBillingMain.objects.filter(bill_date_time__range=[from_date,to_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('net_amount'))
        net_amt = net_amt['net_amount__sum']
        net_disc = OpdBillingMain.objects.filter(bill_date_time__range=[from_date,to_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('discount'))
        net_disc = net_disc['discount__sum']
        amt_pay = OpdBillingMain.objects.filter(bill_date_time__range=[from_date,to_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('pay_amount'))
        amt_pay = amt_pay['pay_amount__sum']
        amt_paid = OpdBillingMain.objects.filter(bill_date_time__range=[from_date,to_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('paid_amount'))
        amt_paid = amt_paid['paid_amount__sum']
    context={
        'payer_by':payer_by,'all':all,"all_in":all_in,'payer_name_all2':payer_name_all2,"to_date":to_date,"from_date":from_date,"net_amt":net_amt,
        "net_disc":net_disc,"amt_pay":amt_pay,"amt_paid":amt_paid
    }
    return render(request,'clinical/payer_by_report.html',context)

@login_required(login_url='/user_login')
def report_datewise_bill(request):
    all_ots_amt = 0
    total_receivable_amt = 0
    total_received_amt = 0
    total_outstanding_amt = 0
    if request.method == "POST":
        from_date = request.POST.get('b_start_date')
        to_date = request.POST.get('b_end_date')
        if from_date and to_date:
            all_ots_amt = OPDBillSettlementTemp.objects.filter(Q(settle_date_time__range=[from_date,to_date],location=request.location)&Q(outstanding_amt='0',location=request.location)).order_by('-settle_date_time')
            total_received_amt = OPDBillSettlementTemp.objects.filter(Q(settle_date_time__range=[from_date,to_date],location=request.location)&Q(outstanding_amt='0',location=request.location)).aggregate(Sum('received_amt'))
            total_received_amt = total_received_amt['received_amt__sum']
            total_receivable_amt = OPDBillSettlementTemp.objects.filter(Q(settle_date_time__range=[from_date,to_date],location=request.location)&Q(outstanding_amt='0',location=request.location)).aggregate(Sum('receivable_amt'))
            total_receivable_amt = total_receivable_amt['receivable_amt__sum']
            total_outstanding_amt = OPDBillSettlementTemp.objects.filter(Q(settle_date_time__range=[from_date,to_date],location=request.location)&Q(outstanding_amt='0',location=request.location)).aggregate(Sum('outstanding_amt'))
            total_outstanding_amt = total_outstanding_amt['outstanding_amt__sum']
        context={
            'all_ots_amt':all_ots_amt,'total_receivable_amt':total_receivable_amt,'total_received_amt':total_received_amt,
            'total_outstanding_amt':total_outstanding_amt
        }
        return render(request,'clinical/report_datewise_bill.html',context)
    return render(request, 'clinical/report_datewise_bill.html')

@login_required(login_url='/user_login')
def mode_of_payment(request):
    all = 0
    payer_id = 0
    if request.method == "POST":
        payer_id = request.POST.get('mode_of_payment')
        start_date = request.POST.get('b_start_date')
        end_date = request.POST.get('b_end_date')
        all = OPDBillSettlementTemp.objects.filter(status2 = payer_id,location=request.location).order_by('-settle_date_time')
        if start_date and end_date and len(payer_id) != 0:
            all = OPDBillSettlementTemp.objects.filter(settle_date_time__range = [start_date,end_date],status2 = payer_id,location=request.location).order_by('-settle_date_time')
    context = {
        'all':all,'payer_id':payer_id,
    }
    return render(request,'clinical/mode_of_payment.html',context)

# ===================== Opd package ======================
@login_required(login_url='/user_login')
def opd_package_master(request):
    records = OpdPackageMaster.objects.all()
    form = OpdPackageMasterForm()
    if request.method == "POST":
        form = OpdPackageMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/opd_package_master')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/opd_package/opd_package_master.html', context)


@login_required(login_url='/user_login')
def opd_package_master_view(request):
    records = OpdPackageMaster.objects.all()
    form = OpdPackageMasterForm()
    if request.method == "POST":
        form = OpdPackageMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/opd_package_master')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/opd_package/opd_package_master_view.html', context)



@login_required(login_url='/user_login')
def opd_package_master_edit(request, pk):
    # name = request.session['Name']
    opd_package_master = OpdPackageMaster.objects.get(id=pk)
    form = OpdPackageMasterForm(instance=opd_package_master)
    editing = 'editing'
    if request.method == 'POST':
        form = OpdPackageMasterForm(request.POST, instance=opd_package_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/opd_package_master_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/opd_package/opd_package_master_edit.html', context)



#======================== For Package Creation 06/06/2023 =======================================
@login_required(login_url='/user_login')
def opd_package_service(request):
    # name = request.session['Name']
    opd_package_master = OpdPackageMaster.objects.all()
    package_list = [data.package_name for data in opd_package_master]
    ser_dep_records = ServiceDepartment.objects.all()
    ser_sub_dep_records = ServiceSubDepartment.objects.all()
    service_master = ServiceMaster.objects.all()
    opd_main=OpdPackageService_main.objects.all()
    item = [data.service_name for data in service_master]
    services_btn = request.POST.get('services_btn')
    package_name = ''
    if services_btn == 'services_btn':
        # package_name = request.POST.get('package_name')
        # request.session['package_name'] = package_name
        request.session['package_name'] = request.POST.get('package_name')
        request.session['department'] = request.POST.get('department')
        request.session['sub_department'] = request.POST.get('sub_department')
        print(request.session['package_name'])
        print(request.session['department'])
        print(request.session['sub_department'])
        return HttpResponseRedirect('/opd_package_service_add')

    context = {
        'package_list': package_list, 'package_name': package_name, 'item': item, "add_service": 'add_service','opd_main':opd_main,
        'ser_dep_records': ser_dep_records, 'ser_sub_dep_records': ser_sub_dep_records,'opd_package_master':opd_package_master,

    }
    return render(request, 'general_master/opd_package/opd_package_service.html', context)

def opd_add_service_delete(request,pk):
    OpdPackageService_temp.objects.get(id=pk).delete()
    return redirect('opd_package_service_add')


# #==========================================================================================================
@login_required(login_url='/user_login')
def opd_package_service_add(request):
    # name = request.session['Name']
    package_name = request.session['package_name']
    department=request.session['department']
    sub_department=request.session['sub_department']
    package_master = OpdPackageMaster.objects.get(id=package_name)
    package_amount = package_master.package_amount
    service_master = ServiceMaster.objects.all()
    service_item = [data.service_name for data in service_master]
    profile_master = ProfileMaster.objects.all()
    profile_item = [data.profile_name for data in profile_master]
    records = OpdPackageService_temp.objects.filter(package_id=package_name)
    preview_record = ''
    records_id = [data.id for data in records]
    records_discount = [data.discount for data in records]
    if len(records_id) > 0:
        id_start = records_id[0]  # number of first id
    else:
        id_start = 0
    tot_id_len = id_start + len(records_id)  # number od last id
    id_count = len(records_id)  # count of record
    total = 0
    for data in records:
        total = total + data.net_amount
    before_total = 0
    for data in records:
        amount = data.quantity * data.rate
        before_total = before_total + amount
    preview = request.POST.get('preview')
    saving = request.POST.get('saving')
    total_net_amount = ''
    total_discount = ''
    msg = ''
    no_of_opdservices_main = OpdPackageService_main.objects.all().count()
    today = date.today()
    today = today.strftime("%y%m%d")
    if len(str(no_of_opdservices_main)) == 1:
        OPS_id = 'OPS' + today + '000' + str(no_of_opdservices_main)
    elif len(str(no_of_opdservices_main)) == 2:
        OPS_id = 'OPS' + today + '00' + str(no_of_opdservices_main)
    elif len(str(no_of_opdservices_main)) == 3:
        OPS_id = 'OPS' + today + '0' + str(no_of_opdservices_main)
    else:
        OPS_id = 'OPS' + today + str(no_of_opdservices_main)

    if request.method == 'POST':
        service_name = request.POST.getlist('service_name')
        print('service_name---->,',service_name)
        # profile_name = request.POST.getlist('profile_name')
        quantity = request.POST.getlist('quantity')
        discount = request.POST.getlist('discount')
        rate = request.POST.getlist('rate')
        net_amount = request.POST.getlist('n_amount')
        total_net_amount = request.POST.get('total_amount')
        records_getting = OpdPackageService_temp.objects.filter(id__in=service_name)
        total_discount = 0
        for data in discount:
            total_discount = int(data) + total_discount
        print('total_net_amount', total_net_amount, total_discount)
        if saving == 'saving':
            ser_name = []
            qua = []
            dis = []
            rat = []
            net_amt = []
            for data in service_name:
                ser_name.append(data)
            for data in quantity:
                qua.append(data)
            for data in discount:
                dis.append(data)
            for data in rate:
                rat.append(data)
            for data in net_amount:
                net_amt.append(data)
            for dat in records_getting:
                opd_package_sub = OpdPackageService(
                    package_id=OPS_id,
                    service_department=dat.service_department,
                    service_sub_department=dat.service_sub_department,
                    package_name=dat.package_name,
                    service_name=dat.service_name,
                    profile_name=dat.profile_name,
                    quantity=dat.quantity,
                    discount=dat.discount,
                    rate=dat.rate,
                    net_amount=dat.net_amount,
                    status=dat.status,
                )
                opd_package_sub.save()
            service_count = OpdPackageService_temp.objects.all().count()
            opd_package_main = OpdPackageService_main.objects.get_or_create(
                package_id=OPS_id,package_name_id=records_getting.last().package_name.id, total_services=service_count, before_total_amt=before_total,
                total_discount=total_discount, after_total_amt=total_net_amount
            )
            OpdPackageService_temp.objects.filter(package_id=package_name).delete()
            return HttpResponseRedirect('/opd_package_service')
        if preview == 'preview':
            if float(package_amount) == float(total_net_amount):
                print('blanced')
                records = ''
                preview_record = zip(service_name, quantity, discount, rate, net_amount)
            else:
                messages.success(request, 'Total amount is not Balanced to package amoount....!')
                print('unbalnce')

    context = {
        'package_name': 'package_name', 'service_item': service_item,'profile_item':profile_item,
        'total': total, 'tot_id_len': tot_id_len, 'id_start': id_start, 'id_count': id_count,
        'records_discount': records_discount, 'records_id': records_id,
        'preview': preview_record, 'total_net_amount': total_net_amount, 'total_discount': total_discount,
        'before_total': before_total, 'package_amount': package_amount,'profile_master':profile_master,
        'msg': msg,'records':records,'department':department,'sub_department':sub_department,'service_master':service_master,
    }
    return render(request, 'general_master/opd_package/opd_package_service.html', context)

@login_required(login_url='/user_login')
def opd_package_service_temp(request,serv):
    department=request.session['department']
    sub_department=request.session['sub_department']
    package_name = request.session['package_name']
    print('package_name=========>,',package_name)
    service_name = ServiceMaster.objects.get(id=serv)
    print('service_name---->,',service_name)
    service_master = ServiceMaster.objects.all()
    # service_master = [data.service_name for data in service_master_all]
    records = OpdPackageService_temp.objects.filter(package_id=package_name)
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        print('======service_name=======,',service_name)
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        rate = request.POST.get('rate')
        net_amount = request.POST.get('net_amount')
        temp_data = OpdPackageService_temp(
            package_id=package_name,
            service_department_id=department,
            service_sub_department_id=sub_department,
            package_name_id=package_name,
            service_name_id=service_name,
            quantity=quantity,
            discount=discount,
            rate=rate,
            net_amount=net_amount,
            status='service_name',
        )
        temp_data.save()
        return HttpResponseRedirect('/opd_package_service_add')
    context = {
        'service_name': service_name,'package_name': 'package_name', 'service_master': service_master, 'records': records,
        'package_name': package_name,
    }
    return render(request, 'general_master/opd_package/opd_package_service.html', context)

#=================== OPD Package Profile 02/06/23 ===========================
@login_required(login_url='/user_login')
def opd_package_profile_temp(request,serv):
    department=request.session['department']
    sub_department=request.session['sub_department']
    package_name = request.session['package_name']
    profile_name = ProfileMaster.objects.get(id=serv)
    service_master_all = ServiceMaster.objects.all()
    item = [data.service_name for data in service_master_all]
    records = OpdPackageService_temp.objects.filter(package_id=package_name)

    if request.method == 'POST':
        prifiles_name = request.POST.get('service_name')
        print('======service_name=======,',prifiles_name)
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        rate = request.POST.get('rate')
        net_amount = request.POST.get('net_amount')
        temp_data = OpdPackageService_temp(
            package_id=package_name,
            service_department_id=department,
            service_sub_department_id=sub_department,
            package_name_id=package_name,
            profile_name_id=prifiles_name,
            quantity=quantity,
            discount=discount,
            rate=rate,
            net_amount=net_amount,
            status='profile_name',
        )
        temp_data.save()
        return HttpResponseRedirect('/opd_package_service_add')
    context = {
        'profile_name': profile_name, 'package_name': package_name, 'item': item, 'records': records,
    }
    return render(request, 'general_master/opd_package/opd_package_service.html', context)
#==================== END PACKAGE CREATION ==============================================
#=========================== opd package link with tariff =========================
@login_required(login_url='/user_login')
def link_opdpackage_tariff(request):
    tariff_data=TariffMaster.objects.all()
    opd_package_data=OpdPackageMaster.objects.all()
    opd_link_data=TarifLinkOpdPackage.objects.all()
    if request.method=="POST":
        tariff_name=request.POST.get('tariff_name')
        opd_pacake_name=request.POST.get('opdpackage_name')
        apply_date=request.POST.get('apply_from')
        data=TarifLinkOpdPackage(
            tariff_id=tariff_name,
            opd_package_id=opd_pacake_name,
            apply_date=apply_date,
        )
        data.save()
        return HttpResponseRedirect('/link_opdpackage_tariff')
    context={
        'tariff_data':tariff_data,'opd_package_data':opd_package_data,'opd_link_data':opd_link_data,
    }
    return render(request,'clinical/link_opdpackage_tariff.html',context)

#bed view wardcategory filter

def load_ward_category(request):
    wardtype=request.GET.get('Ward_type')
    print('wardtype',wardtype)
    floor=BedMaster.objects.filter(ward_category=wardtype)
    print(floor)
    # return render(request,'try/city_dropdown.html',{'cities':cities})
    return JsonResponse(list(floor.values('id','room_number')),safe=False)

def admission_load(request):
    print("admission_load")
    ward_type_id = request.GET.get('ward_type_id')
    ward_cat_id = request.GET.get('ward_cat_id')
    print(ward_type_id, ward_cat_id)
    if ward_cat_id is None:
        ward_type = AdmissionWardCate.objects.filter(ward_type_id=ward_type_id)
        data = list(ward_type.values('id', 'category_name'))
        print('data', data)
    else:
        ward_name = AdmissionWardType.objects.get(id=ward_type_id)
        ward_cat = AdmissionWardCate.objects.get(id=ward_cat_id)

        bed_no = BedMasterMain.objects.filter(ward_category=ward_cat.category_name,
                                              status__in=['Active', 'un_occupied'])
        data = list(bed_no.values('id', 'bed_no'))
    return JsonResponse(data, safe=False)

@login_required(login_url='/user_login')
def doctor_accounting(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'doctor_accounting_services' in access.user_profile.screen_access:
        if True:
            tariff=0
            tariff_name=0
            dr_name=0
            date=0
            doctor_name=0
            tarif_name=0
            service_departments=0
            service_sub_departments=0
            ser_dep=0
            ser_sub_dep=0
            records=''
            records_id=''
            service_charge=''
            records_sm=''
            id_count_d=''
            doctor_table=DoctorTable.objects.filter()
            tariff_table=TariffMaster.objects.all()
            dr_acc=DoctorAccounting.objects.filter()
            service_department=ServiceDepartment.objects.all()
            service_sub_department=ServiceSubDepartment.objects.all()
            search1 = request.POST.get('search1')
            print('search1',search1)
            search2 = request.POST.get('search2')
            save_btn = request.POST.get('insert')
            print('search2',search2)
            if request.method=="POST":
                dr_name = request.POST.get('dr_name')
                tariff_name = request.POST.get('tariff_name')
                dr_names=request.POST.get('dr_names')
                tariff_names=request.POST.get('tariff_names')
                service_name=request.POST.getlist('service_name')
                service_rate=request.POST.getlist('service_rate')
                dr_share=request.POST.getlist('dr_share')
                hospital_share=request.POST.getlist('hospital_share')
                date=request.POST.get('date')
                dates=request.POST.get('dates')
                service_departments=request.POST.get('service_departments')
                service_sub_departments=request.POST.get('service_sub_departments')
                if save_btn == 'insert':
                    for record in range(len(service_name)):
                        var_tariff_name=tariff_names
                        var_dr_name=dr_names
                        var_service_name=service_name[record]
                        var_service_rate=service_rate[record]
                        var_dr_share=dr_share[record]
                        var_hospital_share=hospital_share[record]
                        var_date=dates
                        dataa = DoctorAccounting.objects.filter(doctor_id=var_dr_name, tariff_id=var_tariff_name,
                                                                service_name=var_service_name)
                        if not dataa.exists():
                            Dr_acc=DoctorAccounting(
                                service_name=var_service_name,
                                service_rate=var_service_rate,
                                doctor_id=var_dr_name,
                                tariff_id=var_tariff_name,
                                doctor_share=var_dr_share,
                                hospital_share=var_hospital_share,
                                date=var_date,created_by_id=request.user.id,location_id=request.location,
                            )
                            Dr_acc.save()
                        else:
                            messages.success(request, 'This Data Already Exist')
            if service_departments and service_sub_departments:
                s_d = ServiceDepartment.objects.get(id=service_departments)
                s_s_d = ServiceSubDepartment.objects.get(id=service_sub_departments)
                ser_dep=s_d.service_department
                ser_sub_dep=s_s_d.service_sub_department
                records=ServiceMaster.objects.filter(Q(ServiceSubDepartment_id=service_sub_departments)&Q(service_department_id=service_departments)).exclude(service_name__in=DoctorAccounting.objects.values('service_name'))
                id_count_d=records.count()
            elif tariff_name:
                tariff = ServiceChargeMaster.objects.filter(tariff_id=tariff_name).exclude(service_id__in=DoctorAccounting.objects.values('service_name'))
                service_charge = [data.service_charge for data in tariff]
                records_id = [data.id for data in tariff]
            if len(records_id) > 0:
                id_start = records_id[0]  # number of first id
            else:
                id_start = 0
            tot_id_len = id_start + len(records_id)  # number od last id
            id_count = len(records_id)  # count of record
            if dr_name:
                doctor_table_name = DoctorTable.objects.get(doctor_id=dr_name)
                doctor_name = doctor_table_name.doctor_name
                tariff_table_name = TariffMaster.objects.get(id=tariff_name)
                tarif_name = tariff_table_name.tariff_name
            context={
                'doctor_table':doctor_table,'tariff_table':tariff_table,'tariff':tariff,'doctor_name':doctor_name,
                'tarif_name':tarif_name,'dr_acc':dr_acc,'date':date,'dr_name':dr_name,'tariff_name':tariff_name,
                'records':records,'ser_dep':ser_dep,
                'service_department':service_department,'service_sub_department':service_sub_department,'ser_sub_dep':ser_sub_dep,
                'tot_id_len':tot_id_len,'id_count':id_count,'service_charge':service_charge,'id_count_d':id_count_d,'access':access

            }
            return render(request,'clinical/doctor_accounting.html',context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def dr_accounting_report(request):
    each_dr_name=''
    bill_records=''
    bill_count=''
    karan=''
    karannn=''
    kumar=''
    dr_total_share=''
    summ=''
    g_tot_amt_sum_list = []
    list_dr=DoctorTable.objects.all().order_by('doctor_id')
    summ_bill=request.POST.get('sum_bill')
    detail_bill=request.POST.get('detail_bill')
    g_tot_amt_list = []
    g_tot_amt_list1 = []
    if detail_bill=='Detail_Bill':
        if request.method=="POST":
            doctorlist = request.POST.get('doctorlist')
            start_date = request.POST.get('s_date')
            end_date = request.POST.get('e_date')
            each_dr_name = DoctorTable.objects.get(doctor_id=doctorlist)
            sub_datas2 = OpdBillingSub.objects.filter(Q(bill_date_time__range=[start_date,end_date])&Q(doctor_name__exact=each_dr_name)).order_by('-id')
            uhid_id = [data.uhid for data in sub_datas2]
            uhid_one = set(uhid_id)
            deatils = []
            patient_bill_details = []
            tot_amt_list=[]
            # g_tot_amt_list=[]
            for uhid in uhid_one:
                patient_details = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
                opd_bill_records1 = OpdBillingSub.objects.filter(Q(bill_date_time__range=[start_date,end_date])&Q(uhid=uhid, doctor_name=each_dr_name)).order_by('-id')
                single_patient = []
                opd_bill_list=[]
                single_date_list = []
                opd_records1=[data.bill_no for data in opd_bill_records1]
                opd_records_bill_date1=[data.bill_date_time for data in opd_bill_records1]
                opd_records=list(set(opd_records1))
                opd_record_bill_date=list(set(opd_records_bill_date1))
                mantu=zip(opd_records,opd_record_bill_date)
                em = 'Not Define'
                tot_amt_list1=[]
                tot_amt_listO=[]
                for data_bill,data_date in mantu:
                    opd_list_record=[]
                    opd_bill_list.append(data_bill)
                    single_date_list.append(data_date)
                    opd_bill_records = OpdBillingSub.objects.filter(bill_no=data_bill).order_by('-id')
                    for data1 in opd_bill_records:
                        doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist, service_name=data1.service_id,service_rate=data1.charges).last()
                        if doctor_share is None:
                            opd_list_record.append([data1.service_id, data1.charges,em])

                        else:
                            opd_list_record.append([data1.service_id, data1.charges,doctor_share.doctor_share])

                    single_patient.append(opd_list_record)

                    # ======= FOR SERVICE RATE WISE TOTAL AMT =============================
                    tot_amountO = 0
                    for amtO in opd_bill_records:
                        tot_amountO = tot_amountO + int(amtO.charges)
                    tot_amt_listO.append(tot_amountO)
                    #======= FOR BILL NO WISE TOTAL AMT =============================
                    tot_amount1=0
                    for amt in opd_bill_records:
                        rates = int(amt.charges)
                        doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist,
                                                                       service_name=amt.service_id,
                                                                       service_rate=amt.charges).last()
                        if doctor_share:
                            tot_amount1 = tot_amount1 + int(doctor_share.doctor_share)
                    tot_amt_list1.append(tot_amount1)
                    # print('tot_amt_list1',tot_amt_list1)
                #======= FOR UHID NO WISE TOTAL AMT =============================
                tot_amount=0
                for amt in opd_bill_records1:
                    rates = int(amt.charges)
                    doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist, service_name=amt.service_id,service_rate=amt.charges).last()
                    if doctor_share :
                        tot_amount = tot_amount+int(doctor_share.doctor_share)
                tot_amt_list.append(tot_amount)

                patient_bill_details.append(zip(single_patient,opd_bill_list,single_date_list,tot_amt_listO,tot_amt_list1))
                deatils.append([patient_details.uhid, patient_details.first_name, patient_details.age,patient_details.gender])
            karan = zip(deatils,patient_bill_details,tot_amt_list)
            #======= FOR GRAND TOTAL DOCTOR SHARE =============================
            g_tot_amount = 0
            for g_total in sub_datas2:
                rates=int(g_total.charges)
                doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist,
                                                               service_name=g_total.service_id,
                                                               service_rate=g_total.charges).last()
                if doctor_share:
                    g_tot_amount = g_tot_amount + int(doctor_share.doctor_share)
            g_tot_amt_list.append(g_tot_amount)
            # ======= FOR GRAND TOTAL SERVICE RATE =============================
            g_tot_amount1 = 0
            for g_total1 in sub_datas2:
                # tot=g_total1.charges
                g_tot_amount1 = g_tot_amount1 + int(g_total1.charges)
            g_tot_amt_list1.append(g_tot_amount1)

    if summ_bill=='Sum_Bill':
        if request.method == "POST":
            doctorlist = request.POST.get('doctorlist')
            start_date = request.POST.get('s_date')
            end_date = request.POST.get('e_date')
            each_dr_name = DoctorTable.objects.get(doctor_id=doctorlist)
            doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist)
            sub_datas2 = OpdBillingSub.objects.filter(
                Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(doctor_name__exact=each_dr_name,location=request.location)).order_by('-bill_date_time')
            uhid_id = [data.uhid for data in sub_datas2]
            uhid_one = set(uhid_id)
            deatils = []
            patient_bill_details = []
            tot_amt_list = []
            tot_amt_list10 = []
            # g_tot_amt_list=[]
            for uhid in uhid_one:
                patient_details = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
                opd_bill_records1 = OpdBillingSub.objects.filter(
                    Q(bill_date_time__range=[start_date, end_date],location=request.location) & Q(uhid=uhid, doctor_name=each_dr_name,location=request.location)).order_by('-bill_date_time')
                single_patient = []
                opd_bill_list = []
                single_date_list = []
                opd_records1 = [data.bill_no for data in opd_bill_records1]
                opd_records_bill_date1 = [data.bill_date_time for data in opd_bill_records1]
                opd_records = list(set(opd_records1))
                opd_record_bill_date = list(set(opd_records_bill_date1))
                mantu = zip(opd_records, opd_record_bill_date)
                em = 'Not Define'
                tot_amt_list1 = []
                tot_amt_listO = []
                for data_bill, data_date in mantu:
                    opd_list_record = []
                    opd_bill_list.append(data_bill)
                    single_date_list.append(data_date)
                    # print('single_date_list',single_date_list)
                    opd_bill_records = OpdBillingSub.objects.filter(bill_no=data_bill)
                    for data1 in opd_bill_records:
                        doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist,
                                                                       service_name=data1.service_id,
                                                                       service_rate=data1.charges).last()
                        if doctor_share is None:
                            opd_list_record.append([data1.service_id, data1.charges, em])

                        else:
                            opd_list_record.append([data1.service_id, data1.charges,
                                                    doctor_share.doctor_share])
                    single_patient.append(opd_list_record)
                    # # ======= FOR SERVICE RATE WISE TOTAL AMT =============================
                    tot_amountO = 0
                    for amtO in opd_bill_records:
                        tot_amountO = tot_amountO + int(amtO.charges)
                    tot_amt_listO.append(tot_amountO)
                    # ======= FOR BILL NO WISE TOTAL AMT =============================
                    tot_amount1 = 0
                    for amt in opd_bill_records:
                        doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist,
                                                                       service_name=amt.service_id,
                                                                       service_rate=amt.charges).last()
                        if doctor_share:
                            tot_amount1 = tot_amount1 + int(doctor_share.doctor_share)
                    tot_amt_list1.append(tot_amount1)
                # ======= FOR UHID NO WISE TOTAL AMT =============================
                tot_amount = 0
                for amt in opd_bill_records1:
                    doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist,
                                                                   service_name=amt.service_id,
                                                                   service_rate=amt.charges).last()
                    if doctor_share:
                        tot_amount = tot_amount + int(doctor_share.doctor_share)
                tot_amt_list.append(tot_amount)
                # ======= FOR UHID SERVICE RATE WISE TOTAL AMT =============================
                tot_amount10 = 0
                for amtO in opd_bill_records1:
                    tot_amount10 = tot_amount10 + int(amtO.charges)
                tot_amt_list10.append(tot_amount10)

                patient_bill_details.append(zip(opd_bill_list,single_date_list,tot_amt_listO,tot_amt_list1))
                deatils.append([patient_details.uhid, patient_details.first_name, patient_details.age,
                                patient_details.gender])
            karannn = zip(deatils, patient_bill_details,tot_amt_list10, tot_amt_list)
            # kumar = zip(opd_bill_list, single_date_list,tot_amt_list10, tot_amt_list1)

            # ======= FOR GRAND TOTAL DOCTOR SHARE =============================
            g_tot_amount = 0
            for g_total in sub_datas2:
                doctor_share = DoctorAccounting.objects.filter(doctor_id=doctorlist,
                                                               service_name=g_total.service_id,
                                                               service_rate=g_total.charges).last()
                if doctor_share:
                    g_tot_amount = g_tot_amount + int(doctor_share.doctor_share)
            g_tot_amt_list.append(g_tot_amount)
            # ======= FOR GRAND TOTAL SERVICE RATE =============================
            g_tot_amount1 = 0
            for g_total1 in sub_datas2:
                # tot=g_total1.charges
                g_tot_amount1 = g_tot_amount1 + int(g_total1.charges)
            g_tot_amt_list1.append(g_tot_amount1)

    context={
        'list_dr':list_dr,'each_dr_name':each_dr_name,'bill_records':bill_records,'bill_count':bill_count,
        'karan':karan,'dr_total_share':dr_total_share,'g_tot_amt_list':g_tot_amt_list,'summ':summ,'g_tot_amt_sum_list':g_tot_amt_sum_list,
        'g_tot_amt_list1':g_tot_amt_list1,'karannn':karannn,
    }
    return render(request,'clinical/add_share.html',context)


@login_required(login_url='/user_login')
def all_data_insert(request):
    all=OpdBillingSub.objects.all()
    for data in all:
        a=OpdBillingGetDelete(bill_no=data.bill_no,
                              bill_id=data.bill_id,
                              uhid=data.uhid,
                              bill_date_time=data.bill_date_time,
                              department=data.department,
                              visit_no=data.visit_no,
                              corporate_id=data.corporate_id,
                              billing_group_id=data.billing_group_id,
                              service_id=data.service_id,
                              charges=data.charges,
                              unit=data.unit,
                              pay_amount=data.pay_amount,
                              paid_amount=data.paid_amount,
                              outstanding_amount=data.outstanding_amount,
                              payment_mode=data.payment_mode,
                              total_amount=data.total_amount,
                              discount=data.discount,
                              )
        a.save()
        return HttpResponseRedirect('/all_data_insert')

@login_required(login_url='/user_login')
def profile_master(request):
    records = ProfileMaster.objects.all()
    form = ProfileMasterForm()
    if request.method == "POST":
        form = ProfileMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile_master')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'clinical/profile/profile_master.html', context)

@login_required(login_url='/user_login')
def profile_master_view(request):
    records = ProfileMaster.objects.all()
    form = ProfileMasterForm()
    if request.method == "POST":
        form = ProfileMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile_master_view')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'clinical/profile/profile_master_view.html', context)

@login_required(login_url='/user_login')
def profile_master_edit(request,pk):
    # name = request.session['Name']
    profile_master = ProfileMaster.objects.get(id=pk)
    form = ProfileMasterForm(instance=profile_master)
    editing = 'editing'
    if request.method == 'POST':
        print('this is post method')
        form = ProfileMasterForm(request.POST,instance=profile_master)
        print('this is post method1111')
        if form.is_valid():
            print('for valid============', form)
            form.save()
            return HttpResponseRedirect('/profile_master')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request,'clinical/profile/profile_master_edit.html', context)

# after lunch 14/12/22 =============================
@login_required(login_url='/user_login')
def profile_service(request):
    opd_profile_master = ProfileMaster.objects.exclude(profile_name__in=ProfileService.objects.values('profile_name'))
    package_list = [data.profile_name for data in opd_profile_master]
    ser_dep_records = ServiceDepartment.objects.all()
    ser_sub_dep_records = ServiceSubDepartment.objects.all()
    service_master = Service_Test.objects.all()
    item = [data.test_name for data in service_master]
    services_btn = request.POST.get('services_btn')
    package_name = ''
    if services_btn == 'services_btn':
        request.session['profile_name'] = request.POST.get('profile_name')
        request.session['department'] = request.POST.get('department')
        request.session['sub_department'] = request.POST.get('sub_department')
        request.session['out_source'] = request.POST.get('out_source')
        print(request.session['profile_name'])
        print(request.session['department'])
        print(request.session['sub_department'])
        print(request.session['out_source'])
        return HttpResponseRedirect('/profile_service_add')

    context = {
        'package_list': package_list, 'package_name': package_name, 'item': item, "add_service": 'add_service',
        'ser_dep_records':ser_dep_records,'ser_sub_dep_records':ser_sub_dep_records

    }
    return render(request, 'clinical/profile/profile_service.html', context)


@login_required(login_url='/user_login')
def profile_service_add(request):
    # name = request.session['Name']
    package_name = request.session['profile_name']
    department=request.session['department']
    sub_department=request.session['sub_department']
    out_source=request.session['out_source']
    if out_source == None :
        source = False
        source_save=0
    elif out_source == 'on' :
        source = True
        source_save=1
    print('package_name---------------------',package_name,department,sub_department)
    package_master = ProfileMaster.objects.get(profile_name=package_name)
    package_amount = package_master.profile_amount
    service_master = Service_Test.objects.filter(service_department=department,ServiceSubDepartment=sub_department,test_name__in=ServiceMaster.objects.filter(outsource=source).values('id'))
    item = [data.test_name for data in service_master]
    records = ProfileService_temp.objects.all()
    preview_record = ''
    records_id = [data.id for data in records]
    records_discount = [data.service_name for data in records]
    if len(records_id) > 0:
        id_start = records_id[0]  # number of first id
    else:
        id_start = 0
    preview = request.POST.get('preview')
    saving = request.POST.get('saving')
    total_net_amount = ''
    total_discount = ''
    msg = ''

    no_of_opdservices_main = ProfileService_main.objects.all().count()
    profile_service=ProfileService.objects.filter(profile_name=package_name,service_department=department,service_sub_department=sub_department)
    today = date.today()
    today = today.strftime("%y%m%d")
    if len(str(no_of_opdservices_main)) == 1:
        OPS_id = 'PRO' + today + '000' + str(no_of_opdservices_main)
    elif len(str(no_of_opdservices_main)) == 2:
        OPS_id = 'PRO' + today + '00' + str(no_of_opdservices_main)
    elif len(str(no_of_opdservices_main)) == 3:
        OPS_id = 'PRO' + today + '0' + str(no_of_opdservices_main)
    else:
        OPS_id = 'PRO' + today + str(no_of_opdservices_main)

    if request.method == 'POST':
        service_name = request.POST.getlist('service_name')
        infant_range = request.POST.getlist('infant_range')
        chield_range = request.POST.getlist('chield_range')
        male_range = request.POST.getlist('male_range')
        female_range = request.POST.getlist('female_range')
        units = request.POST.getlist('units')
        print("rate",infant_range,male_range,chield_range)

        for i in range(len(service_name)):
            service_name_sub = service_name[i]
            infant_range_sub = infant_range[i]
            chield_range_sub = chield_range[i]
            male_range_sub = male_range[i]
            female_range_sub = female_range[i]
            units_sub = units[i]
            opd_package_sub = ProfileService(
                profile_id=OPS_id,
                service_department=department,
                service_sub_department=sub_department,
                profile_name=package_name,
                service_name=service_name_sub,
                infant_range=infant_range_sub,
                chield_range=chield_range_sub,
                male_range=male_range_sub,
                female_range=female_range_sub,
                units=units_sub,
                outsource=source_save,
            )
            opd_package_sub.save()
        service_count = ProfileService_temp.objects.all().count()
        opd_package_main = ProfileService_main.objects.get_or_create(
            profile_id=OPS_id,
            service_department=department,
            service_sub_department=sub_department,
            total_services=service_count,
        )
        ProfileService_temp.objects.all().delete()
        return HttpResponseRedirect('/profile_service')

    context = {
        'package_name':package_name, 'item': item,'service_master_all':service_master,
        'records_discount': records_discount, 'records_id': records_id,
        'preview': preview_record, 'total_net_amount': total_net_amount,
        'package_amount': package_amount,'profile_service':profile_service,
        'msg': msg,'records':records,'department':department,'sub_department':sub_department
    }
    return render(request, 'clinical/profile/profile_service.html', context)


@login_required(login_url='/user_login')
def profile_service_temp(request, serv):
    package_name = request.session['profile_name']
    service_master = Service_Test.objects.get(test_name=serv)
    service_master_all = ServiceTest.objects.all()
    item = [data.test_name for data in service_master_all]
    records = ProfileService_temp.objects.all()
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        infant_range = request.POST.get('infant_range')
        chield_range = request.POST.get('chield_range')
        male_range = request.POST.get('male_range')
        female_range = request.POST.get('female_range')
        units = request.POST.get('units')
        temp_data = ProfileService_temp(
            service_name=service_name,
            infant_range=infant_range,
            chield_range=chield_range,
            male_range=male_range,
            female_range=female_range,
            units=units,
        )
        temp_data.save()
        return HttpResponseRedirect('/profile_service_add')
    context = {
        'service_master': service_master, 'package_name': 'package_name', 'item': item, 'records': records,'service_master_all':service_master_all,
        'package_name': package_name,
    }
    return render(request, 'clinical/profile/profile_service.html', context)

@login_required(login_url='/user_login')
def service_test(request):
    test_records=ServiceTest.objects.all()
    service_department=ServiceDepartment.objects.all()
    service_sub_department=ServiceSubDepartment.objects.all()
    department=request.POST.get('department')
    sub_department=request.POST.get('sub_department')

    print('kldfhnaisdh',department,sub_department)
    sevice_records=""
    if department and sub_department:
        sevice_records=ServiceMaster.objects.filter(service_department=department,ServiceSubDepartment=sub_department)
        print(sevice_records)
    context={
        'service_department':service_department,'service_sub_department':service_sub_department,
        "sevice_records":sevice_records
    }
    return render(request,'clinical/profile/service_test1.html',context)

@login_required(login_url='/user_login')
def service_test_search(request,dep,subdep):
    test_records=ServiceTest.objects.all()
    service_department=ServiceDepartment.objects.all()
    service_sub_department=ServiceSubDepartment.objects.all()
    if dep and subdep:
        ser_dep=ServiceDepartment.objects.get(service_department=dep)
        ser_sub_dep=ServiceSubDepartment.objects.get(service_sub_department=subdep)
        sevice_records=ServiceMaster.objects.filter(service_department=ser_dep.id,ServiceSubDepartment=ser_sub_dep.id)
        print(sevice_records)
    context={
        'service_department':service_department,'service_sub_department':service_sub_department,
        "sevice_records":sevice_records
    }
    return render(request,'clinical/profile/service_test1.html',context)

@login_required(login_url='/user_login')
def service_test_range(request,pk):
    sevice_records=''
    sevice_test_records=''
    if Service_Test.objects.filter(test_name_id=pk).exists():
        sevice_test_records=Service_Test.objects.get(test_name_id=pk)
        return HttpResponseRedirect(f'/service_test_range_edit/{pk}')
    else:
        sevice_records=ServiceMaster.objects.get(id=pk)
    if request.method=="POST":
        data=Service_Test(
            test_name_id=pk,
            service_category=sevice_records.service_category,
            service_sub_category=sevice_records.service_sub_category,
            service_department=sevice_records.service_department,
            ServiceSubDepartment=sevice_records.ServiceSubDepartment,
            infant_range=request.POST.get('infant_mini_range'),
            chield_range=request.POST.get('chield_max_range'),
            male_range=request.POST.get('male_max_range'),
            female_range=request.POST.get('female_max_range'),
            units=request.POST.get('units'),
            methodology=request.POST.get('methodology')
        )
        data.save( print('asfbhcioasfioasdbfibasfbaiosf'))
        # data1=ServiceTest_records(
        #     test_name=test_name,
        #     service_category=sevice_records.service_category,
        #     service_sub_category=sevice_records.service_sub_category,
        #     service_department=sevice_records.service_department,
        #     ServiceSubDepartment=sevice_records.ServiceSubDepartment,
        #     infant_range=infant_range,
        #     chield_range=chield_range,
        #     male_range=male_range,
        #     female_range=female_range,
        #     units=units,
        #     date_time=datetime.now(),
        #     logged_name='admin',
        #     methodology=methodology
        # )
        # data1.save()
        return HttpResponseRedirect(f'/service_test1/{sevice_records.service_department}/{sevice_records.ServiceSubDepartment}')
    context={
        "sevice_records":sevice_records,"sevice_test_records":sevice_test_records
    }
    return render(request,'clinical/profile/service_range.html',context)

@login_required(login_url='/user_login')
def service_test_range_edit(request,pk):
    sevice_test_records=Service_Test.objects.get(test_name_id=pk)
    if request.method=="POST":
        units=request.POST.get('units')
        methodologyy=request.POST.get('methodology')
        infant_range=request.POST.get('infant_mini_range')
        chield_range=request.POST.get('chield_max_range')
        male_range=request.POST.get('male_max_range')
        female_range=request.POST.get('female_max_range')
        sevice_test_records.infant_range=infant_range
        sevice_test_records.chield_range=chield_range
        sevice_test_records.male_range=male_range
        sevice_test_records.female_range=female_range
        sevice_test_records.units=units
        sevice_test_records.methodology=methodologyy
        sevice_test_records.save()

        return HttpResponseRedirect(f'/service_test1/{sevice_test_records.service_department}/{sevice_test_records.ServiceSubDepartment}')
    context={
       "sevice_test_records":sevice_test_records,
    }
    return render(request,'clinical/profile/service_range.html',context)

# profile Package Link with tariff 16/12/22 ======================
@login_required(login_url='/user_login')
def profile_package_tarifflink(request):
    tariff_data=TariffMaster.objects.all()
    profile_data=ProfileMaster.objects.all()
    profile_link_data=ProfileMasterlinkTarrif.objects.all()
    if request.method=="POST":
        tariff_name=request.POST.get('tariff_name')
        profile_id=request.POST.get('profile_id')
        apply_date=request.POST.get('apply_from')
        data=ProfileMasterlinkTarrif(
            tariff_id=tariff_name,
            profile_id=profile_id,
            apply_date=apply_date,
        )
        data.save()
        return HttpResponseRedirect('/profile_package_tarifflink')
    context={
        'tariff_data':tariff_data,'profile_data':profile_data,'profile_link_data':profile_link_data,
    }
    return render(request,'clinical/profile/profile_package_tarifflink.html',context)

# ========== karan {16-12-2022}===============

@login_required(login_url='/user_login')
def sample_master(request):
    records=SampleMaster.objects.all()
    form=SampleMasterForm()
    if request.method=='POST':
        form=SampleMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sample_master')
        else:
            print(form.errors)

    context={
        'form':form,'records':records
    }
    return render(request,'general_master/lab_master/sample_master.html',context)


@login_required(login_url='/user_login')
def volume_master(request):
    records=VolumeMaster.objects.all()
    form=VolumeMasterForm()
    if request.method=='POST':
        form=VolumeMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/volume_master')
        else:
            print(form.errors)

    context={
        'form':form,'records':records
    }
    return render(request,'general_master/lab_master/volume_master.html',context)

@login_required(login_url='/user_login')
def sample_master_edit(request):
    name=request.session['Name']
    records = SampleMaster.objects.all()
    form = SampleMasterForm()
    if request.method=='POST':
        form=SampleMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sample_master_edit')
    return render(request, 'general_master/lab_master/sample_master_edit.html',
                  {'records': records,'form':form,'login_name':name})

@login_required(login_url='/user_login')
def sample_master_editing(request,pk):
    name=request.session['Name']
    records = SampleMaster.objects.get(id=pk)
    form = SampleMasterForm(instance=records)
    if request.method == 'POST':
        form = SampleMasterForm(request.POST, instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sample_master_edit')
    return render(request, 'general_master/lab_master/sample_master_editing.html',
                  {'form': form,'login_name':name})

@login_required(login_url='/user_login')
def volume_master_edit(request):
    name=request.session['Name']
    records = VolumeMaster.objects.all()
    form = VolumeMasterForm()
    if request.method=='POST':
        form=VolumeMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/volume_master_edit')
    return render(request, 'general_master/lab_master/volume_master_edit.html',
                  {'records': records,'form':form,'login_name':name})

@login_required(login_url='/user_login')
def volume_master_editing(request,pk):
    name=request.session['Name']
    records = VolumeMaster.objects.get(id=pk)
    form = VolumeMasterForm(instance=records)
    if request.method == 'POST':
        form = VolumeMasterForm(request.POST, instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/volume_master_edit')
    return render(request, 'general_master/lab_master/volume_master_editing.html',
                  {'form': form,'login_name':name})

@login_required(login_url='/user_login')
def lab_pending_investigation(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'pending_investigation' in access.user_profile.screen_access:
        try:
            records=PendingInvestigation_main.objects.extra(select={
                        'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        }).filter(location=request.location).order_by('-date_time')

            sample_records=SampleMaster.objects.all()
            sample=[data.sample_name for data in sample_records]
            volume_records=VolumeMaster.objects.all()
            volume=[data.volume for data in volume_records]
            date_field=datetime.now()
            search_btn=request.POST.get('search_btn')
            if search_btn == 'search_btn':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')
                patient_name=request.POST.get('patient_name')
                if from_date and to_date and patient_name:
                    pat=PatientsRegistrationsAllInOne.objects.values('uhid').filter(first_name__contains=patient_name)
                    records=PendingInvestigation_main.objects.extra(select={
                        'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        }).filter(location=request.location,date_time__range=[from_date,to_date],uhid__in=pat).order_by('-date_time')
                elif from_date and to_date:
                    records=PendingInvestigation_main.objects.extra(select={
                        'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        }).filter(location=request.location,date_time__range=[from_date,to_date]).order_by('-date_time')

                elif patient_name:
                    pat=PatientsRegistrationsAllInOne.objects.values('uhid').filter(first_name__contains=patient_name)
                    records=PendingInvestigation_main.objects.extra(select={
                       'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        }).filter(location=request.location,uhid__in=pat).order_by('-date_time')
                else:
                   records=PendingInvestigation_main.objects.extra(select={
                        'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_pendinginvestigation_main.uhid',
                        }).filter(location=request.location).order_by('-date_time')


            context={
            'records':records,'sample':sample,'volume':volume,'date_field':date_field,'recc':records

            }
            return render(request,'lab_module/lab_pending_investigation.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def lab_sammple_collected(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'sample_collection' in access.user_profile.screen_access:
        try:
            collected_records=SampleCollected.objects.extra(select={
                'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).filter(status__in=['waiting','completed'],location=request.location).order_by('-date_time')
            contex={
                'collected_records':collected_records
            }
            return render(request,'lab_module/lab_sammple_collected.html',contex)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')
def lab_result_entry(request,pk):
    collected_records=SampleCollected.objects.filter(PTID=pk).exclude(status='vallidated')
    print(collected_records)
    records=[]
    for data in collected_records:
        record=[]
        entry_records=LabResultEntry.objects.filter(test_id=data.test_id)
        for data in entry_records:
            dict={}
            range_record=Service_Test.objects.filter(test_name__service_name__exact=data.service_name).last()
            if not range_record:
                messages.success(request, f'{data.service_name} this serive have no ranges')
                return redirect('lab_sammple_collected')
            pen=SampleCollected.objects.filter(test_id=data.test_id).last()
            reg=PatientsRegistrationsAllInOne.objects.filter(uhid=pen.uhid).last()
            if data.service_name == 'Age':
                value = reg.age
            else:
                value = data.value

            if reg.gender == 'Male':
                rangee = range_record.male_range
            elif reg.gender == 'Female':
                rangee = range_record.female_range
            else:
                rangee = range_record.male_range
            dict['service_name']=range_record.test_name
            dict['id']=data.id
            dict['range']=rangee
            dict['unit']=range_record.units
            dict['value']=value
            record.append(dict)
        records.append([data.profile_name,record])

    contex={
        'records':records,'pk':pk,
    }
    return render(request,'lab_module/lab_result_entry.html',contex)

def lab_result_save(request,pk):
    user_record=CreateUser.objects.filter(login_id=request.user).last()
    value_list=request.POST.getlist('value')
    rangee_list=request.POST.getlist('range')
    units_list=request.POST.getlist('units')
    id_list=request.POST.getlist('idss')

    for id,value,range,unit in zip(id_list,value_list,rangee_list,units_list):
        data=LabResultEntry.objects.get(id=id)
        data.value=value
        data.range=range
        data.units=unit
        try:
            ran=data.range.split("-")
            a=float(ran[0])
            b=float(ran[1])
            if float(value) >= a and float(value) <= b:
                data.value=value
                data.status='in_range'
            else:
                data.value=value
                data.status='out_range'
        except:
            data.value=value
            data.status='in_range'
        data.save()
    entry_records=LabResultEntry.objects.filter(id__in=id_list)
    for data in entry_records:
        entry_recordss=LabResultEntry_records(
            PTID=data.PTID,test_id=data.test_id,profile_id=data.profile_id,profile_name=data.profile_name,service_name=data.service_name,
            range=data.range,value=data.value,units=data.units,status=data.status,updated_by=request.user,

        )
        entry_recordss.save()
    collected_records=SampleCollected.objects.filter(test_id=entry_records.last().test_id).last()
    collected_records.status='completed'
    collected_records.result_entry_at=datetime.now()
    collected_records.result_entry_by=user_record
    collected_records.save()
    messages.success(request, 'Values Saved Successfully')
    return HttpResponseRedirect(f'/lab_result_entry/{pk}')

@login_required(login_url='/user_login')
def result_validation(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'result_validation' in access.user_profile.screen_access:
        try:
            collected_records=SampleCollected.objects.extra(select={
                'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).filter(status='completed',location=request.location).order_by('-date_time')
            context={
                'collected_records':collected_records
            }
            return render(request,'lab_module/result_validation.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def result_validation_view(request,pk):
    user_record=CreateUser.objects.filter(login_id=request.user).last()
    # entry_records=LabResultEntry.objects.filter(test_id=pk)
    # collected=SampleCollected.objects.filter(test_id=pk)
    # patient_records=PatientsRegistrationsAllInOne.objects.get(uhid=collected[0].uhid)
    # test_id_list=[data.test_id for data in entry_records]
    # test_id_list=list(set(test_id_list))
    # head=[]
    # body=[]
    # for data in test_id_list:
    #     result_records=LabResultEntry.objects.filter(test_id=data)
    #     body.append(result_records)
    #     head.append(result_records[0].profile_name)
    # records=zip(head,body)
    collected_records=SampleCollected.objects.filter(PTID=pk,status='completed')
    patient_records=PatientsRegistrationsAllInOne.objects.get(uhid=collected_records[0].uhid)
    print(collected_records)
    records=[]
    for data in collected_records:
        entry_records=LabResultEntry.objects.filter(test_id=data.test_id)
        records.append([data.profile_name,entry_records])
    if request.method=='POST':
        for data in collected_records:
            data.status='vallidated'
            data.validated_by=user_record
            data.validated_at=datetime.now()
            data.save()
            validate_data=data
            validate_record=Validation_record(
                PTID=validate_data.test_id,uhid=validate_data.uhid,validated_by=user_record.f_name,
                status="validated"
            )
            validate_record.save()
        return HttpResponseRedirect('/result_validation')
    context={
        'entry_records':entry_records,'pat':patient_records,'records':records
    }
    return render(request,'lab_module/result_validation_view.html',context)

@login_required(login_url='/user_login')
def lab_report(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'lab_report' in access.user_profile.screen_access:
        try:
            name=request.session['Name']
            doctor=request.session['doctor']
            collected=SampleCollected.objects.filter(status='vallidated')
            ptid_list=[data.PTID for data in collected]
            ptid_list=list(set(ptid_list))
            name=[]
            age=[]
            PTID=[]
            gender=[]
            date_time=[]
            uhid=[]
            for data in ptid_list:
                col_rec=SampleCollected.objects.filter(PTID=data).last()
                pat_rec=PatientsRegistrationsAllInOne.objects.get(uhid=col_rec.uhid)
                name.append(pat_rec.first_name)
                age.append(pat_rec.age)
                gender.append(pat_rec.gender)
                PTID.append(col_rec.PTID)
                date_time.append(col_rec.date_time)
                uhid.append(pat_rec.uhid)

            records=zip(name,age,PTID,gender,date_time,uhid)
            context={
                'records':records,'login_name':name, 'doctor':doctor
            }
            return render(request,'lab_module/lab_report.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def dep_lab_report(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'department_lab_report' in access.user_profile.screen_access:
        try:
            collected=SampleCollected.objects.filter(status='vallidated',location=request.location).order_by('-date_time')
            ptid_list=[data.test_id for data in collected]
            name=[]
            age=[]
            PTID=[]
            gender=[]
            date_time=[]
            uhid=[]
            for data in ptid_list:
                col_rec=SampleCollected.objects.get(test_id=data)
                pat_rec=PatientsRegistrationsAllInOne.objects.get(uhid=col_rec.uhid)
                name.append(pat_rec.first_name)
                age.append(pat_rec.age)
                gender.append(pat_rec.gender)
                PTID.append(col_rec.PTID)
                date_time.append(col_rec.date_time)
                uhid.append(pat_rec.uhid)

            records=zip(name,age,PTID,gender,date_time,uhid,ptid_list)
            context={
                'records':records
            }
            return render(request,'lab_module/dep_lab_report.html',context)
        except Exception as error:
            return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')
def dep_lab_report_print(request,pk):
    name=request.session['Name']
    doctor=request.session['doctor']
    entry_records=LabResultEntry.objects.filter(test_id=pk)
    collected=SampleCollected.objects.get(test_id=pk)
    doc_sign=DoctorTable.objects.filter(doctor_id=collected.doctor_id).first()
    patient_records=PatientsRegistrationsAllInOne.objects.get(uhid=collected.uhid)
    test_id_list=[data.test_id for data in entry_records]
    test_id_list=list(set(test_id_list))
    head=[]
    body=[]
    for data in test_id_list:
        result_records=LabResultEntry.objects.filter(test_id=data)
        body.append(result_records)
        head.append(result_records[0].profile_name)
    records=zip(head,body)

    context={
        'records':records,'patient_records':patient_records,'doc_sign':doc_sign,'collected':collected,'login_name':name, 'doctor':doctor
    }
    return render(request,'lab_module/lab_report_print.html',context)

@login_required(login_url='/user_login')
def lab_report_print(request,pk):
    name=request.session['Name']
    doctor=request.session['doctor']
    complete_report='pass'
    entry_records=LabResultEntry.objects.filter(PTID=pk)
    collected=SampleCollected.objects.filter(PTID=pk)
    patient_records=PatientsRegistrationsAllInOne.objects.get(uhid=collected[0].uhid)
    test_id_list=[data.test_id for data in entry_records]
    test_id_list=list(set(test_id_list))
    head=[]
    body=[]
    for data in test_id_list:
        result_records=LabResultEntry.objects.filter(test_id=data)
        body.append(result_records)
        head.append(result_records[0].profile_name)
    records=zip(head,body)
    context={
        'records':records,'patient_records':patient_records,'complete_report':complete_report,'login_name':name, 'doctor':doctor
    }
    return render(request,'lab_module/lab_report_print.html',context)

@login_required(login_url='/user_login')
def report_change(request,pk):
    name=request.session['Name']
    doctor=request.session['doctor']
    sample_rec=SampleCollected.objects.get(test_id=pk)
    records=DoctorTable.objects.all()
    doctor_id=request.POST.get('doct_name')
    print(doctor_id)
    if request.method=='POST':
        doc_records=DoctorTable.objects.get(doctor_id=doctor_id)
        sample_rec.doctor_id=doctor_id
        sample_rec.validated_by=doc_records.doctor_name
        sample_rec.save()
        validate_record=Validation_record(
            PTID=sample_rec.test_id,uhid=sample_rec.uhid,validated_by=doc_records.doctor_name,date_time=datetime.now(),
            status="edited"
        )
        validate_record.save()
        return HttpResponseRedirect(f'/dep_lab_report_print/{pk}')
    context={
        'records':records,'login_name':name, 'doctor':doctor
    }
    return render(request,'lab_module/doctor_change.html',context)


# Service Test Link with tariff 19/12/22 ======================
@login_required(login_url='/user_login')
def service_test_tarifflink(request):
    tariff_data=TariffMaster.objects.all()
    service_test_data=Service_Test.objects.all()
    service_test_link_data=ServiceTestlinkTarrif.objects.all()
    if request.method=="POST":
        tariff_name=request.POST.get('tariff_name')
        service_test_id=request.POST.get('service_test_id')
        apply_date=request.POST.get('apply_from')
        data=ServiceTestlinkTarrif(
            tariff_id=tariff_name,
            service_test_id=service_test_id,
            apply_date=apply_date,
        )
        data.save()
        return HttpResponseRedirect('/service_test_tarifflink')
    context={
        'tariff_data':tariff_data,'service_test_data':service_test_data,'service_test_link_data':service_test_link_data,
    }
    return render(request,'clinical/profile/service_test_tarifflink.html',context)

# 19/12/22 THIS IS FOR ADD CHARGE IN TEST SERVICES =============================
@login_required(login_url='/user_login')
def service_test_edit(request):
    # name=request.session['Name']
    records = ServiceTest.objects.all()
    form = ServiceTestForm()
    if request.method=='POST':
        form=ServiceTestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/service_test_edit')
    return render(request, 'clinical/profile/service_test_edit.html',
                  {'records': records,'form':form})

@login_required(login_url='/user_login')
def service_test_editing(request,pk):
    # name=request.session['Name']
    records = ServiceTest.objects.get(id=pk)
    form = ServiceTestForm(instance=records)
    if request.method == 'POST':
        form = ServiceTestForm(request.POST, instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/service_test_edit')
    return render(request, 'clinical/profile/service_test_editing.html',
                  {'form': form})

# ===================== ward module =================
from django.db.models import Subquery, OuterRef, F, Value
from django.db.models.functions import Concat
from django.db.models import ExpressionWrapper, CharField
@login_required(login_url='/user_login')
def paitent_ward(request):
    subquery = PatientsRegistrationsAllInOne.objects.filter(uhid=OuterRef('uhid')).annotate(
        full_name=Concat(F('title'), Value(' '), F('first_name'), Value(' '), F('middle_name'), Value(' '),
                         F('last_name'), output_field=CharField())
    ).values('full_name')[:1]
    records = AdmissionInfos.objects.filter(status='admitted').order_by('-admission_ID').annotate(
        name=Subquery(subquery)
    )
    context={
        'records':records,
    }
    return render(request,'ward_module/ward.html',context)

def paitent_ward_actions(request,pk):
    name=request.session['Name']
    user=''
    admin=''
    records_ad=AdmissionInfos.objects.get(admission_ID=pk)
    records_pat=PatientsRegistrationsAllInOne.objects.get(uhid=records_ad.uhid)
    title=records_pat.title
    f_name=records_pat.first_name
    m_name=records_pat.middle_name
    l_name=records_pat.last_name
    if m_name != None:
        pat_name=title+' '+f_name+' '+m_name+' '+l_name
    else:
        pat_name=title+' '+f_name+' '+l_name
    uhid=records_ad.uhid
    ad_id=records_ad.admission_ID
    ad_id_id=records_ad.id
    doctory=records_ad.primary_doctor
    bed_num=records_ad.bed_no
    admission_date=date.today()
    # table show
    records=AdmissionInfos.objects.filter(status='admitted')
    user='user'

    # getting button
    bed_transfer_btn=request.POST.get('bed_transfer_button')
    doctor_transfer_btn=request.POST.get('doctor_transfer_button')
    ad=AdmissionInfos.objects.filter(status='admitted')
    ad_uhid=[data.uhid for data in ad]

    # bed  transfer
    no_of_bed_transfer=Bed_Transfer.objects.all().count()
    today=date.today()
    today=today.strftime("%y%m%d")
    if len(str(no_of_bed_transfer))==1:
        BT_id='BT'+today+'000'+str(no_of_bed_transfer)
    elif len(str(no_of_bed_transfer))==2:
        BT_id='BT'+today+'00'+str(no_of_bed_transfer)
    elif len(str(no_of_bed_transfer))==3:
        BT_id='BT'+today+'0'+str(no_of_bed_transfer)
    else:
        BT_id='BT'+today+str(no_of_bed_transfer)
    try:
        bed_transfer_records1=Bed_Transfer.objects.filter(admission_ID=pk)
        bed_transfer_form=''
        bed_transfer_records=Bed_Transfer.objects.all()
        bed_ad=[data.admission_ID for data in bed_transfer_records]

        admissioninfo_records=AdmissionInfos.objects.all()
        ad_unid_list=[data.admission_ID for data in admissioninfo_records]
        if pk in ad_unid_list:
            ad_records=AdmissionInfos.objects.get(admission_ID=pk,status='admitted')
            ad_id=ad_records.admission_ID
        else:
            ad_records=''
        if ad_id in bed_ad:
            for data in bed_transfer_records1:
                bed_transfer_form = BedTransferForm(initial={'uhid': data.uhid,'bed_transfer_id':BT_id,'from_ward_type':data.to_ward_type,'from_bed_no':data.to_bed_no,'from_ward_cat':data.to_ward_cat,'admission_ID':ad_records.admission_ID})
        elif uhid in ad_uhid:
            bed_transfer_form = BedTransferForm(initial={'uhid': ad_records.uhid,'bed_transfer_id':BT_id,'from_ward_type':ad_records.req_ward_type,'from_bed_no':ad_records.bed_no,'from_ward_cat':ad_records.req_ward_cate,'admission_ID':ad_records.admission_ID})
        if bed_transfer_btn == 'bed_transfer_button':
            if request.method=='POST':
                bed_transfer_form=BedTransferForm(request.POST)
                from_ward_type_id=request.POST.get('from_ward_type')
                from_ward_cat_id=request.POST.get('from_ward_cat')
                from_bed_num_id=request.POST.get('from_bed_no')
                to_ward_type_id=request.POST.get('to_ward_type')
                to_ward_cat_id=request.POST.get('to_ward_cat')
                to_bed_num_id=request.POST.get('to_bed_no')
                to_ward_type=AdmissionWardType.objects.get(id=to_ward_type_id)
                to_ward_cat=AdmissionWardCate.objects.get(id=to_ward_cat_id)
                to_bed_num=BedMasterMain.objects.get(id=to_bed_num_id)
                from_ward_type=AdmissionWardType.objects.get(id=from_ward_type_id)
                from_ward_cat=AdmissionWardCate.objects.get(id=from_ward_cat_id)
                from_bed_num=BedMasterMain.objects.get(id=from_bed_num_id)
                if bed_transfer_form.is_valid():
                    bed_transfer_form.save()
                    occu=BedMasterMain.objects.get(ward_type=to_ward_type.ward_type, ward_category=to_ward_cat.category_name,  bed_no=to_bed_num.bed_no
                    )
                    un_occu=BedMasterMain.objects.get(ward_type=from_ward_type.ward_type, ward_category=from_ward_cat.category_name,  bed_no=from_bed_num.bed_no
                    )
                    occu.status='occupied'
                    un_occu.status='un_occupied'
                    occu.save()
                    un_occu.save()

                    return HttpResponseRedirect(f'/diet/paitent_ward_actions/{pk}')
                else:
                    print(bed_transfer_form.errors)
    except:
        pass

    # doctor transfer
    no_of_doctor_transfer = Doctor_Transfer.objects.all().count()
    today = date.today()
    today = today.strftime("%y%m%d")
    if len(str(no_of_doctor_transfer)) == 1:
        DT_id = 'DT' + today + '000' + str(no_of_doctor_transfer)
    elif len(str(no_of_doctor_transfer)) == 2:
        DT_id = 'DT' + today + '00' + str(no_of_doctor_transfer)
    elif len(str(no_of_doctor_transfer)) == 3:
        DT_id = 'DT' + today + '0' + str(no_of_doctor_transfer)
    else:
        DT_id = 'DT' + today + str(no_of_doctor_transfer)
    doctor_transfer_records = Doctor_Transfer.objects.filter(admission_ID__icontains='ADM2304200002')
    doctor_transfer_form = ''
    bed_transfer_records = Doctor_Transfer.objects.all()
    doctor_uhid = [data.admission_ID for data in bed_transfer_records]
    ad_records = AdmissionInfos.objects.get(admission_ID=pk)
    a=Doctor_Transfer.objects.all()
    if doctor_transfer_records:
        for data in doctor_transfer_records:
            doctor_transfer_form = DoctorTransferForm(
                initial={'uhid': data.uhid, 'doctor_transfer_id': DT_id, 'from_doctor': data.to_doctor,
                         'from_department': data.to_department,'admission_ID':data.admission_ID})
    else:
        doctor_transfer_form = DoctorTransferForm(
            initial={'uhid': ad_records.uhid, 'doctor_transfer_id': DT_id, 'from_doctor': ad_records.primary_doctor,
                     'from_department': ad_records.department,'admission_ID':ad_records.admission_ID})
    if doctor_transfer_btn == 'doctor_transfer_button':
        if request.method == 'POST':
            Doctor_Transfer.objects.create(
                uhid=request.POST.get('uhid'),
                admission_ID=request.POST.get('admission_ID'),
                doctor_transfer_id=request.POST.get('doctor_transfer_id'),
                from_doctor_id=request.POST.get('from_doctor'),
                from_department_id=request.POST.get('from_department'),
                to_doctor_id=request.POST.get('to_doctor'),
                to_department_id=request.POST.get('to_department'),
            )
            # doctor_transfer_fo = DoctorTransferForm(request.POST)
            # if doctor_transfer_fo.is_valid():
            #     doctor_transfer_fo.save(print('sucesssss'))
            return HttpResponseRedirect('/paitent_ward')
            # else:
            #     print(bed_transfer_form.errors)
    discharge_btn=request.POST.get('discharge')
    if discharge_btn:
        ad_record_add=AdmissionInfos.objects.get(admission_ID=pk,status='admitted')
        ad_record_add.status='discharge'
        ad_record_add.save()
        return HttpResponseRedirect('/paitent_ward')
    patient_type = PatientType_Master.objects.all()
    diet_type = DietType_Master.objects.all()

    context={
        'records':records,'login_name':name,'admin':admin,'user':user,'bed_transfer_form':bed_transfer_form,'doctor_transfer_form':doctor_transfer_form,
        'uhid':uhid,'ad_id':ad_id,'doctory':doctory,'admission_date':admission_date,'pat_name':pat_name,'bed_num':bed_num,'patient_type':patient_type,
        'diet_type':diet_type,'records_ad':records_ad,'ad_id_id':ad_id_id,
    }
    return render(request,'ward_module/ward_action.html',context)
    
@login_required(login_url='/user_login')

# ===================== ward module end =================

# 29/12/22 mantu ============================

@login_required(login_url='/user_login')
def opdbill_all(request):
    data_sub_bill=''
    data_main_bill=''
    list_uhid = PatientsRegistrationsAllInOne.objects.filter(location=request.location).order_by('uhid')
    opd_bill_sum = request.POST.get('sum_bill')
    opd_bill_main = request.POST.get('detail_bill')

    if opd_bill_sum == 'Sum_Bill':
        if request.method == "POST":
            uhids = request.POST.get('patient_id')
            start_date = request.POST.get('s_date')
            end_date = request.POST.get('e_date')
            data_sub_bill = OpdBillingSub.objects.filter(Q(bill_date_time__range=[start_date,end_date])&Q(uhid=uhids)).order_by('-bill_date_time')

    if opd_bill_main == 'Detail_Bill':
        if request.method == "POST":
            uhids = request.POST.get('patient_id')
            start_date = request.POST.get('s_date')
            end_date = request.POST.get('e_date')
            data_main_bill = OpdBillingSub.objects.filter(Q(bill_date_time__range = [start_date,end_date])&Q(uhid=uhids)).order_by('-bill_date_time')
    context={
        'list_uhid':list_uhid,'data_sub_bill':data_sub_bill,'data_main_bill':data_main_bill,
    }
    return render(request,'clinical/opd_bill/opbill_all.html',context)

@login_required(login_url='/user_login')
def temp_records(request,uhid=None):
    rate_p=[]
    ins_p=[]
    dept_list = []
    unique1=OpdBillingTemper.objects.extra(select={
                'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingTemper.uhid',
                'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingTemper.uhid',
                'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingTemper.uhid',
                'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingTemper.uhid',
                # 'pat_billing_group': 'Select corporate_Name from testapp_CorporateMaster where corporate_ID=testapp_patientsregistrationsallinone.uhid',
                # 'pat_billing_group': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_CorporateMaster.corporate_Name',
                }).filter(location=request.location).order_by('-id')
    for data in unique1:
        patient_data=PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
        dept=PatientVisitMains.objects.get(uhid=data.uhid,visit_id=data.visit_no)
        department=dept.clinical_department
        dept_list.append(department)
        if patient_data.nhif_ins_cor_name == 'Cash':
            ins_p.append('Cash')
        else:
            insurance_d=CorporateMaster.objects.get(id=patient_data.nhif_ins_cor_name)
            ins_pla=insurance_d.corporate_Name
            ins_p.append(ins_pla)
    unique=zip(unique1,dept_list,ins_p)
    return render(request,'clinical/opd_bill/temp_records.html',{'unique':unique,})

# # date 16/03/23 in evening ++++++++++++++++++========================

@login_required(login_url='/user_login')
def opd_billing_temp(request,uhid,vis=None): #By Mantu=====================================
    search_uhiddd=uhid
    if uhid == None:
        uhid = request.session['uhiddd']
    elif uhid != None:
        request.session['uhiddd'] = uhid
        request.session['pay_m_uhidss']=uhid
    if vis != None and vis != 'jquery-3.6.0.min.js':
        request.session['visit_id_temp'] = vis
        request.session['pay_m_visit_id']=vis
    visit_idss= request.session['visit_id_temp']
    data = request.GET.get('service_name')
    visit_get_temp_button = request.POST.get('visit_button')
    request.session['search_datas'] = data
    visit_id=''
    updat_status=OpdBillingTemper.objects.filter(uhid__exact=search_uhiddd,visit_no=visit_idss).last()
    updat_status.status='closed_bill'
    updat_status.save()
    print('updat_status----,updat_status',updat_status)
    temp_data_bill=OpdBillingTemper.objects.filter(uhid__exact=search_uhiddd)
    uhid_no = [*set(data.uhid for data in temp_data_bill)]
    visit_no_temp = [*set(data.visit_no for data in temp_data_bill)]
    request.session['visit_id_temp'] = visit_no_temp[0]
    my_visit_no= request.session['visit_id_temp']
    print('my_visit_no_temp_page',my_visit_no)
    temp_bill_no = [*set(data.temp_bill_no for data in temp_data_bill)]
    #==================== For open set session variable ===============================
    dept = PatientVisitMains.objects.get(uhid=uhid,visit_id=visit_idss)
    doctor_name = dept.doctor
    clinical_departments = dept.clinical_department
    departments_name = str(clinical_departments)
    dr_name = str(doctor_name)
    request.session['clinical_department'] = departments_name
    request.session['nurse_doctor'] = dr_name
    #============================== END =======================================
    if uhid:
        get_uhid_data = PatientsRegistrationsAllInOne.objects.get(uhid__icontains=uhid)
        title=get_uhid_data.title
        title_uhid=get_uhid_data.uhid
        first_name=get_uhid_data.first_name
        middle_name=get_uhid_data.middle_name
        last_name=get_uhid_data.last_name
        dob=get_uhid_data.dob
        gender=get_uhid_data.gender
        mobile_number=get_uhid_data.mobile_number
        billing_group=get_uhid_data.billing_group
        corporate_names=get_uhid_data.nhif_ins_cor_name
        current_year=date.today().year
        dob_year=dob.year
        dob=current_year-dob_year
        if middle_name == None:
            name=title+'. '+first_name+' '+last_name
        else:
            name=title+'. '+first_name+' '+middle_name+' '+last_name
        request.session['patient_name']=name
        request.session['dob']=dob
        request.session['mobile_number']=mobile_number
        request.session['billing_group']=billing_group
        request.session['corporate_name']=corporate_names
        request.session['gender']=gender
        request.session['uhid']=uhid
        request.session['searched_uhid']=uhid
        request.session['visit_id']=visit_id
        service_master = ServiceChargeMaster.objects.all()
        corp_name=''
        # corporate=BillingGroupCorporateMaster.objects.get(id=corporate_names)
        if corporate_names == 'Cash':
            corp_name='Cash'
        else:
            corp_all=CorporateMaster.objects.get(id=corporate_names)
            corp_name=corp_all.corporate_Name
        # corporate_names = corporate.Corporate_Name
        # corporate_billing_groups = corporate.Biiling_Group_id
        tariff=BillingGroupTariffLink.objects.filter(Billing_Group_Name_id=billing_group)
        billing_groups=[data.Billing_Group_Name_id for data in tariff]
        billing_gp=[data.Billing_Group_Name for data in tariff]
        # billing_groups1=[data.Billing_Group_Name for data in tariff]
        billing_groups1=[*set(billing_gp)]
        print('billing_groups1',billing_groups1)
        tariff_names=[data.Tariff_id for data in tariff]
        # billing_groups=tariff. Billing_Group_Name_id
        # billing_groups1=tariff. Billing_Group_Name
        # tariff_names=tariff.Tariff_id
        for data in tariff_names:
            service=ServiceChargeMaster.objects.all().filter(tariff_id__exact=data)
        request.session['tariff_names'] = tariff_names
        # print('tariff_names==123123=============',tariff_names)
        service_id=0
        service_charge=0
        default_unit = 1
        default_discount = 0
        default_out_standing_amount = 0
        request.session['service_id'] = service_id
        request.session['service_charge'] = service_charge

    if request.method == 'POST':
        service_name = request.POST.getlist('service_name')
        uhid = request.POST.get('uhid')
        visit_ids_temp = request.POST.get('visit_id')
        print('visit_id==========',visit_id)
        temp_bill_no = request.POST.get('temp_bill_nos')
        print('temp_bill_no--------------',temp_bill_no)
        amount = request.POST.getlist('amount')
        discount = request.POST.getlist('discount')
        unit = request.POST.getlist('unit')
        net_amount = request.POST.getlist('net_amount')
        outstanding_amount = request.POST.getlist('outstanding_amount')
        total_amount = request.POST.getlist('total_amount')
        receive_amount = request.POST.getlist('receive_amount')
        request.session['searched_uhid'] = uhid
        request.session['visit_id'] = visit_id
        # OPD id payment
        request.session['pay_m_receive_amount'] = receive_amount
        request.session['pay_m_uhid'] = uhid
        request.session['pay_m_visit_id'] = visit_ids_temp
        print('pay_m_visit_id',visit_ids_temp)
        request.session['service_name'] = service_name
        # Generating Bill No and Bil Id Generation Start
        temp_bill = OpdBillingTemper.objects.filter(uhid=uhid_no,visit_no=visit_no_temp)
        # print('temp_bill',temp_bill.temp_bill_no)
        if not temp_bill:
            yy = date.today().year
            current_yy = str(yy)[2:]
            previous_yy = str(yy - 1)[2:]
            finance_year = previous_yy + current_yy
            b_no = str(random.randint(1000, 9999))
            temp_bill_no = 'TEPID' + finance_year + b_no
            request.session['temp_bill_no'] = temp_bill_no
            print('temp_bill_no', temp_bill_no)
        else:
            temp_bill_no=temp_bill[0].temp_bill_no
        print('temp_bill_nou', temp_bill_no)
        for i in range(len(service_name)):
            ind_service_name=service_name[i]
            ind_uhid=uhid
            ind_visit_id=visit_no_temp
            ind_temp_bill_no=temp_bill_no
            ind_amount=amount[i]
            ind_discount=discount[i]
            ind_unit=unit[i]
            ind_net_amount=net_amount[i]
            ind_outstanding_amount=outstanding_amount[i]
            ind_total_amount=total_amount[i]
            ind_receive_amount=receive_amount[i]
            temp_opd_billing = OpdBillingTemper(
                uhid=ind_uhid,
                visit_no=ind_visit_id,
                temp_bill_no=ind_temp_bill_no,
                service_name=ind_service_name,
                rate=ind_amount,
                discount=ind_discount,
                unit=ind_unit,
                net_ammount=ind_net_amount,
                outstanding_amount=ind_outstanding_amount,
                total_amount=ind_total_amount,
                receive_amount=ind_receive_amount,created_by_id=request.user.id,location_id=request.location,
            )
            temp_opd_billing.save()
    messages.success(request, 'Successfully Populated Your Services..')
    name = request.session['patient_name']
    dob = request.session['dob']
    mobile_number = request.session['mobile_number']
    billing_group = request.session['billing_group']
    corporate_names = request.session['corporate_name']
    gender = request.session['gender']
    # visit_id=request.session['pay_m_visit_id']
    request.session['searched_uhid']=uhid
    # request.session['visit_id']=visit_id
    if corporate_names == 'Cash':
        corp_name='Cash'
    else:
        corp_all = CorporateMaster.objects.get(id=corporate_names)
        corp_name = corp_all.corporate_Name
    tariff = BillingGroupTariffLink.objects.filter(Billing_Group_Name_id=billing_group)
    billing_groups1 = [*set(data.Billing_Group_Name for data in tariff)]
    temp_records = OpdBillingTemper.objects.filter(uhid=uhid)
    temp_rec = OpdBillingTemper.objects.filter(uhid=uhid,visit_no=vis).count()
    print('temp_rec=======>>>>>>>>>>>>>>>>>>>>',temp_rec)
    #========================= For Discount ==============================================
    ttl_rate = OpdBillingTemper.objects.filter(visit_no=my_visit_no, uhid=uhid).aggregate(Sum('rate'))
    ttl_rate = ttl_rate['rate__sum']
    ttl_qty = OpdBillingTemper.objects.filter(visit_no=my_visit_no, uhid=uhid).aggregate(Sum('unit'))
    ttl_qty = ttl_qty['unit__sum']
    ttl_dics = OpdBillingTemper.objects.filter(visit_no=my_visit_no, uhid=uhid).aggregate(Sum('discount'))
    ttl_dics = ttl_dics['discount__sum']
    ttl_net_amt = OpdBillingTemper.objects.filter(visit_no=my_visit_no, uhid=uhid).aggregate(Sum('net_ammount'))
    ttl_net_amt = ttl_net_amt['net_ammount__sum']
    ttl_amt = OpdBillingTemper.objects.filter(visit_no=my_visit_no, uhid=uhid).aggregate(Sum('total_amount'))
    ttl_amt = ttl_amt['total_amount__sum']
    #================================= END =============================================================
    context={
        'visit_no':visit_no_temp, 'uhid_no': uhid_no,'temp_records':temp_records,'ttl_rate':ttl_rate,'ttl_qty':ttl_qty,'ttl_amt': ttl_amt, 'ttl_dics': ttl_dics, 'ttl_net_amt': ttl_net_amt,
        'corp_name':corp_name,'temp_bill_no':temp_bill_no,
        'mobile_number':mobile_number,'billing_groups1':billing_groups1,'name':name,'corporate_names':corporate_names,
        'gender':gender,'dob':dob,'searched_uhid':uhid,'visit_id':visit_id,
    }
    return render(request, 'clinical/opd_billing.html',context)

@login_required(login_url='/user_login')
def dr_share_with_package(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'doctor_accounting_packages' in access.user_profile.screen_access:
        try:
            tariff=0
            tariff_name=0
            dr_name=0
            date=0
            doctor_name=0
            tarif_name=0
            service_departments=0
            service_sub_departments=0
            ser_dep=0
            ser_sub_dep=0
            service_name=''
            tariff_service1=''
            records=''
            records_id=''
            service_charge=''
            id_count_d=''
            pack=''
            tariff1=''
            dr_share=''
            tariff_names=''
            doctor_table=DoctorTable.objects.filter()
            tariff_table=TariffMaster.objects.all()
            dr_acc=DoctorAccounting.objects.filter()
            dr_id=[data.doctor_id for data in dr_acc]
            tariff_id=[data.tariff_id for data in dr_acc]
            tariff_service=[data.service_name for data in dr_acc]
            tariff_rate=[data.service_rate for data in dr_acc]
            service_department=ServiceDepartment.objects.all()
            service_sub_department=ServiceSubDepartment.objects.all()
            search1 = request.POST.get('search1')
            print('search1',search1)
            search2 = request.POST.get('search2')
            # print('search2',search2)
            if request.method=="POST":
                dr_name = request.POST.get('dr_name')
                tariff_name = request.POST.get('tariff_name')
                dr_names=request.POST.get('dr_names')
                print('dr_names',dr_name,tariff_name)
                tariff_names=request.POST.get('tariff_names')
                service_name=request.POST.getlist('service_name')
                service_rate=request.POST.getlist('service_rate')
                dr_share=request.POST.getlist('dr_share')
                hospital_share=request.POST.getlist('hospital_share')
                date=request.POST.get('date')
                dates=request.POST.get('dates')
                service_departments=request.POST.get('service_departments')
                service_sub_departments=request.POST.get('service_sub_departments')
                dr_acc1 = DoctorAccounting.objects.filter(doctor_id=dr_names,tariff_id=tariff_names)
                dr_id1 = [data.doctor_id for data in dr_acc1]
                tariff_id1 = [data.tariff_id for data in dr_acc1]
                # print('tariff_id1',tariff_id1)
                tariff_service1 = [data.service_name for data in dr_acc1]
                tariff_rate1 = [data.service_rate for data in dr_acc1]
                for record in range(len(service_name)):
                    var_tariff_name=tariff_names
                    var_dr_name=dr_names
                    var_service_name=service_name[record]
                    var_service_rate=service_rate[record]
                    var_dr_share=dr_share[record]
                    var_hospital_share=hospital_share[record]
                    var_date=dates
                    # print(str(var_service_name) not in str(tariff_service1),str(var_dr_name) not in str(dr_id1))
                    dataa=DoctorAccounting.objects.filter(doctor_id=var_dr_name,tariff_id=var_tariff_name,service_name=var_service_name)
                    print('dataa=======',dataa)
                    if str(var_service_name) not in str(tariff_service1):
                        Dr_acc=DoctorAccounting(
                            service_name=var_service_name,
                            service_rate=var_service_rate,
                            doctor_id=var_dr_name,
                            tariff_id=var_tariff_name,
                            doctor_share=var_dr_share,
                            hospital_share=var_hospital_share,
                            date=var_date,created_by_id=request.user.id,location_id=request.location,
                        )
                        Dr_acc.save()
            package_name_deprt=[]
            package_amt_deprt=[]
            package_name=[]
            package_amt=[]
            id_count=''
            id_counts=''
            pack1=''
            pack=''
            if service_departments and service_sub_departments:
                s_d = ServiceDepartment.objects.get(id=service_departments)
                s_s_d = ServiceSubDepartment.objects.get(id=service_sub_departments)
                ser_dep=s_d.service_department
                ser_sub_dep=s_s_d.service_sub_department
                opd_package=OpdPackageService.objects.filter(Q(service_sub_department=ser_sub_dep)&Q(service_department=ser_dep))
                id_count_d=OpdPackageService.objects.filter(Q(service_sub_department=ser_sub_dep)&Q(service_department=ser_sub_dep)).count()
                package_names=[data.package_name for data in opd_package]
                single_package_name=list(set(package_names))
                records = OpdPackageMaster.objects.filter(package_name__in=single_package_name).exclude(package_name__in=DoctorAccounting.objects.values('service_name'))
                id_count=records.count()
                pack1 = zip(package_name_deprt, package_amt_deprt)
                if dr_name in dr_id and tariff_name in tariff_id:
                    dr_share=DoctorAccounting.objects.filter(tariff_id=tariff_name,doctor_id=dr_name)
                    tariff_ids=[data.tariff_id for data in dr_share]
            elif tariff_name:
                tariff1 = PackageChargeMaster.objects.filter(tariff_id_id=tariff_name).exclude(package_id__in=DoctorAccounting.objects.values('service_name'))
                id_count=tariff1.count()
                service_charge = [data.package_id for data in tariff1]
                for dat in service_charge:
                    tariff=OpdPackageMaster.objects.filter(package_name=dat)
                    p_name=[data.package_name for data in tariff]
                    p_amt=[data.package_amount for data in tariff]
                    package_name.append(p_name)
                    package_amt.append(p_amt)
                pack=zip(package_name,package_amt)
                print('==========',package_name,package_amt)
                records_id = [data.tariff_id_id for data in tariff1]
                if len(records_id) > 0:
                    id_start = records_id[0]
                else:
                    id_start = 0
                print('id_count',id_count)
            if dr_name:
                doctor_table_name = DoctorTable.objects.get(doctor_id=dr_name)
                doctor_name = doctor_table_name.doctor_name
                tariff_table_name = TariffMaster.objects.get(id=tariff_name)
                tarif_name = tariff_table_name.tariff_name
            print('=-----=!!!!!!!',records)
            context={
                'doctor_table':doctor_table,'tariff_table':tariff_table,'tariff':tariff,'doctor_name':doctor_name,
                'tarif_name':tarif_name,'dr_acc':dr_acc,'date':date,'dr_name':dr_name,'tariff_name':tariff_name,
                'pack1':pack1,'ser_dep':ser_dep,
                'service_department':service_department,'service_sub_department':service_sub_department,'ser_sub_dep':ser_sub_dep,
                'id_count':id_count,'id_counts':id_counts,'service_charge':service_charge,'id_count_d':id_count_d,'pack':pack,'dr_share':dr_share,
                'access':access,'records':records,'tariff1':tariff1

            }
            return render(request,'general_master/opd_package/dr_share_with_package.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
#================ Doctor Share with Package 27/12/22 ==================================

@login_required(login_url='/user_login')
def dr_share_with_profile(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'doctor_accounting_profile' in access.user_profile.screen_access:
        try:
            tariff=0
            tariff_name=0
            dr_name=0
            date=0
            doctor_name=0
            tarif_name=0
            service_departments=0
            service_sub_departments=0
            ser_dep=0
            ser_sub_dep=0
            tariff1=''
            service_charge=''
            id_count_d=''
            id_counts=''
            id_count=''
            pack1=''
            pack=''
            doctor_table=DoctorTable.objects.filter()
            tariff_table=TariffMaster.objects.all()
            dr_acc=DoctorAccounting.objects.filter()
            service_department=ServiceDepartment.objects.all()
            service_sub_department=ServiceSubDepartment.objects.all()

            # print('search2',search2)
            if request.method=="POST":
                dr_name = request.POST.get('dr_name')
                tariff_name = request.POST.get('tariff_name')
                dr_names=request.POST.get('dr_names')
                tariff_names=request.POST.get('tariff_names')
                service_name=request.POST.getlist('service_name')
                service_rate=request.POST.getlist('service_rate')
                dr_share=request.POST.getlist('dr_share')
                hospital_share=request.POST.getlist('hospital_share')
                date=request.POST.get('date')
                dates=request.POST.get('dates')
                service_departments=request.POST.get('service_departments')
                service_sub_departments=request.POST.get('service_sub_departments')
                for record in range(len(service_name)):
                    var_tariff_name=tariff_names
                    var_dr_name=dr_names
                    var_service_name=service_name[record]
                    var_service_rate=service_rate[record]
                    var_dr_share=dr_share[record]
                    var_hospital_share=hospital_share[record]
                    var_date=dates
                    dataa = DoctorAccounting.objects.filter(doctor_id=var_dr_name, tariff_id=var_tariff_name,
                                                            service_name=var_service_name)
                    if not dataa.exists():
                        Dr_acc=DoctorAccounting(
                            service_name=var_service_name,
                            service_rate=var_service_rate,
                            doctor_id=var_dr_name,
                            tariff_id=var_tariff_name,
                            doctor_share=var_dr_share,
                            hospital_share=var_hospital_share,
                            date=var_date,created_by_id=request.user.id,location_id=request.location,
                        )
                        Dr_acc.save()
            # HttpResponseRedirect('/dr_share_with_profile')
            if service_departments and service_sub_departments:
                print('serach departmrnt')
                s_d = ServiceDepartment.objects.get(id=service_departments)
                s_s_d = ServiceSubDepartment.objects.get(id=service_sub_departments)
                records=ProfileService.objects.filter(Q(service_sub_department=s_s_d.service_sub_department)&Q(service_department=s_d.service_department))
                id_count=records.count()
                profile_names=[data.profile_name for data in records]
                single_profile_name=list(set(profile_names))
                id_counts = len(single_profile_name)
                pack=ProfileMaster.objects.filter(profile_name__in=single_profile_name).exclude(profile_name__in=DoctorAccounting.objects.values('service_name'))

            elif tariff_name:
                tariff1 = ProfileChargeMaster.objects.filter(tariff_id_id=tariff_name).exclude(profile_id__in=DoctorAccounting.objects.values('service_name'))
                id_count=tariff1.count()
            context={
                'doctor_table':doctor_table,'tariff_table':tariff_table,'tariff':tariff,'doctor_name':doctor_name,
                'tarif_name':tarif_name,'dr_acc':dr_acc,'date':date,'dr_name':dr_name,'tariff_name':tariff_name,
                'ser_dep':ser_dep,'pack1':pack1,'tariff1':tariff1,
                'service_department':service_department,'service_sub_department':service_sub_department,'ser_sub_dep':ser_sub_dep,
                'id_count':id_count,'id_counts':id_counts,'service_charge':service_charge,'id_count_d':id_count_d,'pack':pack,'access':access

            }
            return render(request,'general_master/opd_package/dr_share_with_profile.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


    #====================== API Karan ==========================
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_medication(request):
    if request.method=='GET':
        records=Medication_main.objects.all()
        serializer=Medication_mainSerilizer(records,many=True)

    return Response(utils_response.success_response(data=serializer.data,status_code=status.HTTP_200_OK))


def api_medication_view(request):
    response=requests.get('http://127.0.0.1:1111/api_medication').json()
    response=response['data']
    return render(request,'aip_medication_view.html',{'response':response})

@api_view(['GET'])
def api_PatientsRegistration(request,pk):
    if request.method=='GET':
        records=PatientsRegistrationsAllInOne.objects.filter(uhid=pk)
        records1=AdmissionInfos.objects.filter(uhid=pk,status='admitted')
        serializer=PatientsRegistrationSerilizer(records,many=True)
        serializer1=PatientsAdmissionInfosSerilizer(records1,many=True)
        # ResultSerializer=serializer.data + serializer1.data
        all_list_api=[]
        for patient in serializer.data:
            for admissionin in serializer1.data:
                if patient['uhid']==admissionin['uhid']:
                    dict1=patient
                    dict2=admissionin
                    dict1.update(dict2)
                    all_list_api.append(dict1)
    return Response(utils_response.success_response(data=all_list_api,status_code=status.HTTP_200_OK))

@api_view(['GET'])
def admissioninfo_all(request):
    if request.method=='GET':
        records=AdmissionInfos.objects.filter(status='admitted')
        serializer=PatientsAdmissionInfosSerilizer(records,many=True)

    return Response(utils_response.success_response(data=serializer.data,status_code=status.HTTP_200_OK))

def api_PatientsRegistration_view(request):
    response=requests.get('http://127.0.0.1:8000/api_PatientsRegistration').json()
    response=response['data']
    return render(request,'aip_medication_view.html',{'response':response})

    #===================== For Bed Karan =====================
def bed_load1(request):
    ward_name = request.GET.get('ward_type_id')
    type = AdmissionWardType.objects.get(ward_type=ward_name)
    cat = AdmissionWardCate.objects.filter(ward_type_id=type.id)
    return JsonResponse(list(cat.values('id', 'category_name')), safe=False)

def bed_view(request):
    name = request.session['Name']
    ward_type_records = AdmissionWardType.objects.all()
    ward_cat_records = AdmissionWardCate.objects.all()
    ward_name = request.POST.get('ward_name')
    ward_cat = request.POST.get('ward_cat')
    bed = ''
    bed_number = ''
    if ward_name != 'all':
        bed_number = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat)
        if bed_number:
            bed = 'bed'

    # patient details
    occ_bed = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat, status='occupied')
    bed_id = [data.id for data in occ_bed]
    bed_transfer_record = Bed_Transfer.objects.all()
    transfer_uhid = [data.uhid for data in bed_transfer_record]
    admission_records = AdmissionInfos.objects.all()
    admission_uhid = [data.uhid for data in admission_records]
    uhid_list = []
    for bed_no in bed_id:
        for uhid in admission_uhid:
            if uhid in transfer_uhid:
                bed_transfer_uhid = Bed_Transfer.objects.filter(uhid=uhid, to_bed_no=bed_no).last()
                if bed_transfer_uhid:
                    uhid_list.append(bed_transfer_uhid.uhid)
            else:
                ad_uhid = AdmissionInfos.objects.filter(uhid=uhid, bed_no=bed_no).last()
                if ad_uhid:
                    uhid_list.append(ad_uhid.uhid)

    print('bed_id', bed_id)
    print('uhid_list', uhid_list)
    paitent_name = PatientsRegistrationsAllInOne.objects.filter(uhid__in=uhid_list)

    loo = []
    for data1, data2 in zip(paitent_name, bed_id):
        a = BedMasterMain.objects.get(id=data2)
        age = PatientRegistrationMains.objects.get(uhid=data1.uhid)
        loo.append([data1.first_name, data1.gender, a.bed_no, age.age])
    print('safsda', loo)

    # all
    all_detils = ''
    if ward_name == 'all':
        all_detils = BedMasterMain.objects.all()

        type_cat = []
        bed_nos = []
        ward_type_names = [data.ward_type for data in ward_type_records]
        ward_cat_names = [data.category_name for data in ward_cat_records]
        for type in ward_type_names:
            for cat in ward_cat_names:
                record = BedMasterMain.objects.filter(ward_type=type, ward_category=cat)
                if record:
                    type_cat.append([type, cat])
                    bed_nos.append([record])
        print(type_cat)
        print(bed_nos)
        all_detils = zip(type_cat, bed_nos)

    context = {
        'ward_type': ward_type_records, 'ward_cat': ward_cat_records, 'bed_number': bed_number, 'bed': bed,
        'all_detils': all_detils,
        'loo': loo, 'login_name': name
    }
    return render(request,'try/bed_view.html', context)


def bed_load(request):
    ward_name = request.GET.get('ward_type_id')
    print('wing_id Id', ward_name)
    type = AdmissionWardType.objects.get(ward_type=ward_name)
    cat = AdmissionWardCate.objects.filter(ward_type_id=type.id)

    print(cat)
    return JsonResponse(list(cat.values('id', 'category_name')), safe=False)


import calendar
from datetime import datetime
@login_required(login_url='/user_login')
def doctor_ability_report(request):
    doctor = DoctorTable.objects.filter()
    doctor_shedules_records = AvailableDayScheduleMasterTemp.objects.all()
    doctor_shedules_list = [data.doctor_id for data in doctor_shedules_records]
    search_doc = request.POST.get('search_doc')
    if search_doc:
        doctor_list = [search_doc]
    else:
        doctor_list = [data.doctor_id for data in doctor]
    doctor_names = []
    schedules = []
    doc_time = []
    for id in doctor_list:
        if id in doctor_shedules_list:
            get_doctor_shedules = AvailableDayScheduleMasterTemp.objects.filter(doctor_id=id).last()
            doctor_shedule_dates = get_doctor_shedules.dates_available
            doctor_shedule_dates_list = doctor_shedule_dates.split(',')
            list = []
            for data in doctor_shedule_dates_list:
                a = data.replace("'", '')
                b = a.replace('[', '')
                c = b.replace(']', '')
                d = c.replace(' ', '')
                list.append(d)
            a = []
            mon = []
            tue = []
            wen = []
            thur = []
            fri = []
            sat = []
            sun = []
            count = 0
            aa = datetime.strptime(list[0], '%Y-%m-%d')
            start_da = aa.strftime("%d")
            start_date = int(start_da)
            for data in list:
                toatal = []
                cr_date = datetime.strptime(data, '%Y-%m-%d')
                datee = cr_date.strftime("%d")
                int_date = int(datee)
                day = calendar.day_name[cr_date.weekday()]
                if count == 0:
                    if day == 'Monday':
                        sun.append('')
                    elif day == 'Tuesday':
                        sun.append('')
                        mon.append('')
                    elif day == 'Wednesday':
                        sun.append('')
                        mon.append('')
                        tue.append('')
                    elif day == 'Thursday':
                        sun.append('')
                        mon.append('')
                        tue.append('')
                        wen.append('')
                    elif day == 'Friday':
                        sun.append('')
                        mon.append('')
                        tue.append('')
                        wen.append('')
                        thur.append('')
                    elif day == 'Saturday':
                        sun.append('')
                        mon.append('')
                        tue.append('')
                        wen.append('')
                        thur.append('')
                        fri.append('')
                    elif day == 'Sunday':
                        pass
                if start_date == int_date:
                    if day == 'Monday':
                        mon.append(data)
                    elif day == 'Tuesday':
                        tue.append(data)
                    elif day == 'Wednesday':
                        wen.append(data)
                    elif day == 'Thursday':
                        thur.append(data)
                    elif day == 'Friday':
                        fri.append(data)
                    elif day == 'Saturday':
                        sat.append(data)
                    elif day == 'Sunday':
                        sun.append(data)
                    start_date += 1

                else:
                    if day == 'Monday':
                        sun.append('')
                        mon.append(data)
                    elif day == 'Tuesday':
                        mon.append('')
                        tue.append(data)
                    elif day == 'Wednesday':
                        tue.append('')
                        wen.append(data)
                    elif day == 'Thursday':
                        wen.append('')
                        thur.append(data)
                    elif day == 'Friday':
                        thur.append('')
                        fri.append(data)
                    elif day == 'Saturday':
                        fri.append('')
                        sat.append(data)
                    elif day == 'Sunday':
                        sat.append('')
                        sun.append(data)
                    start_date += 2
                count = 1
            a.append(zip(mon, tue, wen, thur, fri, sat, sun))
            schedules.append(a)
            doctor_na = DoctorTable.objects.get(doctor_id=id)
            doctor_names.append(doctor_na.doctor_name)
            doctor_shedule_time = get_doctor_shedules.time_slots
            start = doctor_shedule_time[2:9]
            end = doctor_shedule_time[-7:-2]
            shedule_timeper_date = start + end
            doc_time.append(shedule_timeper_date)
    records = zip(schedules, doctor_names, doc_time)
    context = {
        'records': records, 'doctor': doctor
    }
    return render(request, 'Reports/doctor_ablility_report.html', context)

@login_required(login_url='/user_login')
def bed_charge(request):
    name = request.session['Name']
    ward_type_records = AdmissionWardType.objects.all()
    ward_name = request.POST.get('ward_name')
    ward_cat = request.POST.get('ward_cat')
    request.session['bed_records'] = ''
    before_charge = ''
    after_charge = ''
    bed_charge = BedCharge.objects.filter(ward_type=ward_name, ward_cat=ward_cat)
    if bed_charge:
        bed_master = bed_charge
        after_charge = 'after_charge'
        request.session['ward_name'] = ward_name
        request.session['ward_cat'] = ward_cat
    else:
        print('else')
        bed_master = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat)
        if bed_master:
            before_charge = 'before_charge'
            request.session['ward_name'] = ward_name
            request.session['ward_cat'] = ward_cat
    # print(bed_master)

    context = {
        'ward_type_records': ward_type_records, 'bed_master': bed_master, "ward_name": ward_name, 'ward_cat': ward_cat,
        'before_charge': before_charge, 'bed_charge': bed_charge, 'after_charge': after_charge, 'login_name': name
    }
    return render(request, 'general_master/bed_charge.html', context)



@login_required(login_url='/user_login')
def single_bed_charge_load(request):
    name = request.session['Name']
    ward_name = request.session['ward_name']
    ward_cat = request.session['ward_cat']
    print(ward_name, ward_cat)
    charge = request.POST.get('Total_charge')
    a = BedCharge.objects.all()
    bed_master = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat)
    bed_no_list = [data.bed_no for data in bed_master]
    if not charge:
        charge_list = request.POST.getlist('single_charge')
        old_data = BedCharge.objects.filter(ward_type=ward_name, ward_cat=ward_cat)
        old_data.delete()
        for i in range(len(charge_list)):
            single_charge = charge_list[i]
            bed_no = bed_no_list[i]
            data = BedCharge.objects.get_or_create(ward_type=ward_name, ward_cat=ward_cat, bed_no=bed_no,
                                                   bed_charge=single_charge)
        return HttpResponseRedirect('/bed_charge')
    context = {
        'bed_master': bed_master, "ward_name": ward_name, 'ward_cat': ward_cat, 'charge': charge, 'login_name': name

    }
    return render(request, 'general_master/bed_charge.html', context)



@login_required(login_url='/user_login')
def Bed_charge_edit(request):
    name = request.session['Name']
    ward_name = request.session['ward_name']
    ward_cat = request.session['ward_cat']
    bed_master = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat)
    before_charge = 'before_charge'
    context = {
        'before_charge': before_charge, 'bed_master': bed_master, 'login_name': name
    }
    return render(request, 'general_master/bed_charge.html', context)


def auto_bed_charge_save(ad_id):
    adid_list = [ad_id]
    for adid in adid_list:
        records = Bed_Transfer.objects.filter(admission_ID=adid)
        ad_record= AdmissionInfos.objects.get(admission_ID=adid)
        bed_charge = BedCharge.objects.get(ward_type=ad_record.req_ward_type, ward_cat=ad_record.req_ward_cate,
                                                bed_no=ad_record.bed_no)
        admission_datetime = ad_record.admission_datetime
        if records:
            record = records.first()
            current_datetime = record.transfer_datatime
        else:
            current_datetime = datetime.now()
        between_dates = current_datetime - admission_datetime
        for i in range(between_dates.days):
            date = admission_datetime + timedelta(days=i)
            data = BedChargeSlip_main(uhid=ad_record.uhid, ward_type=ad_record.req_ward_type, ward_cat=ad_record.req_ward_cate,
                                    bed_no=ad_record.bed_no,
                                    datetime=date, bed_charge=bed_charge.bed_charge,
                                    admission_ID=ad_record.admission_ID
                                    )
            data.save()
        if records:
            count = 1
            for s_record in records:
                bed_charge = BedCharge.objects.filter(ward_type=s_record.to_ward_type, ward_cat=s_record.to_ward_cat,
                                                    bed_no=s_record.to_bed_no).last()
                if count < len(records):
                    r = records[count]
                    current_datetime = r.transfer_datatime
                    count += 1
                else:
                    current_datetime = datetime.now()
                last_datetime = s_record.transfer_datatime
                between_dates = current_datetime - last_datetime

                for i in range(between_dates.days):
                    date = last_datetime + timedelta(days=i)
                    data = BedChargeSlip_main(uhid=ad_record.uhid, ward_type=s_record.to_ward_type, ward_cat=s_record.to_ward_cat,
                                            bed_no=s_record.to_bed_no,
                                            datetime=date, bed_charge=bed_charge.bed_charge,
                                            admission_ID=ad_record.admission_ID
                                            )
                    data.save()

def auto_bed_charge():
    BedChargeSlip.objects.all().delete()
    admission_records = AdmissionInfos.objects.filter(status='admitted')
    adid_list = [data.admission_ID for data in admission_records]

    for adid in adid_list:
        records = Bed_Transfer.objects.filter(admission_ID=adid)
        ad_record= AdmissionInfos.objects.get(admission_ID=adid)
        bed_charge = BedCharge.objects.get(ward_type=ad_record.req_ward_type, ward_cat=ad_record.req_ward_cate,
                                                bed_no=ad_record.bed_no)
        admission_datetime = ad_record.admission_datetime
        if records:
            record = records.first()
            current_datetime = record.transfer_datatime
        else:
            current_datetime = datetime.now()
        between_dates = current_datetime.date() - admission_datetime.date()
        for i in range(between_dates.days + 1):
            date = admission_datetime + timedelta(days=i)
            data = BedChargeSlip(uhid=ad_record.uhid, ward_type=ad_record.req_ward_type, ward_cat=ad_record.req_ward_cate,
                                    bed_no=ad_record.bed_no,
                                    datetime=date, bed_charge=bed_charge.bed_charge,
                                    admission_ID=ad_record.admission_ID
                                    )
            data.save()
        if records:
            count = 1
            for s_record in records:
                bed_charge = BedCharge.objects.filter(ward_type=s_record.to_ward_type, ward_cat=s_record.to_ward_cat,
                                                    bed_no=s_record.to_bed_no).last()
                if count < len(records):
                    r = records[count]
                    current_datetime = r.transfer_datatime
                    count += 1
                else:
                    current_datetime = datetime.now()
                last_datetime = s_record.transfer_datatime
                between_dates = current_datetime.date() - last_datetime.date()

                for i in range(between_dates.days + 1):
                    date = last_datetime + timedelta(days=i)
                    data = BedChargeSlip(uhid=ad_record.uhid, ward_type=s_record.to_ward_type, ward_cat=s_record.to_ward_cat,
                                            bed_no=s_record.to_bed_no,
                                            datetime=date, bed_charge=bed_charge.bed_charge,
                                            admission_ID=ad_record.admission_ID
                                            )
                    data.save()


@login_required(login_url='/user_login')
def bed_charge_slip(request):
    auto_bed_charge()
    name = request.session['Name']
    ad_records = AdmissionInfos.objects.filter(status='admitted')
    uhid_list = [data.uhid for data in ad_records]
    records = PatientsRegistrationsAllInOne.objects.filter(uhid__in=uhid_list)
    return render(request, 'Reports/bed_charge_slip.html',{'records': records, 'login_name': name})

@login_required(login_url='/user_login')
def bed_charge_slip_details(request,pk):
    name = request.session['Name']
    request.session['uhid_pk'] = pk
    records = BedChargeSlip.objects.filter(uhid=pk).order_by('-datetime')
    ward_type_records = AdmissionWardType.objects.all()
    ward_cat_records = AdmissionWardCate.objects.all()
    ward_name = request.POST.get('ward_name')
    ward_cat = request.POST.get('ward_cat')
    bed_no = request.POST.get('id_to_bed_no')
    charge_slip = request.POST.get('charge_slip')
    date_time = request.POST.get('date_time')
    date_time = datetime.now()
    form = BedChargeSlipForm()
    if request.method == 'POST':
        data = BedChargeSlip.objects.get_or_create(
            uhid=pk,
            ward_type=ward_name,
            ward_cat=ward_cat,
            bed_no=bed_no,
            bed_charge=charge_slip,
            datetime=date_time
        )
        return HttpResponseRedirect(f'/bed_charge_slip_details/{pk}')
    context = {
        'records': records, 'form': form, 'ward_type_records': ward_type_records, 'ward_cat_records': ward_cat_records,
        'date_time': date_time, 'uhid': pk, 'login_name': name
    }
    return render(request, 'Reports/bed_charge_slip_details.html', context)



@login_required(login_url='/user_login')
def charge_slip_load(request):
    ward_name = request.GET.get('ward_type_id')
    ward_cat = request.GET.get('ward_cat_id')
    print('wing_id', ward_name, ward_cat)
    if ward_cat:
        print('==============')
        bed = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat)
        print('oieshfish', bed)
        return JsonResponse(list(bed.values('bed_no', 'bed_no')), safe=False)
    else:
        type = AdmissionWardType.objects.get(ward_type=ward_name)
        cat = AdmissionWardCate.objects.filter(ward_type_id=type.id)
        print(cat)
        return JsonResponse(list(cat.values('id', 'category_name')), safe=False)



@login_required(login_url='/user_login')
def bed_charge_slip_details_edit(request, pk):
    name = request.session['Name']
    uhid = request.session['uhid_pk']
    records = BedChargeSlip.objects.filter(uhid=pk).order_by('-datetime')
    context = {
        'records': records, 'uhid': uhid, 'login_name': name
    }
    return render(request, 'Reports/bed_charge_slip_details_edit.html', context)



@login_required(login_url='/user_login')
def bed_charge_slip_details_editing(request, pk):
    name = request.session['Name']
    uhid = request.session['uhid_pk']
    records = BedChargeSlip.objects.get(id=pk)
    ward_name = request.POST.get('ward_type')
    ward_cat = request.POST.get('ward_cat')
    bed_no = request.POST.get('bed_no')
    charge_slip = request.POST.get('charge_slip')
    date_time = request.POST.get('date_time')
    # datee=datetime.strptime(date_time, "%b.%d-%Y-%H:%M:%S")
    # # datee=date_time.strftime("%Y-%d-%m %H:%M:%S")
    # print('date_time',datee)
    if request.method == 'POST':
        records.uhid = uhid
        records.ward_type = ward_name
        records.ward_cat = ward_cat
        records.bed_no = bed_no
        records.bed_charge = charge_slip
        records.datetime = date_time
        records.save()
        return HttpResponseRedirect(f'/bed_charge_slip_details/{uhid}')
    context = {
        'records': records, 'login_name': name
    }
    return render(request, 'Reports/bed_charge_slip_editing.html', context)


#  bed charge genrating function

@login_required(login_url='/user_login')
def discharge_report(request):
    dis_records = discharge.objects.all()
    dis_records_uhid = [data.uhid for data in dis_records]
    dis_records_uhid_f = [data.uhid for data in dis_records]
    bed_transfer_records = Bed_Transfer.objects.all()
    bed_transfer_uhid = [data.uhid for data in bed_transfer_records]
    doctor_transfer_records = Doctor_Transfer.objects.all()
    doctor_transfer_uhid = [data.uhid for data in doctor_transfer_records]
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    doctor_name = request.POST.get('doctor_name')
    ward_type_f = request.POST.get('ward_type')
    ward_cat_f = request.POST.get('ward_cat')
    print(start_date, end_date, doctor_name, ward_type_f, ward_cat_f)
    if start_date or end_date or doctor_name or ward_type_f or ward_cat_f:
        if start_date and end_date:
            dis_records = discharge.objects.filter(discharge_datetime__range=[start_date, end_date])
            dis_records_uhid = [data.uhid for data in dis_records]
        elif doctor_name:
            print('doctor_name', doctor_name)
            dis_records_uhid_f = []
            for uhid in dis_records_uhid:
                if uhid in doctor_transfer_uhid:
                    doctor = Doctor_Transfer.objects.filter(uhid=uhid).last()
                    doctor_i = DoctorTable.objects.get(doctor_name=doctor.to_doctor)
                    print('doctor_i', doctor_i)
                    print('1', doctor_i.doctor_id, doctor_name)
                    if doctor_i.doctor_id == doctor_name:
                        dis_records_uhid_f.append(uhid)
                else:
                    doctor = AdmissionInfos.objects.filter(uhid=uhid).last()
                    doctor_i = DoctorTable.objects.get(doctor_name=doctor.primary_doctor)
                    print('2', doctor_i.doctor_id, doctor_name)
                    if doctor_i.doctor_id == doctor_name:
                        dis_records_uhid_f.append(uhid)
            print('records1', dis_records_uhid_f)
        elif ward_type_f:
            dis_records_uhid_f = []
            for uhid in dis_records_uhid:
                if uhid in bed_transfer_uhid:
                    bed = Bed_Transfer.objects.filter(uhid=uhid).last()
                    ward_type_id = AdmissionWardType.objects.get(ward_type=bed.to_ward_type)
                    if str(ward_type_id.id) == str(ward_type_f):
                        dis_records_uhid_f.append(uhid)
                else:
                    print('else')
                    bed = AdmissionInfos.objects.filter(uhid=uhid).last()
                    ward_type_id = AdmissionWardType.objects.get(ward_type=bed.req_ward_type)
                    print(str(ward_type_id.id), str(ward_type_f))
                    if str(ward_type_id.id) == str(ward_type_f):
                        dis_records_uhid_f.append(uhid)
            print('records2', dis_records_uhid_f)
        elif ward_cat_f:
            dis_records_uhid_f = []
            for uhid in dis_records_uhid:
                if uhid in bed_transfer_uhid:
                    bed = Bed_Transfer.objects.filter(uhid=uhid).last()
                    ward_cat_id = AdmissionWardCate.objects.get(category_name=bed.to_ward_cat)
                    if str(ward_cat_id.id) == str(ward_cat_f):
                        dis_records_uhid_f.append(uhid)
                else:
                    bed = AdmissionInfos.objects.filter(uhid=uhid).last()
                    ward_cat_id = AdmissionWardCate.objects.get(category_name=bed.req_ward_cate)
                    if str(ward_cat_id.id) == str(ward_cat_f):
                        dis_records_uhid_f.append(uhid)
            print('records3', dis_records_uhid_f)

    pat_records = PatientsRegistrationsAllInOne.objects.filter(uhid__in=dis_records_uhid_f)
    ad_records = AdmissionInfos.objects.filter(uhid__in=dis_records_uhid_f)

    ward_type_records = AdmissionWardType.objects.all()
    ward_cat_records = AdmissionWardCate.objects.all()
    doctor_records = DoctorTable.objects.all()
    ward_type_list = []
    ward_cat_list = []
    bed_no_list = []
    # all discharge records
    for uhid in dis_records_uhid_f:
        if uhid in bed_transfer_uhid:
            bed = Bed_Transfer.objects.filter(uhid=uhid).last()
            ward_type = AdmissionWardType.objects.get(id=bed.to_ward_type_id)
            ward_cat = AdmissionWardCate.objects.get(id=bed.to_ward_cat_id)
            bed_no = BedMasterMain.objects.get(id=bed.to_bed_no_id)
            ward_type_list.append(ward_type.ward_type)
            ward_cat_list.append(ward_cat.category_name)
            bed_no_list.append(bed_no.bed_no)
        else:
            ad = AdmissionInfos.objects.filter(uhid=uhid).last()
            ward_type = AdmissionWardType.objects.get(id=ad.req_ward_type_id)
            ward_cat = AdmissionWardCate.objects.get(id=ad.req_ward_cate_id)
            # bed_no=BedMasterMain.objects.get(id=ad.bed_no)
            ward_type_list.append(ward_type.ward_type)
            ward_cat_list.append(ward_cat.category_name)
            bed_no_list.append(ad.bed_no)
    records = zip(dis_records, pat_records, ad_records, ward_type_list, ward_cat_list, bed_no_list)

    context = {
        'records': records, 'ward_type_records': ward_type_records, 'ward_cat_records': ward_cat_records,
        'doctor_records': doctor_records
    }

    return render(request, 'Reports/discharge_report.html', context)

#========================== 02/01/2023 Mantu ===========================

@login_required(login_url='/user_login')
def add_charge_profile(request):
    if request.method=='POST':
        qdict=request.POST
        print('Our Dict = ',qdict)
        sample_dict=dict(qdict.lists())
        profile_id=sample_dict.get('profile_id')
        profile_charge=sample_dict.get('profile_charge')
        # print('profile_charge= ',profile_charge)
        print('profile_id= ',profile_id)
        if profile_id is None and profile_charge is None:
            return HttpResponseRedirect('/composite_services')
        profile_master=ProfileMaster.objects.filter(profile_name__in=profile_id)
        print('=========================',profile_master)
        if profile_master.exists():
            print('Yes',profile_master.count())
            for id in range(profile_master.count()):
                if profile_charge[id]=='':
                    print('profile_charge============',profile_charge)
                    continue
                print('profile_chargesssssss', profile_charge)
                adding_charge = ProfileMaster.objects.get(profile_name=profile_id[id])
                adding_charge.profile_amount = profile_charge[id]  # updating
                adding_charge.save()  # Saving
                # print(f'id =  {service_id[id]} Charges = {charges[id]}')

        print(f'Service Id {profile_id} , Charges {profile_charge}')
        # return HttpResponseRedirect('/service_charge_master')
    return HttpResponseRedirect('/composite_services')

@login_required(login_url='/user_login')
def composite_services(request):
    print('This is composite_services...')
    service_charge_master = ServiceChargeMaster.objects.all()
    tariff_master = TariffMaster.objects.all()
    # ward_type = WardType.objects.all()
    # ward_category = WardCategory.objects.all()
    ward_type = AdmissionWardType.objects.all()
    ward_category = AdmissionWardCate.objects.all()
    service_cate=ServiceCategory.objects.all()
    service_sub_cate=ServiceSubCategory.objects.all()
    service_department = ServiceDepartment.objects.all()
    service_sub_department = ServiceSubDepartment.objects.all()
    form = ServiceChargeMaster()
    sd = service_department
    ssd = service_sub_department
    records = None
    record=''
    recordssss=''
    d2_list = []
    d3_list = []
    d4_list = []
    d1_list = []
    if request.method == 'POST':
        form = ServiceChargeMaster(request.POST)
        searching = request.POST.get('search')
        submit = request.POST.get('submit')
        print('Search============')
        if searching == 'Search':
            print('Im searching data...')
            service_department = request.POST.get('service_department')
            service_sub_department = request.POST.get('service_sub_department')
            print(f'service department = {service_department}, service id = {service_sub_department}')
            records = ProfileService.objects.filter(
                service_department=service_department,service_sub_department=service_sub_department)
            d1=[data.profile_name for data in records]
            d3=[data.units for data in records]
            d5=[data.service_department for data in records]
            d7=[data.service_sub_department for data in records]
            d2=set(d1)#profile_name
            d4=set(d3)#units
            d6=set(d5)#service_department
            d8=set(d7)#service_sub_department
            # records1=[]
            # data=zip(d2,d4,d6,d8)
            # print(d2,d4,d6,d8)
            records_profile = ProfileMaster.objects.filter(profile_name__in=d2)
            print('records_profile----->,',records_profile)
            for data in d2:
                recorddddd = ProfileMaster.objects.filter(profile_name=data)
                da1 = [data.profile_name for data in recorddddd]
                da2= [data.profile_amount for data in recorddddd]
                da3= [data.id for data in recorddddd]
                d1_list.append(da1)
                d2_list.append(da2)
                d3_list.append(da3)
                # records1.append(recorddddd)
                print('recordssss==============',recordssss)

            record=zip(d1_list,d2_list,d3_list)
            recordssss=zip(d1_list,d2_list,d3_list)
            s_d = ServiceDepartment.objects.get(service_department=service_department)
            s_s_d = ServiceSubDepartment.objects.get(service_sub_department=service_sub_department)
            ser_dep = s_d.service_department
            ser_sub_dep = s_s_d.service_sub_department
            ser_dep_id = s_d.id
            ser_sub_dep_id = s_s_d.id
            context = {
                'service_charge_master': service_charge_master, 'form': form, 'tariff_master': tariff_master,
                'service_department': sd, 'service_sub_department': ssd, 'ward_category': ward_category,
                'ward_type': ward_type,'record':record,'recordssss':recordssss,
                'records': records, 's_d': ser_dep, 's_s_d': ser_sub_dep, 'ser_dep_id': ser_dep_id,
                'ser_sub_dep_id': ser_sub_dep_id,'service_cate':service_cate,'service_sub_cate':service_sub_cate,
                'records_profile':records_profile,
            }
            return render(request, 'clinical/composite_services.html', context)
        elif submit=='Save':
            tariff_id = request.POST.get('tariff_id')
            profile_id = request.POST.getlist('profile_id')
            profile_charge = request.POST.getlist('profile_charge')
            applicable_date = request.POST.get('applicable_date')
            service_category = request.POST.get('service_category')
            service_sub_category = request.POST.get('service_sub_category')
            ward_type = request.POST.get('ward_type')
            ward_category = request.POST.get('ward_category')
            ipd_opd = request.POST.get('ipd_opd')
            print('alldata',ward_type,ward_category,ipd_opd,profile_id,profile_charge)
            print('alldataservice_sub_category',service_category,service_sub_category)
            service_check = ''
            for d in range(len(profile_id)):
                var_tariff_id=tariff_id
                var_profile_id=profile_id[d]
                var_profile_charge=profile_charge[d]
                var_applicable_date=applicable_date
                var_service_category=service_category
                var_ward_type=ward_type
                var_ward_category=ward_category
                var_ipd_opd=ipd_opd
                var_service_sub_category=service_sub_category
                print('var_profile_id',var_profile_id)
                if ipd_opd == 'OPD':
                    print('OPD')
                    service_check=ProfileChargeMaster.objects.filter(tariff_id=var_tariff_id,profile_id=var_profile_id)
                else:
                    service_check=ProfileChargeMaster.objects.filter(tariff_id=var_tariff_id,profile_id=var_profile_id,ward_type=var_ward_type,ward_category=var_ward_category)
                if not service_check.exists():
                    data =ProfileChargeMaster(
                        tariff_id_id=var_tariff_id,
                        profile_id_id=var_profile_id,
                        profile_charge=var_profile_charge,
                        applicable_date=var_applicable_date,
                        service_category_id=var_service_category,
                        service_sub_category_id=var_service_sub_category,
                        ward_type_id=var_ward_type,
                        ward_category_id=var_ward_category,
                        # inactive=var_inactive,
                        ipd_opd=var_ipd_opd,
                        created_by_id = request.user.id,
                        location_id = request.location,
                    )
                    data.save()
                    print('data saved..............', data)
                else:
                    print('this data allready there -------------------------')
            return HttpResponseRedirect('/composite_services')
    context = {
        'service_charge_master': service_charge_master, 'form': form, 'tariff_master': tariff_master,
        'ward_category': ward_category, 'ward_type': ward_type,
        'service_department': service_department, 'service_sub_department': service_sub_department, 'records': records,
        'recordssss':recordssss,'service_cate':service_cate,'service_sub_cate':service_sub_cate,

    }
    return render(request,'clinical/composite_services.html',context)

@login_required(login_url='/user_login')
def add_charge_package_services(request):
    if request.method=='POST':
        qdict=request.POST
        print('Our Dict = ',qdict)
        sample_dict=dict(qdict.lists())
        profile_id=sample_dict.get('profile_id')
        profile_charge=sample_dict.get('profile_charge')
        # print('profile_charge= ',profile_charge)
        print('profile_id= ',profile_id)
        if profile_id is None and profile_charge is None:
            return HttpResponseRedirect('/composite_services')
        package_master=OpdPackageMaster.objects.filter(package_name__in=profile_id)
        print('=========================',package_master)
        if package_master.exists():
            print('Yes',package_master.count())
            for id in range(package_master.count()):
                if profile_charge[id]=='':
                    print('profile_charge============',profile_charge)
                    continue
                print('profile_chargesssssss', profile_charge)
                adding_charge = OpdPackageMaster.objects.get(package_name=profile_id[id])
                adding_charge.package_amount = profile_charge[id]  # updating
                adding_charge.save()  # Saving
                # print(f'id =  {service_id[id]} Charges = {charges[id]}')

        print(f'Service Id {profile_id} , Charges {profile_charge}')
        # return HttpResponseRedirect('/service_charge_master')
    return HttpResponseRedirect('/package_services')

# @login_required(login_url='/user_login')
# def package_services(request):
#     print('This is composite_services...')
#     service_charge_master = ServiceChargeMaster.objects.all()
#     tariff_master = TariffMaster.objects.all()
#     ward_type = WardType.objects.all()
#     ward_category = WardCategory.objects.all()
#     service_department = ServiceDepartment.objects.all()
#     service_sub_department = ServiceSubDepartment.objects.all()
#     form = ServiceChargeMaster()
#     sd = service_department
#     ssd = service_sub_department
#     records = None
#     record=''
#     recordssss=''
#     d1_list = []
#     d2_list = []
#     d3_list = []
#     d4_list = []
#     d1_list = []
#     if request.method == 'POST':
#         form = ServiceChargeMaster(request.POST)
#         searching = request.POST.get('search')
#         submit = request.POST.get('submit')
#         print('Search============')
#         if searching == 'Search':
#             print('Im searching data...')
#             service_department = request.POST.get('service_department')
#             service_sub_department = request.POST.get('service_sub_department')
#             print(f'service department = {service_department}, service id = {service_sub_department}')
#             records = OpdPackageService.objects.filter(
#                 service_department=service_department,service_sub_department=service_sub_department)
#             d1=[data.package_name for data in records]
#             d5=[data.service_department for data in records]
#             d7=[data.service_sub_department for data in records]
#             d2=set(d1)
#             d6=set(d5)
#             d8=set(d7)
#             data=zip(d2,d6,d8)
#             print(d2,d6,d8)
#             for data in d2:
#                 recorddddd = OpdPackageMaster.objects.filter(package_name=data)
#                 # recordssss.append(recorddddd)
#                 da1 = [data.package_name for data in recorddddd]
#                 da2= [data.package_amount for data in recorddddd]
#                 d1_list.append(da1)
#                 d2_list.append(da2)
#                 print('recordssss==============',recordssss)
#             # for p_name,p_unit,p_deprt,p_sub_deprt in data:
#             #
#             #     d3_list.append(p_deprt)
#             #     d4_list.append(p_sub_deprt)
#             record=zip(d1_list,d2_list)
#             recordssss=zip(d1_list,d2_list)
#             s_d = ServiceDepartment.objects.get(service_department=service_department)
#             s_s_d = ServiceSubDepartment.objects.get(service_sub_department=service_sub_department)
#             ser_dep = s_d.service_department
#             ser_sub_dep = s_s_d.service_sub_department
#             ser_dep_id = s_d.id
#             ser_sub_dep_id = s_s_d.id
#             context = {
#                 'service_charge_master': service_charge_master, 'form': form, 'tariff_master': tariff_master,
#                 'service_department': sd, 'service_sub_department': ssd, 'ward_category': ward_category,
#                 'ward_type': ward_type,'record':record,'recordssss':recordssss,
#                 'records': records, 's_d': ser_dep, 's_s_d': ser_sub_dep, 'ser_dep_id': ser_dep_id,
#                 'ser_sub_dep_id': ser_sub_dep_id,
#             }
#             return render(request, 'clinical/package_services.html', context)
#         elif submit == 'Save':
#             print('Im ready to save your data')
#             tariff_id = request.POST.get('tariff_id')
#             package_id = request.POST.getlist('profile_id')
#             package_charge = request.POST.getlist('profile_charge')
#             applicable_date = request.POST.get('applicable_date')
#             print('profile_id', package_id,tariff_id,package_charge,applicable_date)

#             ward_type = request.POST.get('ward_type')
#             ward_category = request.POST.get('ward_category')
#             inactive = request.POST.get('inactive')
#             for d in range(len(package_id)):
#                 var_tariff_id = tariff_id
#                 var_package_id = package_id[d]
#                 var_package_charge =package_charge[d]
#                 var_applicable_date = applicable_date
#                 var_ward_type = ward_type
#                 var_inactive = inactive
#                 var_ward_category = ward_category
#                 data = PackageChargeMaster(
#                     tariff_id_id=var_tariff_id,
#                     package_id=var_package_id,
#                     package_charge=var_package_charge,
#                     applicable_date=var_applicable_date,
#                     ward_type_id=var_ward_type,
#                     ward_category_id=var_ward_category,
#                     inactive=var_inactive,
#                 )
#                 data.save()
#                 print('data saved..............', data)
#             return HttpResponseRedirect('/package_services')
#     context = {
#         'service_charge_master': service_charge_master, 'form': form, 'tariff_master': tariff_master,
#         'ward_category': ward_category, 'ward_type': ward_type,
#         'service_department': service_department, 'service_sub_department': service_sub_department, 'records': records,
#         'recordssss':recordssss,
#     }
#     return render(request,'clinical/package_services.html',context)


@login_required(login_url='/user_login')
def package_services(request):
    tariff_master = TariffMaster.objects.all()
    service_category=ServiceCategory.objects.all()
    service_sub_category=ServiceSubCategory.objects.all()
    service_department = ServiceDepartment.objects.all()
    service_sub_department = ServiceSubDepartment.objects.all()
    sd = service_department
    ssd = service_sub_department
    records = None
    recordssss=''
    d1_list = []
    d2_list = []
    d3_list = []
    if request.method == 'POST':
        searching = request.POST.get('search')
        submit = request.POST.get('submit')
        print('searching',searching)
        if searching == 'Search':
            service_department = request.POST.get('service_department')
            service_sub_department = request.POST.get('service_sub_department')
            s_d = ServiceDepartment.objects.get(service_department=service_department)
            s_s_d = ServiceSubDepartment.objects.get(service_sub_department=service_sub_department)
            records = OpdPackageService.objects.filter(service_department=s_d.id,service_sub_department=s_s_d.id)
            package=[data.package_name for data in records]
            p_name=set(package)
            for dat in p_name:
                recorddddd = OpdPackageMaster.objects.filter(package_name=dat)
                da_id = [data.id for data in recorddddd]
                da1 = [data.package_name for data in recorddddd]
                da2= [data.package_amount for data in recorddddd]
                d3_list.append(da_id)
                d1_list.append(da1)
                d2_list.append(da2)
            record=zip(d1_list,d2_list)
            recordssss=zip(d3_list,d2_list)
            s_d = ServiceDepartment.objects.get(service_department=service_department)
            s_s_d = ServiceSubDepartment.objects.get(service_sub_department=service_sub_department)
            ser_dep = s_d.service_department
            ser_sub_dep = s_s_d.service_sub_department
            ser_dep_id = s_d.id
            ser_sub_dep_id = s_s_d.id
            context = {
                'service_charge_master': service_charge_master,'tariff_master': tariff_master,
                'service_department': sd, 'service_sub_department': ssd,'service_category':service_category,
                'service_sub_category':service_sub_category,'record':record,'recordssss':recordssss,
                'records': records, 's_d': ser_dep, 's_s_d': ser_sub_dep, 'ser_dep_id': ser_dep_id,
                'ser_sub_dep_id': ser_sub_dep_id,
            }
            return render(request, 'clinical/package_services.html', context)
        elif submit == 'Save':
            print('Im ready to save your data')
            tariff_id = request.POST.get('tariff_id')
            package_id = request.POST.getlist('profile_id')
            package_charge = request.POST.getlist('profile_charge')
            applicable_date = request.POST.get('applicable_date')
            print('profile_id', package_id,tariff_id,package_charge,applicable_date)

            ward_type = request.POST.get('ward_type')
            ward_category = request.POST.get('ward_category')
            inactive = request.POST.get('inactive')
            for d in range(len(package_id)):
                var_tariff_id = tariff_id
                var_package_id = package_id[d]
                var_package_charge =package_charge[d]
                var_applicable_date = applicable_date
                var_ward_type = ward_type
                var_inactive = inactive
                var_ward_category = ward_category
                service_check = PackageChargeMaster.objects.filter(tariff_id=var_tariff_id, package_id=var_package_id)
                if not service_check.exists():
                    data = PackageChargeMaster(
                        tariff_id_id=var_tariff_id,
                        package_id_id=var_package_id,
                        package_charge=var_package_charge,
                        applicable_date=var_applicable_date,
                        ward_type_id=var_ward_type,
                        ward_category_id=var_ward_category,
                        inactive=var_inactive,
                    )
                    data.save()
                    print('data saved..............', data)
                else:
                    print('data allready there-------------...')
            return HttpResponseRedirect('/package_services')
    context = {
        'service_charge_master': service_charge_master, 'tariff_master': tariff_master,
        'service_category':service_category,'service_sub_category':service_sub_category,
        'service_department': service_department, 'service_sub_department': service_sub_department, 'records': records,
        'recordssss':recordssss,
    }
    return render(request,'clinical/package_services.html',context)



import schedule
import time

# ================ Gohila report================================

@login_required(login_url='/user_login')
def Patient_registration_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        city = request.POST.get('city')

        if start_date and end_date and city:
            records = PatientsRegistrationsAllInOne.objects.filter(
                registration_date_and_time__range=[start_date, end_date], city__icontains=city,location=request.location).order_by("-id")
            context = {
                'records': records,
            }
            return render(request, 'Reports/patient_registration.html', context)

        elif city:
            records = PatientsRegistrationsAllInOne.objects.filter(city__icontains=city,location=request.location).order_by("-id")
            context = {
                'records': records,
            }
            return render(request, 'Reports/patient_registration.html', context)
        elif start_date and end_date:
            records = PatientsRegistrationsAllInOne.objects.filter(
                registration_date_and_time__range=[start_date, end_date],location=request.location).order_by("-id")
            context = {
                'records': records,
            }
            return render(request, 'Reports/patient_registration.html', context)

    return render(request, 'Reports/patient_registration.html')

import datetime



@login_required(login_url='/user_login')
def Patient_registration_summery_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        records = PatientsRegistrationsAllInOne.objects.filter(
            registration_date_and_time__range=[start_date, end_date],
            location=request.location
        ).order_by('-registration_date_and_time')

        unique_dates = set(record.registration_date_and_time.date() for record in records)

        number_of_registrations = [
            PatientsRegistrationsAllInOne.objects.filter(
                registration_date_and_time__date=date,
                location=request.location
            ).count()
            for date in unique_dates
        ]

        total_registration = sum(number_of_registrations)

        all_records = zip(unique_dates, number_of_registrations)
        context = {
            'all_records': all_records,"total_registration":total_registration
        }
        return render(request, 'Reports/patient_registration_summery.html', context)
    return render(request, 'Reports/patient_registration_summery.html')



@login_required(login_url='/user_login')
def appointment_report(request):
    filtering_records = None
    if request.method == 'POST':
        direct = request.POST.get('direct')
        hospital = request.POST.get('hospital')
        if direct == 'User':
            filtering_records = BookedAppointments.objects.filter(admin="user",location=request.location).order_by('-patient_appointment_date')
        elif hospital == "Admin":
            filtering_records = BookedAppointments.objects.filter(admin='admin',location=request.location).order_by('-patient_appointment_date')
    return render(request, 'Reports/appointment_report.html',{'filtering_records': filtering_records})

@login_required(login_url='/user_login')
def patientvisit_report(request):
    form = PatientVisitMainForm()
    records1 = ''
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        UHID = request.POST.get('UHID').strip()
        if start_date and end_date and UHID:
            records1 = PatientVisitMains.objects.extra(select={
                'fname':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'mname':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'lname':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',

            }).filter(visit_date_time__range=[start_date, end_date],uhid=UHID,location=request.location).order_by("-uhid")

        elif start_date and end_date:
            records1 = PatientVisitMains.objects.extra(select={
                'fname':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'mname':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'lname':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',

            }).filter(visit_date_time__range=[start_date, end_date],location=request.location).order_by("-uhid")


        elif UHID:
            records1 = PatientVisitMains.objects.extra(select={
                'fname':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'mname':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'lname':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',

            }).filter(uhid=UHID,location=request.location).order_by("-uhid")

    return render(request, 'Reports/patient_visit.html', {'form': form,'records_list':records1})



@login_required(login_url='/user_login')
def consultant_report(request):
    records = DoctorTable.objects.all()
    doctor = [data.doctor_name for data in records]
    doctors = request.POST.get('consultant')
    filtering_records = None
    if request.method == 'POST':
        if doctors == 'all':
            filtering_records = BookedAppointments.objects.filter(location=request.location).order_by('-patient_appointment_date')
        else:
            filtering_records = BookedAppointments.objects.filter(doctor_name=doctors,location=request.location).order_by('-patient_appointment_date')
    context = {
        'doctor': doctor,'filtering_records': filtering_records
    }
    return render(request, 'Reports/consultant.html', context)


# =================================================================================================

@login_required(login_url='/user_login')
def grouping_admission_report(request):
    doctorr = DoctorTable.objects.filter(location=request.location)
    department = Ipd_Dept.objects.all()
    patient_categorys = AdmissionWardCate.objects.all()
    conditions = "Filters_only"
    seaching_butn = request.POST.get('Search')
    if seaching_butn == "search_btn":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        doctor_name = request.POST.get('primary_doctor')
        department_name = request.POST.get('department_name')
        patient_category = request.POST.get('Patient_category')
        floor_name = request.POST.get('floor_name')
        conditions = "Show_only_records"
        if doctor_name:
            records1 = AdmissionInfos.objects.exclude(status="discharged").filter(admission_datetime__range=[start_date, end_date],primary_doctor = doctor_name)
            patient_name = []
            age = []
            gender = []
            if records1:
                for data in records1:
                    pat_rec = PatientsRegistrationsAllInOne.objects.filter(uhid=data.uhid).last()
                    patient_name.append(f'{pat_rec.first_name} {pat_rec.middle_name} {pat_rec.last_name}')
                    age.append(pat_rec.age)
                    gender.append(pat_rec.gender)
            records = zip(records1,patient_name,age,gender)    
            context = {
                    'doctorr': doctorr, 'department': department,
                    'patient_categorys': patient_categorys,
                    'records': records,
                }
            return render(request, 'Reports/patient_admission.html', context)      

        elif start_date and end_date:
            records1 = AdmissionInfos.objects.exclude(status="discharged").filter(admission_datetime__range=[start_date, end_date])
            patient_name = []
            age = []
            gender = []
            if records1:
                for data in records1:
                    pat_rec = PatientsRegistrationsAllInOne.objects.filter(uhid=data.uhid).last()
                    patient_name.append(f'{pat_rec.first_name} {pat_rec.middle_name} {pat_rec.last_name}')
                    age.append(pat_rec.age)
                    gender.append(pat_rec.gender)
            records = zip(records1,patient_name,age,gender)
            context = {
                    'doctorr': doctorr, 'department': department,
                    'patient_categorys': patient_categorys,
                    'records': records,
                }
            return render(request, 'Reports/patient_admission.html', context)

        elif department_name:
            records1 = AdmissionInfos.objects.exclude(status="discharged").filter(admission_datetime__range=[start_date, end_date],department = department_name )
            patient_name = []
            age = []
            gender = []
            if records1:
                for data in records1:
                    pat_rec = PatientsRegistrationsAllInOne.objects.filter(uhid=data.uhid).last()
                    patient_name.append(f'{pat_rec.first_name} {pat_rec.middle_name} {pat_rec.last_name}')
                    age.append(pat_rec.age)
                    gender.append(pat_rec.gender)
            records = zip(records1,patient_name,age,gender)
            context = {
                    'doctorr': doctorr, 'department': department,
                    'patient_categorys': patient_categorys,
                    'records': records,
                }
            return render(request, 'Reports/patient_admission.html', context)
            

        elif patient_category:           
            records1 = AdmissionInfos.objects.exclude(status="discharged").filter(admission_datetime__range=[start_date, end_date],req_ward_cate = patient_category )
            patient_name = []
            age = []
            gender = []
            if records1:
                for data in records1:
                    pat_rec = PatientsRegistrationsAllInOne.objects.filter(uhid=data.uhid).last()
                    patient_name.append(f'{pat_rec.first_name} {pat_rec.middle_name} {pat_rec.last_name}')
                    age.append(pat_rec.age)
                    gender.append(pat_rec.gender)
            records = zip(records1,patient_name,age,gender)
            context = {
                    'doctorr': doctorr, 'department': department,
                    'patient_categorys': patient_categorys,
                    'records': records,
                }
            return render(request, 'Reports/patient_admission.html', context)

    context = {
        'doctorr': doctorr,'patient_categorys':patient_categorys,
        'department': department,"conditions":conditions
    }
    return render(request, 'Reports/patient_admission.html', context)



@login_required(login_url='/user_login')
def Bed_Transfer_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        records = Bed_Transfer.objects.filter(transfer_datatime__range=[start_date, end_date])
        return render(request, 'Reports/bed_transfer_report.html', {'records': records})
    return render(request, 'Reports/bed_transfer_report.html')



@login_required(login_url='/user_login')
def bed_occupancy_report(request):
    patient_categorys = AdmissionWardType.objects.all()
    ward_name_list = [data.ward_type for data in patient_categorys]
    ward_name = request.POST.get('Patient_category')
    if request.method == 'POST':
        if ward_name == "all":
            all_records = "all_records"
            patient_categorys = AdmissionWardType.objects.all()
            ward_name_list = [data.ward_type for data in patient_categorys]
            total_no_beds = BedMasterMain.objects.all()
            records = [data.bed_no for data in total_no_beds]
            rest = [*set(records)]
            Total = len(records)
            wards_name = []
            total_beds = []
            occupaid = []
            for data in ward_name_list:
                wards_name.append(data)
                beds = BedMasterMain.objects.filter(ward_type=data)
                all_beds = [data.bed_no for data in beds]
                count = len(all_beds)
                total_beds.append(count)
                aa = AdmissionWardType.objects.get(ward_type=data)
                ID = aa.id
                occupaid_bed = AdmissionInfos.objects.filter(req_ward_type=ID,status="admitted")
                occupaid_beds = [data.bed_no for data in occupaid_bed]
                length = len(occupaid_beds)
                occupaid.append(length)
            free_beds = []
            for total_bed, occcupaid_bed in zip(total_beds, occupaid):
                free_bed = total_bed - occcupaid_bed
                free_beds.append(free_bed)
            all_record = zip(wards_name, total_beds, occupaid, free_beds)
            context = {
                'patient_categorys': patient_categorys, 'ward_name': ward_name, 'all_records': all_records,
                'all_record': all_record
            }
            return render(request, 'Reports/bed_occupancy_report.html', context)
        else:
            # how many beds there in one ward
            separate = "separate ward"
            total_no_beds = BedMasterMain.objects.filter(ward_type=ward_name)
            records = [data.bed_no for data in total_no_beds]
            rest = [*set(records)]
            Total = len(rest)
            # find value of wardname
            ward_master = AdmissionWardType.objects.filter(ward_type=ward_name)
            ward = [data.id for data in ward_master]
            # find occupaid beds
            occupaid = AdmissionInfos.objects.filter(req_ward_type__in=ward)
            occupaid_beds = [data.bed_no for data in occupaid]
            res = [*set(occupaid_beds)]
            occupaid_len = len(res)
            free_beds = Total - occupaid_len
            context = {
                'patient_categorys': patient_categorys, 'ward_name': ward_name, 'Total': Total, "occupaid_len": occupaid_len,
                'free_beds': free_beds, 'separate': separate
            }
            return render(request, 'Reports/bed_occupancy_report.html', context)
    context = {
        'ward_name_list': ward_name_list, 'ward_name': ward_name,'patient_categorys':patient_categorys
    }
    return render(request, 'Reports/bed_occupancy_report.html', context)

@login_required(login_url='/user_login')
def detail_bed_occupany_report(request):
    admission = AdmissionInfos.objects.all()
    ad = [data.uhid for data in admission]
    bedtrans = Bed_Transfer.objects.all()
    bt = [data.uhid for data in bedtrans]
    if len(ad) == 0:
        No_records = "No_records"
        context = {
            'No_records': No_records
        }
        return render(request, 'Reports/detail_bed_occupancy_report.html', context)
    else:
        other = "other"
        for data in ad:
            if data in bt:
                uhid = []
                datelist = []
                bedlist = []
                wardtypelist = []
                Patient_name = []
                genderlist = []
                wardcatelist = []
                admissions_id = []
                bedtrans1 = Bed_Transfer.objects.filter(uhid=data)
                for data in bedtrans1:
                    date = data.transfer_datatime
                    bedno = data.to_bed_no
                    wardtype = data.to_ward_type
                    UHID = data.uhid
                    admission = PatientsRegistrationsAllInOne.objects.get(uhid=UHID)
                    first_name = admission.first_name
                    mid_name = admission.middle_name
                    last_name = admission.last_name
                    patient_name = (f'{first_name} {mid_name} {last_name}')
                    gender = admission.gender
                    admissioninfo = AdmissionInfos.objects.filter(uhid=UHID).last()
                    ward_cate = admissioninfo.req_ward_cate
                    admission_id = admissioninfo.admission_ID
                datelist.append(date)
                bedlist.append(bedno)
                wardtypelist.append(wardtype)
                uhid.append(UHID)
                Patient_name.append(patient_name)
                genderlist.append(gender)
                wardcatelist.append(ward_cate)
                admissions_id.append(admission_id)

            elif data not in bt:
                uhid = []
                datelist = []
                bedlist = []
                wardtypelist = []
                Patient_name = []
                genderlist = []
                wardcatelist = []
                admissions_id = []
                admn = AdmissionInfos.objects.filter(uhid=data).last()
                ad_uhid = data
                uhid.append(ad_uhid)
                admission_id = admn.admission_ID
                admissions_id.append(admission_id)
                ad_date = admn.admission_datetime
                datelist.append(ad_date)
                ad_bedno = admn.bed_no
                bedlist.append(ad_bedno)
                ad_ward_type = admn.req_ward_type
                wardtypelist.append(ad_ward_type)
                ad_ward_cate = admn.req_ward_cate
                wardcatelist.append(ad_ward_cate)
                patient_registrations = PatientsRegistrationsAllInOne.objects.get(uhid=data)
                ad_first_name = patient_registrations.first_name
                ad_mid_name = patient_registrations.middle_name
                ad_last_name = patient_registrations.last_name
                patient_name = (f'{ad_first_name} {ad_mid_name} {ad_last_name}')
                Patient_name.append(patient_name)
                ad_gender = patient_registrations.gender
                genderlist.append(ad_gender)

        all_records = zip(uhid, admissions_id, Patient_name, genderlist, bedlist, wardtypelist, wardcatelist, datelist)
        context = {
            'all_records': all_records, "other": other
        }

    return render(request, 'Reports/detail_bed_occupancy_report.html', context)

@login_required(login_url='/user_login')
def bed_view(request):
    ward_type_records = AdmissionWardType.objects.all()
    ward_cat_records = AdmissionWardCate.objects.all()
    ward_name = request.POST.get('ward_name')
    ward_cat = request.POST.get('ward_cat')
    bed = ''
    bed_number = ''
    if ward_name != 'all':
        bed_number = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat)
        if bed_number:
            bed = 'bed'
    occ_bed = BedMasterMain.objects.filter(ward_type=ward_name, ward_category=ward_cat, status='occupied')
    bed_id = [data.id for data in occ_bed]
    bed_transfer_record = Bed_Transfer.objects.all()
    transfer_uhid = [data.uhid for data in bed_transfer_record]
    admission_records = AdmissionInfos.objects.all()
    admission_uhid = [data.uhid for data in admission_records]
    uhid_list = []
    for bed_no in bed_id:
        for uhid in admission_uhid:
            if uhid in transfer_uhid:
                bed_transfer_uhid = Bed_Transfer.objects.filter(uhid=uhid, to_bed_no=bed_no).last()
                if bed_transfer_uhid:
                    uhid_list.append(bed_transfer_uhid.uhid)
            else:
                ad_uhid = AdmissionInfos.objects.filter(uhid=uhid, bed_no=bed_no).last()
                if ad_uhid:
                    uhid_list.append(ad_uhid.uhid)

    paitent_name = PatientsRegistrationsAllInOne.objects.filter(uhid__in=uhid_list)

    loo = []
    for data1, data2 in zip(paitent_name, bed_id):
        a = BedMasterMain.objects.get(id=data2)
        age = PatientsRegistrationsAllInOne.objects.get(uhid=data1.uhid)
        
        loo.append([data1.first_name, data1.gender, a.bed_no, age.age])

    # all
    all_detils = ''
    if ward_name == 'all':
        all_detils = BedMasterMain.objects.all()

        type_cat = []
        bed_nos = []
        ward_type_names = [data.ward_type for data in ward_type_records]
        ward_cat_names = [data.category_name for data in ward_cat_records]
        for type in ward_type_names:
            for cat in ward_cat_names:
                record = BedMasterMain.objects.filter(ward_type=type, ward_category=cat)
                if record:
                    type_cat.append([type, cat])
                    bed_nos.append([record])
        all_detils = zip(type_cat, bed_nos)

    context = {
        'ward_type': ward_type_records, 'ward_cat': ward_cat_records, 'bed_number': bed_number, 'bed': bed,
        'all_detils': all_detils,
        'loo': loo
    }
    return render(request, 'Reports/bed_view.html', context)

import calendar
from datetime import datetime



#==================== For invoice and Dialysis ===========================

@login_required(login_url='/user_login')
def nursing_notes(request):
    view=Nursing_Notes.objects.all()
    if request.method == 'POST':
        uhid='000001'
        p_name=request.POST.get('p_name')
        p_age=request.POST.get('p_age')
        p_gender=request.POST.get('p_gender')
        p_diagnosis=request.POST.get('p_diagnosis')
        p_hosp_no=request.POST.get('p_hosp_no')
        p_chemotherapy=request.POST.get('p_chemotherapy')
        p_date=request.POST.getlist('p_date')
        p_notes=request.POST.getlist('p_notes')
        pa_name_sign=request.POST.getlist('pa_name_sign')
        dat1 = ' '.join(p_date).split()
        for dat in range(len(dat1)):
            dat_p_date=p_date[dat]
            dat_p_notese=p_notes[dat]
            dat_pa_name_sign=pa_name_sign[dat]
            data=Nursing_Notes_sub(
                uhid=uhid,
                date_time=dat_p_date,
                nursing_notes=dat_p_notese,
                name_sign=dat_pa_name_sign,
            )
            data.save()
        data1=Nursing_Notes(
            uhid=uhid,
            patient_name=p_name,
            age=p_age,
            gender=p_gender,
            diagnosis=p_diagnosis,
            hosp_no=p_hosp_no,
            chemotherapy_protocol=p_chemotherapy,
        )
        data1.save()
        HttpResponseRedirect('/nursing_notes')
    return render(request,'clinical/mantu/nursing_notes.html',{'view':view})

@login_required(login_url='/user_login')
def view_nursing_notes(request,pk):
    view=Nursing_Notes.objects.get(id=pk)
    uhid=view.uhid
    view_sub=Nursing_Notes_sub.objects.filter(uhid=uhid)
    context={
        'view':view,'view_sub':view_sub,
    }
    return render(request,'clinical/mantu/view_nursing_notes.html',context)

@login_required(login_url='/user_login')
def pre_dialysis_details(request,pk):
    access = CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'post_dialysis' in access.user_profile.screen_access:
        # try:
            uhid_visit_ud=pk.split('-')
            uhid=uhid_visit_ud[0]
            visit_id=uhid_visit_ud[1]
            equipment_master = PreEquipPreparationMaster.objects.all()
            accet=Access_site.objects.all()
            anticoagulation=Anticoagulation.objects.all()
            asset=Asset_type.objects.all()
            bruit= Bruit_thrill.objects.all()
            closing=Closing_Attendent.objects.all()
            completion_sataus=Completion_Status_Master.objects.all()
            cannulation_nurses = CannulationNurse.objects.all()
            dalysis=Dialysate_Type.objects.all()
            dialyzer=Dialyzer.objects.all()
            heparin=Heparin_Type.objects.all()
            machine=Machine_name.objects.all()
            needle=Needle_type.objects.all()
            primary=Primary_dialysis_theropist.objects.all()
            rating=Rating.objects.all()
            secondery=Secondry_dialysis_theropist.objects.all()
            shift=Shift.objects.all()
            status=Status.objects.all()
            completion=Completion_Status_Master.objects.all()
            doctor_list=DoctorTable.objects.all()
            records=PatientsRegistrationsAllInOne.objects.filter(uhid=uhid).last()
            pre_dialysis=Permanent_Access.objects.filter(uhid=uhid).last()
            uhid_pat=records.uhid
            pat_fname=records.first_name
            pat_mname=records.middle_name
            pat_lname=records.last_name
            pat_age=records.age
            pat_sex=records.gender
            pat_con_no=records.mobile_number
            pat_name=''
            if pat_mname==None:
                pat_name = pat_fname + ' ' + pat_lname
            else:
                pat_name=pat_fname+' '+pat_mname+' '+pat_lname
            request.session['pat_uhid']=uhid_pat
            request.session['pat_visit']=visit_id
            request.session['pat_name']=pat_name
            request.session['pat_age']=pat_age
            request.session['pat_con_no']=pat_con_no
            request.session['pat_sex']=pat_sex
            # records_pre=Pre_Dialysis_Details.objects.filter(uhid=uhid,visit_id=visit_id)
            main_form=request.POST.get('main_form')
            pre_equip=request.POST.get('sub_form')
            assessment=request.POST.get('assessment')
            # display_data=PreEquipPreparationPreDialysis.objects.all().last()#filter(uhid=uhid,visit_id=visit_id)
            # pre_form2=PreEquipPreparationPreDialysisForm(request.POST,display_data)
            assessment_records = PreDialysisAssessment.objects.filter(uhid=uhid,visit_id=visit_id).last()
            if assessment_records  != None:
                assess_form = PreDialysisAssessmentForm(instance=assessment_records)
                if assessment == 'ASSESSMENT':
                    if request.method == 'POST':
                        assess_form = PreDialysisAssessmentForm(request.POST, instance=assessment_records)
                        if assess_form.is_valid():
                            assess_form.save()
                            return HttpResponseRedirect(f'/pre_dialysis_details/{pk}')
            elif assessment_records == None:
                assess_form = PreDialysisAssessmentForm(initial={'uhid': uhid, 'visit_id': visit_id})
                if assessment == 'ASSESSMENT':
                    print('asswwwwwww')
                    if request.method == 'POST':
                        assess_form = PreDialysisAssessmentForm(request.POST)
                        if assess_form.is_valid():
                            assess_form.save()
                            return HttpResponseRedirect(f'/pre_dialysis_details/{pk}')
                        else:
                            print(assess_form.errors)
                            print(uhid)
                            print(visit_id)
            pre_records=PreEquipPreparationPreDialysis.objects.filter(uhid=uhid, visit_id=visit_id).last()
            if pre_records != None:
                pre_form=PreEquipPreparationPreDialysisForm(instance=pre_records)
                if pre_equip == 'SUB_FORM':
                    if request.method == 'POST':
                        pre_form = PreEquipPreparationPreDialysisForm(request.POST)
                        if pre_form.is_valid():
                            pre_form.save()
                            return HttpResponseRedirect(f'/pre_dialysis_details/{pk}')
               
            elif pre_records == None:
                pre_form=PreEquipPreparationPreDialysisForm(initial={'uhid': uhid, 'visit_id': visit_id})
                if pre_equip == 'SUB_FORM':
                    if request.method == 'POST':
                        pre_form = PreEquipPreparationPreDialysisForm(request.POST)
                        if pre_form.is_valid():
                            pre_form.save()
                            return HttpResponseRedirect(f'/pre_dialysis_details/{pk}')
            if main_form == 'MAIN_FORM':
                # if request.method=="POST":
                Uhid=request.POST.get('uhid')
                # ==== For Session Details =====================
                status=request.POST.get('status')
                pre_equip_preparation=request.POST.get('pre_equip_preparation')
                physian=request.POST.get('physian')
                primary_dialysis_theraphy=request.POST.get('primary_dialysis_theraphy')
                secondry_dialysis_theraphy=request.POST.get('secondry_dialysis_theraphy')
                password=request.POST.get('password')
                cannulation_nurse=request.POST.get('cannulation_nurse')
                location=request.POST.get('location')
                machine_name=request.POST.get('machine_name')
                asset_type=request.POST.get('asset_type')
                bruit_thrill=request.POST.get('bruit_thrill')
                access_site=request.POST.get('access_site')
                access_site_infection=request.POST.get('access_site_infection')
                iso_uf=request.POST.get('iso_uf')
                any_remark=request.POST.get('any_remark')
                dialysis_type=request.POST.get('dialysis_type')
                other_staff=request.POST.get('other_staff')
                needle_type=request.POST.get('needle_type')
                #======== for Dialyzer Reuse =========================
                dialyser=request.POST.get('dialyser')
                bundle_volume=request.POST.get('bundle_volume')
                reprocess_number=request.POST.get('reprocess_number')
                reprocessed_date=request.POST.get('reprocessed_date')
                rating=request.POST.get('rating')
                single_used_dialyzer=request.POST.get('single_used_dialyzer')
                # ===== for Patient Condition ====================
                bp_sitting_max=request.POST.get('bp_sitting_max')
                bp_sitting_min=request.POST.get('bp_sitting_min')
                bp_standing_max=request.POST.get('bp_standing_max')
                bp_standing_min=request.POST.get('bp_standing_min')
                respiration=request.POST.get('respiration')
                pulse_sitting=request.POST.get('pulse_sitting')
                pulse_standing=request.POST.get('pulse_standing')
                tempreture=request.POST.get('tempreture')
                measured_wt=request.POST.get('measured_wt')
                wheelchair_wt=request.POST.get('wheelchair_wt')
                prosthetic_wt=request.POST.get('prosthetic_wt')
                condition_assessment=request.POST.get('condition_assessment')
                assessment=request.POST.get('assessment')
                current_wt=request.POST.get('current_wt')
                previous_wt=request.POST.get('previous_wt')
                weight_change=request.POST.get('weight_change')
                # ========= for Dialysis Details ===================
                dry_wt_date=request.POST.get('dry_wt_date')
                target_wt=request.POST.get('target_wt')
                excess=request.POST.get('excess')
                duration=request.POST.get('duration')
                target_UF_Vol_kg=request.POST.get('target_UF_Vol_kg')
                target_UFR_vol_kg_hr=request.POST.get('target_UFR_vol_kg_hr')
                anticoagulation=request.POST.get('anticoagulation')
                heparin_type=request.POST.get('heparin_type')
                initial_dose=request.POST.get('initial_dose')
                interim_Dose=request.POST.get('interim_Dose')
                total_heparin_bolus=request.POST.get('total_heparin_bolus')
                hourly=request.POST.get('hourly')
                unit_in_syringe=request.POST.get('unit_in_syringe')
                dialysis_odometer_str_reading=request.POST.get('dialysis_odometer_str_reading')
                pre_dialysis_assessment=request.POST.get('pre_dialysis_assessment')
                notes_pre_dialysis_session=request.POST.get('notes_pre_dialysis_session')
                fluids_volume_ml=request.POST.get('fluids_volume_ml')
                data=Pre_Dialysis_Details(
                    uhid=uhid,
                    visit_id=visit_id,
                    # ==== For Session Details =====================
                    status=status,
                    # pre_equip_preparation=pre_equip_preparation,
                    physian=physian,
                    primary_dialysis_theraphy=primary_dialysis_theraphy,
                    secondry_dialysis_theraphy=secondry_dialysis_theraphy,
                    password=password,
                    cannulation_nurse=cannulation_nurse,
                    location=location,
                    machine_name=machine_name,
                    asset_type=asset_type,
                    bruit_thrill=bruit_thrill,
                    access_site=access_site,
                    access_site_infection=access_site_infection,
                    iso_uf=iso_uf,
                    any_remark=any_remark,
                    dialysis_type=dialysis_type,
                    other_staff=other_staff,
                    needle_type=needle_type,
                    #======== for Dialyzer Reuse =========================
                    dialyser=dialyser,
                    bundle_volume=bundle_volume,
                    reprocess_number=reprocess_number,
                    reprocessed_date=reprocessed_date,
                    rating=rating,
                    single_used_dialyzer=single_used_dialyzer,
                    # ===== for Patient Condition ====================
                    bp_sitting_max=bp_sitting_max,
                    bp_sitting_min=bp_sitting_min,
                    bp_standing_max=bp_standing_max,
                    bp_standing_min=bp_standing_min,
                    respiration=respiration,
                    pulse_sitting=pulse_sitting,
                    pulse_standing=pulse_standing,
                    tempreture=tempreture,
                    measured_wt=measured_wt,
                    wheelchair_wt=wheelchair_wt,
                    prosthetic_wt=prosthetic_wt,
                    condition_assessment=condition_assessment,
                    assessment='assessment',
                    current_wt=current_wt,
                    previous_wt=previous_wt,
                    weight_change=weight_change,
                    # ========= for Dialysis Details ===================
                    dry_wt_date=dry_wt_date,
                    target_wt=target_wt,
                    excess=excess,
                    duration=duration,
                    target_UF_Vol_kg=target_UF_Vol_kg,
                    target_UFR_vol_kg_hr=target_UFR_vol_kg_hr,
                    anticoagulation=anticoagulation,
                    heparin_type=heparin_type,
                    initial_dose=initial_dose,
                    interim_Dose=interim_Dose,
                    total_heparin_bolus=total_heparin_bolus,
                    hourly=hourly,
                    unit_in_syringe=unit_in_syringe,
                    dialysis_odometer_str_reading=dialysis_odometer_str_reading,
                    pre_dialysis_assessment=pre_dialysis_assessment,
                    notes_pre_dialysis_session=notes_pre_dialysis_session,
                    fluids_volume_ml=fluids_volume_ml,
                    created_by_id=request.user.id,
                    location_id_id=request.location,
                )
                data.save()
                visit_status=PatientVisitMains.objects.filter(uhid=uhid,visit_id=visit_id).last()
                if visit_status:
                    visit_status.claim_no=status
                    visit_status.save()
                else:
                    dialysis_admission=AdmissionStatus.objects.filter(uhid=uhid,admission_ID=visit_id).last()
                    dialysis_admission.status=status
                    dialysis_admission.save()
                HttpResponseRedirect('/pre_dialysis_details')
            context={
                'records':records,
                'accet':accet,'anticoagulation':anticoagulation,'asset':asset,'bruit':bruit,'closing':closing,
                'completion_sataus':completion_sataus,'dalysis':dalysis,'dialyzer':dialyzer,"heparin":heparin,
                'machine':machine,'needle':needle,'primary':primary,'rating':rating,'secondery':secondery,'shift':shift,
                'status':status,'completion':completion,'uhid':uhid,'visit_id':visit_id,'doctor_list':doctor_list,'pre_dialysis':pre_dialysis,
                'uhid_pat': uhid_pat, 'pat_name': pat_name, 'pat_age': pat_age, 'pat_con_no': pat_con_no,'assess_form':assess_form,
                'pat_sex': pat_sex,'equipment_master':equipment_master,'pre_form':pre_form,'cannulation_nurses':cannulation_nurses,
            }
            return render(request,'dialysis/pre_dialysis_details.html',context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
@login_required(login_url='/user_login')
def view_pre_dialysis_details(request,pk):
    uh_visit_id = pk.split('-')
    uhid_p = uh_visit_id[0]
    visit_id = uh_visit_id[1]
    view=Pre_Dialysis_Details.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
    records=PatientsRegistrationsAllInOne.objects.get(uhid=uhid_p)
    context={
        'view':view,'records':records,
    }
    return render(request,'dialysis/view_pre_dialysis_details.html',context)

@login_required(login_url='/user_login')
def post_dialysis_details(request,pk):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'post_dialysis' in access.user_profile.screen_access:
        try:
            uh_visit_id = pk.split('-')
            uhid_p = uh_visit_id[0]
            visit_id = uh_visit_id[1]
            records = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid_p).last()
            uhid_pat = records.uhid
            pat_fname = records.first_name
            pat_mname = records.middle_name
            pat_lname = records.last_name
            pat_age = records.age
            pat_sex = records.gender
            pat_con_no = records.mobile_number
            pat_name = ''
            if pat_mname == None:
                pat_name = pat_fname + ' ' + pat_lname
            else:
                pat_name = pat_fname + ' ' + pat_mname + ' ' + pat_lname
            accet = Access_site.objects.all()
            anticoagulation = Anticoagulation.objects.all()
            medical_list = Inventory_ItemMaster.objects.filter(assets='0').order_by('item_name')
            asset = Asset_type.objects.all()
            bruit = Bruit_thrill.objects.all()
            closing = Closing_Attendent.objects.all()
            completion_sataus = Completion_Status_Master.objects.all()
            dalysis = Dialysate_Type.objects.all()
            dialyzer = Dialyzer.objects.all()
            heparin = Heparin_Type.objects.all()
            machine = Machine_name.objects.all()
            needle = Needle_type.objects.all()
            primary = Primary_dialysis_theropist.objects.all()
            rating = Rating.objects.all()
            secondery = Secondry_dialysis_theropist.objects.all()
            shift = Shift.objects.all()
            status = Status.objects.all()
            completion = Completion_Status_Master.objects.all()
            drugs_table = AddDrugs_Dialysis.objects.filter(uhid=uhid_p,visit_id=visit_id)
            records=PatientsRegistrationsAllInOne.objects.all().last()
            post_dialysis=Post_Dialysis_Details.objects.all()
            doctor_list=DoctorTable.objects.all()
            add_medicine = request.POST.get('add_medicines')
            if add_medicine == 'ADD_DRUGS':
                medical_list = request.POST.get('medical_list')
                rout = request.POST.get('rout')
                dosage_pr_adm = request.POST.get('dosage_pr_adm')
                batch_no = request.POST.get('batch_no')
                exp_date = request.POST.get('exp_date')
                quantity = request.POST.get('quantity')
                administered_by = request.POST.get('administered_by')
                doctor = request.POST.get('doctor')
                remark = request.POST.get('remark')
                add_drug=AddDrugs_Dialysis(
                    uhid=uhid_p,
                    visit_id=visit_id,
                    medicine_name=medical_list,
                    rout=rout,
                    dosage_pr_adm=dosage_pr_adm,
                    batch_no=batch_no,
                    expiry_date=exp_date,
                    quantity=quantity,
                    remark=remark,
                    doctor=doctor,
                    administered_by=administered_by,
                )
                add_drug.save()
                HttpResponseRedirect('/post_dialysis_details')
            if request.POST.get('main_form'):
                Uhid=request.POST.get('uhid')
                # ==== For Session Details =====================
                status=request.POST.get('status')
                closing_attendent=request.POST.get('closing_attendent')
                completion_status=request.POST.get('completion_status')
                end_time=request.POST.get('end_time')
                duration=request.POST.get('duration')
                next_day_dialysis=request.POST.get('next_day_dialysis')
                shift=request.POST.get('shift')
                # ===== for Patient Condition ====================
                bp_sitting_max=request.POST.get('bp_sitting_max')
                bp_sitting_min=request.POST.get('bp_sitting_min')
                bp_standing_max=request.POST.get('bp_standing_max')
                bp_standing_min=request.POST.get('bp_standing_min')
                respiration=request.POST.get('respiration')
                pulse_sitting=request.POST.get('pulse_sitting')
                pulse_standing=request.POST.get('pulse_standing')
                tempreture=request.POST.get('tempreture')
                measured_wt=request.POST.get('measured_wt')
                wheelchair_wt=request.POST.get('wheelchair_wt')
                prosthetic_wt=request.POST.get('prosthetic_wt')
                condition_assessment=request.POST.get('condition_assessment')
                prolonged_bleeding_at_punctured_sites=request.POST.get('prolonged_bleeding_at_punctured_sites')
                # ========= for Dialysis Details ===================
                weight_lost=request.POST.get('weight_lost')
                fluid_removed=request.POST.get('fluid_removed')
                heparin_Left=request.POST.get('heparin_Left')
                total_heparin_infused=request.POST.get('total_heparin_infused')
                dialyzer_rating=request.POST.get('dialyzer_rating')
                bruit_thrill=request.POST.get('bruit_thrill')
                minimum_BP_max=request.POST.get('minimum_BP_max')
                minimum_BP_min=request.POST.get('minimum_BP_min')
                minimum_BP_time=request.POST.get('minimum_BP_time')
                dialysis_odometer_end_eading=request.POST.get('dialysis_odometer_end_eading')
                next_pre_dialysis_notes=request.POST.get('next_pre_dialysis_notes')
                data=Post_Dialysis_Details(
                    uhid=uhid_p,
                    visit_id=visit_id,
                    # ==== For Session Details =====================
                    status = status,
                    closing_attendent = closing_attendent,
                    completion_status = completion_status,
                    end_time = end_time,
                    duration = duration,
                    next_day_dialysis =next_day_dialysis,
                    shift = shift,
                    # ===== for Patient Condition ====================
                    bp_sitting_max = bp_sitting_max,
                    bp_sitting_min =bp_sitting_min,
                    bp_standing_max = bp_standing_max,
                    bp_standing_min = bp_standing_min,
                     respiration = respiration,
                    pulse_sitting = pulse_sitting,
                    pulse_standing = pulse_standing,
                    tempreture = tempreture,
                    measured_wt = measured_wt,
                    wheelchair_wt = wheelchair_wt,
                    prosthetic_wt = prosthetic_wt,
                    condition_assessment = condition_assessment,
                    prolonged_bleeding_at_punctured_sites = prolonged_bleeding_at_punctured_sites,
                    # ========= for Dialysis Details ===================
                    weight_lost = weight_lost,
                    fluid_removed = fluid_removed,
                    heparin_Left = heparin_Left,
                    total_heparin_infused = total_heparin_infused,
                    dialyzer_rating = dialyzer_rating,
                    bruit_thrill = bruit_thrill,
                    minimum_BP_max = minimum_BP_max,
                    minimum_BP_min = minimum_BP_min,
                    minimum_BP_time =minimum_BP_time,
                    dialysis_odometer_end_eading = dialysis_odometer_end_eading,
                    next_pre_dialysis_notes = next_pre_dialysis_notes,
                    created_by_id=request.user.id, location_id=request.location,
                )
                data.save()
                visit_status=PatientVisitMains.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
                if visit_status:
                    visit_status.claim_no=status
                    visit_status.save()
                else:
                    dialysis_admission=AdmissionStatus.objects.filter(uhid=uhid_p,admission_ID=visit_id).last()
                    dialysis_admission.status=status
                    dialysis_admission.save()
                HttpResponseRedirect('/post_dialysis_details')

            # print('all_data',Uhid,status,bp_sitting_max,weight_lost)
            context={
                'records':records,'post_dialysis':post_dialysis,
                'accet': accet, 'anticoagulation': anticoagulation, 'asset': asset, 'bruit': bruit, 'closing': closing,
                'completion_sataus': completion_sataus, 'dalysis': dalysis, 'dialyzer': dialyzer, "heparin": heparin,
                'machine': machine, 'needle': needle, 'primary': primary, 'rating': rating, 'secondery': secondery,
                'shift': shift,'uhid_pat': uhid_pat, 'pat_name': pat_name, 'pat_age': pat_age, 'pat_con_no': pat_con_no,
                'pat_sex': pat_sex,'doctor_list':doctor_list,'medical_list':medical_list,'drugs_table':drugs_table,
                'status': status, 'completion': completion,'access':access,'pk':pk
            }
            return render(request,'dialysis/post_dialysis_details.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
def delete_add_drugs(request):
    records = AddDrugs_Dialysis.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse(data='Data Deleted Successfully',safe=False)

@login_required(login_url='/user_login')
def view_post_dialysis(request,pk):
    uhid_visit_ud = pk.split('-')
    uhidd = uhid_visit_ud[0]
    visit_idd = uhid_visit_ud[1]
    drugs_table = AddDrugs_Dialysis.objects.filter(uhid=uhidd, visit_id=visit_idd)
    post_dialysis=Post_Dialysis_Details.objects.filter(uhid=uhidd,visit_id=visit_idd).last()
    records=PatientsRegistrationsAllInOne.objects.get(uhid=uhidd)
    context={
        'post_dialysis':post_dialysis,'records':records,'drugs_table':drugs_table,
    }
    return render(request,'dialysis/view_post_dialysis.html',context)

@login_required(login_url='/user_login')
def dialysis_details(request,pk):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'dialysis_details' in access.user_profile.screen_access:
        form=''
        form_post=''
        session_form=''
        # try:
        uh_visit_id=pk.split('-')
        uhid_p=uh_visit_id[0]
        visit_id=uh_visit_id[1]
        records = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid_p).last()
        uhid_pat = records.uhid
        pat_fname = records.first_name
        pat_mname = records.middle_name
        pat_lname = records.last_name
        pat_age = records.age
        pat_sex = records.gender
        pat_con_no = records.mobile_number
        pat_name = ''
        if pat_mname == None:
            pat_name = pat_fname + ' ' + pat_lname
        else:
            pat_name = pat_fname + ' ' + pat_mname + ' ' + pat_lname
        completion_sataus = Completion_Status_Master.objects.all()
        status = Status.objects.all()
        intra_records_per_hour = IntraDialysisPerHourInput.objects.filter(uhid=uhid_pat,visit_id=visit_id)
        # pre_dialysis_details=Pre_Dialysis_Details.objects.filter(uhid=uhid_pat,visit_id=visit_id).last()
        intra_dialysis=request.POST.get('intra_dialysis')
        main_form_intra=request.POST.get('main_form_intra')
        post_equipment=request.POST.get('post_equipment')
        note_session=request.POST.get('note_session')
        now =datetime.now().time()
        pre_dialysis_records=Pre_Dialysis_Details.objects.filter(uhid=uhid_pat,visit_id=visit_id).last()
        intra_dialysis_records=IntraDialysis.objects.filter(uhid=uhid_pat,visit_id=visit_id).last()
        post_equip=PostEquip_preparation.objects.filter(uhid=uhid_pat,visit_id=visit_id).last()
        session_form = SessionNoteForm(initial={'uhid': uhid_pat, 'visit_id': visit_id,'time':now})
        if note_session == 'INTRA_DIALYSIS_SESSION_NOTES':
            if request.method == "POST":
                session_form = SessionNoteForm(request.POST,)
                if session_form.is_valid():
                    session_form.save()
                    print('session_form saved---',session_form)
                    # return HttpResponseRedirect(f'/dialysis_details,{pk}')
        if post_equip != None:
            form_post = PostEquip_preparationForm(instance=post_equip)
            if post_equipment == "POST_EQUIPMENT_PRAPARATION":
                if request.method == "POST":
                    form_post = PostEquip_preparationForm(request.POST,instance=post_equip)
                    if form_post.is_valid():
                        form_post.save()
                        # return HttpResponseRedirect(f'/dialysis_details,{pk}')
        elif post_equip == None :
            form_post = PostEquip_preparationForm(initial={'uhid': uhid_pat, 'visit_id': visit_id})
            if post_equipment == "POST_EQUIPMENT_PRAPARATION":
                if request.method == 'POST':
                    form_post = PostEquip_preparationForm(request.POST)
                    if form_post.is_valid():
                        form_post.save()
                        print('form_post',form_post)
                        # return HttpResponseRedirect(f'/dialysis_details,{pk}')
        if intra_dialysis == 'INTRA_DIALYSIS':
            if request.method=='POST':
                time=request.POST.get('time')
                bp_mmhg1=request.POST.get('bp_mmhg1')
                bp_mmhg2=request.POST.get('bp_mmhg2')
                bp_time=request.POST.get('bp_time')
                pulse=request.POST.get('pulse')
                total_uf_removal=request.POST.get('total_uf_removal')
                uf_rate=request.POST.get('uf_rate')
                blood_pump_flow_rate=request.POST.get('blood_pump_flow_rate')
                heparine_pump_infusion_rate=request.POST.get('heparine_pump_infusion_rate')
                dialysate_temp=request.POST.get('dialysate_temp')
                conductivity=request.POST.get('conductivity')
                venus_pressure=request.POST.get('venus_pressure')
                dialysate_pressure=request.POST.get('dialysate_pressure')
                tmp=request.POST.get('tmp')
                dialysis_time=request.POST.get('conductivity')
                dialysis_flow_rate=request.POST.get('conductivity')
                datas=IntraDialysisPerHourInput(
                    uhid=uhid_pat,
                    visit_id =visit_id,
                    time=time,
                    bp_mmhg1 = bp_mmhg1,
                    bp_mmhg2 = bp_mmhg2,
                    bp_time = bp_time,
                    pulse = pulse,
                    total_uf_removal = total_uf_removal,
                    uf_rate = uf_rate,
                    blood_pump_flow_rate =blood_pump_flow_rate,
                    heparine_pump_infusion_rate =heparine_pump_infusion_rate,
                    dialysate_temp = dialysate_temp,
                    conductivity = conductivity,
                    venus_pressure = venus_pressure,
                    dialysate_pressure = dialysate_pressure,
                    tmp = tmp,
                    dialysis_time = dialysis_time,
                    dialysis_flow_rate = dialysis_flow_rate,
                )
                datas.save()
        elif main_form_intra == 'MAIN_FORM_INTRA_DIA':
            if request.method=='POST':
                status=request.POST.get('status')
                completion_status=request.POST.get('completion_sataus')
                intra_data=IntraDialysis(
                    uhid=uhid_pat,
                    visit_id=visit_id,
                    status=status,
                    completion_status=completion_status
                )
                intra_data.save()
            # records=PatientsRegistrationsAllInOne.objects.all().last()
            visit_status = PatientVisitMains.objects.filter(uhid=uhid_pat, visit_id=visit_id).last()
            if visit_status:
                visit_status.claim_no = status
                visit_status.save()
            else:
                dialysis_admission = AdmissionStatus.objects.filter(uhid=uhid_pat, admission_ID=visit_id).last()
                dialysis_admission.status = status
                dialysis_admission.save()
        context={
           'access':access,'form':form,'intra_records_per_hour':intra_records_per_hour,'session_form':session_form,
            'uhid_pat': uhid_pat, 'pat_name': pat_name, 'pat_age': pat_age, 'pat_con_no': pat_con_no,'form_post':form_post,
            'pat_sex': pat_sex,'pre_dialysis_details':pre_dialysis_details,'completion_sataus':completion_sataus,
            'status':status,'pre_dialysis_records':pre_dialysis_records,'pk':pk,'intra_dialysis_records':intra_dialysis_records,

        }
        return render(request,'dialysis/dialysis_details.html',context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def chemotherapy_treatment_sheet(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'chemotherapy_treatment' in access.user_profile.screen_access:
        try:
            records=PatientsRegistrationsAllInOne.objects.all().last()
            records1=Chemotherapy_treatment_sheet.objects.all()
            if request.method=="POST":
                patient_name = request.POST.get('patient_name')
                gender = request.POST.get('gender')
                age = request.POST.get('age')
                stage = request.POST.get('stage')
                weight = request.POST.get('weight')
                height = request.POST.get('height')
                BSA = request.POST.get('BSA')
                histology = request.POST.get('histology')
                drugs = request.POST.get('drugs')
                dose_m2 = request.POST.get('dose_m2')
                notes = request.POST.get('notes')
                date = request.POST.getlist('date')
                bp = request.POST.getlist('bp')
                p_temp = request.POST.getlist('p_temp')
                wht = request.POST.getlist('wht')
                wbc = request.POST.getlist('wbc')
                hb = request.POST.getlist('hb')
                plt = request.POST.getlist('plt')
                uec = request.POST.getlist('uec')
                remark1 = request.POST.getlist('remark1')
                remark2 = request.POST.getlist('remark2')
                remark3 = request.POST.getlist('remark3')
                remark4 = request.POST.getlist('remark4')
                UHID='00001'
                dat1=' '.join(date).split()
                print('=======',dat1)
                for chemo in range(len(dat1)):
                    chemo_date=date[chemo]
                    chemo_bp=bp[chemo]
                    chemo_p_temp=p_temp[chemo]
                    chemo_wht=wht[chemo]
                    chemo_wbc=wbc[chemo]
                    chemo_hb=hb[chemo]
                    chemo_plt=plt[chemo]
                    chemo_uec=uec[chemo]
                    chemo_remark1=remark1[chemo]
                    chemo_remark2=remark2[chemo]
                    chemo_remark3=remark3[chemo]
                    chemo_remark4=remark4[chemo]
                    data=Chemotherapy_treatment_sheet_sub(
                        uhid=UHID,
                        date = chemo_date,
                        bp = chemo_bp,
                        p_temp =chemo_p_temp,
                        wht =chemo_wht,
                        wbc =chemo_wbc,
                        hb =chemo_hb,
                        plt =chemo_plt,
                        uec =chemo_uec,
                        remark1 =chemo_remark1,
                        remark2 =chemo_remark2,
                        remark3 =chemo_remark3,
                        remark4 =chemo_remark4,
                    )
                    data.save()
                data2=Chemotherapy_treatment_sheet(
                    uhid=UHID,
                    patient_name=patient_name,
                    gender=gender,
                    age=age,
                    stage=stage,
                    weight=weight,
                    height=height,
                    BSA=BSA,
                    histology=histology,
                    drugs=drugs,
                    dose_m2=dose_m2,
                    notes=notes,
                )
                data2.save()
                HttpResponseRedirect('/chemotherapy_treatment_sheet')
            context={
                'records':records,'records1':records1,'access':access
            }
            return render(request,'dialysis/chemotherapy_treatment_sheet.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')
def view_chemotherapy(request,pk):
    view=Chemotherapy_treatment_sheet.objects.get(id=pk)
    uhid=view.uhid
    sub_table=Chemotherapy_treatment_sheet_sub.objects.filter(uhid=uhid)
    context={
        'view':view,'sub_table':sub_table,
    }
    return render(request,'dialysis/chemotherapy_view.html',context)
# def search_uhid(request):
#     service_name=request.GET.get('service_name')
#     payload=[]
#     if service_name and len(service_name)>1:
#         fake_address_objs=ServiceMaster.objects.filter(service_name__icontains=service_name)
#         for fake_address_obj in fake_address_objs:
#             payload.append(str(fake_address_obj.service_name+'~'+str(fake_address_obj.id)))
#     return JsonResponse({'status':200,'data':payload})

@login_required(login_url='/user_login')
def estimate(request):
    records=''
    records_sub=''
    patient_details=PatientsRegistrationsAllInOne.objects.all()
    service = ServiceMaster.objects.all()
    bil_group = BillingGroup.objects.all()
    uhid = request.POST.get('uhid')
    if request.method=="POST":
        uhids=request.POST.get('uhid')
        name=request.POST.get('name')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        contact_no=request.POST.get('contact_no')
        billing_group=request.POST.get('billing_group')
        if name:
            data=Estimate_bill_sub(
                uhid=uhids,
                name=name,
                age=age,
                sex=gender,
                billing_group_id=billing_group,
                contact_no=contact_no,
            )
            data.save()
            print('data---======',data)
            # return HttpResponseRedirect('/estimate')
        records1=PatientsRegistrationsAllInOne.objects.filter(uhid=uhid)
        if records1.exists():
            records= PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
            first_name=records.first_name
            m_name=records.middle_name
            l_name=records.last_name
            name=first_name+' '+m_name+' '+l_name
            id=records.uhid
            age=records.age
            gender=records.gender
            mobile_number=records.mobile_number
            billing_groups=records.billing_group
            print('billing_groups----',billing_groups)
            request.session['id']=id
            request.session['name']=name
            request.session['age'] = age
            request.session['sex'] = gender
            request.session['contact_no'] = mobile_number
            request.session['billing_group'] = str(billing_groups)
        else:
            messages.success(request,'This UHID not Registered')
        if uhid == None:
            records_sub = Estimate_bill_sub.objects.all().last()
            id_tem=records_sub.id
            name_temp=records_sub.name
            age_temp=records_sub.age
            gender_temp=records_sub.sex
            contact_no_temp=records_sub.contact_no
            billing_groups_temp=records_sub.billing_group.id
            print('billing_groups_temp------>,,',billing_groups_temp)
            request.session['id']=id_tem
            request.session['name']=name_temp
            request.session['age']=age_temp
            request.session['sex']=gender_temp
            request.session['contact_no']=contact_no_temp
            request.session['billing_group'] = str(billing_groups_temp)


            # print("====name,id",id,name)
    context={
        'patient_details':patient_details,'records':records,'service':service,'records_sub':records_sub,'bil_group':bil_group,
    }
    return render(request,'clinical/mantu/estimate1.html',context)

@login_required(login_url='/user_login')
def estimate_temp(request):
    service_master=''
    b_group=request.session['billing_group']
    print('b_group-------->,',b_group)
    bil_group_tariff = BillingGroupTariffLink.objects.filter(Billing_Group_Name=b_group).last()
    tariff_name=bil_group_tariff.Tariff_id
    print('tariff_name====,',tariff_name)
    request.session['tariff_name']=str(tariff_name)
    service_master1=ServiceMaster.objects.all()
    service_charge = ServiceChargeMaster.objects.filter(tariff_id=tariff_name)
    package_charge= PackageChargeMaster.objects.filter(tariff_id=tariff_name)
    profile_charge = ProfileChargeMaster.objects.filter(tariff_id=tariff_name)
    item = [data.service_name for data in service_master1]
    item1 = [data.service_id for data in service_charge]
    item2= [data.package_id for data in package_charge]
    item3 = [data.profile_id for data in profile_charge]
    # service_master2=zip(item,item1,item2,item3)
    service_master2=item1+item2+item3
    id=request.session['id']
    name=request.session['name']
    age=request.session['age']
    gender=request.session['sex']
    contact_no=request.session['contact_no']
    print("name,id", id, name)
    if request.method=="POST":
        service_name=request.POST.getlist('services')
        service_rate=request.POST.getlist('services_rate')
        print('-----',service_name,service_rate)
        for dat in range(len(service_name)):
            print('--len',range(len(service_name)))
            dat_id=id
            dat_name=name
            dat_age=age
            dat_gender=gender
            dat_contact_no=contact_no
            dat_service_name=service_name[dat]
            dat_services_rate=service_rate[dat]
            data = Estimate_bill_mains(
                uhid=dat_id,
                name=dat_name,
                age=dat_age,
                sex=dat_gender,
                contact_no=dat_contact_no,
                services=dat_service_name,
                services_rate=dat_services_rate,
            )
            data.save()
            Estimate_bill_temp.objects.filter(uhid=id, name=name).delete()
        return HttpResponseRedirect('/estimate_pdf')
        print('all==',service_rate,service_name)
    records=Estimate_bill_temp.objects.filter(uhid=id,name=name)
    total=Estimate_bill_temp.objects.filter(uhid=id,name=name).aggregate(Sum('services_rate'))
    total = total['services_rate__sum']
    context={
        'service_master':service_master,'item':item,'name':name,'age':age,'gender':gender,'contact_no':contact_no,
        'records':records,"total":total,'service_master2':service_master2,'service_charge':service_charge,
    }
    return render(request,'clinical/mantu/estimate_temp.html',context)

@login_required(login_url='/user_login')
def estimate_sub_temp(request,serv):
    id=request.session['id']
    name=request.session['name']
    age=request.session['age']
    gender=request.session['sex']
    contact_no=request.session['contact_no']
    tariff_id=request.session['tariff_name']
    service_master=''
    service1=ServiceChargeMaster.objects.filter(service_id=serv,tariff_id=tariff_id)
    service2 = PackageChargeMaster.objects.filter(package_id__package_name__icontains=serv,tariff_id=tariff_id)
    service3 = ProfileChargeMaster.objects.filter(profile_id=serv,tariff_id=tariff_id)
    if service1.exists():
    #     service_master=ServiceMaster.objects.get(service_name=serv)
    # elif service2.exists():
        service_master = ServiceChargeMaster.objects.get(service_id=serv,tariff_id=tariff_id)
    elif service2.exists():
        service_master=PackageChargeMaster.objects.get(package_id__package_name__icontains=serv,tariff_id=tariff_id)
    elif service3.exists():
        service_master = ProfileChargeMaster.objects.get(profile_id=serv,tariff_id=tariff_id)
    service_master_all = ServiceMaster.objects.all()
    item = [data.service_name for data in service_master_all]
    if request.method=="POST":
        services=request.POST.get('service_name')
        services_rate=request.POST.get('rate')
        data=Estimate_bill_temp(
            uhid =id,
            name = name,
            age = age,
            sex = gender,
            contact_no = contact_no,
            services = services,
            services_rate =services_rate,
        )
        data.save()
        return HttpResponseRedirect('/estimate_temp')
    records=Estimate_bill_temp.objects.filter(uhid=id,name=name)
    total=Estimate_bill_temp.objects.filter(uhid=id,name=name).aggregate(Sum('services_rate'))
    total = total['services_rate__sum']
    context={
        'service_master':service_master,'item':item,'service_master_all':service_master_all,
        'name':name,'age':age,'gender':gender,'contact_no':contact_no,'records':records,"total":total,
        'service1':service1,'service2':service2,'service3':service3,
    }
    return render(request,'clinical/mantu/estimate_temp.html',context)


# @login_required(login_url='/user_login')
# def estimate_pdf(request):
#     package_records=''
#     id=request.session['id']
#     name=request.session['name']
#     age=request.session['age']
#     gender=request.session['sex']
#     contact_no=request.session['contact_no']
#     datas=Estimate_bill_mains.objects.filter(uhid=id,name=name)
#     for dt in datas:
#         d=dt.services
#         package_records=OpdPackageService.objects.filter(package_name=d)
#         profile_records=ProfileService.objects.filter(profile_name=d)
#         print('package===package_records',package_records)
#     total=Estimate_bill_mains.objects.filter(uhid=id,name=name).aggregate(Sum('services_rate'))
#     total = total['services_rate__sum']
#     context={
#         'datas':datas,'name':name,'age':age,'gender':gender,'contact_no':contact_no,'id':id,
#         'total':total,'package_records':package_records,'profile_records':profile_records,
#     }
#     return render(request,'clinical/mantu/estimate_pdf.html',context)

@login_required(login_url='/user_login')
def dashboard_report(request):
    return render(request,'Reports/dashboard_report.html')


@login_required(login_url='/user_login')
def estimate_pdf(request):
    package_records=''
    id=request.session['id']
    name=request.session['name']
    age=request.session['age']
    gender=request.session['sex']
    contact_no=request.session['contact_no']
    datas=Estimate_bill_mains.objects.filter(uhid=id,name=name)
    for dt in datas:
        d=dt.services
        print('d------->,',d)
        package_records=OpdPackageService.objects.filter(package_name__package_name__icontains=d)
        profile_records=ProfileService.objects.filter(profile_name=d)
        print('package===package_records',package_records)
    total=Estimate_bill_mains.objects.filter(uhid=id,name=name).aggregate(Sum('services_rate'))
    total = total['services_rate__sum']
    context={
        'datas':datas,'name':name,'age':age,'gender':gender,'contact_no':contact_no,'id':id,
        'total':total,'package_records':package_records,'profile_records':profile_records,
    }
    return render(request,'clinical/mantu/estimate_pdf.html',context)


#==== for dialysis master 01/02/2023 ===============================

@login_required(login_url='/user_login')
def status_dialysis(request):
    records = Status.objects.all()
    form = StatusForm()
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/status_dialysis')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/status.html', context)

@login_required(login_url='/user_login')
def status_dialysis_view(request):
    records = Status.objects.all()
    form = StatusForm()
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/status_dialysis')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/status_view.html', context)



@login_required(login_url='/user_login')
def status_dialysis_edit(request, pk):
    # name = request.session['Name']
    status_master = Status.objects.get(id=pk)
    form = StatusForm(instance=status_master)
    editing = 'editing'
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/status_dialysis_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/status_dialysis_edit.html', context)


@login_required(login_url='/user_login')
def primary_dialysis_theropist(request):
    records = Primary_dialysis_theropist.objects.all()
    form = Primary_dialysis_theropistForm()
    if request.method == "POST":
        form = Primary_dialysis_theropistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/primary_dialysis_theropist')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/primary_dialysis_theropist.html', context)


@login_required(login_url='/user_login')
def primary_dialysis_theropist_view(request):
    records = Primary_dialysis_theropist.objects.all()
    form = Primary_dialysis_theropistForm()
    if request.method == "POST":
        form = Primary_dialysis_theropistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/primary_dialysis_theropist')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/primary_dialysis_theropist_view.html', context)



@login_required(login_url='/user_login')
def primary_dialysis_theropist_edit(request, pk):
    # name = request.session['Name']
    status_master = Primary_dialysis_theropist.objects.get(id=pk)
    form = Primary_dialysis_theropistForm(instance=status_master)
    editing = 'editing'
    if request.method == 'POST':
        form = Primary_dialysis_theropistForm(request.POST, instance=status_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/primary_dialysis_theropist_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/primary_dialysis_theropist_edit.html', context)


@login_required(login_url='/user_login')
def secondry_dialysis_theropist(request):
    records = Secondry_dialysis_theropist.objects.all()
    form = Secondry_dialysis_theropistForm()
    if request.method == "POST":
        form = Secondry_dialysis_theropistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/secondry_dialysis_theropist')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/secondry_dialysis_theropist.html', context)


@login_required(login_url='/user_login')
def secondry_dialysis_theropist_view(request):
    records = Secondry_dialysis_theropist.objects.all()
    form = Secondry_dialysis_theropistForm()
    if request.method == "POST":
        form = Secondry_dialysis_theropistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/secondry_dialysis_theropist')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/secondry_dialysis_theropist_view.html', context)



@login_required(login_url='/user_login')
def secondry_dialysis_theropist_edit(request, pk):
    # name = request.session['Name']
    status_master = Secondry_dialysis_theropist.objects.get(id=pk)
    form = Secondry_dialysis_theropistForm(instance=status_master)
    editing = 'editing'
    if request.method == 'POST':
        form = Secondry_dialysis_theropistForm(request.POST, instance=status_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/secondry_dialysis_theropist_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/secondry_dialysis_theropist_edit.html', context)


@login_required(login_url='/user_login')
def machine_name(request):
    records = Machine_name.objects.all()
    form = Machine_nameForm()
    if request.method == "POST":
        form = Machine_nameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/machine_name')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/machine_name.html', context)


@login_required(login_url='/user_login')
def machine_name_view(request):
    records = Machine_name.objects.all()
    form = Machine_nameForm()
    if request.method == "POST":
        form = Machine_nameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/machine_name')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/machine_name_view.html', context)



@login_required(login_url='/user_login')
def machine_name_edit(request, pk):
    # name = request.session['Name']
    machine_name = Machine_name.objects.get(id=pk)
    form = Machine_nameForm(instance=machine_name)
    editing = 'editing'
    if request.method == 'POST':
        form = Machine_nameForm(request.POST, instance=machine_name)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/machine_name_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/machine_name_edit.html', context)


@login_required(login_url='/user_login')
def asset_type(request):
    records = Asset_type.objects.all()
    form =Asset_typeForm()
    if request.method == "POST":
        form = Asset_typeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/asset_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/asset_type.html', context)


@login_required(login_url='/user_login')
def asset_type_view(request):
    records = Asset_type.objects.all()
    form = Asset_typeForm()
    if request.method == "POST":
        form = Asset_typeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/asset_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/asset_type_view.html', context)



@login_required(login_url='/user_login')
def asset_type_edit(request, pk):
    # name = request.session['Name']
    asset_type = Asset_type.objects.get(id=pk)
    form = Asset_typeForm(instance=asset_type)
    editing = 'editing'
    if request.method == 'POST':
        form = Asset_typeForm(request.POST, instance=asset_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/asset_type_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/asset_type_edit.html', context)


@login_required(login_url='/user_login')
def bruit_thrill(request):
    records = Bruit_thrill.objects.all()
    form =Bruit_thrillForm()
    if request.method == "POST":
        form = Bruit_thrillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bruit_thrill')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/bruit_thrill.html', context)


@login_required(login_url='/user_login')
def bruit_thrill_view(request):
    records = Bruit_thrill.objects.all()
    form = Bruit_thrillForm()
    if request.method == "POST":
        form = Bruit_thrillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bruit_thrill')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/bruit_thrill_view.html', context)



@login_required(login_url='/user_login')
def bruit_thrill_edit(request, pk):
    # name = request.session['Name']
    bruit_thrill = Bruit_thrill.objects.get(id=pk)
    form = Bruit_thrillForm(instance=bruit_thrill)
    editing = 'editing'
    if request.method == 'POST':
        form = Bruit_thrillForm(request.POST, instance=bruit_thrill)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bruit_thrill_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/bruit_thrill_edit.html', context)


@login_required(login_url='/user_login')
def access_site(request):
    records = Access_site.objects.all()
    form =Access_siteForm()
    if request.method == "POST":
        form = Access_siteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/access_site')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/access_site.html', context)


@login_required(login_url='/user_login')
def access_site_view(request):
    records = Access_site.objects.all()
    form = Access_siteForm()
    if request.method == "POST":
        form = Access_siteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/access_site')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/access_site_view.html', context)



@login_required(login_url='/user_login')
def access_site_edit(request, pk):
    # name = request.session['Name']
    access_site = Access_site.objects.get(id=pk)
    form = Access_siteForm(instance=access_site)
    editing = 'editing'
    if request.method == 'POST':
        form = Access_siteForm(request.POST, instance=access_site)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/access_site_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/access_site_edit.html', context)


@login_required(login_url='/user_login')
def dialysis_type(request):
    records = Dialysate_Type.objects.all()
    form =Dialysate_TypeForm()
    if request.method == "POST":
        form = Dialysate_TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dialysis_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/dialysis_type.html', context)


@login_required(login_url='/user_login')
def dialysis_type_view(request):
    records = Dialysate_Type.objects.all()
    form = Dialysate_TypeForm()
    if request.method == "POST":
        form = Dialysate_TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dialysis_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/dialysis_type_view.html', context)



@login_required(login_url='/user_login')
def dialysis_type_edit(request, pk):
    # name = request.session['Name']
    dialysis_type = Dialysate_Type.objects.get(id=pk)
    form = Dialysate_TypeForm(instance=dialysis_type)
    editing = 'editing'
    if request.method == 'POST':
        form = Dialysate_TypeForm(request.POST, instance=dialysis_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dialysis_type_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/dialysis_type_edit.html', context)
#================ completion_Status ======


@login_required(login_url='/user_login')
def completion_Status(request):
    records = Completion_Status_Master.objects.all()
    form =Completion_Status_MasterForm()
    if request.method == "POST":
        form = Completion_Status_MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/completion_Status')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/completion_Status.html', context)


@login_required(login_url='/user_login')
def completion_Status_view(request):
    records = Completion_Status_Master.objects.all()
    form = Completion_Status_MasterForm()
    if request.method == "POST":
        form = Completion_Status_MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/completion_Status')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/completion_Status_view.html', context)



@login_required(login_url='/user_login')
def completion_Status_edit(request, pk):
    # name = request.session['Name']
    completion_Status = Completion_Status_Master.objects.get(id=pk)
    form = Completion_Status_MasterForm(instance=completion_Status)
    editing = 'editing'
    if request.method == 'POST':
        form = Completion_Status_MasterForm(request.POST, instance=completion_Status)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/completion_Status_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/completion_Status_edit.html', context)

#================


@login_required(login_url='/user_login')
def needle_type(request):
    records = Needle_type.objects.all()
    form =Needle_typeForm()
    if request.method == "POST":
        form = Needle_typeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/needle_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/Needle_type.html', context)


@login_required(login_url='/user_login')
def needle_type_view(request):
    records = Needle_type.objects.all()
    form = Needle_typeForm()
    if request.method == "POST":
        form = Needle_typeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/needle_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/needle_type_view.html', context)



@login_required(login_url='/user_login')
def needle_type_edit(request, pk):
    # name = request.session['Name']
    needle_type = Needle_type.objects.get(id=pk)
    form = Needle_typeForm(instance=needle_type)
    editing = 'editing'
    if request.method == 'POST':
        form = Needle_typeForm(request.POST, instance=needle_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/needle_type_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/needle_type_edit.html', context)

#================

@login_required(login_url='/user_login')
def dialyzer(request):
    records = Dialyzer.objects.all()
    form =DialyzerForm()
    if request.method == "POST":
        form = DialyzerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dialyzer')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/dialyzer.html', context)


@login_required(login_url='/user_login')
def dialyzer_view(request):
    records = Dialyzer.objects.all()
    form = DialyzerForm()
    if request.method == "POST":
        form = DialyzerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dialyzer')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/dialyzer_view.html', context)


@login_required(login_url='/user_login')
def dialyzer_edit(request, pk):
    # name = request.session['Name']
    dialyzer = Dialyzer.objects.get(id=pk)
    form = DialyzerForm(instance=dialyzer)
    editing = 'editing'
    if request.method == 'POST':
        form = DialyzerForm(request.POST, instance=dialyzer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dialyzer_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/dialyzer_edit.html', context)


@login_required(login_url='/user_login')
#================
def rating(request):
    records = Rating.objects.all()
    form =RatingForm()
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rating')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/rating.html', context)


@login_required(login_url='/user_login')
def rating_view(request):
    records = Rating.objects.all()
    form = RatingForm()
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rating')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/rating_view.html', context)


@login_required(login_url='/user_login')
def rating_edit(request, pk):
    # name = request.session['Name']
    rating = Rating.objects.get(id=pk)
    form = RatingForm(instance=rating)
    editing = 'editing'
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rating_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/rating_edit.html', context)

#================

@login_required(login_url='/user_login')
def anticoagulation(request):
    records = Anticoagulation.objects.all()
    form =AnticoagulationForm()
    if request.method == "POST":
        form = AnticoagulationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/anticoagulation')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/anticoagulation.html', context)


@login_required(login_url='/user_login')
def anticoagulation_view(request):
    records = Anticoagulation.objects.all()
    form = AnticoagulationForm()
    if request.method == "POST":
        form = AnticoagulationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/anticoagulation')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/anticoagulation_view.html', context)


@login_required(login_url='/user_login')
def anticoagulation_edit(request, pk):
    # name = request.session['Name']
    anticoagulation = Anticoagulation.objects.get(id=pk)
    form = AnticoagulationForm(instance=anticoagulation)
    editing = 'editing'
    if request.method == 'POST':
        form = AnticoagulationForm(request.POST, instance=anticoagulation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/anticoagulation_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/anticoagulation_edit.html', context)

#================

@login_required(login_url='/user_login')
def heparin_type(request):
    records = Heparin_Type.objects.all()
    form =Heparin_TypeForm()
    if request.method == "POST":
        form = Heparin_TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/heparin_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/heparin_type.html', context)


@login_required(login_url='/user_login')
def heparin_type_view(request):
    records = Heparin_Type.objects.all()
    form =Heparin_TypeForm()
    if request.method == "POST":
        form = Heparin_TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/heparin_type')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/heparin_type_view.html', context)


@login_required(login_url='/user_login')
def heparin_type_edit(request, pk):
    # name = request.session['Name']
    heparin_type = Heparin_Type.objects.get(id=pk)
    form = Heparin_TypeForm(instance=heparin_type)
    editing = 'editing'
    if request.method == 'POST':
        form = Heparin_TypeForm(request.POST, instance=heparin_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/heparin_type_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/heparin_type_edit.html', context)

#================

@login_required(login_url='/user_login')
def closing_attendent(request):
    records = Closing_Attendent.objects.all()
    form =Closing_AttendentForm()
    if request.method == "POST":
        form = Closing_AttendentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/closing_attendent')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/closing_attendent.html', context)


@login_required(login_url='/user_login')
def closing_attendent_view(request):
    records = Closing_Attendent.objects.all()
    form =Closing_AttendentForm()
    if request.method == "POST":
        form = Closing_AttendentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/closing_attendent')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/closing_attendent_view.html', context)


@login_required(login_url='/user_login')
def closing_attendent_edit(request, pk):
    # name = request.session['Name']
    closing_attendent = Closing_Attendent.objects.get(id=pk)
    form = Closing_AttendentForm(instance=closing_attendent)
    editing = 'editing'
    if request.method == 'POST':
        form = Closing_AttendentForm(request.POST, instance=closing_attendent)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/closing_attendent_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/closing_attendent_edit.html', context)

#================

@login_required(login_url='/user_login')
def shift(request):
    records = Shift.objects.all()
    form =ShiftForm()
    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shift')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/shift.html', context)


@login_required(login_url='/user_login')
def shift_view(request):
    records = Shift.objects.all()
    form =ShiftForm()
    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shift')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/dialysis_master/shift_view.html', context)


@login_required(login_url='/user_login')
def shift_edit(request, pk):
    # name = request.session['Name']
    shift = Shift.objects.get(id=pk)
    form = ShiftForm(instance=shift)
    editing = 'editing'
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shift_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/dialysis_master/shift_edit.html', context)
 #===========Schedule Master =======================
# ================

@login_required(login_url='/user_login')
def schedule_master(request):
    records = Schedule_Master.objects.all()
    form = Schedule_MasterForm()
    if request.method == "POST":
        form = Schedule_MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/schedule_master')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/medical_equipment/schedule_master.html', context)



@login_required(login_url='/user_login')
def schedule_master_view(request):
    records = Schedule_Master.objects.all()
    form = Schedule_MasterForm()
    if request.method == "POST":
        form = Schedule_MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/schedule_master')
    context = {
        'form': form, 'records': records
    }
    return render(request, 'general_master/medical_equipment/schedule_master_view.html', context)



@login_required(login_url='/user_login')
def schedule_master_edit(request, pk):
    # name = request.session['Name']
    schedule_master = Schedule_Master.objects.get(id=pk)
    form = Schedule_MasterForm(instance=schedule_master)
    editing = 'editing'
    if request.method == 'POST':
        form = Schedule_MasterForm(request.POST, instance=schedule_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/schedule_master_view')
    context = {
        'form': form, 'editing': editing,
    }
    return render(request, 'general_master/medical_equipment/schedule_master_edit.html', context)
#================== END DIALYSIS MASTERS =============================

#=================== START MEDICAL EQUIPMENT SYSTEM ======================

@login_required(login_url='/user_login')
def medical_equipment(request):
    records=Inventory_ItemMaster.objects.filter(assets='1')
    context={
        'records':records
    }
    return render(request,'general_master/medical_equipment/medical_equip.html',context)

@login_required(login_url='/user_login')
def medical_equipment_edit(request,pk):
    request.session['id']=pk
    records=Inventory_ItemMaster.objects.filter(assets='1')
    context={
        'records':records
    }
    return render(request,'general_master/medical_equipment/medical_equip.html',context)

@login_required(login_url='/user_login')
def search_data(request):
    service_name=request.GET.get('service_name')
    payload=[]
    if service_name and len(service_name)>1:
        fake_address_objs=ServiceChargeMaster.objects.all()
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.service_id))
            # payload.append(str(fake_address_obj.id))
    print('payload=111111111====================================',payload)
    return JsonResponse({'status':200,'data':payload})

from dateutil.relativedelta import relativedelta

@login_required(login_url='/user_login')
def maintanence_deatils(request):
    pk=request.session['id']
    due_date=''
    dates=date.today()
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_id=get_item_data.hsn_item_code
    get_item_all=Maintanence_Deatils.objects.filter(item_model_no=get_id)
    get_schedule_data=Schedule_Master.objects.all()
    if request.method=="POST":
        schedule_name=request.POST.get('schedule_name')
        item_sub_id=request.POST.get('item_sub_id')
        item_id=request.POST.get('item_id')
        item_model_no=request.POST.get('item_model_no')
        description=request.POST.get('description')
        # today =date.today()
        # month_count = 0
        # while month_count < 12:
        #     day = today - relativedelta(months=month_count)
        #     print('day============y',day)
        # month_count += 1
        if schedule_name=='Monthly':
            month=1
            due_date = date.today() + relativedelta(months=+1)
        elif schedule_name=='Quarterly':
            month=3
            due_date = date.today() + relativedelta(months=+3)
            print('=========',month,due_date)
        elif schedule_name=='Half Yearly':
            month=6
            due_date = date.today() + relativedelta(months=+6)
            print('=========',month,due_date)
        elif schedule_name=='Yearly':
            month=12
            due_date = date.today() + relativedelta(months=+12)
            print('=========',month,due_date)
        data=Maintanence_Deatils(
            schedule_name=schedule_name,
            item_sub_id=item_sub_id,
            item_id=item_id,
            item_model_no=item_model_no,
            created_at=dates,
            due_date=due_date,
            description=description,
        )
        data.save()
        return HttpResponseRedirect('/maintanence_deatils')
    context={
        'get_item_data':get_item_data,'get_schedule_data':get_schedule_data,'get_item_all':get_item_all,
    }
    return render(request,'general_master/medical_equipment/maintanence_deatils.html',context)

@login_required(login_url='/user_login')
def mainmaintenance_pdf(request):
    pk=request.session['id']
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_ids=get_item_data.hsn_item_code
    get_name=get_item_data.item_name
    data=Maintanence_Deatils.objects.filter(item_model_no=get_ids).last()
    context={
        'data':data,'get_name':get_name,
    }
    return render(request,'general_master/medical_equipment/maintanence_pdf.html',context)

@login_required(login_url='/user_login')
def unplanned_maintanence(request):
    pk=request.session['id']
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_name=get_item_data.item_name
    get_ids = get_item_data.hsn_item_code
    data=Unplanned_Maintanence.objects.filter(item_model_no=get_ids)
    sche=Maintanence_Deatils.objects.get(item_model_no=get_ids)

    if request.method=="POST":
        sub_id=request.POST.get('item_sub_id')
        item_id=request.POST.get('item_id')
        model_id=request.POST.get('item_model_no')
        done_by=request.POST.get('done_by')
        problem_date=request.POST.get('problem_date')
        problem_name=request.POST.get('problem_name')
        resolve_date=request.POST.get('resolve_date')
        remark=request.POST.get('remark')
        datas=Unplanned_Maintanence(
            item_sub_id=sub_id,
            item_id=item_id,
            item_model_no=model_id,
            done_by=done_by,
            problem_occure_date=problem_date,
            problem_name=problem_name,
            resolve_date=resolve_date,
            remark=remark,
        )
        datas.save()
    context={
        'sche':sche,'data':data,'get_name':get_name,
    }
    return render(request,'general_master/medical_equipment/unplanned_maintanence.html',context)

@login_required(login_url='/user_login')
def unplanned_maintanence_pdf(request):
    pk=request.session['id']
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_ids=get_item_data.hsn_item_code
    get_name=get_item_data.item_name
    datas=Maintanence_Deatils.objects.get(item_model_no=get_ids)
    schedule_name=datas.schedule_name
    print('schedule_name',schedule_name)
    data=Unplanned_Maintanence.objects.filter(item_model_no=get_ids).last()
    context={
        'data':data,'get_name':get_name,'schedule_name':schedule_name,
    }
    return render(request,'general_master/medical_equipment/unplanned_maintanence_pdf.html',context)

@login_required(login_url='/user_login')
def preventory_maintanence(request):
    pk=request.session['id']
    data=''
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_name=get_item_data.item_name
    get_ids=get_item_data.hsn_item_code

    records=Preventory_Maintanence.objects.filter(item_model_no=get_ids)
    sche=Maintanence_Deatils.objects.get(item_model_no=get_ids)
    if request.method=="POST":
        sub_id=request.POST.get('item_sub_id')
        item_id=request.POST.get('item_id')
        model_id=request.POST.get('item_model_no')
        done_by=request.POST.get('done_by')
        done_date=request.POST.get('done_date')
        due_date=request.POST.get('due_date')
        description=request.POST.get('description')
        remark=request.POST.get('remark')

        date_format ="%Y-%m-%d"
        a = datetime.strptime(str(due_date), date_format)
        b = datetime.strptime(str(done_date), date_format)
        delta = b - a
        due_days=delta.days
        print('due_dayss',due_days)
        datas=Preventory_Maintanence(
            item_sub_id=sub_id,
            item_id=item_id,
            item_model_no=model_id,
            done_by=done_by,
            done_date=done_date,
            due_date=due_date,
            description=description,
            remark=remark,
            delay_days=due_days,
        )
        datas.save()
        return HttpResponseRedirect('/preventory_maintanence')
    context={
        'sche':sche,'records':records,'get_name':get_name,
    }
    return render(request,'general_master/medical_equipment/preventory_maintanence.html',context)
def preventory_maintanence_pdf(request):
    pk=request.session['id']
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_ids=get_item_data.hsn_item_code
    get_name=get_item_data.item_name
    datas=Maintanence_Deatils.objects.get(item_model_no=get_ids)
    schedule_name=datas.schedule_name
    print('schedule_name',schedule_name)
    data=Preventory_Maintanence.objects.filter(item_model_no=get_ids).last()
    context={
        'data':data,'get_name':get_name,'schedule_name':schedule_name,
    }
    return render(request,'general_master/medical_equipment/preventory_maintanence_pdf.html',context)
def validation_calibration(request):
    pk=request.session['id']
    data=''
    print('pk========',pk)
    get_schedule_data=Schedule_Master.objects.all()
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_name=get_item_data.item_name
    get_ids=get_item_data.hsn_item_code
    data=Validation_Calibration.objects.filter(item_model_no=get_ids).last()

    # data=Preventory_Maintanence.objects.get(item_model_no=pk)
    sche=Inventory_ItemMaster.objects.get(id=pk)
    # data=Validation_Calibration.objects.get(item_model_no=pk)
    if request.method=="POST":
        sub_id=request.POST.get('item_sub_id')
        item_id=request.POST.get('item_id')
        model_id=request.POST.get('item_model_no')
        done_by=request.POST.get('done_by')
        schedule_name=request.POST.get('schedule_name')
        dispensive=request.POST.get('dispensive')
        date_time=request.POST.get('date_time')
        validation_date=request.POST.get('validation_date')
        remark=request.POST.get('remark')
        datas=Validation_Calibration(
            item_sub_id=sub_id,
            item_id=item_id,
            item_model_no=model_id,
            done_by=done_by,
            schedule_name=schedule_name,
            dispensive=dispensive,
            date_time=date_time,
            validation_date=validation_date,
            remark=remark,
        )
        datas.save()
        return HttpResponseRedirect('/validation_calibration')
    context={
        'sche':sche,'data':data,'get_name':get_name,'get_schedule_data':get_schedule_data,
    }
    return render(request,'general_master/medical_equipment/validation_calibration.html',context)
def validation_calibration_pdf(request):
    pk=request.session['id']
    get_item_data=Inventory_ItemMaster.objects.get(id=pk)
    get_ids=get_item_data.hsn_item_code
    get_name=get_item_data.item_name
    datas=Maintanence_Deatils.objects.get(item_model_no=get_ids)
    schedule_name=datas.schedule_name
    print('schedule_name',schedule_name)
    data=Validation_Calibration.objects.filter(item_model_no=get_ids).last()
    context={
        'data':data,'get_name':get_name,'schedule_name':schedule_name,
    }
    return render(request,'general_master/medical_equipment/validation_calibration_pdf.html',context)
def get_report(request):
    # data=Validation_Calibration.objects.filter(item_model_no=get_ids).last()
    return render(request,'general_master/medical_equipment/get_report.html')
def new_invoice(request):
    return render(request,'clinical/mantu/new_invoice.html')


@login_required(login_url='/user_login')
def ins_document(request):
    ins_records=Ins_Document.objects.all()
    form = Ins_DocumentForm()
    if request.method=="POST":
        form = Ins_DocumentForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/ins_document')
    context={
        'form':form,'ins_records':ins_records,
    }
    return render(request,'general_master/ins_document_type.html',context)

#=================== for Email Verification =======================


def email_sending(subject,message,mail):
    mail_from = 'mkr715official@gmail.com'
    email_to = mail
    send_mail(
        subject,
        message,
        mail_from,
        [email_to],
        fail_silently=False
    )
    return HttpResponse("Mail Send Successfully")

def send_email(request):
    if request.method=="POST":
        name=request.POST.get('user_name')
        subject=request.POST.get('subject')
        message=request.POST.get('msg')
        email_id=request.POST.get('email_id')
        file=request.FILES.get('files')
        print('file============',file)
        mail1 = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email_id])
        mail1.attach(file.name, file.read(), file.content_type)
        mail1.send()
        print('mail1----',mail1)
    return render(request,'clinical/opd_bill/send_email.html')


@login_required(login_url='/user_login')
def finalized_bill(request):
    rate_p=[]
    ins_p=[]
    ins_pla = ''
    rate_pla = ''
    # all_result=OpdBillingMain.objects.filter(claim_status='fully_paid',location=request.location).order_by('-id')
    data=''
    all_result1 = OpdBillingMain.objects.extra(select={
        'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
    }).filter(claim_status='fully_paid', location=request.location).order_by('-id')
    uhid_list = [data.uhid for data in all_result1]
    patient_data = PatientsRegistrationsAllInOne.objects.filter(uhid__in=uhid_list)
    for dat in patient_data:
        # print('dat_billing_group', dat.billing_group)
        print('nhif_ins_cor_name', dat.nhif_ins_cor_name)
        insurance_data = BillingGroup.objects.get(id=dat.billing_group)
        rate_plan = insurance_data.billing_group
        rate_p.append(rate_plan)
        if dat.nhif_ins_cor_name == 'Cash':
            ins_p.append('Cash')
        else:
            insurance_d = CorporateMaster.objects.get(id=dat.nhif_ins_cor_name)
            ins_pla = insurance_d.corporate_Name
            print('ins_pla------,', insurance_d.id)
            ins_p.append(ins_pla)
        print('ins_p====>,',ins_p)
    all_result = zip(all_result1, ins_p)
    # if request.method=='POST':
    bill_nos = request.POST.get('bill_nos')
    pat_namess = request.POST.get('name')
    if pat_namess:
        print('pat_namess---->,', pat_namess)
        pat_record = PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=pat_namess,
                                                                  location=request.location)
        list_uhidss = [data.uhid for data in pat_record]
        print('pat_record,', pat_record, list_uhidss)
        all_result1 = OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        }).filter(uhid__in=list_uhidss, claim_status='fully_paid')
        print('data----,', all_result1)
        uhid_list = [data.uhid for data in all_result1]
        insurance_data = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid_list)
        for dat in insurance_data:
            print('dat_billing_group',dat.billing_group)
            print('nhif_ins_cor_name',dat.nhif_ins_cor_name)
            insurance_data = BillingGroup.objects.get(id=dat.billing_group)
            rate_plan = insurance_data.billing_group
            rate_p.append(rate_plan)
            if dat.nhif_ins_cor_name == 'Cash':
                ins_p.append('Cash')
            else:
                insurance_d = CorporateMaster.objects.get(id=dat.nhif_ins_cor_name)
                ins_pla = insurance_d.corporate_Name
                ins_p.append(ins_pla)
        all_result = zip(all_result1, ins_p)
        # data=OpdBillingMain.objects.extra(select={
        #         'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         }).get(bill_no=bill_nos)
        # print('data==========>>>>>>',data.uhid)
    if bill_nos:
        data = OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        }).get(bill_no__exact=bill_nos, claim_status='fully_paid', location=request.location)
        insurance_data = PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
        billing_group = insurance_data.billing_group
        ins_name = insurance_data.nhif_ins_cor_name
        print('nhif_ins_cor_name------,', ins_name)
        insurance_data1 = BillingGroup.objects.get(id=billing_group)
        rate_pla = insurance_data1.billing_group
        if ins_name == 'Cash':
            ins_p.append('Cash')
        else:
            insurance_d = CorporateMaster.objects.get(id=ins_name)
            ins_pla = insurance_d.corporate_Name
            ins_p.append(ins_pla)
            print('ins_pla,ins_pla',ins_pla)
    else:
        pass
    context={
        'all_result':all_result,'data':data,'ins_pla':ins_pla,'rate_pla':rate_pla,
    }
    return render(request,'clinical/opd_bill/finalized_bill.html',context)



@login_required(login_url='/user_login')
def closed_bill(request):
    rate_p=[]
    ins_p=[]
    ins_pla = ''
    rate_pla = ''
    all_result2 = ''
    all_result1=OpdBillingMain.objects.extra(select={
                'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                }).filter(claim_status='pending',location=request.location).exclude(status='cancel').order_by('-id')
    for data in all_result1:
        patient_data=PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
        insurance_data=BillingGroup.objects.get(id=patient_data.billing_group)
        rate_plan=insurance_data.billing_group
        rate_p.append(rate_plan)
        if patient_data.nhif_ins_cor_name == 'Cash':
            ins_p.append('Cash')
        else:
            insurance_d=CorporateMaster.objects.get(id=patient_data.nhif_ins_cor_name)
            ins_pla=insurance_d.corporate_Name
            ins_p.append(ins_pla)
    all_result=zip(all_result1,ins_p)
    data=''
    # if request.method=='POST':
    bill_nos=request.POST.get('bill_nos')
    pat_namess=request.POST.get('name')
    if pat_namess:
        print('pat_namess---->,',pat_namess)
        pat_record = PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=pat_namess,location=request.location)
        list_uhidss = [data.uhid for data in pat_record]
        print('pat_record,',pat_record,list_uhidss)
        all_result1 = OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        }).filter(uhid__in=list_uhidss,claim_status='pending')
        for data in all_result1:
            patient_data=PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
            insurance_data=BillingGroup.objects.get(id=patient_data.billing_group)
            rate_plan=insurance_data.billing_group
            rate_p.append(rate_plan)
            if patient_data.nhif_ins_cor_name == 'Cash':
                ins_p.append('Cash')
            else:
                insurance_d=CorporateMaster.objects.get(id=patient_data.nhif_ins_cor_name)
                ins_pla=insurance_d.corporate_Name
                ins_p.append(ins_pla)
        all_result = zip(all_result1, ins_p)
        # data=OpdBillingMain.objects.extra(select={
        #         'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        #         }).get(bill_no=bill_nos)
        # print('data==========>>>>>>',data.uhid)
    if bill_nos :
        data = OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        }).get(bill_no__exact=bill_nos,claim_status='pending',location=request.location)
        insurance_data = PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
        billing_group =insurance_data.billing_group
        ins_name = insurance_data.nhif_ins_cor_name
        print('nhif_ins_cor_name------,', ins_name)
        insurance_data1 = BillingGroup.objects.get(id=billing_group)
        rate_pla = insurance_data1.billing_group
        if ins_name == 'Cash':
            ins_p.append('Cash')
        else:
            insurance_d = CorporateMaster.objects.get(id=ins_name)
            ins_pla = insurance_d.corporate_Name
            ins_p.append(ins_pla)
    else:
        pass
    context={
        'all_result':all_result,'data':data,'ins_pla':ins_pla,'rate_pla':rate_pla,'all_result2':all_result2,
    }
    return render(request,'clinical/opd_bill/closed_bill.html',context)


@login_required(login_url='/user_login')
def cancel_bill(request):
    get_submit=request.POST.get('get_submit')
    cancel_bill=CancelBillRemarkForm()
    if get_submit == 'Cance_Form':
        if request.method=="POST":
            bill_no = request.POST.get('bill_nod')
            cancel_bill = CancelBillRemarkForm(request.POST)
            if cancel_bill.is_valid():
                bill=cancel_bill.save(commit=False)
                bill.bill_no_id=bill_no
                bill.created_by_id = request.user.id
                bill.location_id = request.location
                #=========================== For Update in main table ===============
                record = OpdBillingMain.objects.get(id=bill_no)
                bill_num = record.bill_no
                pending = PendingInvestigation_main.objects.filter(bill_no=bill_num).last()
                if pending:
                    pending.delete(print('successfull deletet'))
                bill_num = record.bill_no
                record.status = 'cancel'
                record.save()
                print('record saved to main bill ,', record)
                # ===================== For Update Cancel Bill in OPDPAYMENT and OPDBillingSub Table =================
                cash_data = OpdPayment.objects.filter(bill_id=bill_num).last()
                insurance_data = Credit.objects.filter(bill_no=bill_num).last()
                if insurance_data:
                    insurance_data.department = 'cancel'
                    insurance_data.save()
                    print('insurance_data saved to insurance bill ,', insurance_data)
                elif cash_data != None:
                    cash_data.status = 'cancel'
                    cash_data.save()
                    print('cash_data saved to cash bill ,', cash_data)
                else:
                    print('nothing to dooo.....')
                sub_data = OpdBillingSub.objects.filter(bill_no=bill_num)
                for data in sub_data:
                    data.status = 'inactive'
                    data.save()
                    print('data saved Sub Bill table bill ,', data)
                bill.save()
                print('data saved Cancel remark table bill ,',bill)
                return HttpResponseRedirect('/cancel_bill')
            else:
                print('Errors=====>,',cancel_bill.errors)
    sample_collection=SampleCollected.objects.values('bill_no')
    all_result=OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
        }).filter(location=request.location).exclude(bill_no__in=sample_collection).order_by('-id')
    all_result=all_result.exclude(status__in=['cancel'])
    data=''
    bill_nos=request.POST.get('bill_nos')
    name=request.POST.get('name')
    if bill_nos:
        data=OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
        }).get(bill_no=bill_nos)
    if name:
        print('name',name)
        patient_details=PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=name,location=request.location)
        uhids_list=[data.uhid for data in patient_details]
        print('uhids_list',uhids_list)
        all_result=OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
            'pat_billing_group': 'Select billing_group from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid LIMIT 1',
        }).filter(uhid__in=uhids_list,location=request.location)
    context={
        'all_result':all_result,'data':data,'cancel_bill':cancel_bill,
    }
    return render(request,'clinical/opd_bill/cancel_bill.html',context)



@login_required(login_url='/user_login')
def cancel_bill_store(request,pk):
    record=OpdBillingMain.objects.get(id=pk)
    bill_num=record.bill_no
    pending=PendingInvestigation_main.objects.filter(bill_no=bill_num).last()
    if pending:
        pending.delete(print('successfull deletet'))
    bill_num=record.bill_no
    # main_table = OpdBillingMain.objects.get(bill_no=var_bill_no)
    record.status = 'cancel'
    record.save()
    # sub_data=OpdBillingSub.objects.filter(bill_no=bill_num)
    # count_sub_data=OpdBillingSub.objects.filter(bill_no=bill_num).count()
    #===================== For Update Cancel Bill in OPDPAYMENT and OPDBillingSub Table =================
    cash_data=OpdPayment.objects.filter(bill_id=bill_num).last()
    insurance_data=Credit.objects.filter(bill_no=bill_num).last()
    if insurance_data:
        insurance_data.department='cancel'
        insurance_data.save()
    elif cash_data != None:
        cash_data.status= 'cancel'
        cash_data.save()
    else:
        print('nothing to dooo.....')
    sub_data=OpdBillingSub.objects.filter(bill_no=bill_num)
    for data in sub_data:
        data.status= 'inactive'
        data.save()
    #=============================== END ===========================
    data=CancelOpdBillingMain(
        bill_no = record.bill_no,
        bill_id = record.bill_id,
        bill_date_time = record.bill_date_time,
        uhid = record.uhid,
        temp_bill_no = record.temp_bill_no,
        department = record.department,
        doctor_name = record.doctor_name,
        visit_no = record.visit_no,
        corporate_id = record.corporate_id,
        billing_group_id = record.billing_group_id,
        package_profile_id = record.package_profile_id,
        net_amount = record.net_amount,
        discount = record.discount,
        pay_amount = record.pay_amount,
        paid_amount = record.paid_amount,
        outstanding_amount = record.outstanding_amount,
        payment_mode = record.payment_mode,
        paid_amt = record.paid_amt,
        paid_amt_update_date = record.paid_amt_update_date,
        updated_at = record.updated_at,
        status = record.status,
    )
    data.save()
    # record.delete()
    # sub_data.delete()
    return HttpResponseRedirect('/cancel_bill')

@login_required(login_url='/user_login')
def discharge_form(request):
    return render(request,'clinical/mantu/discharge_form.html')

@login_required(login_url='/user_login')
def case_summery(request):
    record=CaseSummery.objects.all()
    if request.method=="POST":
        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        hosp_no = request.POST.get('hosp_no')
        tel_no = request.POST.get('tel_no')
        address = request.POST.get('address')
        d_o_a = request.POST.get('d_o_a')
        d_o_d = request.POST.get('d_o_d')
        consultant = request.POST.get('consultant')
        dept = request.POST.get('dept')
        medical_history = request.POST.get('medical_history')
        physi_find = request.POST.get('physi_find')
        investigation = request.POST.get('investigation')
        management = request.POST.get('management')
        treat_discharge = request.POST.get('treat_discharge')
        recommendation = request.POST.get('recommendation')
        follow_up = request.POST.get('follow_up')
        day = request.POST.get('day')
        date = request.POST.get('date')
        time = request.POST.get('time')
        name_sign = request.POST.get('name_sign')
        doctor_notes = request.POST.get('doctor_notes')
        uhid = 'UHID2301120000'
        dat=CaseSummery(
            uhid = uhid,
            patient_name = patient_name,
            age = age,
            hosp_no = hosp_no,
            tel_no = tel_no,
            address = address,
            d_o_a = d_o_a,
            d_o_d = d_o_d,
            consultant = consultant,
            dept = dept,
            medical_history = medical_history,
            physi_find = physi_find,
            investigation = investigation,
            management = management,
            treat_discharge = treat_discharge,
            recommendation =recommendation,
            follow_up = follow_up,
            day = day,
            date = date,
            time = time,
            name_sign = name_sign,
            doctor_notes =doctor_notes,
        )
        dat.save()

    return render(request,'clinical/mantu/case_summery.html',{'record':record})

@login_required(login_url='/user_login')
def print_case_summery(request,pk):
    record=CaseSummery.objects.get(id=pk)
    return render(request,'clinical/mantu/case_summery.html',{'dt':record})

@login_required(login_url='/user_login')
def consent_chemotherapy(request):
    consent = ConsentChemotherapy.objects.all()
    if request.method=="POST":
        patient_name=request.POST.get('patient_name')
        patient_nhif_id = request.POST.get('nhif_id')
        patient_national_id = request.POST.get('national_id')
        date = request.POST.get('date')
        time=request.POST.get('time')
        patient_email=request.POST.get('email')
        diagnosis = request.POST.get('diagnosis')
        chemotherapy_protocol =request.POST.get('chemotherapy_protocol')
        inform_by_dr = request.POST.get('inform_by_dr')
        i_have = request.POST.get('i_have')
        language =request.POST.get('language')
        patient_sign = request.POST.get('patient_sign')
        patient_relative_sign =request.POST.get('patient_relative_sign')
        witness = request.POST.get('witness')
        uhid='UHID2301120000'
        data=ConsentChemotherapy(
            uhid =uhid,
            patient_name=patient_name,
            patient_nhif_id = patient_nhif_id,
            patient_national_id = patient_national_id,
            date = date,
            time=time,
            patient_email=patient_email,
            diagnosis = diagnosis,
            chemotherapy_protocol =chemotherapy_protocol,
            inform_by_dr = inform_by_dr,
            i_have = i_have,
            language =language,
            patient_sign = patient_sign,
            patient_relative_sign =patient_relative_sign,
            witness = witness,
        )
        data.save()
    return render(request,'clinical/mantu/consent_chemotherapy.html',{'consent':consent})

@login_required(login_url='/user_login')
def print_consent_chemotherapy(request,pk):
    dt=ConsentChemotherapy.objects.get(id=pk)
    return render(request,'clinical/mantu/consent_chemotherapy.html',{'dt':dt})

@login_required(login_url='/user_login')
def refferal_form(request):
    record=Refferal_notes.objects.all()
    if request.method=="POST":
        date=request.POST.get('date')
        dr=request.POST.get('dr')
        re=request.POST.get('re')
        age=request.POST.get('age')
        diagnosis=request.POST.get('diagnosis')
        uhid='UHID2301120000'
        data=Refferal_notes(
            uhid=uhid,
            date=date,
            dr=dr,
            re=re,
            age=age,
            diagnosis=diagnosis,
        )
        data.save()
    context={
        'record':record,
    }
    return render(request,'clinical/mantu/refferal_form.html',context)


@login_required(login_url='/user_login')
def print_refferal_form(request,pk):
    dt=Refferal_notes.objects.get(id=pk)
    return render(request,'clinical/mantu/refferal_form.html',{'dt':dt})


@login_required(login_url='/user_login')
def discharge_list(request):
    records1 = PatientsRegistrationsAllInOne.objects.all()
    print(records1.count())
    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        get_dob = request.POST.get('dob')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if get_dob == '':
            get_dob = date.today()
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records = PatientsRegistrationsAllInOne.objects.filter(
                Q(uhid__exact=uhid) | Q(first_name=patient_name) | Q(mobile_number__exact=mobile_number))
            print('records', records.count())
            success_search = 'success'
            context = {
                'records': records, 'success_search': success_search,'discharge_list':discharge_list,
            }
            return render(request, 'clinical/mantu/discharge_list.html', context)
        except Exception as e:
            # raise e
            pass

    context = {
        'records1': records1,
    }
    return render(request,'clinical/mantu/discharge_list.html',context)

#============================= for opd billing data ==========================

@login_required(login_url='/user_login')
def discharge_listopd(request):
    records1 = OpdBillingMain.objects.all()
    if request.method == 'POST':
        bill_no = request.POST.get('bill_no')
        if bill_no == '':
            bill_no = "Not Provided"
        try:
            records1 = OpdBillingMain.objects.filter(bill_no=bill_no)
            success_search = 'success'
            context = {'records': records1, 'success_search': success_search,}                      
            return render(request, 'clinical/mantu/discharge_listopd.html', context)
        except Exception as e:
            pass
    return render(request,'clinical/mantu/discharge_listopd.html',{'records1': records1})

@login_required(login_url='/user_login')
def discharge_reportopd(request,pk):
    datas=pk
    lab_records=''
    list_da=datas.split('-')
    uhid=list_da[0]
    bill_no=list_da[1]
    date_field = datetime.now()
    data = PatientsRegistrationsAllInOne.objects.get(uhid=uhid)
    records = OpdBillingMain.objects.filter(uhid=uhid,bill_no=bill_no).last()
    lab_test_id=SampleCollected.objects.filter(uhid=uhid,bill_no=bill_no).last()
    if lab_test_id != None:
        test_ids=lab_test_id.test_id
        lab_records=LabResultEntry_records.objects.filter(test_id=test_ids)
    name=data.title+' '+data.first_name+' '+data.middle_name+' '+data.last_name
    context={
        'dt':data,'name':name,'date_field':date_field,'records':records,'lab_records':lab_records,
    }
    return render(request,'clinical/mantu/discharge_reportopd.html',context)
#================================================= END ==================================================
@login_required(login_url='/user_login')
def discharge_report(request,pk):
    date_field = datetime.now()
    data = PatientsRegistrationsAllInOne.objects.get(uhid=pk)
    name=data.title+' '+data.first_name+' '+data.middle_name+' '+data.last_name
    context={
        'dt':data,'name':name,'date_field':date_field,
    }
    return render(request,'clinical/mantu/discharge_report.html',context)

#==================== Detail for all ==========================================
@login_required(login_url='/user_login')
def dep_lab_report_all(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'lab_report' in access.user_profile.screen_access:
        try:

            records = SampleCollected.objects.extra(select={
                'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).exclude(status__in=['waiting','completed',]).order_by('-date_time')
            if request.method=='POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')
                patient_name=request.POST.get('patient_name')
                if from_date and to_date:
                    records = SampleCollected.objects.extra(select={
                        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        }).exclude(status__in=['waiting','completed',]).filter(date_time__range=[from_date,to_date]).order_by('-date_time')
                elif patient_name:
                    patient=PatientsRegistrationsAllInOne.objects.filter(Q(first_name__icontains=patient_name) | Q(middle_name__icontains=patient_name) | Q(last_name__icontains=patient_name))
                    records = SampleCollected.objects.extra(select={
                        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                        }).exclude(status__in=['waiting','completed',]).filter(uhid__in=patient.values('uhid')).order_by('-date_time')
            context={
                'records':records
            }
            return render(request,'lab_module/dep_lab_report_all.html',context)
        except Exception as error:
            return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
#=================================== END ====================================

#  old lab report code
@login_required(login_url='/user_login')
def dep_lab_report_print_all(request,pk):
    entry_records=LabResultEntry.objects.filter(test_id=pk)
    collected=SampleCollected.objects.filter(PTID=pk,status='vallidated')
    doctor=[data.doctor_id for data in collected]
    depts=[data.department for data in collected]
    uhids=[data.uhid for data in collected]
    dr_set=set(doctor)
    dept=list(set(depts))
    uhid=set(uhids)
    for dat in dr_set:
        doc_sign=DoctorTable.objects.filter(doctor_id=dat).first()
        if doc_sign:
            doc_sign=doc_sign.doctor_sign_image
        else:
            doc_sign=''
    for dt in uhid:
        patient_records=PatientsRegistrationsAllInOne.objects.get(uhid=dt)
        uhiddd=patient_records.uhid
        name=str(patient_records.first_name)+' '+str(patient_records.middle_name)+' '+patient_records.last_name
        age=patient_records.age
        gender=patient_records.gender
        registration_date_and_time=patient_records.registration_date_and_time
        if patient_records.referred_by == 'Walked By':
            referred_by=patient_records.referred_by
        else:
            refer=Refered_by_Master.objects.filter(id=patient_records.referred_by).last()
            referred_by=refer.Staff_name
        patient_barcode=PatientBarCode.objects.get(uhid=dt)
        barcodes=patient_barcode.barcode
    test_id_list=[data.test_id for data in entry_records]
    type_of_samples = SampleCollection.objects.filter(PTID=pk)
    sample_type=[data.type_of_sample for data in type_of_samples]
    sample_time=[data.date_time for data in type_of_samples]
    s_type=list(set(sample_type))
    s_time=list(set(sample_time))
    test_id_list=list(set(test_id_list))
    if name:
        ser_dep = ''
        if ser_dep:
            collected = SampleCollected.objects.filter(PTID=pk, department__in=ser_dep,status='vallidated')
        else:
            collected = SampleCollected.objects.filter(PTID=pk,status='vallidated')
    else:
        return HttpResponseRedirect('/user_login')

    a=[]
    b=[]
    for data in collected:
        rec=LabResultEntry.objects.filter(test_id=data.test_id)
        a.append(rec.last().profile_name)
        b.append(rec)
    # =======================================
    rec=''
    profile_n=[]
    service_list=[]
    dep_list=[]
    time=[]
    type=[]
    dr_name=[]
    dr_dept=[]
    dr_sign=[]
    dr_qualifi=[]
    booking_id=[]
    ranges=[]
    tech_id=[]
    technician=''
    technician_name=[]
    for data in dept:
        samp_rec=SampleCollected.objects.filter(department=data,PTID=pk,status='vallidated')
        for pro in samp_rec:
            type_of_samples = SampleCollection.objects.filter(test_id=pro.test_id).last()
            doc_sign = DoctorTable.objects.filter(doctor_id=pro.doctor_id).first()
            time.append(type_of_samples.date_time)
            type.append(type_of_samples.type_of_sample)
            dep_list.append(pro.sub_department)
            profile_n.append(pro.profile_name)
            booking_id.append(pro.bill_no)
            if doc_sign:
                dr_name.append(doc_sign.doctor_name)
                dr_sign.append(doc_sign.doctor_sign_image)
                dr_dept.append(doc_sign.doctor_department)
                dr_qualifi.append(doc_sign.doctor_register_by)
            else:
                dr_name.append('')
                dr_sign.append('')
                dr_dept.append('')
                dr_qualifi.append('')
            lab_rec=LabResultEntry.objects.filter(test_id=pro.test_id)
            tech_id.append(type_of_samples.technician_name)
            if request.user.is_superuser:
                technician_names=request.user
            else:
                technicianname=CreateUser.objects.get(login_id=request.user)
                technician_names = technicianname.f_name + ' ' + technicianname.middle_name + ' ' + technicianname.last_name
            technician_name.append(pro.validated_by)
            range = [data.range for data in lab_rec]
            service_name = [data.service_name for data in lab_rec]
            value = [data.value for data in lab_rec]
            service_list.append(lab_rec)
            min = []
            max = []
            # for item in range:
            #     split_item = item.split("-")
            #     min.append(split_item[0])
            #     max.append(split_item[1])
    template=[]
    for data in profile_n:
        tem=LabTemplateMaster.objects.filter(profile_name=data)
        if tem:
            template.append(tem.first())
        else:
            template.append('')
    dat1 = zip(value,service_name,min,max)
    records=zip(booking_id,type,time,dep_list,service_list,profile_n,technician_name,dr_name,dr_sign,dr_dept,dr_qualifi,template)
    print('referred_by',referred_by)
    context={
        'records':records,'dept':dept,'barcodes':barcodes,'uhiddd':uhiddd,'b':b,
        'rec':rec,'a':a,'uhiddd':uhiddd,'name':name,'age':age,'gender':gender,'registration_date_and_time':registration_date_and_time,
        'referred_by':referred_by,'doc_sign':doc_sign,'s_type':s_type,'s_time':s_time,'service_list':service_list,'dat1':dat1,
    }

    return render(request,'lab_module/all_report_print.html',context)


#  new lab report code
def final_lab_report(request,pk):
    collected=SampleCollected.objects.filter(PTID=pk,status='vallidated').order_by('id')
    patient_record=PatientsRegistrationsAllInOne.objects.get(uhid=collected.last().uhid)
    barcode=PatientBarCode.objects.filter(uhid=collected.last().uhid).last()
    if patient_record.referred_by == 'Walked By':
        referred_by=patient_record.referred_by
    else:
        refer=Refered_by_Master.objects.filter(id=patient_record.referred_by).last()
        referred_by=refer.Staff_name
    opd_record=OpdBillingMain.objects.filter(uhid=collected.last().uhid).last()
    department=list(set([data.sub_department for data in collected]))
    records=[]
    for dep in department:
        List=[]
        collected=SampleCollected.objects.filter(PTID=pk,sub_department=dep,status='vallidated').order_by('-id')
        for data in collected:
            history=Validation_record.objects.filter(PTID=data.test_id).last()
            print('history',history)
            record=LabResultEntry.objects.filter(test_id=data.test_id)
            tem=LabTemplateMaster.objects.filter(profile_name=data.profile_name)
            tem2=RadiologyTemplateMaster.objects.filter(service__service_name=data.profile_name)
            if tem:
                template=tem.first()
            elif tem2:
                template=tem2.first()
            else:
                template=''
            List.append([data,record,template,history])
        records.append([dep,List])
    # print(records)
    # for data in records:
    #     print(data)
    context={
        'records':records,'patient_record':patient_record,'barcode':barcode,'referred_by':referred_by
        }

    return render(request,'lab_module/final_lab_report.html',context)
#=========================== END ==================================================
#================== To Send Lab Report On Email ===================================================

from django.core.mail import send_mail,EmailMessage

@login_required(login_url='/user_login')
def send_email(request,pk):
    patient_records=''
    collected=SampleCollected.objects.filter(PTID=pk)
    uhids=[data.uhid for data in collected]
    bill_nos=[data.bill_no for data in collected]
    uhid=set(uhids)
    bill_no=set(bill_nos)
    print('uhid----------->>>>>>>>>>>>>>>>>>>>',uhid)
    print('uhid----------->>>>>>>>>>>>>>>>>>>>',bill_no)
    for dt in uhid:
        patient_records=PatientsRegistrationsAllInOne.objects.get(uhid=dt)
        name=patient_records.first_name+' '+patient_records.middle_name+' '+patient_records.last_name
        email_id=patient_records.email
    if request.method=="POST":
        name=request.POST.get('user_name')
        subject=request.POST.get('subject')
        message=request.POST.get('msg')
        email_id=request.POST.get('email_id')
        file=request.FILES.get('files')
        print('file============',file)
        data=LabReportStore(uhid=uhid,bill_no=bill_no,report=file)
        data.save()
        mail1 = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email_id])
        mail1.attach(file.name, file.read(), file.content_type)
        mail1.send()
        print('mail1----',mail1)
    context={
        'patient_records':patient_records,'name':name,'email_id':email_id,
    }
    return render(request,'lab_module/send_email.html',context)



@login_required(login_url='/user_login')
def list_dialysis_patient(request):
    records1 = PatientsRegistrationsAllInOne.objects.all()
    print(records1.count())
    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records1 = PatientsRegistrationsAllInOne.objects.filter(
                Q(uhid__exact=uhid) | Q(first_name=patient_name) | Q(mobile_number__exact=mobile_number))
            success_search = 'success'
            context = {
            'success_search': success_search,'discharge_list':discharge_list,'records1':records1,
            }
            return render(request, 'dialysis/list_dialysis_patient.html', context)
        except Exception as e:
            # raise e
            pass
    context = {
        'records1': records1,
    }
    return render(request,'dialysis/list_dialysis_patient.html',context)


###--Insurance Module---###


def unique_id(pre, suf):
    tot_rec_count = len(suf) + 1
    if len(str(tot_rec_count)) == 1:
        id = pre + '00' + str(tot_rec_count)
    elif len(str(tot_rec_count)) == 2:
        id = pre + '0' + str(tot_rec_count)
    else:
        id = pre + str(tot_rec_count)
    return id



@login_required(login_url='/user_login')
def checklist_master(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'checklist_master' in access.user_profile.screen_access:
        try:
            record = Insurance_CheckList_Master.objects.all()
            form = Insurance_CheckList_MasterForm()
            if request.method == 'POST':
                form = Insurance_CheckList_MasterForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/checklist_master')
            context = {
                'form': form,
                'record': record,
            }

            return render(request, 'insurance_claim/checklist_master.html', context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


import dateutil.parser



@login_required(login_url='/user_login')
def insurance_claim(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'insurance_claim' in access.user_profile.screen_access:
        try:
            record = OpdBillingMain.objects.extra(select={
                    'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                }).filter(checklist_status='pending',location_id=request.location).order_by('-bill_date_time')

            checklist = Insurance_CheckList_Master.objects.all()
            context = {
                'checklist': checklist,
                'record': record,
            }
            checklist_count = Insurance_Checklist_Parent.objects.all()

            checklist_no = unique_id('CDN', checklist_count)

            if request.method == "POST":

                checklist_parent = Insurance_Checklist_Parent(
                    checklist_no=checklist_no,
                    checklist_date=datetime.now(),
                    bill_no=request.POST.get('bill_no'),
                    bill_datetime=dateutil.parser.parse(request.POST.get('bill_datetime')),
                    lou_no=request.POST.get('lou_no'),
                    claim_no=request.POST.get('claim_no'),
                    batch_no=request.POST.get('batch_no'),
                    uhid=request.POST.get('uhid'),
                    bill_amt=request.POST.get('bill_amount'),
                    net_amt=request.POST.get('net_amount'),
                    status='',created_by_id=request.user.id,location_id=request.location,
                )
                checklist_parent.save()

                for data in checklist:
                    prepare_status = request.POST.get(f'prepared_{data.id}')
                    checklist_child = Insurance_Checklist_Child(
                        checklist_no=checklist_no,
                        checklist_date=datetime.now(),
                        document_name=data.checklist_name,
                        prepare_status=prepare_status,
                        status='',created_by_id=request.user.id,location_id=request.location,
                    )
                    checklist_child.save()

                status = OpdBillingMain.objects.get(bill_no=request.POST.get('bill_no'))
                status.checklist_status = 'prepared'
                status.batch_no = request.POST.get('batch_no')
                status.claim_no = request.POST.get('claim_no')
                status.save()

            return render(request, 'insurance_claim/insurance_claim.html', context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')




@login_required(login_url='/user_login')
def checklisted_bill(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'checklisted_bill' in access.user_profile.screen_access:
        try:
            checklist = OpdBillingMain.objects.extra(select={
                    'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                }).filter(checklist_status='prepared', claim_status__in=['pending', 'raising_queries'],location_id=request.location).order_by('-bill_date_time')

            return render(request, 'insurance_claim/checklisted_bill.html', {'checklist': checklist})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')



@login_required(login_url='/user_login')
def claim_acknowledge(request, bill_no):
    bill_details = OpdBillingMain.objects.get(bill_no=bill_no)
    if request.method == "POST":
        claim_acknowledge = Insurance_Claim_Acknowledge(
            bill_no=request.POST.get('bill_no'),
            bill_datetime=dateutil.parser.parse(request.POST.get('bill_date_time')),
            uhid=request.POST.get('uhid'),
            bill_amt=request.POST.get('bill_amt'),
            net_amt=request.POST.get('net_amt'),
            claim_amt=request.POST.get('claim_amt'),
            acknowledge=request.POST.get('acknowledge'),
            status='',created_by_id=request.user.id,location_id=request.location,
        )
        claim_acknowledge.save()

        status = OpdBillingMain.objects.get(bill_no=request.POST.get('bill_no'))
        status.claim_status = 'acknowledge'
        status.claim_amt = request.POST.get('claim_amt')
        status.save()

    return render(request, 'insurance_claim/claim_acknowledge.html', {'bill_details': bill_details})



@login_required(login_url='/user_login')
def raising_queries(request, bill_no):
    bill_details = OpdBillingMain.objects.get(bill_no=bill_no)
    if request.method == "POST":
        raising_queries = Insurance_Raising_Queries(
            bill_no=request.POST.get('bill_no'),
            bill_datetime=dateutil.parser.parse(request.POST.get('bill_date_time')),
            uhid=request.POST.get('uhid'),
            bill_amt=request.POST.get('bill_amt'),
            net_amt=request.POST.get('net_amt'),
            question=request.POST.get('question'),
            answer=request.POST.get('answer'),
            status='',created_by_id=request.user.id,location_id=request.location,
        )
        raising_queries.save()

        status = OpdBillingMain.objects.get(bill_no=request.POST.get('bill_no'))
        status.claim_status = 'raising_queries'
        status.save()

    return render(request, 'insurance_claim/raising_queries.html', {'bill_details': bill_details})

@login_required(login_url='/user_login')
def view_document_details(request, bill_no):
    checklist_no = Insurance_Checklist_Parent.objects.get(bill_no=bill_no)
    document_details = Insurance_Checklist_Child.objects.filter(checklist_no=checklist_no.checklist_no,
                                                                prepare_status='1',location_id=request.location)
    context = {
        'document_details': document_details,
        'bill_no': bill_no,
    }
    return render(request, 'insurance_claim/view_document_details.html', context)


@login_required(login_url='/user_login')

def acknowledge_claim(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'acknowledged_claim' in access.user_profile.screen_access:
        try:
            bill_details = OpdBillingMain.objects.extra(select={
                    'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                }).filter(checklist_status='prepared', claim_status__in=['acknowledge','partially_paid'],location_id=request.location).order_by('-bill_date_time')

            return render(request, 'insurance_claim/acknowledge_claim.html', {'bill_details': bill_details})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

@login_required(login_url='/user_login')

def payment_details_claim(request,pk):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'acknowledged_claim' in access.user_profile.screen_access:
        try:
            checklist_no = Insurance_Checklist_Parent.objects.filter(bill_no=pk).last()
            claim_amt = Insurance_Claim_Acknowledge.objects.filter(bill_no=pk).last()
            bill_amt = OpdBillingMain.objects.get(bill_no=pk)
            payable_amt = int(claim_amt.claim_amt) - int(bill_amt.paid_claim_amt)
            if request.method=='POST':
                messages.success(request,'')
                pay_m_uhid=request.POST.get('pay_m_uhid')
                pay_m_bill_nos=request.POST.get('bill_no')
                amount=request.POST.get('net_amount')
                mode_type=request.POST.get('mode_type')

                # ================== fields ===========
                    # m-pesa
                mpesa_paid_by=request.POST.get('mpesa_paid_by')
                mpesa_ref_no=request.POST.get('mpesa_ref_no')
                mpesa_card_holder_name=request.POST.get('mpesa_card_holder_name')
                mpesa_mobile_no=request.POST.get('mpesa_mobile_no')
                mpesa_pay_amount=request.POST.get('mpesa_pay_amount')
                # bank
                bank=request.POST.get('bank')
                bank_ref_no=request.POST.get('bank_ref_no')
                bank_card_holder_name=request.POST.get('bank_card_holder_name')
                bank_pay_amount=request.POST.get('bank_pay_amount')
                # eft
                eft_ref_no=request.POST.get('eft_ref_no')
                eft_bank_no=request.POST.get('eft_bank_no')
                eft_paid_by=request.POST.get('eft_paid_by')
                eft_pay_amount=request.POST.get('eft_pay_amount')
                # cheque
                cheque_ref_no=request.POST.get('cheque_ref_no')
                cheque_bank_no=request.POST.get('cheque_bank_no')
                cheque_paid_by=request.POST.get('cheque_paid_by')
                cheque_pay_amount=request.POST.get('cheque_pay_amount')

                # pay_m_uhid = request.session['pay_m_uhid']
                # pay_m_bill_nos = request.session['pay_m_bill_no']
                paid_amt = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                if mode_type == 'm_pesa':
                    receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                    today=date.today()
                    today_date=today.strftime("%d%m%y")
                    receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                    claim_paid_amt = int(paid_amt.paid_claim_amt) + int(mpesa_pay_amount)
                    if int(amount) == claim_paid_amt:
                        status='fully_paid'
                    else:
                        status='partially_paid'

                    Insurance_Payement_Detail.objects.create(
                        receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type=mode_type,
                        paid_by=mpesa_paid_by,net_amount=amount,paid_amount=mpesa_pay_amount,ref_number=mpesa_ref_no,status=status,card_holder_name=mpesa_card_holder_name,mobile_nummber=mpesa_mobile_no,

                    )
                    opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                    opd_billmain.claim_status = status
                    opd_billmain.paid_claim_amt = claim_paid_amt
                    opd_billmain.save()
                elif mode_type == 'bank':
                    receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                    today=date.today()
                    today_date=today.strftime("%d%m%y")
                    receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                    claim_paid_amt = int(paid_amt.paid_claim_amt) + int(bank_pay_amount)
                    if int(amount) == claim_paid_amt:
                        status='fully_paid'
                    else:
                        status='partially_paid'

                    Insurance_Payement_Detail.objects.create(
                        receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type=mode_type,
                        bank_no=bank,net_amount=amount,paid_amount=bank_pay_amount,ref_number=bank_ref_no,status=status,card_holder_name=bank_card_holder_name
                    )
                    opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                    opd_billmain.claim_status = status
                    opd_billmain.paid_claim_amt = claim_paid_amt
                    opd_billmain.save()
                elif mode_type == 'eft':
                    receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                    today=date.today()
                    today_date=today.strftime("%d%m%y")
                    receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                    claim_paid_amt = int(paid_amt.paid_claim_amt) + int(eft_pay_amount)
                    if int(amount) == claim_paid_amt:
                        status='fully_paid'
                    else:
                        status='partially_paid'

                    Insurance_Payement_Detail.objects.create(
                        receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type=mode_type,
                            paid_by=eft_paid_by,net_amount=amount,paid_amount=eft_pay_amount,ref_number=eft_ref_no,status=status,bank_no=eft_bank_no
                    )
                    opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                    opd_billmain.claim_status = status
                    opd_billmain.paid_claim_amt = claim_paid_amt
                    opd_billmain.save()
                elif mode_type == 'cheque':
                    receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                    today=date.today()
                    today_date=today.strftime("%d%m%y")
                    receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                    claim_paid_amt = int(paid_amt.paid_claim_amt) + int(cheque_pay_amount)
                    if int(amount) == claim_paid_amt:
                        status='fully_paid'
                    else:
                        status='partially_paid'

                    Insurance_Payement_Detail.objects.create(
                            receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type=mode_type,
                            paid_by=cheque_paid_by,net_amount=amount,paid_amount=cheque_pay_amount,ref_number=cheque_ref_no,status=status,bank_no=cheque_bank_no
                    )
                    opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                    opd_billmain.claim_status = status
                    opd_billmain.paid_claim_amt = claim_paid_amt
                    opd_billmain.save()
                elif mode_type == 'all':
                    total=int(paid_amt.paid_claim_amt) + int('0'+mpesa_pay_amount)+int('0'+bank_pay_amount)+int('0'+eft_pay_amount)+int('0'+cheque_pay_amount)
                    if int(amount) == total:
                        status='fully_paid'
                    else:
                        status='partially_paid'
                    if mpesa_pay_amount:
                        receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                        today=date.today()
                        today_date=today.strftime("%d%m%y")
                        receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                        claim_paid_amt = int(paid_amt.paid_claim_amt) + int(mpesa_pay_amount)
                        Insurance_Payement_Detail.objects.create(
                                receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type='m_pesa',
                                bank_no=mpesa_paid_by,net_amount=amount,paid_amount=mpesa_pay_amount,ref_number=mpesa_ref_no,status=status,card_holder_name=mpesa_card_holder_name,mobile_nummber=mpesa_mobile_no
                        )
                        opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                        opd_billmain.claim_status = status
                        opd_billmain.paid_claim_amt = claim_paid_amt
                        opd_billmain.save()
                    if bank_pay_amount:
                        receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                        today=date.today()
                        today_date=today.strftime("%d%m%y")
                        receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                        claim_paid_amt = int(paid_amt.paid_claim_amt) + int(bank_pay_amount)
                        Insurance_Payement_Detail.objects.create(
                                receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type='bank',
                                bank_no=bank,net_amount=amount,paid_amount=bank_pay_amount,ref_number=bank_ref_no,status=status,card_holder_name=bank_card_holder_name
                        )
                        opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                        opd_billmain.claim_status = status
                        opd_billmain.paid_claim_amt = claim_paid_amt
                        opd_billmain.save()
                    if eft_pay_amount:
                        receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                        today=date.today()
                        today_date=today.strftime("%d%m%y")
                        receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                        claim_paid_amt = int(paid_amt.paid_claim_amt) + int(eft_pay_amount)
                        Insurance_Payement_Detail.objects.create(
                                receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type='eft',
                                paid_by=eft_paid_by,net_amount=amount,paid_amount=eft_pay_amount,ref_number=eft_ref_no,status=status,bank_no=eft_bank_no
                        )
                        opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                        opd_billmain.claim_status = status
                        opd_billmain.paid_claim_amt = claim_paid_amt
                        opd_billmain.save()
                    if cheque_pay_amount:
                        receipt_no_count=Insurance_Payement_Detail.objects.all().count()
                        today=date.today()
                        today_date=today.strftime("%d%m%y")
                        receipt_no='RC'+today_date+"00"+str(receipt_no_count)

                        claim_paid_amt = int(paid_amt.paid_claim_amt) + int(cheque_pay_amount)
                        Insurance_Payement_Detail.objects.create(
                            receipt_no=receipt_no,pay_type='Settlement',created_by_id=request.user.id,location_id_id=request.location,uhid=pay_m_uhid,bill_id=pay_m_bill_nos,mode_type='cheque',
                            paid_by=cheque_paid_by,net_amount=amount,paid_amount=cheque_pay_amount,ref_number=cheque_ref_no,status=status,bank_no=cheque_bank_no
                        )
                        opd_billmain = OpdBillingMain.objects.get(bill_no=pay_m_bill_nos)
                        opd_billmain.claim_status = status
                        opd_billmain.paid_claim_amt = claim_paid_amt
                        opd_billmain.save()
            context = {
                'checklist_no': checklist_no,
                'bill_no': pk,
                'claim_amt':claim_amt,
                'payable_amt':payable_amt,
            }
            return render(request, 'insurance_claim/payment_details_claim.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def raising_queries_list(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'raising_queries_list' in access.user_profile.screen_access:
        try:
            bill_details = Insurance_Raising_Queries.objects.extra(select={
                    'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_insurance_raising_queries.uhid',
                    'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_insurance_raising_queries.uhid',
                    'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_insurance_raising_queries.uhid',
                    'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_insurance_raising_queries.uhid',
                }).filter(location_id=request.location)
            return render(request, 'insurance_claim/raising_queries_list.html', {'bill_details': bill_details})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


@login_required(login_url='/user_login')
def queries_list(request, bill_no):
    query_details = Insurance_Raising_Queries.objects.filter(bill_no=bill_no)

    return render(request, 'insurance_claim/queries_list.html', {'query_details': query_details})


@login_required(login_url='/user_login')
def settled_claim_list(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'settled_queries_list' in access.user_profile.screen_access:
        try:
            bill_details = OpdBillingMain.objects.extra(select={
                    'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                    'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                }).filter(checklist_status='prepared', claim_status='fully_paid',location_id=request.location)

            return render(request, 'insurance_claim/settled_claim_list.html', {'bill_details': bill_details})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')


import json
@login_required(login_url='/user_login')
def save_claim_settle(request):
    claim_amount = Insurance_Claim_Acknowledge.objects.get(bill_no=request.GET.get('bill_no'))
    data = claim_amount.claim_amt
    status = OpdBillingMain.objects.get(bill_no=request.GET.get('bill_no'))
    status.claim_status = 'claim_settled'
    status.claim_amt = data
    status.save()

    return HttpResponse(data, content_type='application/json')

#=============================nephromed pharmacy=====================

# Gohila pharmacy
# Start Vendor Master
@login_required(login_url='/user_login')
def vendor_master(request):
    error=''
    vendor_master=[]
    vendarshortnames=[]
    vendor_master = VendorMaster.objects.all()
    vendarname=request.POST.get('vendor_name')
    vendarshortname=request.POST.get('vendor_short_name')
    contact_person=request.POST.get('contact_person')
    address=request.POST.get('address')
    pin_code=request.POST.get('pin_code')
    cityid=request.POST.get('city')
    district=request.POST.get('district')
    phone1=request.POST.get('phone1')
    phone2=request.POST.get('phone2')
    fax_no=request.POST.get('fax_no')
    email=request.POST.get('email')
    website=request.POST.get('website')
    tax_id=request.POST.get('tax_id')
    rating=request.POST.get('rating')
    afc_code=request.POST.get('afc_code')
    type_char=request.POST.get('type_char')
    inactive=request.POST.get('inactive')
    insert=request.POST.get('insert')
    if insert is True:
        vendarname.append(vendor_master)
        vendarshortname.append(vendarshortnames)

    records =zip(vendor_master,vendarshortnames)


    if inactive == "none":
        inactive='1'
    else:
        inactive='0'
    if request.method == 'POST':
        vendarmaster = VendorMaster(
            vendor_name=vendarname,
            vendor_short_name=vendarshortname,
            contact_person=contact_person,
            address=address,
            city=cityid,
            district=district,
            pincode=pin_code,
            phone1=phone1,
            phone2=phone2,
            fax_no=fax_no,
            email=email,
            website=website,
            tax_id=tax_id,
            rating=rating,
            afc_code=afc_code,
            type_char=type_char,
            payment_mode = request.POST.get('payment_mode'),
            payment_terms = request.POST.get('payment_terms'),
            inactive=inactive,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        vendarmaster.save(print("vendar master is saved"))
        return redirect('vendor_master')
        context={
       'vendor_master': vendor_master,'error':error
        }
        return render(request, 'inventory_master/vendor_master.html',context)
    vendormaster=VendorMaster.objects.all()
    context={
       'vendor_master': vendor_master,'error':error,'vendormaster':vendormaster,'records':records,'insert':insert
    }
    return render(request, 'inventory_master/vendor_master.html',context)

@login_required(login_url='/user_login')
def edit_vendor_master(request):
    form = VendorMasterrForm()
    vendor_master = VendorMaster.objects.all()
    if request.method == 'POST':
        form = VendorMasterrForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'inventory_master/edit_vendor_master.html', {'form': form, 'vendor_master': vendor_master})


@login_required(login_url='/user_login')
def editing_vendor_master(request, id):
    vendor_master = VendorMaster.objects.get(id=id)
    form = VendorMasterrForm(instance=vendor_master)
    if request.method == 'POST':
        form = VendorMasterrForm(request.POST, instance=vendor_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_vendor_master')
    return render(request, 'inventory_master/editing_vendor_master.html',
                  {'form': form, 'vendor_master': vendor_master})


@login_required(login_url='/user_login')
def deleting_vendor_master(request, id):
    vendor_master = VendorMaster.objects.get(id=id)
    vendor_master.delete()
    return HttpResponseRedirect('/vendor_master')


# End Vendor Master

@login_required(login_url='/user_login')
def itemsubcategory_master(request):
    records=ItemsubcategoryMaster.objects.all()
    itemsubcatogory_form =ItemsubcategoryMasterForm()
    if request.method=='POST':
        itemsubcatogory_form=ItemsubcategoryMasterForm(request.POST)
        if itemsubcatogory_form.is_valid():
            itemsubcatogory_form.save()
            return HttpResponseRedirect('/itemsubcategory_master')
    context={
        'itemsubcatogory_form':itemsubcatogory_form,'records':records
    }
    return render(request,'inventory_master/itemsubcategorymaster.html',context)

@login_required(login_url='/user_login')
def generic_master(request):
    records=Generic_Master.objects.all()
    generic_master_form =Generic_MasterForm()
    if request.method=='POST':
        generic_master_form=Generic_MasterForm(request.POST)
        if generic_master_form.is_valid():
            generic_master_form.save()
            return HttpResponseRedirect('/generic_master')
    context={
        'generic_master_form':generic_master_form,'records':records
    }
    return render(request,'inventory_master/generic_master.html',context)

#only use ajax script for item master

@login_required(login_url='/user_login')
def load_itemcategory(request):
    itemcategory_id=request.GET.get('itemcategory')
    print(itemcategory_id)
    subcategory=ItemsubcategoryMaster.objects.filter(itemcategory=itemcategory_id)
    print('subcategory',subcategory)
    return JsonResponse(list(subcategory.values('id','itemsubcategory')),safe=False)


@login_required(login_url='/user_login')
def inventory_itemmaster(request):
    name=request.session['Name']
    belongs_to=ItemBelongsToMaster.objects.all()
    item_category=ItemCategoryMaster.objects.all()
    item_subcategory=ItemsubcategoryMaster.objects.all()
    generic=Generic_Master.objects.all()
    packing=PackagigMaster.objects.all()
    item_unit=ItemUnitMaster.objects.all()
    item_manufact = ItemManufact.objects.all()
    supplier = ItemSupplier.objects.all()
    manu_temp = ManufactureTempTable.objects.all()
    department_1=ServiceDepartment.objects.all()
    form = Inventory_ItemMasterForm()
    belongs=request.POST.get('belongs_to')
    department=request.POST.get('department')
    category=request.POST.get('item_category')
    subcategory=request.POST.get('item_subcategory')
    generic_id=request.POST.get('generic_id')
    itemname=request.POST.get('item_name')
    short_code=request.POST.get('short_code')
    package=request.POST.get('packaging')
    contain=request.POST.get('contain')
    unit=request.POST.get('unit')
    conversion_factor=request.POST.get('conversion_factor')
    hsn_code=request.POST.get('hsn_code')
    hos_item_code=request.POST.get('hos_item_code')
    tax=request.POST.get('tax')
    remark=request.POST.get('remark')
    inactive=request.POST.get('inactive')
    expiry=request.POST.get('expiry')
    is_reusable=request.POST.get('is_reusable')
    no_reusable=request.POST.get('no_reusable')
    serial_batch=request.POST.get('serial_batch')
    reusable_rate=request.POST.get('reusable_rate')
    tpa=request.POST.get('tpa')
    service_charge=request.POST.get('service_charge')
    min_quantity=request.POST.get('min_quantity')
    max_quantity=request.POST.get('max_quantity')
    reorder_level=request.POST.get('reorder_level')
    autoindent=request.POST.get('autoindent')
    assets=request.POST.get('Assets')
    if inactive == "none":
        inactive="1"
    else:
        inactive="0"

    if assets == "on":
        assets="1"
    else:
        assets="0"
    if belongs != None:
        if request.method == "POST":
            inventory=Inventory_ItemMaster(
                belongs_to=belongs,
                department_id=department,
                item_category=category,
                item_subcategory_id=subcategory,
                generic_id_id=generic_id,
                item_name=itemname,
                shortcode=short_code,
                packing=package,
                contain=contain,
                unit=unit,
                conversion_factor=conversion_factor,
                hsn_code=hsn_code,
                hsn_item_code=hos_item_code,
                remark=remark,
                tax=tax,
                num_of_reuse=no_reusable,
                serial_batch_control=serial_batch,
                reusable_rate=reusable_rate,
                min_quantity=min_quantity,
                max_quantity=max_quantity,
                re_order_level=reorder_level,
                expiry=expiry,
                is_reusable=is_reusable,
                tpa=tpa,
                service_charge=service_charge,
                autointent=autoindent,
                create_by=datetime.now(),
                updated_by=datetime.now(),
                status=inactive,
                assets=assets,

            )
            inventory.save(print('saveee'))
            return HttpResponseRedirect('/inventory_itemmaster')
        context = {
            'form': form, 'item_manufact': item_manufact, 'manu_temp': manu_temp,'login_name':name,'belongs_to':belongs_to,'item_category':item_category,'item_subcategory':item_subcategory,'packing':packing,
    'item_unit':item_unit,"department_1":department_1,'generic':generic
        }
        return render(request, 'inventory_master/item_master.html', context)
    context = {
            'form': form, 'item_manufact': item_manufact, 'manu_temp': manu_temp,'login_name':name,'belongs_to':belongs_to,'item_category':item_category,'item_subcategory':item_subcategory,'packing':packing,
    'item_unit':item_unit,"department_1":department_1,'generic':generic
        }
    return render(request, 'inventory_master/item_master.html', context)


# start Store Master
@login_required(login_url='/user_login')
def store_master(request):
    form = StoreMasterForm()
    store_master = StoreMaster.objects.all()
    if request.method == 'POST':
        form = StoreMasterForm(request.POST)
        print("valid")
        if form.is_valid():
            print("notvalid")
            form.save()
            print(form.as_p)
            return HttpResponseRedirect('/store_master')
    return render(request, 'inventory_master/store_master.html', {'form': form, 'store_master': store_master})



#======================== For list of cancel bill 22/03/2023 ===============================================
def list_cancel_bill(request):
    data=''
    list_can_records=OpdBillingMain.objects.filter(status='cancel').order_by('-updated_at')
    if request.method=='POST':
        bill_nos=request.POST.get('bill_nos')
        data=OpdBillingMain.objects.get(bill_no=bill_nos)
        print('data==========>>>>>>',data.uhid)
    else:
        pass
    context={
        'list_can_records':list_can_records,'data':data,
    }
    return render(request,'clinical/opd_bill/list_cancel_bill.html',context)

def vitals_sign(request):
    searching_uhid = request.GET.get('uhid')
    pat_name = request.GET.get('name')
    # total_p = VitalSign.objects.all().count()
    records=VitalSign.objects.extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
    }).filter(location=request.location).order_by("-id").exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','completed',]))
    total_p=records.count()
    if searching_uhid:
        total_p = VitalSign.objects.filter(Q(uhid__exact=searching_uhid) | Q(bill_id__exact=searching_uhid)).count()
        records = VitalSign.objects.filter(Q(uhid__exact=searching_uhid)|Q(bill_id__exact=searching_uhid)).extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
    }).exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','completed',]))
    if pat_name:
        pat_record = PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=pat_name,
                                                                  location=request.location)
        list_uhid = [data.uhid for data in pat_record]
        records = VitalSign.objects.filter(uhid__in=list_uhid).extra(
            select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
            }).order_by("-id").exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','completed',]))
    context={
        'records':records,'total_p':total_p,
    }
    return render(request,'nurse_station/vitals_sign.html',context)
#========================================== Appointment searching by name merging code 29/03/2023 =======================================
def list_of_appointment(request):
    records=''
    patient_details = BookedAppointments.objects.filter(location=request.location).exclude(patient_scheduled_id__icontains='n/a').order_by('-patient_id')
    if request.method=="POST":
        try:
            pa_name=request.POST.get('patient_name').strip()
            pa_name_1 = pa_name.split(" ")
            print(len(pa_name_1))
            if len(pa_name_1) == 3:
                records=BookedAppointments.objects.filter(Q(first_name__icontains=pa_name_1[0]) & Q(middle_name__icontains=pa_name_1[1]) & Q(last_name__icontains=pa_name_1[2])).exclude(patient_scheduled_id__icontains='n/a')
            elif len(pa_name_1) == 2:
                records=BookedAppointments.objects.filter(Q(first_name__icontains=pa_name_1[0]) & Q(last_name__icontains=pa_name_1[1]) | Q(first_name__icontains=pa_name_1[0]) & Q(middle_name__icontains=pa_name_1[1])).exclude(patient_scheduled_id__icontains='n/a')

        except:
            messages.error(request,'This Name Related Data Not Exists')
            print('This Name Related Data Not Exists')
    context={
        'patient_details':patient_details,'records':records,
    }
    return render(request,'admin1/appointment_table.html',context)

def location_master(request):
    records=LocationMaster.objects.all()
    form=LocationMasterForm()
    if request.method=='POST':
        form=LocationMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_master')
    return render(request,'general_master/location_master.html',{'form':form,'records':records})

def edit_location_master(request,pk):
    records=LocationMaster.objects.get(id=pk)
    form=LocationMasterForm(instance=records)
    if request.method=='POST':
        form=LocationMasterForm(request.POST,request.FILES,instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/location_master')
    return render(request,'general_master/edit_location_master.html',{'form':form,'records':records})

#  RIS module

def RIS_pendinginvestigation(request):
    records=RIS_PendingInvestigation_main.objects.select_related('uhid').filter(location=request.location,status='active')
    return render(request,'RIS/RIS_pendinginvestigation.html',{'records':records})

def note_book(request,pk):
    record=RIS_PendingInvestigation_main.objects.select_related('uhid','service').get(id=pk)
    template=RadiologyTemplateMaster.objects.filter(service=record.service).first()
    if request.method=='POST':
        if template:
            RIS_Report.objects.create(
                RIS_PendingInvestigation_id=pk,discerption=template.content,
                conclusion=request.POST.get('conclusion'),created_by_id=request.user.id,location_id=request.location,
            )
        else:
            RIS_Report.objects.create(
            RIS_PendingInvestigation_id=pk,discerption=request.POST.get('content'),
            conclusion=request.POST.get('conclusion'),created_by_id=request.user.id,location_id=request.location,
        )
        record.status='completed'
        record.save()
        return redirect('RIS_pendinginvestigation')
    return render(request,'RIS/note_book.html',{'record':record,'template':template})

def RIS_report(request):
    records=RIS_PendingInvestigation_main.objects.select_related('uhid').filter(location=request.location,status='completed')
    return render(request,'RIS/RIS_report.html',{'records':records})


def RIS_report_print(request,pk):
    pending=RIS_PendingInvestigation_main.objects.select_related('uhid').get(id=pk)
    report=RIS_Report.objects.filter(RIS_PendingInvestigation_id=pk).first()
    return render(request,'RIS/RIS_report_print.html',{'pending':pending,'report':report})

def final_bill(request):
    ins_pending=OpdBillingMain.objects.filter(claim_status='pending',location=request.location)
    cash_pat=OpdBillingMain.objects.exclude(payment_mode='',location=request.location)
    context={
        'ins_pending':ins_pending,'cash_pat':cash_pat
    }
    return render(request,'clinical/opd_bill/final_bill.html',context)

def template_master(request):
    records=LabTemplateMaster.objects.all()
    records1=RadiologyTemplateMaster.objects.all()
    context={
       'records':records,'records1':records1
    }
    return render(request,'general_master/template_master.html',context)

def radiology_template_master(request):
    service=ServiceMaster.objects.exclude(id__in=RadiologyTemplateMaster.objects.values('service'))
    if request.method=='POST':
        RadiologyTemplateMaster.objects.create(
            service_id=request.POST.get('service'),
            content=request.POST.get('content'),
            status='Active',
        )
        return redirect('template_master')
    context={
       'service':service
    }
    return render(request,'general_master/radiology_template_master.html',context)


def lab_template_master(request):
    service=ProfileMaster.objects.exclude(profile_name__in=LabTemplateMaster.objects.values('profile_name'))
    if request.method=='POST':
        profile=ProfileMaster.objects.filter(id=request.POST.get('service')).first()
        LabTemplateMaster.objects.create(
            profile_id=request.POST.get('service'),
            profile_name=profile.profile_name,
            content=request.POST.get('content'),
            status='Active',
        )
        return redirect('template_master')
    context={
       'service':service
    }
    return render(request,'general_master/lab_template_master.html',context)

def radiology_template_master_edit(request,pk):
    record=RadiologyTemplateMaster.objects.get(id=pk)
    if request.method=='POST':
        record.content=context
        record.save()
        return redirect('template_master')
    context={
       'record':record
    }
    return render(request,'general_master/radiology_template_master_edit.html',context)

def lab_template_master_edit(request,pk):
    record=LabTemplateMaster.objects.get(id=pk)
    if request.method=='POST':
        record.content=request.POST.get('content')
        record.save()
        return redirect('template_master')
    context={
       'record':record
    }
    return render(request,'general_master/lab_template_master_edit.html',context)

import json
def appointment_by_admin(request):
    form=NewAppointmentByAdminForm()
    if request.method=='POST':
        digits='0123456789'
        p_ids= randint(111111,999999)
        appointment_id=randint(100000000,9999999999)
        patient_id='patient'+str(p_ids)
        first_name=request.POST.get('first_name')
        middle_name=request.POST.get('middle_name')
        last_name=request.POST.get('last_name')
        email_id=request.POST.get('email_id')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        appointment_id=appointment_id
        patient_id=patient_id
        mobile_number=request.POST.get('mobile_number')
        request.session['appointment_id']=appointment_id
        request.session['patient_id']=patient_id
        request.session['first_name']=first_name
        request.session['middle_name']=middle_name
        request.session['last_name']=last_name
        request.session['email_id']=email_id
        request.session['age']=age
        request.session['gender']=gender
        request.session['mobile_number']=mobile_number
        return HttpResponseRedirect('/choose-doctor')
    context={
    'form':form
    }
    return render(request,'patient/new_appointment.html',context)

def choose_doctor(request):
    form = NewAppointmentByAdminChooseDoctorForm()
    if request.method == 'POST':
        choose_doctor = 'choose_doctor'
        doctor_name = request.POST.get('doctor_name')
        appointment_date = request.POST.get('appointment_date')
        request.session['appointment_date'] = appointment_date
        request.session['doctor_name'] = doctor_name
        return HttpResponseRedirect('/booked-slots')
    context={
    'form':form
    }
    return render(request,'patient/choose_doctor.html',context)

def booked_slots(request):
    try:
        booking_for_slots = 'booking_for_slots'
        doctor_id = request.session['doctor_name']
        last_name = request.session['last_name']
        first_name = request.session['first_name']
        middle_name = request.session['middle_name']
        appointment_date = request.session['appointment_date']
        doctor_details = DoctorTable.objects.get(doctor_id=doctor_id)
        booked_appointment_id = BookedAppointments.objects.all().only('patient_scheduled_id')
        slots = AvailabilityIntradayScheduleMaster.objects.filter(Q(doctor_id=doctor_id)&Q(time_slot_id__contains=appointment_date))
        records = AvailabilityIntradayScheduleMaster.objects.filter(doctor_id=doctor_id)#Getting D_id From
        records2 = BookedAppointments.objects.all().only('patient_scheduled_id')
        records3 = []
        records4 = []
        for data in records:
            data = data.time_slot_id
            records3.append(data)
        for data2 in records2:
            data = data2.patient_scheduled_id
            records4.append(data)
        #Generate Schedule
        fresh_schedule = []
        for item in records3:
            if item not in records4:
                fresh_schedule.append(item)
        slots = AvailabilityIntradayScheduleMaster.objects.filter(Q(time_slot_id__in=fresh_schedule)&Q(time_slot_id__contains=appointment_date))
        context={
        'booking_for_slots':booking_for_slots,'slots':slots,"last_name":last_name,'first_name':first_name,'middle_name':middle_name,'appointment_date':appointment_date,'doctor_details':doctor_details
        }
        return render(request,'patient/booked_slots.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

def successfully_booked(request):
    doctor_id=request.session['doctor_name']
    age=request.session['age']
    email_id=request.session['email_id']
    appointment_date=request.session['appointment_date']
    appointment_id=request.session['appointment_id']
    patient_id=request.session['patient_id']
    gender=request.session['gender']
    mobile_number=request.session['mobile_number']
    last_name = request.session['last_name']
    first_name = request.session['first_name']
    middle_name = request.session['middle_name']
    doctor_records=DoctorTable.objects.get(doctor_id=doctor_id)
    doctor_name=doctor_records.doctor_name
    doctor_department=doctor_records.doctor_department
    patient_payment_mode='Cash'
    time_slots_id=request.POST.get('time_slots_id')
    get_schedule=AvailabilityIntradayScheduleMaster.objects.filter(time_slot_id=time_slots_id).last()
    scheduled=get_schedule.time_slot_start_time+'-'+get_schedule.time_slot_end_time
    scheduled=appointment_date+','+scheduled
    no_of_appointment=BookedAppointments.objects.all().count()
    today=date.today()
    today=today.strftime("%y%m%d")
    if len(str(no_of_appointment))==1:
        appointment_id='app'+today+'000'+str(no_of_appointment)
        patient_id='pid'+today+'000'+str(no_of_appointment)
    elif len(str(no_of_appointment))==2:
        appointment_id='app'+today+'00'+str(no_of_appointment)
        patient_id='pid'+today+'00'+str(no_of_appointment)
    elif len(str(no_of_appointment))==3:
        appointment_id='app'+today+'0'+str(no_of_appointment)
        patient_id='pid'+today+'0'+str(no_of_appointment)
    else:
        appointment_id='app'+today+str(no_of_appointment)
        patient_id='pid'+today+str(no_of_appointment)

    if request.method=='POST':
        time_slots_id=request.POST.get('time_slots_id')
        patient_scheduled_id=time_slots_id
        records=BookedAppointments.objects.get_or_create(
        patient_id=patient_id,
        first_name =first_name,
        middle_name = middle_name,
        last_name =last_name,
        patient_appointment_date=appointment_date,
        patient_age=age,
        patient_gender=gender,
        patient_email_id=email_id,
        patient_appointment_id =appointment_id,
        patient_mobile_number=mobile_number,
        patient_schedule_date_and_time=scheduled,
        patient_payment_mode=patient_payment_mode,
        doctor_name=doctor_name,
        doctor_department=doctor_department,
        patient_scheduled_id=patient_scheduled_id,
        admin="admin",created_by_id=request.user.id,location_id=request.location,
        # patient_gender=gend
        )
    success='success'
    context={
    'success':success,'patient_id':patient_id,'scheduled':scheduled,'gender':gender,'doctor_name':doctor_name,'doctor_department':doctor_department
    }
    return render(request,'patient/success_booked_by_admin.html',context)

@login_required(login_url='/user_login')
def appointment_patient_search(request):
    # try:
    records1 = BookedAppointments.objects.all().order_by('-patient_appointment_id')
    if request.method=='POST':
        appoint_id=request.POST.get('appointmnt').strip()
        mobile_no=request.POST.get('mobile_number').strip()
        patient_name=request.POST.get('patient_name').strip()
        patient_name=request.POST.get('patient_name').strip()
        patient_name_1 = patient_name.split(" ")
        if appoint_id:
            records1 = BookedAppointments.objects.filter(Q(patient_appointment_id__iexact = appoint_id))
        elif mobile_no:
            records1 = BookedAppointments.objects.filter(Q(patient_mobile_number__icontains = mobile_no))
        elif len(patient_name_1) == 3:
            records1 = BookedAppointments.objects.filter(Q(patient_appointment_id=appoint_id) | Q(patient_mobile_number=mobile_no) | Q(first_name__icontains = patient_name_1[0],middle_name__icontains=patient_name_1[1],last_name__icontains=patient_name_1[2]) )
        elif len(patient_name_1) == 2:
            records1 = BookedAppointments.objects.filter(Q(patient_appointment_id=appoint_id) | Q(patient_mobile_number=mobile_no) | Q(first_name__icontains = patient_name_1[0],last_name__icontains=patient_name_1[2]) | Q(first_name__icontains = patient_name_1[0],middle_name__icontains=patient_name_1[1]))
        elif len(patient_name_1) == 1:
            records1 = BookedAppointments.objects.filter(Q(patient_appointment_id=appoint_id) | Q(patient_mobile_number=mobile_no) | Q(first_name__icontains = patient_name_1[0]) | Q(middle_name__icontains = patient_name_1[0]) | Q(last_name__icontains = patient_name_1[0]))
    context={
    'records1':records1,
    }
    return render(request,'clinical/appoint_patient_search.html',context)

def appointment_detail(request):
    # try:
        scheduled=request.POST.get('scheduled')
        print('scheduled----->,',scheduled)
        time_slots_name=request.POST.get('time_slots_id')
        print('time_slots_name====>,',time_slots_name)
        get_schedule=AvailabilityIntradayScheduleMaster.objects.get(time_slot_id__exact=time_slots_name)
        scheduled=get_schedule.time_slot_start_time+'-'+get_schedule.time_slot_end_time
        request.session['get_schedule_time_slot_id']=get_schedule.time_slot_id
        request.session['scheduled']=scheduled
        scheduled=request.session['scheduled']
        doctor_name=request.session['doctor_name']
        print('doctor_name--->,',doctor_name)
        doctor_department=request.session['doctor_department']
        doctor_location=request.session['doctor_location']
        doctor_profile_image=request.session['doctor_profile_image']
        doctor_appointment=request.session['doctor_appointment']
        mobile_number=request.session['mobile_number']
        first_name = request.session['first_name']
        middle_name = request.session['middle_name']
        last_name = request.session['last_name']
        doctor_fee=request.session['doctor_fee']
        context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'scheduled':scheduled, 'mobile_number':mobile_number,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'doctor_fee':doctor_fee}
        return render(request,'testapp/appointment_detail.html',context)
    # except Exception as error:
    #     return render(request,'error.html',{'error':error})

def schedule_date(request):
    if request.method=='POST':
        date_list=request.session['date_list']
        schedule_date_list=[]
        for date_listed in date_list:
            schedule_date=request.POST.get(date_listed)
            schedule_date_list.append(schedule_date)
    scheduled_date_list=[]
    for scheduled_date in schedule_date_list:
        if scheduled_date == None:
            continue
        else:
            scheduled_date_list.append(scheduled_date)
    request.session['scheduled_date_list']=scheduled_date_list
    context={
    'scheduled_date_list':scheduled_date_list,
    }
    return render(request,'testapp/doctor_schedule_time.html',context)

def permanent_access_master(request):
    permanent_access_master=Permanent_Access_Master.objects.all()
    form=Permanent_Access_MasterForm()
    add='add'
    if request.method=='POST':
        form=Permanent_Access_MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/permanent_access_master')

    context={
    'add':add,'form':form,"permanent_access_master":permanent_access_master
    }
    return render(request,"general_master/permanent_access_master.html",context)

def edit_permanent_access_master(request,pk):
    permanent_access_master=Permanent_Access_Master.objects.get(id=pk)
    form=Permanent_Access_MasterForm(instance=permanent_access_master)
    if request.method=='POST':
        form=Permanent_Access_MasterForm(request.POST,instance=permanent_access_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/permanent_access_master')
    context = {
        "form":form
    }
    return render(request,"general_master/edit_permanent_access_master.html",context)


#======================================= for Dialysis 02/04/2023 =======================================
@login_required(login_url='/user_login')
def list_dialysis_patient(request):
    # records2 = PatientVisitMains.objects.filter(visit_type='2')
    for dat in PatientVisitMains.objects.filter(visit_type='2'):
        data=dat.visit_id
        print('visit_type',data)
        datas = PrescriptionDialysis.objects.filter(visit_id=data)
        print('data=========,',datas)
    records1 = PatientVisitMains.objects.filter(visit_type=2,description='Re-visit').order_by('-id').extra(select={
        'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
    })#.include(uhid__in=PrescriptionDialysis.objects.values('uhid'))
    print(records1.count())
    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records1 = PatientVisitMains.objects.filter(uhid__exact=uhid,visit_type=2,description='Re-visit').extra(select={
                'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
            })
            success_search = 'success'
            print('records1------,',records1)
            context = {
            'success_search': success_search,'discharge_list':discharge_list,'records1':records1,
            }
            return render(request, 'dialysis/list_dialysis_patient.html', context)
        except Exception as e:
            print('e----',e)
            pass
    context = {
        'records1': records1,
    }
    return render(request,'dialysis/list_dialysis_patient.html',context)

@login_required(login_url='/user_login')
def list_new_dialysis_patient(request):
    records1 = PatientVisitMains.objects.filter(visit_type=2,location=request.location).order_by('-id').extra(select={
        'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_machine_name': 'Select machine_name from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
        'pat_attendant_name': 'Select cannulation_nurse from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
        'pat_created_at': 'Select created_at from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
    })

    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records1 = PatientVisitMains.objects.filter(uhid__exact=uhid,visit_type=2,location=request.location).extra(select={
                'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_attendant_name': 'Select cannulation_nurse from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
                'pat_created_at': 'Select created_at from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
                'pat_machine_name':'Select machine_name from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
            })
            success_search = 'success'
            context = {
            'success_search': success_search,'discharge_list':discharge_list,'records1':records1,
            }
            return render(request, 'dialysis/list_new_dialysis_patient.html', context)
        except Exception as e:
            pass
    context = {
        'records1': records1,
    }
    return render(request,'dialysis/list_new_dialysis_patient.html',context)

@login_required(login_url='/user_login')
def prescription_dialysis(request,pk):
    uhid_visit_ud = pk.split('-')
    uhid = uhid_visit_ud[0]
    visit_id_new = uhid_visit_ud[1]
    temporary_dat=Temp_Access.objects.filter(uhid=uhid,visit_id=visit_id_new)
    permanent_dat=Permanent_Access.objects.filter(uhid=uhid,visit_id=visit_id_new)
    prescription_records=PrescriptionDialysis.objects.filter(uhid=uhid).last()
    pre_dialysis_type=''
    records = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid).last()
    uhid_pat_new = records.uhid
    pat_fname = records.first_name
    pat_mname = records.middle_name
    pat_lname = records.last_name
    pat_age_new = records.age
    pat_sex_new = records.gender
    pat_con_no_new = records.mobile_number
    pat_name_new = ''
    if pat_mname == None:
        pat_name_new = pat_fname + ' ' + pat_lname
    else:
        pat_name_new = pat_fname + ' ' + pat_mname + ' ' + pat_lname
    request.session['pat_uhid_new'] = uhid_pat_new
    request.session['pat_visit_new'] = visit_id_new
    request.session['pat_name_new'] = pat_name_new
    request.session['pat_age_new'] = pat_age_new
    request.session['pat_con_no_new'] = pat_con_no_new
    request.session['pat_sex_new'] = pat_sex_new
    doctor_list=DoctorTable.objects.all()
    type_list=VisitTyoeMaster.objects.all()
    dept_list=ClinicalOrDepartment.objects.all()
    access_type = Access_site.objects.all()
    shift_list = Shift.objects.all()
    dialysate_type = Dialysate_Type.objects.all()
    dialyzer_type = Dialyzer.objects.all()
    heparin_Type = Heparin_Type.objects.all()
    permanent_access_master = Permanent_Access_Master.objects.all()
    temp_access=request.POST.get('temp_access')
    Permanent_access=request.POST.get('Permanent_access')
    main_form=request.POST.get('main_form')
    create_schedule=request.POST.get('create_schedule')
    if temp_access == 'TEMP_ACCESS':
        if request.method=='POST':
            temp_ac=request.POST.get('temp_ac')
            date_of_initiation=request.POST.get('date_of_initiation')
            dr_name=request.POST.get('dr_name')
            access_type=request.POST.get('access_type')
            date_of_removal=request.POST.get('date_of_removal')
            Remark=request.POST.get('Remark')
            hospital_name=request.POST.get('hospital_name')
            dat=Temp_Access(
                uhid=uhid,
                visit_id =visit_id_new,
                temp_aces =temp_ac,
                date_initiation=date_of_initiation,
                doctor_name_id =dr_name,
                access_site_id =access_type,
                date_removal =date_of_removal,
                remark =Remark,
                hospital_name=hospital_name,
            )
            dat.save()
    elif create_schedule == 'Create_Schedule':
        if request.method == 'POST':
            department = request.POST.get('department')
            sub_dept = request.POST.get('sub_dept')
            shifting_date = request.POST.getlist('shifting_date')
            shift = request.POST.getlist('shift')
            for i in range(len(shifting_date)):
                no_of_schedule = DialysisSchedule.objects.all().count()
                if len(str(no_of_schedule)) == 1:
                    schedule_id = 'SC' + '00000' + str(no_of_schedule)
                elif len(str(no_of_schedule)) == 2:
                    schedule_id = 'SC' + '0000' + str(no_of_schedule)
                elif len(str(no_of_schedule)) == 3:
                    schedule_id = 'SC' + '000' + str(no_of_schedule)
                elif len(str(no_of_schedule)) == 4:
                    schedule_id = 'SC' + '00' + str(no_of_schedule)
                elif len(str(no_of_schedule)) == 5:
                    schedule_id = 'SC' + '0' + str(no_of_schedule)
                else:
                    schedule_id = 'VI' + str(no_of_schedule)
                schedule_dat = DialysisSchedule(
                    uhid=uhid,
                    schedule_id=schedule_id,
                    department=department,
                    sub_dept=sub_dept,
                    shifting_date=shifting_date[i],
                    shift_id=shift[i],
                )
                schedule_dat.save()
            # return HttpResponseRedirect('/prescription_dialysis,{pk}')
    elif Permanent_access == 'Permanent_Access':
        if request.method == 'POST':
            per_access = request.POST.get('per_access')
            date_of_initiation = request.POST.get('date_of_initiation')
            dr_name = request.POST.get('dr_name')
            access_type = request.POST.get('access_type')
            date_of_removal = request.POST.get('date_of_removal')
            Remark = request.POST.get('Remark')
            hospital_name = request.POST.get('hospital_name')
            dat = Permanent_Access(
                uhid=uhid,
                visit_id=visit_id_new,
                prim_aces_id=per_access,
                date_initiation=date_of_initiation,
                doctor_name_id=dr_name,
                access_site_id=access_type,
                date_failure=date_of_removal,
                remark=Remark,
                hospital_name=hospital_name,
            )
            dat.save()
    elif main_form == 'MAIN_FORM':
        if request.method=='POST':
            dr_name_id = request.POST.get('dr_nameid')
            prescription_date =request.POST.get('prescription_date')
            status = request.POST.get('status')
            s_date = request.POST.get('s_date')
            e_date = request.POST.get('e_date')
            dry_weight = request.POST.get('dry_weight')
            dry_weight_date = request.POST.get('dry_date')
            diagnosis = request.POST.get('Diagnosis')
            day1 = request.POST.get('day1')
            shift1 = request.POST.get('shift1')
            Duration = request.POST.get('Duration')
            day2 = request.POST.get('day2')
            shift2 = request.POST.get('shift2')
            Weekly = request.POST.get('Weekly')
            day3 = request.POST.get('day3')
            shift3 =request.POST.get('shift3')
            dialysis_membrane =request.POST.get('dialysis_membrane')
            day4 = request.POST.get('day4')
            shift4 = request.POST.get('shift4')
            day5 = request.POST.get('day5')
            shift5 = request.POST.get('shift5')
            dialysis_type = request.POST.get('Dialysis_type')
            dialyzer = request.POST.get('Dialyzer')
            dialysate_temp = request.POST.get('Dialysate_temp')
            k_meql = request.POST.get('k_pluse')
            ca_meal = request.POST.get('ca_pluse')
            mg_meal = request.POST.get('mg_pluse')
            glucose = request.POST.get('glucose')
            target_bvp = request.POST.get('Target')
            #======================================
            dialysate_flow = request.POST.get('dialysis_flow')
            profile1 = request.POST.get('Profile1')
            blood_flow = request.POST.get('blood_flow')
            profile2 = request.POST.get('Profile2')
            bicarb = request.POST.get('Bicarb')
            profile3 = request.POST.get('Profile3')
            na_meql = request.POST.get('na_id')
            profile4 = request.POST.get('Profile5')
            uf_rate = request.POST.get('uf_rate')
            ufr_profile = request.POST.get('ufr_profile')
            heparin_type = request.POST.get('heparine_type')
            initial_dose = request.POST.get('initial_dose')
            interim_dose = request.POST.get('interim_dose')
            total_heparin_bolus = request.POST.get('total_heparin')
            hourly = request.POST.get('hourly')
            cut_off_time = request.POST.get('cutoff_time')
            heparin_profile = request.POST.get('heparin_profile')
            comments = request.POST.get('Comment')
            notes = request.POST.get('Notes')
            data=PrescriptionDialysis(
                uhid=uhid,
                visit_id=visit_id_new,
                dr_name_id=dr_name_id,
                drid=dr_name_id,
                prescription_date=prescription_date,
                status=status,
                s_date=s_date,
                e_date=e_date,
                dry_weight=dry_weight,
                dry_weight_date=dry_weight_date,
                diagnosis=diagnosis,
                day1=day1,
                shift1=shift1,
                duration=Duration,
                day2=day2,
                shift2=shift2,
                weekly=Weekly,
                day3=day3,
                shift3=shift3,
                dialysis_membrane=dialysis_membrane,
                day4=day4,
                shift4 =shift4,
                day5=day5,
                shift5=shift5,
                dialysis_type_id=dialysis_type,
                dialyzer_id=dialyzer,
                dialysate_temp=dialysate_temp,
                k_meql=k_meql,
                ca_meal=ca_meal,
                mg_meal=mg_meal,
                glucose=glucose,
                target_bvp=target_bvp,
                dialysate_flow=dialysate_flow,
                profile1=profile1,
                blood_flow=blood_flow,
                profile2=profile2,
                bicarb=bicarb,
                profile3=profile3,
                na_meql=na_meql,
                profile4=profile4,
                uf_rate=uf_rate,
                ufr_profile=ufr_profile,
                heparin_type_id=heparin_type,
                initial_dose=initial_dose,
                interim_dose=interim_dose,
                total_heparin_bolus=total_heparin_bolus,
                hourly=hourly,
                cut_off_time=cut_off_time,
                heparin_profile=heparin_profile,
                comments=comments,
                notes=notes,
                created_by_id=request.user.id, location_id=request.location,
            )
            data.save()
            update_status=PatientVisitMains.objects.filter(uhid__exact=uhid,visit_id__exact=visit_id_new).last()
            update_status.claim_no='Prepared'
            update_status.save()
    context={
        'doctor_list':doctor_list,'access_type':access_type,'temporary_dat':temporary_dat,'permanent_dat':permanent_dat,'pk':pk,
        'uhid_pat_new': uhid_pat_new, 'visit_id_new': visit_id_new, 'pat_age_new': pat_age_new, 'pat_name_new': pat_name_new,
        'pat_con_no_new': pat_con_no_new,'pat_sex_new':pat_sex_new,'dialysate_type':dialysate_type,'dialyzer_type':dialyzer_type,
        'heparin_Type':heparin_Type,'prescription_records':prescription_records,'permanent_access_master':permanent_access_master,
        'dept_list':dept_list,'type_list':type_list,'shift_list':shift_list,
    }
    return render(request,'dialysis/prescription_dialysis.html',context)


#===================== FOR UPDATE PRESCRIPTION DETAILS =========================
def prescription_dialysis_update(request,pk):
    uhid_visit_ud = pk.split('-')
    uhid = uhid_visit_ud[0]
    visit_id_new = uhid_visit_ud[1]
    temporary_dat=Temp_Access.objects.filter(uhid=uhid)
    permanent_dat=Permanent_Access.objects.filter(uhid=uhid)
    prescription_records=PrescriptionDialysis.objects.filter(uhid=uhid).last()
    records = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid).last()
    uhid_pat_new = records.uhid
    pat_fname = records.first_name
    pat_mname = records.middle_name
    pat_lname = records.last_name
    pat_age_new = records.age
    pat_sex_new = records.gender
    pat_con_no_new = records.mobile_number
    pat_name_new = ''
    if pat_mname == None:
        pat_name_new = pat_fname + ' ' + pat_lname
    else:
        pat_name_new = pat_fname + ' ' + pat_mname + ' ' + pat_lname
    request.session['pat_uhid_new'] = uhid_pat_new
    request.session['pat_visit_new'] = visit_id_new
    request.session['pat_name_new'] = pat_name_new
    request.session['pat_age_new'] = pat_age_new
    request.session['pat_con_no_new'] = pat_con_no_new
    request.session['pat_sex_new'] = pat_sex_new
    doctor_list=DoctorTable.objects.all()
    access_type = Asset_type.objects.all()
    dialysate_type = Dialysate_Type.objects.all()
    dialyzer_type = Dialyzer.objects.all()
    heparin_Type = Heparin_Type.objects.all()
    permanent_access_master = Permanent_Access_Master.objects.all()
    temp_access=request.POST.get('temp_access')
    Permanent_access=request.POST.get('Permanent_access')
    main_form=request.POST.get('main_form')
    if temp_access == 'TEMP_ACCESS':
        if request.method=='POST':
            temp_ac=request.POST.get('temp_ac')
            date_of_initiation=request.POST.get('date_of_initiation')
            dr_name=request.POST.get('dr_name')
            access_type=request.POST.get('access_type')
            date_of_removal=request.POST.get('date_of_removal')
            Remark=request.POST.get('Remark')
            hospital_name=request.POST.get('hospital_name')
            dat=Temp_Access(
                uhid=uhid,
                visit_id =visit_id_new,
                temp_aces =temp_ac,
                date_initiation=date_of_initiation,
                doctor_name =dr_name,
                access_site =access_type,
                date_removal =date_of_removal,
                remark =Remark,
                hospital_name=hospital_name,
            )
            dat.save()
    elif Permanent_access == 'Permanent_Access':
        if request.method == 'POST':
            per_access = request.POST.get('per_access')
            date_of_initiation = request.POST.get('date_of_initiation')
            dr_name = request.POST.get('dr_name')
            access_type = request.POST.get('access_type')
            date_of_removal = request.POST.get('date_of_removal')
            Remark = request.POST.get('Remark')
            hospital_name = request.POST.get('hospital_name')
            dat = Permanent_Access(
                uhid=uhid,
                visit_id=visit_id_new,
                prim_aces=per_access,
                date_initiation=date_of_initiation,
                doctor_name=dr_name,
                access_site=access_type,
                date_failure=date_of_removal,
                remark=Remark,
                hospital_name=hospital_name,
            )
            dat.save()
    elif main_form == 'MAIN_FORM':
        if request.method=='POST':
            dr_name = request.POST.get('dr_nameid')
            prescription_date =request.POST.get('prescription_date')
            status = request.POST.get('status')
            s_date = request.POST.get('s_date')
            e_date = request.POST.get('e_date')
            dry_weight = request.POST.get('dry_weight')
            dry_weight_date = request.POST.get('dry_date')
            diagnosis = request.POST.get('Diagnosis')
            day1 = request.POST.get('day1')
            shift1 = request.POST.get('shift1')
            Duration = request.POST.get('Duration')
            day2 = request.POST.get('day2')
            shift2 = request.POST.get('shift2')
            Weekly = request.POST.get('Weekly')
            day3 = request.POST.get('day3')
            shift3 =request.POST.get('shift3')
            dialysis_membrane =request.POST.get('dialysis_membrane')
            day4 = request.POST.get('day4')
            shift4 = request.POST.get('shift4')
            day5 = request.POST.get('day5')
            shift5 = request.POST.get('shift5')
            dialysis_type = request.POST.get('Dialysis_type')
            dialyzer = request.POST.get('Dialyzer')
            dialysate_temp = request.POST.get('Dialysate_temp')
            k_meql = request.POST.get('k_pluse')
            ca_meal = request.POST.get('ca_pluse')
            mg_meal = request.POST.get('mg_pluse')
            glucose = request.POST.get('glucose')
            target_bvp = request.POST.get('Target')
            #======================================
            dialysate_flow = request.POST.get('dialysis_flow')
            profile1 = request.POST.get('Profile1')
            blood_flow = request.POST.get('blood_flow')
            profile2 = request.POST.get('Profile2')
            bicarb = request.POST.get('Bicarb')
            profile3 = request.POST.get('Profile3')
            na_meql = request.POST.get('na_id')
            profile4 = request.POST.get('Profile5')
            uf_rate = request.POST.get('uf_rate')
            ufr_profile = request.POST.get('ufr_profile')
            heparin_type = request.POST.get('heparine_type')
            initial_dose = request.POST.get('initial_dose')
            interim_dose = request.POST.get('interim_dose')
            total_heparin_bolus = request.POST.get('total_heparin')
            hourly = request.POST.get('hourly')
            cut_off_time = request.POST.get('cutoff_time')
            heparin_profile = request.POST.get('heparin_profile')
            comments = request.POST.get('Comment')
            notes = request.POST.get('Notes')
            update_records=PrescriptionDialysis.objects.filter(uhid=uhid).last()
            # dr_id=update_records.drid
            update_records.uhid=uhid
            update_records.visit_id=visit_id_new
            update_records.dr_name=dr_name
            # update_records.drid=dr_id
            update_records.prescription_date=prescription_date
            update_records.status=status
            update_records.s_date=s_date
            update_records.e_date=e_date
            update_records.dry_weight=dry_weight
            update_records.dry_weight_date=dry_weight_date
            update_records.diagnosis=diagnosis
            update_records.day1=day1
            update_records.shift1=shift1
            update_records.duration=Duration
            update_records.day2=day2
            update_records.shift2=shift2
            update_records.weekly=Weekly
            update_records.day3=day3
            update_records.shift3=shift3
            update_records.dialysis_membrane=dialysis_membrane
            update_records.day4=day4
            update_records.shift4 =shift4
            update_records.day5=day5
            update_records.shift5=shift5
            update_records.dialysate_temp=dialysate_temp
            update_records.k_meql=k_meql
            update_records.ca_meal=ca_meal
            update_records.mg_meal=mg_meal
            update_records.glucose=glucose
            update_records.target_bvp=target_bvp
            update_records.dialysate_flow=dialysate_flow
            update_records.profile1=profile1
            update_records.blood_flow=blood_flow
            update_records.profile2=profile2
            update_records.bicarb=bicarb
            update_records.profile3=profile3
            update_records.na_meql=na_meql
            update_records.profile4=profile4
            update_records.uf_rate=uf_rate
            update_records.ufr_profile=ufr_profile
            update_records.initial_dose=initial_dose
            update_records.interim_dose=interim_dose
            update_records.total_heparin_bolus=total_heparin_bolus
            update_records.hourly=hourly
            update_records.cut_off_time=cut_off_time
            update_records.heparin_profile=heparin_profile
            update_records.comments=comments
            update_records.notes=notes
            update_records.save()
    context={
        'doctor_list':doctor_list,'access_type':access_type,'temporary_dat':temporary_dat,'permanent_dat':permanent_dat,
        'uhid_pat_new': uhid_pat_new, 'visit_id_new': visit_id_new, 'pat_age_new': pat_age_new, 'pat_name_new': pat_name_new,
        'pat_con_no_new': pat_con_no_new,'pat_sex_new':pat_sex_new,'dialysate_type':dialysate_type,'dialyzer_type':dialyzer_type,
        'heparin_Type':heparin_Type,'prescription_records':prescription_records,'permanent_access_master':permanent_access_master,
        'pk':pk,
    }
    return render(request,'dialysis/prescription_dialysis_update.html',context)

def temp_access_delete(request):
    records = Temp_Access.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse(data='Data Deleted Successfully',safe=False)
def perm_access_delete(request):
    records = Permanent_Access.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse(data='Data Deleted Successfully',safe=False)

#================================= END ============================================
def temp_access(request):
    uhid_new= request.session['pat_uhid_new']
    visit_new=request.session['pat_visit_new']
    pat_new=request.session['pat_name_new']
    pat_new_age=request.session['pat_age_new']
    pat__new_con_no_new=request.session['pat_con_no_new']
    pat_gender=request.session['pat_sex_new']
    if request.method=='POST':
        temp_access=request.POST.get('temp_access')
        date_of_initiation=request.POST.get('date_of_initiation')
        dr_name=request.POST.get('dr_name')
        access_type=request.POST.get('access_type')
        date_of_removal=request.POST.get('date_of_removal')
        Remark=request.POST.get('Remark')
        hospital_name=request.POST.get('hospital_name')
        dat=Temp_Access(
            uhid=uhid_new,
            visit_id =visit_new,
            temp_aces =temp_access,
            date_initiation=date_of_initiation,
            doctor_name =dr_name,
            access_site =access_type,
            date_removal =date_of_removal,
            remark =Remark,
            hospital_name=hospital_name,
        )
        dat.save
        print('data saved in table-----')
    return render(request,'dialysis/prescription_dialysis.html')

#===================== INTRA dialysis ==============================
def intradialysisperhourinput(request):
    intra_per_input=IntraDialysisPerHourInput.objects.all()
    form=IntraDialysisPerHourInputForm()
    add='add'
    if request.method=='POST':
        form=IntraDialysisPerHourInputForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/')
    context={
    'add':add,'form':form,"permanent_access_master":permanent_access_master
    }
    return render(request,"general_master/dialysis_master/permanent_access_master.html",context)

def edit_intradialysisperhourinput(request,pk):
    permanent_access_master=Permanent_Access_Master.objects.get(id=pk)
    form=Permanent_Access_MasterForm(instance=permanent_access_master)
    if request.method=='POST':
        form=Permanent_Access_MasterForm(request.POST,instance=permanent_access_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/permanent_access_master')
    context = {
        "form":form
    }
    return render(request,"general_master/dialysis_master/edit_permanent_access_master.html",context)

def prescription_dialysis_update1(request,pk):
    uhid_visit_ud = pk.split('-')
    uhid = uhid_visit_ud[0]
    visit_id_new = uhid_visit_ud[1]
    records = PrescriptionDialysis.objects.get(uhid=uhid)
    form=PrescriptionDialysisForm(instance=records)
    if request.method=="POST":
        form=PrescriptionDialysisForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
            return redirect('prescription_dialysis')
    context={
       'form':form
    }
    return render(request,'dialysis/prescription_dialysis_update1.html',context)

def refered_bymaster(request):
    refered_bymaster=Refered_by_Master.objects.all()
    form=Refered_by_MasterForm()
    add='add'
    if request.method=='POST':
        form=Refered_by_MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/refered_bymaster')
    context={
    'add':add,'form':form,"refered_bymaster":refered_bymaster
    }
    return render(request,"general_master/refered_by_master.html",context)

def edit_refered_bymaster(request,pk):
    refered_bymaster=Refered_by_Master.objects.get(id=pk)
    form=Refered_by_MasterForm(instance=refered_bymaster)
    if request.method=='POST':
        form=Refered_by_MasterForm(request.POST,instance=refered_bymaster)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/refered_bymaster')
    context = {
        "form":form
    }
    return render(request,"general_master/edit_referedbymaster.html",context)




# ============ opd print  ==============
def opd_print_view(request):
    cop_master=BillingGroup.objects.get(billing_group__icontains='Cash')
    credit=Credit.objects.all()
    bill=OpdBillingMain.objects.filter(billing_group_id=str(cop_master.id))
    ids=[data.bill_no for data in bill]
    for data in credit:
        ids.append(data.bill_no)
    records=OpdBillingMain.objects.extra(select={
        'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
    }).filter(location=request.location,bill_no__in=ids).order_by('-updated_at')
    context={
        'records':records,'cop_master':str(cop_master.id)
    }
    return render(request,'clinical/opd_bill/opd_print_view.html',context)

def opd_print_credit(request,pk):
    credit=Credit.objects.filter(bill_no=pk).first()
    if credit:
        pay_m_uhid=credit.uhid
        pay_m_visit_id=credit.visit_no
        patient_detail=PatientsRegistrationsAllInOne.objects.get(uhid=pay_m_uhid)
        bill_detail=OpdBillingMain.objects.get(bill_no=pk)
        title=patient_detail.title
        first_name=patient_detail.first_name
        middle_name=patient_detail.middle_name
        last_name=patient_detail.last_name
        address=patient_detail.address
        if middle_name == None:
            patinet_name = title + ' ' + first_name + ' ' + last_name
        else:
            patinet_name=title+' '+first_name+' '+middle_name+' '+last_name
        billing_groups=BillingGroup.objects.get(id=bill_detail.billing_group_id)
        if bill_detail.corporate_id == 'Cash':
            sponsors='Cash'
        else:
            sponsors=CorporateMaster.objects.get(id=bill_detail.corporate_id)
        list_d=['Walked By','AAA ','BBB']
        if patient_detail.referred_by in list_d:
            reffered_by = 'Walked By'
            print('reffered_by----,',reffered_by)
        else:
            reffered_bys = Refered_by_Master.objects.get(id=patient_detail.referred_by)
            reffered_by=reffered_bys.Staff_name
        pay_m_visit_id = pay_m_visit_id
        visit_detail=PatientVisitMains.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_id=pay_m_visit_id))
        temp_record = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_no=pay_m_visit_id,bill_no=pk)).last()
        ser_name=OpdBillingSub.objects.filter(uhid=pay_m_uhid,visit_no=pay_m_visit_id,bill_no=pk)
        inv_name=[data.service_category for data in ser_name]
        ins_records = ServiceCategory.objects.filter(service_category__in=inv_name).order_by('id')
        ttl_amt = OpdBillingSub.objects.filter(uhid=pay_m_uhid,visit_no=pay_m_visit_id,bill_no=pk,service_category__in=inv_name).aggregate(Sum('paid_amount'))
        ttl_amt = ttl_amt['paid_amount__sum']

        temp_reco = OpdBillingMain.objects.filter(bill_no__exact=pk).last()
        exact_bill_no=temp_reco.bill_no
        temp_records = OpdBillingSub.objects.filter(bill_no=pk)
        #=================== Here To calculate sub total in invoice =======================
        sub_list=[]
        for inv in ins_records:
            ttl_amt = OpdBillingSub.objects.filter(bill_no=pk,service_category=inv.service_category).aggregate(Sum('charges'))
            net_amount = ttl_amt['charges__sum']
            sub_list.append(net_amount)
        #============================ Here total Amount  ==============================
        # net_amount = OpdBillingMain.objects.filter(bill_no=pk).aggregate(Sum('paid_amount'))
        # print('net_amount',net_amount)
        # net_amount = net_amount['paid_amount__sum']
        # print('net_amount',net_amount)
        net_amount = OpdBillingSub.objects.filter(bill_no=pk).aggregate(Sum('charges'))
        net_amount = net_amount['charges__sum']
        net_amount_main = OpdBillingMain.objects.filter(bill_no__exact=pk).aggregate(Sum('paid_amount'))
        net_amount_main = net_amount_main['paid_amount__sum']
        net_disc_main = OpdBillingMain.objects.filter(bill_no__exact=pk).aggregate(Sum('discount'))
        net_disc_main = net_disc_main['discount__sum']
        # ================= Seprate Pharmacy Bill No. for see pharmacy invoice =================================================
        temp_recordss = OpdBillingSub.objects.filter(bill_no=pk, service_id__startswith='Pharmacy Sales Bill').last()
        if temp_recordss:
            ph_bill_seprate = temp_recordss.service_id.split(' ')
            ph_bill = ph_bill_seprate[3]
        else:
            ph_bill = ''
        #================= END =================================================
        for visit_detail in visit_detail:
            visit_date_time = visit_detail.visit_date_time
        all_data=zip(ins_records,sub_list)
        context = {
            'patinet_name':patinet_name,'address':address,'visit_detail':visit_detail,
            'patient_detail':patient_detail,"temp_record":temp_record,'net_amount':net_amount,
            'temp_records':temp_records,'billing_groups':billing_groups,'sponsors':sponsors,'all_data':all_data,
            'reffered_by':reffered_by,'back_btn':'back_btn','temp_recordss':temp_recordss,'ph_bill':ph_bill,
        }
        return render(request, 'clinical/opd_billiing_receipt_insurance.html', context)
    else:
        return redirect('opd_print_view')


def opd_print_cash(request,pk):
    tatol_package_amt=0
    opd_main = OpdBillingMain.objects.filter(bill_no=pk).first()
    patient_detail=PatientsRegistrationsAllInOne.objects.get(uhid=opd_main.uhid)
    bill_detail = OpdBillingMain.objects.get(bill_no=pk)
    title=patient_detail.title
    first_name=patient_detail.first_name
    middle_name=patient_detail.middle_name
    last_name=patient_detail.last_name
    mobile_number=patient_detail.mobile_number
    address=patient_detail.address
    if middle_name== None:
        patinet_name = title + ' ' + first_name + ' ' + last_name
    else:
        patinet_name = title + ' ' + first_name + ' ' + middle_name + ' ' + last_name
    billing_groups = BillingGroup.objects.get(id=bill_detail.billing_group_id)
    if bill_detail.corporate_id == 'Cash':
        sponsors = 'Self'
    else:
        sponsorss = CorporateMaster.objects.get(id=bill_detail.corporate_id)
        sponsors=sponsorss.corporate_Name
    list_d=['Walked By','AAA ','BBB']
    if patient_detail.referred_by in list_d:
        reffered_by = 'Walked By'
        print('reffered_by----,',reffered_by)
    else:
        reffered_bys = Refered_by_Master.objects.get(id=patient_detail.referred_by)
        reffered_by=reffered_bys.Staff_name
    #========Card no some field *****1234 like this ===============
    pay_m_uhid = opd_main.uhid
    pay_m_visit_id = opd_main.visit_no
    pay_m_bill_nos = pk
    default_unit=2
    default_discount=10.0
    payment_details=OpdPayment.objects.filter(uhid=pay_m_uhid,bill_id=pay_m_bill_nos,visit_id=pay_m_visit_id)
    print('payment_details---------------------->,',payment_details)
    visit_detail=PatientVisitMains.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_id=pay_m_visit_id))
    temp_record = OpdBillingMain.objects.filter(Q(uhid=pay_m_uhid)&Q(visit_no=pay_m_visit_id)).last()
    ser_name = OpdBillingSub.objects.filter(uhid=pay_m_uhid, visit_no=pay_m_visit_id, bill_no=pay_m_bill_nos)
    inv_name = [data.service_category for data in ser_name]
    print('inv_name------>,',inv_name,ser_name)
    ins_records = ServiceCategory.objects.filter(service_category__in=inv_name).order_by('id')
    ttl_amt = OpdBillingSub.objects.filter(uhid=pay_m_uhid, visit_no=pay_m_visit_id, bill_no=pay_m_bill_nos,
                                            service_category__in=inv_name).aggregate(Sum('paid_amount'))
    ttl_amt = ttl_amt['paid_amount__sum']
    temp_reco = OpdBillingMain.objects.filter(bill_no__exact=pk).last()
    exact_bill_no=temp_reco.bill_no
    temp_records = OpdBillingSub.objects.filter(bill_no=pk)
    print('temp_records---->',temp_records)
    # =================== Here To calculate sub total in invoice =======================
    sub_list = []
    for inv in ins_records:
        ttl_amt = OpdBillingSub.objects.filter(bill_no=pk,
                                                service_category=inv.service_category).aggregate(Sum('charges'))
        net_amount = ttl_amt['charges__sum']
        sub_list.append(net_amount)
    # ============================ Here total Amount  ==============================
    net_amount = OpdBillingSub.objects.filter(bill_no=pk).aggregate(Sum('charges'))
    net_amount = net_amount['charges__sum']

    net_amount_main = OpdBillingMain.objects.filter(bill_no=pk).aggregate(Sum('paid_amount'))
    net_amount_main = net_amount_main['paid_amount__sum']
    #============================= Here Total Discount ==============================
    net_disc = OpdBillingSub.objects.filter(bill_no=pk).aggregate(Sum('discount'))
    net_disc = net_disc['discount__sum']
    print('net_disc----->,',net_disc)
    #============================= Here Total Discount Main Table ======================
    net_disc_main = OpdBillingMain.objects.filter(bill_no=pk).aggregate(Sum('discount'))
    net_disc_main = net_disc_main['discount__sum']
    print('net_disc_main----->,',net_disc_main)
    # ================= END =================================================
    for visit_detail in visit_detail:
        visit_date_time = visit_detail.visit_date_time
    print('===....',ins_records, sub_list)
    all_data = zip(ins_records, sub_list)

    context = {
        'pay_m_visit_id': pay_m_visit_id,'pay_m_uhid':pay_m_uhid,'bill_no':pk,
        'patinet_name':patinet_name,'mobile_number':mobile_number,'address':address,'visit_detail':visit_detail,
        'default_unit':default_unit,'default_discount':default_discount,'patient_detail':patient_detail,'all_data':all_data,
        'temp_records':temp_records,'temp_record':temp_record,
        'net_amount':net_amount,'net_disc_main':net_disc_main,'net_amount_main':net_amount_main,
        'tatol_package_amt':tatol_package_amt,
        'billing_groups':billing_groups,'payment_details':payment_details,'reffered_by':reffered_by,
        'sponsors':sponsors,'back_btn':'back_btn'
    }
    # return render(request, 'clinical/opdbillrecipte.html', context)
    return render(request, 'clinical/opd_billing_receipt_cash.html', context)


def opd_temp_delete(request):
    records = OpdBillingTemper.objects.get(id=request.POST.get('id'))
    patient=PatientsRegistrationsAllInOne.objects.get(uhid=records.uhid)
    if patient.billing_group != "1":
        package_records=OpdPackageService_main.objects.filter(package_name__package_name__exact=records.service_name)
        if records.service_sub_category.service_sub_category == 'Lab Investigation':
            if records.order_id:
                bill_number=records.order_id
            else:
                bill_number=records.temp_bill_no
            pen_records=PendingInvestigation_main.objects.filter(bill_no=bill_number,profile_name=records.service_name).last()
            if pen_records:
                pen_records.delete()
                records.delete()
        elif package_records:
            pass
        else:
            records.delete()
    else:
        records.delete()
    return JsonResponse(data='Data Deleted Successfully',safe=False)

def relation_nhif(request):
    refered_bymaster=Relation.objects.all()
    form=RelationForm()
    add='add'
    if request.method=='POST':
        form=RelationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/relation_nhif')
    context={
    'add':add,'form':form,"refered_bymaster":refered_bymaster
    }
    return render(request,"general_master/relation_nhif.html",context)

def edit_relation_nhif(request,pk):
    refered_bymaster=Relation.objects.get(id=pk)
    form=RelationForm(instance=refered_bymaster)
    if request.method=='POST':
        form=RelationForm(request.POST,instance=refered_bymaster)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/relation_nhif')
    context = {
        "form":form
    }
    return render(request,"general_master/edit_relation_nhif.html",context)


def user_collection_summary(request):
    context={}
    if request.method=='POST':
        s_date=request.POST.get('b_start_date')
        e_date=request.POST.get('b_end_date')
        records = OpdPayment.objects.extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
            'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
            'disc': 'Select discount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
            'payable': 'Select pay_amount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
        }).filter(date_time__range=[s_date,e_date],location=request.location).order_by('created_by').exclude(status='cancel')
        records2 = Insurance_Payement_Detail.objects.extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
            'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_Insurance_Payement_Detail.uhid',
            'disc': 'Select discount from testapp_opdbillingmain where uhid=testapp_Insurance_Payement_Detail.uhid',
            'payable': 'Select pay_amount from testapp_opdbillingmain where uhid=testapp_Insurance_Payement_Detail.uhid',
        }).filter(date_time__range=[s_date,e_date],location_id=request.location).order_by('-id')
        #mode_types=['cash','debit_credit_card','m_pesa','bank','eft','cheque',]
        mode_type=[data.mode_type for data in records]
        mode_types=set(mode_type)
        print('datacreated_by for data in records2',mode_types)
        userr_ins=[data.created_by for data in records2]
        users_ins=set(userr_ins)
        user_table_ins=CreateUser.objects.filter(user_id__in=users_ins)
        ttl_amt_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],location_id=request.location).aggregate(
            Sum('net_amount'))
        ttl_amt_ins = ttl_amt_ins['net_amount__sum']
        rcv_amt_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],location_id=request.location).aggregate(
            Sum('paid_amount'))
        paid_amt_ins = rcv_amt_ins['paid_amount__sum']
        #-================================= Here TO start cash Patient calculation ==================================
        userr=[data.created_by for data in records]
        print('userr00---------->,',userr)
        users=set(userr)
        user_table=CreateUser.objects.filter(user_id__in=users)
        datas_records=[data.f_name for data in user_table]
        print('datas_records users name----->,',datas_records)
        ttl_amt = OpdPayment.objects.filter(date_time__range=[s_date,e_date],location=request.location).exclude(status='cancel').aggregate(
            Sum('net_amount'))
        ttl_net = ttl_amt['net_amount__sum']
        rcv_amt = OpdPayment.objects.filter(date_time__range=[s_date,e_date],location=request.location).exclude(status='cancel').aggregate(
            Sum('paid_amount'))
        paid_amt_cash = rcv_amt['paid_amount__sum']
        print('paid_amt_cash-------------->>>>>>>>>>>,,,',paid_amt_cash)
        #======================================== Here Both insurance and cash total calculation ========================
        if paid_amt_cash is None:
            paid_amt_cash=0
        if paid_amt_ins is None:
            paid_amt_ins=0
        paid_amt=paid_amt_cash+paid_amt_ins
        print(' GRAND total',paid_amt)
        #================= for user wise and payment modes wise total calculation ==========================
        list_cash=[]
        list_debit=[]
        list_eft=[]
        list_m_pesa=[]
        list_sum_total=[]
        list_bank=[]
        list_cheque=[]
        sum_total_all=0
        sub_total_summary=0
        sub_total_summary_debit=0
        sub_total_summary_m_pesa=0
        sub_total_summary_bank=0
        sub_total_summary_eft=0
        sub_total_summary_cheque=0
        sub_total_summary_cash_list=[]
        sub_total_summary_debit_list=[]
        sub_total_summary_m_pesa_list=[]
        sub_total_summary_bank_list=[]
        sub_total_summary_eft_list=[]
        sub_total_summary_cheque_list=[]
        total_summary_list=[]
        grand_total_summary_list=[]
        for user in user_table:
            cashs = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='cash',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            cash_cash = cashs['paid_amount__sum']
            cashs_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='cash', created_by=user.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            cash_ins = cashs_ins['paid_amount__sum']
            if cash_cash is None:
                cash_cash = 0
            if cash_ins is None:
                cash_ins = 0
            cash=cash_cash+cash_ins
            sub_total_summary=sub_total_summary+cash
            list_cash.append(cash)
            debits_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='debit_credit_card',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            debit_cash = debits_cash['paid_amount__sum']
            debits_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='debit_credit_card', created_by=user.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            debit_ins = debits_ins['paid_amount__sum']
            if debit_cash is None:
                debit_cash = 0
            if debit_ins is None:
                debit_ins = 0
            debit=debit_cash+debit_ins
            sub_total_summary_debit=sub_total_summary_debit+debit
            list_debit.append(debit)
            efts_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='eft',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            eft_cash = efts_cash['paid_amount__sum']
            efts__ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='eft', created_by=user.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            eft__ins = efts__ins['paid_amount__sum']
            if eft_cash is None:
                eft_cash = 0
            if eft__ins is None:
                eft__ins = 0
            eft=eft_cash+eft__ins
            sub_total_summary_eft=sub_total_summary_eft+eft
            list_eft.append(eft)
            m_pesas_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='m_pesa',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            m_pesa_cash = m_pesas_cash['paid_amount__sum']
            m_pesas_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='m_pesa', created_by=user.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            m_pesa_ins = m_pesas_ins['paid_amount__sum']
            if m_pesa_cash is None:
                m_pesa_cash = 0
            if m_pesa_ins is None:
                m_pesa_ins = 0
            m_pesa=m_pesa_cash+m_pesa_ins
            sub_total_summary_m_pesa=sub_total_summary_m_pesa+m_pesa
            list_m_pesa.append(m_pesa)
            banks_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='bank',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            bank_cash = banks_cash['paid_amount__sum']
            banks_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='bank', created_by=user.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            bank_ins = banks_ins['paid_amount__sum']
            if bank_cash is None:
                bank_cash = 0
            if bank_ins is None:
                bank_ins = 0
            bank=bank_cash+bank_ins
            sub_total_summary_bank=sub_total_summary_bank+bank
            list_bank.append(bank)
            cheques_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='cheque',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            cheque_cash = cheques_cash['paid_amount__sum']
            cheques_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='cheque', created_by=user.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            cheque_ins = cheques_ins['paid_amount__sum']
            if cheque_cash is None:
                cheque_cash = 0
            if cheque_ins is None:
                cheque_ins = 0
            cheque=cheque_cash+cheque_ins
            sub_total_summary_cheque=sub_total_summary_cheque+cheque
            list_cheque.append(cheque)
            if cash is None:
                cash = 0
            if debit is None :
                debit = 0
            if eft is None:
                eft = 0
            if m_pesa is None :
                m_pesa = 0
            if bank is None:
                bank = 0
            if cheque is None:
                cheque = 0
            sum_total=cash+debit+eft+m_pesa+bank+cheque
            list_sum_total.append(sum_total)
            sum_total_all=sum_total_all+sum_total
        sub_total_summary_cash_list.append(sub_total_summary)
        sub_total_summary_debit_list.append(sub_total_summary_debit)
        sub_total_summary_eft_list.append(sub_total_summary_eft)
        sub_total_summary_m_pesa_list.append(sub_total_summary_m_pesa)
        sub_total_summary_bank_list.append(sub_total_summary_bank)
        sub_total_summary_cheque_list.append(sub_total_summary_cheque)
        total_summary_list.append(sum_total_all)
        grand_total_summary_list.append(sum_total_all)
        print('---sub_total_summary_cash_list-----,',sub_total_summary_cash_list)
        user_summary=zip(user_table,list_cash,list_debit,list_eft,list_m_pesa,list_bank,list_cheque,list_sum_total)
        #======================================= End ==================================================
        mode_wise_total=[]
        mode_list=[]
        for users in user_table:
            for mode_sub in mode_types:
                sub_total_mode = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type=mode_sub,created_by=users.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                total_mode_wise = sub_total_mode['paid_amount__sum']
                mode_wise_total.append(total_mode_wise)
                mode_list.append(mode_sub)
                # print('mode_sub--->',mode_sub)
        payment_sub_total = zip(mode_list, mode_wise_total)
        #==================================== Here For user wise sum total =============================================
        sub_total_list=[]
        sub_total_both=0
        grand_total=0
        for sub in user_table:
            sub_total_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],created_by=sub.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            sub_total_cash = sub_total_cash['paid_amount__sum']
            sub_total_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],created_by=sub.login_id.id,location_id=request.location).aggregate(
                Sum('paid_amount'))
            sub_total_ins = sub_total_ins['paid_amount__sum']
            print('sub_total_ins--------,',sub_total_ins)
            if sub_total_cash is None:
                sub_total_cash = 0
            if sub_total_ins is None:
                sub_total_ins = 0
            sub_total_both=sub_total_cash+sub_total_ins
            grand_total=grand_total+sub_total_both
            print('grand_total------->',grand_total)
            sub_total_list.append(sub_total_both)
            print('sub_total_list---,',sub_total_list)
        #=================================== END =================================
        all_rec=zip(user_table,sub_total_list)
        context={
          'records':records,'ttl_net':ttl_net,'paid_amt':grand_total,'mode_types':mode_types,'users':users,'all_rec':all_rec,
            'user_table':user_table,'user_summary':user_summary,'payment_sub_total':payment_sub_total,'records2':records2,
            'sub_total_summary_cash_list':sub_total_summary,'sub_total_summary_debit_list':sub_total_summary_debit,
            'sub_total_summary_m_pesa_list':sub_total_summary_m_pesa,'sub_total_summary_bank_list':sub_total_summary_bank,
            'sub_total_summary_eft_list':sub_total_summary_eft,'sub_total_summary_cheque_list':sub_total_summary_cheque,
            'total_summary_list':sum_total_all,'grand_total_summary_list':sum_total_all,
        }
    return render(request,'Reports/user_collection_summary.html',context)


def out_sourse_service(request):
    try:
        collected_records=SampleCollected.objects.filter(status__in=['waiting','completed'],location=request.location,outsource=True)
        contex={
            'collected_records':collected_records
        }
        return render(request,'lab_module/out_sourse_service.html',contex)
    except Exception as error:
        return render(request,'error.html',{'error':error})

# ================== for POST Dialysis Discharge Summery 09/05/2023==========================================
@login_required(login_url='/user_login')
def post_dialysis_discharge(request,uhid_visit):
    uh_visit_idds = uhid_visit.split('-')
    uhid_id = uh_visit_idds[0]
    visit_id_id = uh_visit_idds[1]
    print('visit_id',visit_id_id)
    print('uhid',uhid_id)
    records = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid_id).last()
    discharge_reco=PostDialysisDischargeSheet.objects.filter(uhid=uhid_id,visit_id=visit_id_id).last()
    uhid_pat = records.uhid
    pat_fname = records.first_name
    pat_mname = records.middle_name
    pat_lname = records.last_name
    pat_age = records.age
    pat_sex = records.gender
    # pat_con_no = records.mobile_number
    pat_name = ''
    if pat_mname == None:
        pat_name = pat_fname + ' ' + pat_lname
    else:
        pat_name = pat_fname + ' ' + pat_mname + ' ' + pat_lname
    records=PostDialysisDischargeSheet.objects.filter(uhid=uhid_id,visit_id=visit_id_id)
    medicinelist=Inventory_ItemMaster.objects.filter(assets='0')
    medicine=request.POST.get('medicine')
    print('medicine---,',medicine)
    prescription_dia=request.POST.get('prescription_dialysis')
    print('prescription_dia---,', prescription_dia)
    post_medicine=request.POST.get('post_medicine')
    main_form=request.POST.get('main_form')
    print('main_form---,', main_form)
    print('post_medicine---,', post_medicine)
    if request.method=='POST':
        cause = request.POST.get('cause')
        dod = request.POST.get('dod')
        coe_com = request.POST.get('coe_com')
        duration = request.POST.get('duration')
        access = request.POST.get('access')
        status = request.POST.get('status')
        medicines = request.POST.get('medicines')
        dosage = request.POST.get('dosage')
        dialysis1 = request.POST.get('dialysis1')
        dialysis2 = request.POST.get('dialysis2')
        medicine_post_dialysis = request.POST.get('medicine_post_dialysis')
        outs_ource_med_name = request.POST.get('outs_ource_med_name')
        bp = request.POST.get('bp')
        kt_v = request.POST.get('kt_v')
        acc_qb = request.POST.get('acc_qb')
        out_come = request.POST.get('out_come')
        recommendation = request.POST.get('recommendation')
        tca = request.POST.get('tca')
        nephrologist = request.POST.get('nephrologist')
        image = request.FILES.get('imagee')
        print('image---,',image)
        # print('nephrologist---,',nephrologist)
        if main_form == 'MAIN_form':
            main_data=PostDialysisDischargeSheet(
                uhid=uhid_id,
                visit_id=visit_id_id,
                cause_ESRD=cause,
                d_of_d=dod,
                cc=coe_com,
                access=access,
                status=status,
                duration=duration,
                bp=bp,
                kt_v=kt_v,
                acc_qb=acc_qb,
                out_come=out_come,
                recommendant=recommendation,
                tca=tca,
                nephrologist=nephrologist,
                created_by_id=request.user.id,
                location_id=request.location,
            )
            main_data.save()
            update_status = PatientVisitMains.objects.filter(uhid__exact=uhid_id, visit_id__exact=visit_id_id).last()
            if update_status:
                if update_status.claim_no == 'Closed':
                    update_status.claim_no = 'discharged'
                    update_status.save()
            else:
                dialysis_admission = AdmissionStatus.objects.filter(uhid=uhid_id, admission_ID=visit_id_id).last()
                dialysis_admission.status = 'discharged'
                dialysis_admission.save()
            return HttpResponseRedirect(f'/post_dialysis_discharge/{uhid_visit}')
        if main_form == 'UPDATE_form':
            update_data = PostDialysisDischargeSheet.objects.filter(uhid=uhid_id,visit_id=visit_id_id).last()
            update_data.uhid=uhid_id
            update_data.visit_id=visit_id_id
            update_data.cause_ESRD=cause
            update_data.d_of_d=dod
            update_data.cc=coe_com
            update_data.access=access
            update_data.status=status
            update_data.duration=duration
            update_data.bp=bp
            update_data.kt_v=kt_v
            update_data.acc_qb=acc_qb
            update_data.out_come=out_come
            update_data.recommendant=recommendation
            update_data.tca=tca
            update_data.nephrologist=nephrologist
            update_data.save()
            return HttpResponseRedirect(f'/post_dialysis_discharge/{uhid_visit}')
        elif medicine == 'MEDICINE':
            records1 = PostDialysisDischargeSheet.objects.filter(uhid=uhid_id, visit_id=visit_id_id).last()
            ids=records1.id
            print('ids===--,',ids)
            medi=DialysisDishchargeMedicine(main_id_id=ids,med_name=medicines,dosage=dosage)
            medi.save()
            print('main_data------,', medi)
        elif prescription_dia == 'prescription_dialysis':
            records1 = PostDialysisDischargeSheet.objects.filter(uhid=uhid_id, visit_id=visit_id_id).last()
            ids=records1.id
            print('ids===--,',ids)
            dialysis_presc=DialysisPrescription(main_id_id=ids,namw1=dialysis1,name2=dialysis2)
            dialysis_presc.save()
            print('main_data------,', dialysis_presc)
        elif post_medicine == 'POST_MEDICINE':
            records1 = PostDialysisDischargeSheet.objects.filter(uhid=uhid_id, visit_id=visit_id_id).last()
            ids=records1.id
            print('ids===--,',ids)
            post_med=PostDialysisDishchargeMedicine(main_id_id=ids,post_med_name_id=medicine_post_dialysis,outs_ource_med_name=outs_ource_med_name)
            post_med.save()
            print('post_med------,', post_med)
        else:
            print('this is else condition')
    else:
        print('This reqiest.medoth==post condition else ')
    records1 = PostDialysisDischargeSheet.objects.filter(uhid=uhid_id, visit_id=visit_id_id).last()
    print('records1---',records1)
    med_records=''
    presc_records=''
    post_med_records=''
    all_in=''
    if records1 != None:
        med_records = DialysisDishchargeMedicine.objects.filter(main_id=records1.id)
        presc_records = DialysisPrescription.objects.filter(main_id=records1.id)
        post_med_records = PostDialysisDishchargeMedicine.objects.filter(main_id=records1.id)
        print('med_records,',med_records)
        all_in=zip(presc_records,post_med_records)
    context={
        'medicinelist':medicinelist,'records':records,'med_records':med_records,'presc_records':presc_records,'post_med_records':post_med_records,'uhid_visit':uhid_visit,
        'all_in':all_in,'pat_name':pat_name,'pat_age':pat_age,'pat_sex':pat_sex,'uhid':uhid_id,'visit_id':visit_id_id,'discharge_reco':discharge_reco,
    }
    return render(request,'dialysis/post_dialysis_discharge.html',context)

def list_of_post_dialysis(request):
    records1 = Post_Dialysis_Details.objects.filter(location=request.location).order_by('-id').extra(select={
        'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
        'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
        'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
        'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
        'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
    })
    print(records1.count())
    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records1 =Post_Dialysis_Details.objects.filter(uhid__exact=uhid,location=request.location).extra(select={
                'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
                'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
                'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
                'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
                'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
                'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_Post_Dialysis_Details.uhid',
            })
            success_search = 'success'
            print('records1------,',records1)
            context = {
            'success_search': success_search,'discharge_list':discharge_list,'records1':records1,
            }
            return render(request, 'dialysis/list_new_dialysis_patient.html', context)
        except Exception as e:
            print('e----',e)
            pass
    context = {
        'records1': records1,
    }
    # post_records=Post_Dialysis_Details.objects.all()
    # context={
    #     'post_records':post_records,
    # }
    return render(request, 'dialysis/list_of_post_dialysis.html', context)


def dialysis_dishcharge_report(request,uhid_visit):
    uh_visit_idds = uhid_visit.split('-')
    uhid_id = uh_visit_idds[0]
    visit_id_id = uh_visit_idds[1]
    records = PatientsRegistrationsAllInOne.objects.filter(uhid=uhid_id).last()
    uhid_pat = records.uhid
    pat_fname = records.first_name
    pat_mname = records.middle_name
    pat_lname = records.last_name
    pat_age = records.age
    pat_sex = records.gender
    # pat_con_no = records.mobile_number
    pat_name = ''
    if pat_mname == None:
        pat_name = pat_fname + ' ' + pat_lname
    else:
        pat_name = pat_fname + ' ' + pat_mname + ' ' + pat_lname
    records1 = PostDialysisDischargeSheet.objects.filter(uhid=uhid_id,visit_id=visit_id_id).last()
    print('records1----->,',records1.nephrologist)
    med_records = ''
    presc_records = ''
    post_med_records = ''
    if records1 != None:
        med_records = DialysisDishchargeMedicine.objects.filter(main_id=records1.id)
        presc_records = DialysisPrescription.objects.filter(main_id=records1.id)
        post_med_records = PostDialysisDishchargeMedicine.objects.filter(main_id=records1.id)
    context={
        'records': records1, 'med_records': med_records, 'presc_records': presc_records,
        'post_med_records': post_med_records,'pat_name':pat_name,'pat_age':pat_age,'pat_sex':pat_sex,
    }
    return render(request, 'dialysis/dialysis_discharge_report.html',context)
#=============== For Clinical Mnagement Single report Patient Wise 12/05/2023===================================
def list_cl_patient(request):
    searching_uhid = request.GET.get('uhid')
    pat_name = request.GET.get('name')
    # total_p = VitalSign.objects.all().count()
    records=VitalSign.objects.extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
    }).order_by("-id").exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','open']))
    total_p=records.count()
    if searching_uhid:
        total_p = VitalSign.objects.filter(Q(uhid__exact=searching_uhid) | Q(bill_id__exact=searching_uhid)).count()
        records = VitalSign.objects.filter(Q(uhid__exact=searching_uhid)|Q(bill_id__exact=searching_uhid)).extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
    }).exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','open']))
    if pat_name:
        pat_record = PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=pat_name,
                                                                  location=request.location)
        list_uhid = [data.uhid for data in pat_record]
        records = VitalSign.objects.filter(uhid__in=list_uhid).extra(
            select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
            }).order_by("-id").exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','open']))
    context={
        'records':records,'total_p':total_p,
    }
    return render(request,'nurse_station/list_cl_patient.html',context)

def cl_patient_report(request,uhid_visit):
    uh_visit_idds = uhid_visit.split('~')
    print('uh_visit_idds------->,',uh_visit_idds)
    uhid_id = uh_visit_idds[0]
    visit_id_id = uh_visit_idds[1]
    pat_details=PatientVisitMains.objects.extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
    }).filter(uhid=uhid_id,visit_id=visit_id_id)
    ci_records=VitalSign.objects.extra(select={
        'pat_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_VitalSign.uhid',
    }).filter(uhid=uhid_id,visit_id=visit_id_id)
    records_medicine = PreMedicine.objects.filter(uhid=uhid_id, visit_id=visit_id_id)
    diagnosis_records = DiagnosisSub.objects.filter(uhid=uhid_id, visit_id=visit_id_id)
    complaints = PresentingComplaintSub.objects.filter(uhid=uhid_id, visit_id=visit_id_id)
    patient_allergy = PatientAllergy.objects.filter(uhid=uhid_id, visit_id=visit_id_id)
    advice = Advice.objects.filter(uhid=uhid_id,visit_id=visit_id_id)
    invest_and_proce_records = InvestigationProcedure.objects.filter(uhid=uhid_id, visit_id=visit_id_id)
    history_diagnosis = HistoryAndExamination.objects.filter(uhid=uhid_id, visit_id=visit_id_id)
    context={
        'ci_records':ci_records,'records_medicine':records_medicine,'invest_and_proce_records':invest_and_proce_records,'diagnosis_records':diagnosis_records,
        'pat_details':pat_details,'complaints':complaints,'history_diagnosis':history_diagnosis,'advice':advice,

    }
    return render(request,'nurse_station/cl_patient_report.html',context)

#========================== for Pre Dialysis 15/05/2023 ===================================
def pre_equipment_master(request):
    equipment_master=PreEquipPreparationMaster.objects.all()
    form=PreEquipPreparationMasterForm()
    add='add'
    if request.method=='POST':
        form=PreEquipPreparationMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pre_equipment_master')
    context={
    'add':add,'form':form,"refered_bymaster":equipment_master
    }
    return render(request,"general_master/dialysis_master/pre_equipment_master.html",context)

def edit_pre_equipment_master(request,pk):
    equipment_master=PreEquipPreparationMaster.objects.get(id=pk)
    form=PreEquipPreparationMasterForm(instance=equipment_master)
    if request.method=='POST':
        form=PreEquipPreparationMasterForm(request.POST,instance=equipment_master)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pre_equipment_master')
    context = {
        "form":form
    }
    return render(request,"general_master/dialysis_master/edit_pre_equipment_master.html",context)



def sample_collection(request,ptid):
    records=PendingInvestigation_main.objects.filter(PTID=ptid)
    patient_record = PatientsRegistrationsAllInOne.objects.filter(uhid=records.last().uhid).last()
    sample_records=SampleMaster.objects.all()
    if request.method=='POST':
        id_list=request.POST.getlist('sample_id')
        sample_type=request.POST.getlist('sample_type')
        for i in range(len(id_list)):
            pend_records=PendingInvestigation_main.objects.filter(id=id_list[i]).last()
            Volume='N/A'
            technician_name=request.user.first_name
            sample_col=SampleCollection(
                test_id=pend_records.test_id,lab_service_name=pend_records.profile_name,type_of_sample=sample_type[i],Volume=Volume,
                technician_name=technician_name,date_time=datetime.now(),PTID=pend_records.PTID,created_by_id=request.user.id,location_id=request.location,
            )
            sample_col.save(print('sucessful save SampleCollection'))
            collected=SampleCollected(
                test_id=pend_records.test_id,uhid=pend_records.uhid,visit_no=pend_records.visit_no,bill_no=pend_records.bill_no,
                profile_id=pend_records.profile_id,profile_name=pend_records.profile_name,date_time=datetime.now(),
                status='waiting',PTID=pend_records.PTID,department=pend_records.department,sub_department=pend_records.sub_department,created_by_id=request.user.id,location_id=request.location,
                outsource=pend_records.outsource,
            )
            collected.save(print('sucessful save SampleCollected'))
            pend_records.delete()
        # if records:
        #     return HttpResponseRedirect(f'/sample_collection/{ptid}')
        # else:
        return HttpResponseRedirect('/lab_pending_investigation')
    context = {
        "records":records,'patient_record':patient_record,'sample_records':sample_records,'ptid':ptid,
    }
    return render(request,"lab_module/sample_collection.html",context)


def lab_service_temp(request,ptid):
    records=PendingInvestigation_main.objects.filter(PTID=ptid)
    if not records:
        records=SampleCollected.objects.filter(PTID=ptid)
    profile=ProfileService.objects.all()
    service=ServiceMaster.objects.filter(service_sub_category__service_sub_category='Lab Investigation')
    if request.method=='POST':
        profile_name=request.POST.get('profile')
        profile=ProfileService.objects.filter(profile_name=profile_name)
        te_id = str(random.randint(100000, 999999))
        test_id = 'TST' + te_id
        for data in profile:
            LabResultEntry.objects.create(
                test_id=test_id,
                profile_name=data.profile_name,
                service_name=data.service_name,
                range=data.male_range,
                value='',
                units=data.units,
                created_by_id=request.user.id,location_id=request.location
            )
        PendingInvestigation_main.objects.create(
            PTID=records.last().PTID,
            test_id=test_id,
            uhid=records.last().uhid,
            visit_no=records.last().visit_no,
            bill_no=records.last().bill_no,
            profile_id=' ',
            profile_name=profile_name,
            department=profile.last().service_department,
            sub_department=profile.last().service_sub_department,
            date_time=records.last().date_time,
            created_by=records.last().created_by,
            location=records.last().location,
            )
        return HttpResponseRedirect(f"lab_service_temp/{ptid}")
    context = {
        'records':records,'profile':profile,'service':service,'ptid':ptid
    }
    return render(request,"lab_module/lab_service_temp.html",context)


def lab_service_temp1(request,ptid):
    records=PendingInvestigation_main.objects.filter(PTID=ptid)
    if not records:
        records=SampleCollected.objects.filter(PTID=ptid)
    if request.method=='POST':
        service_get=request.POST.get('service')
        service=ServiceMaster.objects.filter(id=service_get).last()
        te_id = str(random.randint(100000, 999999))
        test_id = 'TST' + te_id
        # for data in service:
        range_record=Service_Test.objects.filter(test_name=service_get).last()
        if range_record:
            LabResultEntry.objects.create(
                test_id=test_id,
                profile_name=service.service_name,
                service_name=service.service_name,
                range=range_record.male_range,
                value='',
                units=range_record.units,
                created_by_id=request.user.id,location_id=request.location
            )
            PendingInvestigation_main.objects.create(
                PTID=records.last().PTID,
                test_id=test_id,
                uhid=records.last().uhid,
                visit_no=records.last().visit_no,
                bill_no=records.last().bill_no,
                profile_id=' ',
                profile_name=service.service_name,
                department=service.service_department,
                sub_department=service.ServiceSubDepartment,
                date_time=records.last().date_time,
                created_by=records.last().created_by,
                location=records.last().location,
            )

        return HttpResponseRedirect(f"lab_service_temp/{ptid}")

def delete_lab_temp(request,test_id):
    pen=PendingInvestigation_main.objects.filter(test_id=test_id)
    id=pen.last().PTID
    pen.delete()
    lab=LabResultEntry.objects.filter(test_id=test_id).delete()
    return HttpResponseRedirect(f'/lab_service_temp/{id}')


def opdbilling_details(request):
    try:
        # opdbill_parent=OpdBillingMain.objects.filter(location=request.location)

        opdbill_parent = OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        }).filter(location=request.location).exclude(status='cancel').order_by('-id')

        context={
            'opdbill_parent':opdbill_parent
        }
        return render(request,'clinical/opd_bill/opdbilling_details.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

def opdbilling_list_details(request,pk):
    try:
        opdbill_main = OpdBillingMain.objects.extra(select={
            'pst_title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        }).filter(bill_no=pk).last()
        opdbill_child=OpdBillingSub.objects.filter(bill_no=pk)
        context={
            'dat':opdbill_main,'opdbill_child':opdbill_child,'pk':pk,
        }
        return render(request,'clinical/opd_bill/opdbilling_list_details.html',context)
    except Exception as error:
        return render(request,'error.html',{'error':error})

def lab_inves_senses(request):
    category=ServiceCategory.objects.filter(service_category='Investigation').last()
    sub_category=ServiceSubCategory.objects.filter(service_sub_category='Lab Investigation').last()
    service_records=ServiceMaster.objects.filter(service_category=category.id,service_sub_category=sub_category.id)
    service_list=[data.service_name for data in service_records]
    opd_records=OpdBillingSub.objects.filter(service_category='Investigation',service_sub_category='Lab Investigation').order_by('service_id')
    context={
        'opd_records':opd_records,
    }
    return render(request,'Reports/lab_inves_senses.html',context)


def tat_all_report_print(request,pk):
    collected=SampleCollected.objects.filter(test_id=pk).last()
    sample_date_time=SampleCollection.objects.get(test_id=pk).date_time
    result_entry_date_time=LabResultEntry_records.objects.filter(test_id=pk).last().upadated_date_time
    validayion_date=Validation_record.objects.filter(PTID=collected.PTID).last()
    if validayion_date:
        validayion_date_time=validayion_date.date_time
    else:
        validayion_date_time=Validation_record.objects.filter(PTID=collected.test_id).last().date_time
    billing=OpdBillingMain.objects.filter(bill_no=collected.bill_no).last().bill_date_time
    # consume time
    c = validayion_date_time-billing
    seconds_in_day = 24 * 60 * 60
    minutes=divmod(c.days * seconds_in_day + c.seconds, 60)
    consume=f'{minutes[0]}, minutes,{minutes[1]}, seconds'

    context={
        'collected':collected,'sample_date_time':sample_date_time,'result_entry_date_time':result_entry_date_time,
        'validayion_date_time':validayion_date_time,'billing':billing,'consume':consume
    }
    return render(request,'lab_module/tat_report_print.html',context)


def tat_lab_report_all(request):
    records=SampleCollected.objects.extra(select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).filter(status='vallidated').order_by('-date_time')
    if request.method=='POST':
        from_date=request.POST.get('from_date')
        to_date=request.POST.get('to_date')
        patient_name=request.POST.get('patient_name')
        if from_date and to_date and patient_name:
            patient_record=PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=patient_name).values('uhid')
            records=SampleCollected.objects.extra(select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).filter(status='vallidated',uhid__in=patient_record,date_time__range=[from_date,to_date]).order_by('-date_time')
        elif from_date and to_date:
            records=SampleCollected.objects.extra(select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).filter(status='vallidated',date_time__range=[from_date,to_date]).order_by('-date_time')
        elif patient_name:
            patient_record=PatientsRegistrationsAllInOne.objects.filter(first_name__icontains=patient_name).values('uhid')
            records=SampleCollected.objects.extra(select={
                'pat_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_SampleCollected.uhid',
                }).filter(status='vallidated',uhid__in=patient_record).order_by('-date_time')

    context={
        'records':records,
    }
    return render(request,'lab_module/tat_report.html',context)

#========================== for Prescription Dialysis 26/05/2023 ===================================
def cannulation_nurse(request):
    cannulation_nurses=CannulationNurse.objects.all()
    form=CannulationNurseForm()
    add='add'
    if request.method=='POST':
        form=CannulationNurseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cannulation_nurse')
    context={
    'add':add,'form':form,"cannulation_nurses":cannulation_nurses
    }
    return render(request,"general_master/dialysis_master/cannulation_nurse.html",context)

def edit_cannulation_nurse(request,pk):
    Cannulation_nurse=CannulationNurse.objects.get(id=pk)
    form=CannulationNurseForm(instance=Cannulation_nurse)
    if request.method=='POST':
        form=CannulationNurseForm(request.POST,instance=Cannulation_nurse)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cannulation_nurse')
    context = {
        "form":form
    }
    return render(request,"general_master/dialysis_master/edit_cannulation_nurse.html",context)

#====================== For Clinical Dialysis Patient 05\06\2023 ======================================

@login_required(login_url='/user_login')
def list_discharge_dialysis_patient(request):
    records1 = PatientVisitMains.objects.filter(visit_type=2,location=request.location).order_by('-id').extra(select={
        'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_machine_name': 'Select machine_name from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
        'pat_attendant_name': 'Select cannulation_nurse from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
        'pat_created_at': 'Select created_at from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
    }).exclude(uhid__in=PostDialysisDischargeSheet.objects.values('uhid'),visit_id__in=PostDialysisDischargeSheet.objects.values('visit_id'),claim_no='discharged')
    print(records1.count())
    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records1 = PatientVisitMains.objects.filter(uhid__exact=uhid,visit_type=2,location=request.location).exclude(claim_no='discharged').extra(select={
                'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_attendant_name': 'Select cannulation_nurse from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
                'pat_created_at': 'Select created_at from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
                'pat_machine_name':'Select machine_name from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
            }).exclude(uhid__in=PostDialysisDischargeSheet.objects.values('uhid'))
            success_search = 'success'
            context = {
            'success_search': success_search,'discharge_list':discharge_list,'records1':records1,
            }
            return render(request, 'dialysis/list_discharge_dialysis_patient.html', context)
        except Exception as e:
            pass
    context = {
        'records1': records1,
    }
    return render(request,'dialysis/list_discharge_dialysis_patient.html',context)

@login_required(login_url='/user_login')
def discharged_dialysis_patient(request):
    records1 = PatientVisitMains.objects.filter(visit_type=2,claim_no='discharged',location=request.location).order_by('-id').extra(select={
        'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
        'pat_machine_name': 'Select machine_name from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
        'pat_attendant_name': 'Select cannulation_nurse from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
        'pat_created_at': 'Select created_at from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
    })
    if request.method == 'POST':
        uhid = request.POST.get('uhid')
        patient_name = request.POST.get('patient_name')
        mobile_number = request.POST.get('mobile_number')
        if uhid == '':
            uhid = "Not Provided"
        if patient_name == '':
            patient_name = "Not Provided"
        if mobile_number == '':
            mobile_number = "Not Provided"
        try:
            records1 = PatientVisitMains.objects.filter(uhid__exact=uhid,visit_type=2,claim_no='discharged',location=request.location).extra(select={
                'pat_f_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_m_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_l_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_age':'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_sex':'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_dob':'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PatientVisitMains.uhid',
                'pat_attendant_name': 'Select cannulation_nurse from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
                'pat_created_at': 'Select created_at from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
                'pat_machine_name':'Select machine_name from testapp_Pre_Dialysis_Details where uhid=testapp_PatientVisitMains.uhid',
            })
            success_search = 'success'
            context = {
            'success_search': success_search,'discharge_list':discharge_list,'records1':records1,
            }
            return render(request, 'dialysis/discharged_dialysis_patient.html', context)
        except Exception as e:
            print('e----',e)
            pass
    context = {
        'records1': records1,
    }
    return render(request,'dialysis/discharged_dialysis_patient.html',context)


def doctor_request(request):
    requested_files = FileRequest_MRD.objects.filter(status = "send_doctor_approval")
    context = {
      'requested_files':requested_files,
    }
    return render(request,"doctor/doctor_request.html",context)

def doctor_confirmation(request,pk):
    doctor_approval = FileRequest_MRD.objects.get(id = pk[0])
    doctor_approval.status = "approval_confirm"
    doctor_approval.save()
    clparent = Checklist_Parent.objects.get(admission_id = pk[1])
    clparent.file_action = "doctor_approved"
    clparent.save()

    return redirect('doctor_request')


def doctor_notes(request):
    save_btn = request.POST.get("save_btn")
    if save_btn == "Save":
        Doctor_Notes.objects.create(
            name = request.POST.get("Name"),
            age = request.POST.get("age") ,
            date = request.POST.get("date") ,
            diagnosis = request.POST.getlist("diagonsis") ,
            duration_on_dialysis = request.POST.get("durations") ,
            current_medications = request.POST.getlist("current_medication") ,
            general_status = request.POST.get("general_status") ,
            access_site = request.POST.getlist("access_site") ,
            bp = request.POST.get("BP") ,
            QB_rate = request.POST.get("QB_rate") ,
            ultrafiltration = request.POST.get("ultrafiltration") ,
            investication = request.POST.getlist("investigations") ,
            plan = request.POST.getlist("plan"),
        )
        return redirect("doctor_notes")
    return render(request,'nurse_station/doctor_notesform.html')

def doctornotes_view(request):
    records = Doctor_Notes.objects.all()
    context = {
        "records":records
    }
    return render(request,"nurse_station/doctornotes_view.html",context)


def doctornotes_print(request,pk):
    records = Doctor_Notes.objects.get(id=pk)
    diagnosis = records.plan
    print(diagnosis.split("', "))
    context = {
        "records":records,"diagnosis":diagnosis
    }
    return render(request,"nurse_station/doctors_noteprint.html",context)

def refferal_dialysis_patient(request):
    numbers = range(1, 5)
    save_button = request.POST.get("save_button")
    if save_button == "Save":
        Refferal_Form.objects.create(
            reffering_doctor = request.POST.get("reffering_doctor"),
            refferal_hospital =request.POST.get("reffering_hospital"),
            patient_last_name = request.POST.get("patient_last_name"),
            other_names = request.POST.get("other_name"),
            age = request.POST.get("age"),
            gender = request.POST.get("gender"),
            duration_dialysis = request.POST.get("duration_dialysis"),
            cause_kidney = request.POST.get("cause_kidney"),
            comorbidities = request.POST.get("comorbidities"),
            reason = request.POST.get("reason"),
            current_medication = request.POST.getlist("current_medication"),
            dosage = request.POST.getlist("dosage"),
            duration =request.POST.getlist("duration_of_use"),
            others = request.POST.get("others"),
            procedural_notes = request.POST.get("procedure_notes"),
            doctor_name = request.POST.get("doctor_name"),
        )
        return redirect("refferal_dialysis_patient")
    return render(request,"nurse_station/refferal_dialysis_patient.html",{"numbers":numbers})

def refferal_dialysis_view(request):
    records = Refferal_Form.objects.all()
    return render(request,"nurse_station/refferaldialysis_view.html",{"records":records})

def refferal_dialysisprint(request,pk):
    records = Refferal_Form.objects.get(id=pk)
    context = {
        "records":records
    }
    return render(request,"nurse_station/refferaldialysis_print.html",context)

def preprocedural_checklist(request):
    numbers = range(1, 5)
    save_btn = request.POST.get("save_button")
    if save_btn == "Save":
        Pre_Procedural_Checklist.objects.create(
            reffering_doctor = request.POST.get("reffering_doctor"),
            patient_last_name = request.POST.get("patient_last_name"),
            other_name = request.POST.get("other_name"),
            age =request.POST.get("age"),
            gender = request.POST.get("gender"),
            duration = request.POST.get("duration"),
            cause_kidney_disease = request.POST.get("cause_kidney"),
            Comorbidities = request.POST.get("comorbidities"),
            type1 = request.POST.getlist("type"),
            site = request.POST.getlist("site"),
            duration_use = request.POST.getlist("duration_of_use"),
            others = request.POST.get("others"),
            reason_last_accesss_failure = request.POST.get("reason"),
            current_intend_access = request.POST.get("current_intended"),
            reason_for_current_intended = request.POST.get("reason_current_intended"),
            procedure_notes= request.POST.get("procedure_notes"),
            final_access_site = request.POST.get("Final_access"),
            surgeon_name = request.POST.get("surgeon_name"),
            signature = request.POST.get("signature"),
        )
        return redirect("preprocedural_checklist")
    context = {
    "numbers":numbers
    }
    return render(request,"nurse_station/preprocedural_checklist.html",context)

def preprocedural_checklist_view(request):
    records = Pre_Procedural_Checklist.objects.all()
    return render(request,"nurse_station/preprocedural_checklist_view.html",{"records":records})

def preprocedural_checklistprint(request,pk):
    records = Pre_Procedural_Checklist.objects.get(id=pk)
    return render(request,"nurse_station/preprocedural_checklistprint.html",{"records":records})

def informed_consent_form(request):
    save_button = request.POST.get("save_button")
    if save_button == "Save":
        Informed_Consent.objects.create(
            date =request.POST.get("date"),
            time = request.POST.get("time"),
            mental_state = request.POST.get("mental_state"),
            doctor_performing = request.POST.get("doctor_performing"),
            description = request.POST.get("description"),
            explain_parent_patient = request.POST.get("explain_parent_patient"),
            intened_benefits = request.POST.getlist("intened_benefits"),
            serious_risk = request.POST.getlist("serious_risk"),
            extra_procedure = request.POST.getlist("extra_procedure"),
            alternative_treatment = request.POST.get("alternative_treatment"),
            date2 =request.POST.get("date2"),
            time2 = request.POST.get("time2"),
            mental_state2 = request.POST.get("mental_state2"),
            administering_sedation = request.POST.get("administering_sedation"),
            mode_of_anasthesia = request.POST.get("mode_of_anasthesia"),
            doctor_name = request.POST.get("doctor_name"),
            dr_explain_procedure = request.POST.getlist("dr_explain_procedure"),
            benefites_mode_anasthesia = request.POST.getlist("benefites_mode_anasthesia"),
            alternative = request.POST.getlist("alternative"),
            patient_qstn = request.POST.get("patient_qstn"),
            patient_explain = request.POST.getlist("patient_explain"),
            name_of_doctor = request.POST.get("name_of_doctor"),
            doctor_signature = request.POST.get("doctor_signature"),
            date3 =request.POST.get("date3"),
            time3 = request.POST.get("time3"),
            patient_accept_procedure = request.POST.getlist("patient_accept_procedure"),
            patient_signature = request.POST.get("patient_signature"),
            date4 =request.POST.get("date4"),
            time4 = request.POST.get("time4"),
            patient_upderstand_procedure = request.POST.getlist("patient_upderstand_procedure"),
            signature_self = request.POST.get("signature_self"),
            date5 =request.POST.get("date5"),
            time5 = request.POST.get("time5"),
            signature_guardian = request.POST.get("signature_guardian"),
            date6 =request.POST.get("date6"),
            time6 = request.POST.get("time6"),
        )
        return redirect("informed_consent_form")
    return render(request,"nurse_station/informed_consent_form.html")

def informed_consent_view(request):
    records = Informed_Consent.objects.all()
    return render(request,"nurse_station/informed_consent_view.html",{"records":records})

def informed_consentprint(request,pk):
    records = Informed_Consent.objects.get(id=pk)
    return render(request,"nurse_station/informed_consentprint.html",{"records":records})

def consent_kidney_dialysis(request):
    save_button = request.POST.get("save_button")
    if save_button == "Save":
        Consent_KidneyDialysis.objects.create(
            patient_name = request.POST.get("patient_name"),
            patient_address = request.POST.getlist("patient_address"),
            age = request.POST.get("age"),
            sex = request.POST.get("gender"),
            admission_no = request.POST.get("admissionno"),
            name1 = request.POST.get("name1"),
            blood_sample = request.POST.get("blood_sample"),
            PO_box_no =  request.POST.get("PO_box"),
            name2 = request.POST.get("name2"),
            signature = request.POST.get("signature"),
            id_no = request.POST.get("ID_no"),
            next_kin = request.POST.get("next_kin"),
            mobile_no = request.POST.get("mobileno"),
            witnessed_admitted_nurse =  request.POST.get("witness_admitted_nurse"),
            date = request.POST.get("date"),
            time = request.POST.get("time"),
        )
        return redirect("consent_kidney_dialysis")
    return render(request,"nurse_station/consent_kidney_dialysis.html")

def consent_kidney_view(request):
    records = Consent_KidneyDialysis.objects.all()
    return render(request,"nurse_station/consent_kidney_view.html",{"records":records})

def consent_kidneyprint(request,pk):
    records = Consent_KidneyDialysis.objects.get(id=pk)
    return render(request,"nurse_station/consent_kidneyprint.html",{"records":records})

def branch_restrict(request):
    records = BranchRestrict.objects.all()
    form = BranchRestrictForm()
    if request.method == 'POST':
        form = BranchRestrictForm(request.POST)
        if form.is_valid:
            form.save()
        return HttpResponseRedirect('/branch_restrict')
    return render(request,"mainapp/branch_restrict.html",{'form':form,"records":records})