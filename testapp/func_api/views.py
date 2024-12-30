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
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# @api_view['GET']
class PatientView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='api/testapp/index.html'
    def get(self,request):
        print('Im Get Method')
        return Response({'hello':'Ram'})
    def post(self,request,*args,**kwargs):
        print("I'm Post Method")
        return Response({'Hi Ram':'Hello'})
def patient_view(request):
    return render(request,'testapp/index.html')
def book_appointment(request):
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

def mobile_register(request):
    print('calendar')
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
        # response.set_cookie(doctor_location,doctor_department)
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
def date_time(request):
    doctor_id=request.session['doctor_id']
    mobile_number=request.POST.get('mobile_number')
    name=request.POST.get('name')
    request.session['mobile_number']=mobile_number
    request.session['name']=name
    doctor_name=request.session['doctor_name']
    doctor_department=request.session['doctor_department']
    doctor_location=request.session['doctor_location']
    doctor_profile_image=request.session['doctor_profile_image']
    doctor_appointment=request.session['doctor_appointment']
    mobile_number=request.session['mobile_number']
    # doctor_time_slot=request.session['doctor_time_slot']
    mobile_number=request.session['mobile_number']
    name=request.session['name']
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
    # for data in records:
    #     print(f'{data.time_slot_start_time}-{data.time_slot_end_time}')
    # for data in records:
    #     print(data.time_slot_id)
    time_slot_lists='time_slots'
    context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'name':name,'time_slots':time_slot_lists,'records':records,'doctor_fee':doctor_fee}
    return render(request,'testapp/date_time.html',context)
def appointment_detail(request):
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
    name=request.session['name']
    doctor_fee=request.session['doctor_fee']
    context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'scheduled':scheduled, 'mobile_number':mobile_number,'name':name,'doctor_fee':doctor_fee}
    return render(request,'testapp/appointment_detail.html',context)
def booking_detail(request):
    global records_of_members
    doctor_name=request.session['doctor_name']
    scheduled=request.session['scheduled']
    doctor_department=request.session['doctor_department']
    doctor_location=request.session['doctor_location']
    doctor_profile_image=request.session['doctor_profile_image']
    doctor_appointment=request.session['doctor_appointment']
    mobile_number=request.session['mobile_number']
    name=request.session['name']
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
            patient_name=request.POST.get('patient_name')
            gender=request.POST.get('gender')
            age=request.POST.get('age')
            mobile_number=request.POST.get('mobile_number')
            email=request.POST.get('email')
            records=AddMembers.objects.get_or_create(
            reference_mobile_number=reference_mobile_number,
            title_name=title_name,
            patient_name=patient_name,
            gender=gender,
            age=age,
            mobile_number=mobile_number,
            email=email,
            )
            records_of_members=AddMembers.objects.filter(reference_mobile_number=reference_mobile_number)
            no_of_member=records_of_members.count()
            # if no_of_member !=0:
            #     without_discount=base_price*(no_of_member+1)
            #     print('without_discount',without_discount)
            #     print(type(without_discount))
            #     with_discount=without_discount*(90/100)
            base_price=doctor_fee
            without_discount=doctor_fee
            with_discount=630
            context={
            'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment, 'mobile_number':mobile_number,'name':name,'scheduled':scheduled,'records_of_members':records_of_members,'without_discount':without_discount,'with_discount':with_discount,
            }
            return render(request,'testapp/booking_detail.html',context)
    records_of_members=AddMembers.objects.filter(reference_mobile_number=reference_mobile_number)
    no_of_member=records_of_members.count()
    # if no_of_member !=0:
    #     without_discount=base_price*(no_of_member+1)
    #     with_discount=without_discount*(90/100)
    base_price=float(doctor_fee)
    without_discount=float(doctor_fee)
    with_discount=(base_price-(base_price*10)/100)
    context={
    'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'records_of_members':records_of_members, 'mobile_number':mobile_number,'name':name,'scheduled':scheduled,'without_discount':without_discount,'with_discount':with_discount,
    }
    return render(request,'testapp/booking_detail.html',context)
@login_required
def doctor_view(request):
    form=DoctorTableForm()
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
        print('doc_id',doc_id)
        print('doc_reg',doc_reg)
        form=DoctorTableForm(request.POST,request.FILES)
        if form.is_valid():
            doctor_id=form.cleaned_data['doctor_id']
            doctor_belogns_to=form.cleaned_data['doctor_belogns_to']
            doctor_email_address=form.cleaned_data['doctor_email_address']
            doctor_password=form.cleaned_data['doctor_password']
            doctor_name=form.cleaned_data['doctor_name']
            doctor_profile_image=form.cleaned_data['doctor_profile_image']
            doctor_phone_no=form.cleaned_data['doctor_phone_no']
            doctor_appointment=form.cleaned_data['doctor_appointment']
            doctor_address=form.cleaned_data['doctor_address']
            doctor_date_of_birth=form.cleaned_data['doctor_date_of_birth']
            doctor_department=form.cleaned_data['doctor_department']
            doctor_status=form.cleaned_data['doctor_status']
            doctor_fee=form.cleaned_data['doctor_fee']
            doctor_registration_no=form.cleaned_data['doctor_registration_no']
            registration_exparing_date=form.cleaned_data['registration_exparing_date']
            doctor_register_by=form.cleaned_data['doctor_register_by']
            doctor_location=form.cleaned_data['doctor_location']
            DT=DoctorTable(doctor_id=doc_id,doctor_belogns_to=doctor_belogns_to,doctor_email_address=doctor_email_address,doctor_password=doctor_password,doctor_name=doctor_name,doctor_profile_image=doctor_profile_image,doctor_phone_no=doctor_phone_no,doctor_appointment=doctor_appointment,doctor_address=doctor_address,doctor_date_of_birth=doctor_date_of_birth,doctor_department=doctor_department,doctor_status=doctor_status,doctor_fee=doctor_fee,doctor_registration_no=doc_reg,registration_exparing_date=registration_exparing_date,doctor_register_by=doctor_register_by,doctor_location=doctor_location)
            print('dt',DT)
            DT.save()
            # doctor_table=DoctorTable()
            # form.save()
            return render(request,'testapp/doctor_view.html',{'form':form,'success':success})
        else:
            return render(request,'testapp/doctor_view.html',{'form':form})
    return render(request,'testapp/doctor_view.html',{'form':form,'records':records})
def doctor_schedule_view(request):
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
def appointment_view(request):
    form=AppointmentTableForm()
    if request.method=='POST':
        form=AppointmentTableForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("ThanksYOU")
        else:
            return render(request,'testapp/appointment_view.html',{'form':form})
    return render(request,'testapp/appointment_view.html',{'form':form})
def patient_view_detail(request):
    form=PatientTableForm()
    if request.method=='POST':
        form=AppointmentTableForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("ThanksYOU")
        else:
            return render(request,'testapp/patient_view.html',{'form':form})
    return render(request,'testapp/patient_view.html',{'form':form})
#dashbord
class DoctorDashbordView(ListView):
    model=DoctorTable
    template_name='patient/doctortable_list.html'
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
    template_name='patient/doctortable_detail_view.html'
    context_object_name='data'
class AppoitmentView(ListView):
    model=BookedAppointments
    template_name='patient/appointment_table.html'
    def get_queryset(self):
        patient_details=BookedAppointments.objects.order_by('-patient_appointment_date')
        return BookedAppointments.objects.order_by('-patient_schedule_date_and_time')
class AppointmentDeleteView(DeleteView):
    model=BookedAppointments
    template_name='patient/bookedappointment_confirm_delete.html'
    success_url=reverse_lazy('delete-appointment')
class AppointmentDetailView(DetailView):
    model=BookedAppointments
    template_name='patient/bookedappointment_detail.html'
    context_object_name='data'
def cancel_appointment(request,patient_id):
    records_patient_id=BookedAppointments.objects.get(patient_id=patient_id)
    form=BookedAppointmentsForm()#instance=records_patient_id
    if request.method=='POST':
        form=BookedAppointmentsForm(request.POST,instance=records_patient_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/appointment_table')
    return render(request,'patient/cancel_appointment.html',{'form':form})
@login_required
def patient_dashboard(request):
    today=date.today()
    doctor_records=DoctorTable.objects.all()
    appointment_records=BookedAppointments.objects.all()
    today_total_appointment_records=BookedAppointments.objects.filter(patient_appointment_date=today)
    no_of_doctor=doctor_records.count()
    total_appointment=appointment_records.count()
    today_total_appointment_records=today_total_appointment_records.count()
    context={
    'no_of_doctor':no_of_doctor,'total_appointment':total_appointment,'today_total_appointment_records':today_total_appointment_records,
    }
    return render(request,'patient/patient_dashboard.html',context)
def admin_list_table(request):
    records=User.objects.all()
    context={
    'records':records
    }
    return render(request,'patient/admin_list_table.html',context)
# def appointment_table(request):
#     records=BookedAppointment.objects.all()
#     return render(request,'')
def patient_table(request):
    return render(request,'patient/patient_table.html')
def doctor_table(request):
    records=DoctorTable.objects.all()
    context={
    'records':records,
    }
    return render(request,'patient/doctor_table.html',context)
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
from random import *
def success_booked(request):
    digits='0123456789'
    # p_ids= randint(111111,999999)
    # appointment_id=randint(100000000,9999999999)
    # patient_id='patient'+str(p_ids)
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
    print('App_id',appointment_id)
    print('App_id',patient_id)
    success='success'
    title_name=request.POST.get('sub')
    patient_name=request.POST.get('patient_name')
    gender=request.POST.get('gender')
    age=request.POST.get('age')
    phone=request.POST.get('phone')
    email=request.POST.get('email')
    request.session['title_name']=title_name
    request.session['patient_name']=patient_name
    schedule_time=request.POST.get('schedule_time')
    payment=request.POST.get('payment')
    doctor_name=request.session['doctor_name']
    doctor_name=request.session['doctor_name']
    doctor_department=request.session['doctor_department']
    doctor_appointment=request.session['doctor_appointment']
    patient_name=request.session['patient_name']
    title_name=request.session['title_name']
    mobile_number=request.session['mobile_number']
    get_schedule_time_slot_id=request.session['get_schedule_time_slot_id']
    patient_name=title_name + patient_name
    add_this_member=request.POST.get('add_this_member')
    print('Add This ',add_this_member)
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
        print(patient_name)
    print(patient_name)
    records=BookedAppointments.objects.get_or_create(
    patient_id=patient_id,
    patient_name=patient_name,
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
    doctor_department=doctor_department

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
def doctor_schedule_view(request):
    form=DoctorScheduleForm()
    if request.method=='POST':
        doctor_name=request.POST.get('doctor_name')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        date_array =(start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1))
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
import time
def time_scheduling(request):
    scheduled_date_list=request.session['scheduled_date_list']
    if request.method=='POST':
        select_scheduled=request.POST.get('select_scheduled')
        start_time=request.POST.get('start_time')
        end_time=request.POST.get('end_time')
        average_duration=request.POST.get('average_duration')
        start_time_obj=time.strptime(start_time,"%H:%M")
        end_time_obj=time.strptime(end_time,"%H:%M")
        average_duration_obj=time.strptime(average_duration,"%M")
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
        current_start_time=datetime.datetime.strptime(start_time,"%H:%M")
        time_mn=00.34
        time_scheduled=[]
        if average_duration_obj==10:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.17)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==15:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.26)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==20:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.34)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==25:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.42)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==30:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.5)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==35:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.59)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==40:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.67)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M %p")
        elif average_duration_obj==45:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.75)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==50:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.84)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        elif average_duration_obj==55:
            for i in range(0,slots):
                schedule=(current_start_time + timedelta(hours=0.92)).strftime("%H:%M")
                time_scheduled.append(schedule)
                current_start_time=datetime.datetime.strptime(schedule,"%H:%M")
        time_scheduled.insert(0,start_time)
        actual_time_schedule=[]
        for i in range(0,len(time_scheduled)):
            for j in range(i+1,i+2):
                if time_scheduled[i]==time_scheduled[-1]:
                    break;
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
    print('scheduled_date_list',scheduled_date_list)
    print('get_time_list',get_time_list)
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
            add_records=AvailabilityIntradayScheduleMaster.objects.get_or_create(
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
def patient_registraions(request):
    return render(request,'patient/patient_registraions.html')

#Appointment_dashboard
def doctor_dash(request):
    records=BookedAppointments.objects.all().count()
    context={
    'records':records
    }
    return render(request,'doctor/doctor_dash.html',context)
def doctor_appointment(request):
    records=BookedAppointments.objects.all()
    context={
    'records':records
    }
    return render(request,'doctor/doctor_appointment.html',context)
def prescription(request):
    return render(request,'doctor/prescription.html')
def appointment_list(request):
    return render(request,'doctor/appointment_list.html')
def patient_list(request):
    return render(request,'doctor/patient_list.html')
def interface_dashboard(request):
    return render(request,'interface/interface_dashboard.html')
def patient(request):
    return render(request,'interface/patient.html')
#=========================Reports=========================
def reports(request):
    return render(request,'testapp/reports.html')
def cancellation_reports(request):
    records=BookedAppointments.objects.filter(patient_scheduled_id='N/A')
    print('BookedAppointment',records)
    context={
    'records':records
    }
    return render(request,'testapp/cancellation_reports.html',context)
from django.db.models import Q
def shorting_filter(request):
    records=BookedAppointments.objects.all()
    if request.method=='POST':
        consultant=request.POST.get('consultant')
        department=request.POST.get('department')
        print(consultant)
        if 'department'==department:
            print(f'consultant:=> {consultant}, department:=> {department}')
            filtering_records=BookedAppointments.objects.filter(doctor_department=department)
            filtered='filter'
        else:
            print(f'consultant:=> {consultant}, department:=> {department}')
            filtering_records=BookedAppointments.objects.filter(doctor_name=consultant)
            filtered='filter'
        context={
        'records':records,'filtered':filtered,'filtering_records':filtering_records,
        }
        return render(request,'testapp/shorting_filter.html',context)
    context={
    'records':records
    }
    return render(request,'testapp/shorting_filter.html',context)
def filtering_department(request):
    department=request.POST.get('department')
    print(f' department:=> {department}')
    filtering_records=BookedAppointments.objects.filter(doctor_department=department)
    filtered='filter'
    context={
    'filtered':filtered,'filtering_records':filtering_records,
    }
    return render(request,'testapp/shorting_filter.html',context)

def appointment_detail_reports(request):
    if request.method=='POST':
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        print(f'Start Date {start_date}, end date {end_date}')
        records=BookedAppointments.objects.filter(patient_appointment_date__range=[start_date,end_date])
        print('records',records)
        context={
        'records':records,
        }
        return render(request,'testapp/appointment_detail_reports.html',context)
    return render(request,'testapp/appointment_detail_reports.html')
#Updated
def login(request):
    return render(request,'interface/login.html')
def box(request):
    return render(request,'interface/box.html')
def modal(request):
    return render(request,'interface/modal.html')
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
# # CREATE Appointment
# def create_appointment(request):
#     return render(request,'create/create_appointment.html')
# def appointment_mobile(request):
#     return render(request,'create/appointment_mobile.html')
# def appointment_date(request):
#     return render(request,'create/appointment_date.html')
# def book_detail(request):
#     return render(request,'create/book_detail.html')
def appointment_by_admin(request):
    form=NewAppointmentByAdminForm()
    if request.method=='POST':
        digits='0123456789'
        p_ids= randint(111111,999999)
        appointment_id=randint(100000000,9999999999)
        patient_id='patient'+str(p_ids)
        patient_name=request.POST.get('patient_name')
        email_id=request.POST.get('email_id')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        appointment_id=appointment_id
        patient_id=patient_id
        mobile_number=request.POST.get('mobile_number')
        request.session['appointment_id']=appointment_id
        request.session['patient_id']=patient_id
        request.session['patient_name']=patient_name
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
    form=NewAppointmentByAdminChooseDoctorForm()
    if request.method=='POST':
        choose_doctor='choose_doctor'
        doctor_name=request.POST.get('doctor_name')
        appointment_date=request.POST.get('appointment_date')
        request.session['appointment_date']=appointment_date
        request.session['doctor_name']=doctor_name
        return HttpResponseRedirect('/booked-slots')

    # return HttpResponseRedirect('/booked-slots')
    context={
    'form':form
    }
    return render(request,'patient/choose_doctor.html',context)
def booked_slots(request):
    booking_for_slots='booking_for_slots'
    doctor_id=request.session['doctor_name']
    patient_name=request.session['patient_name']
    appointment_date=request.session['appointment_date']
    doctor_details=DoctorTable.objects.get(doctor_id=doctor_id)
    booked_appointment_id=BookedAppointments.objects.all().only('patient_scheduled_id')
    slots=AvailabilityIntradayScheduleMaster.objects.filter(Q(doctor_id=doctor_id)&Q(time_slot_id__contains=appointment_date))
    print('#'*30)
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
    slots=AvailabilityIntradayScheduleMaster.objects.filter(Q(time_slot_id__in=fresh_schedule)&Q(time_slot_id__contains=appointment_date))
    print(records.count())
    # for data in records:
    #     print(f'{data.time_slot_start_time}-{data.time_slot_end_time}')
    # for data in records:
    #     print(data.time_slot_id)
    # already_booking_slots=[]
    # all_solts=[]
    # available_slots=[]
    # for data in booked_appointment_id:
    #     already_booking_slots.append(data.patient_scheduled_id)
    # for data in slots:
    #     all_solts.append(data.time_slot_id)
    # print('already_booking_slots',already_booking_slots)
    # print('all_solts',all_solts)
    context={
    'booking_for_slots':booking_for_slots,'slots':slots,'patient_name':patient_name,'appointment_date':appointment_date,'doctor_details':doctor_details
    }
    return render(request,'patient/booked_slots.html',context)
def successfully_booked(request):
    doctor_id=request.session['doctor_name']
    patient_name=request.session['patient_name']
    age=request.session['age']
    email_id=request.session['email_id']
    appointment_date=request.session['appointment_date']
    appointment_id=request.session['appointment_id']
    patient_id=request.session['patient_id']
    gender=request.session['gender']
    mobile_number=request.session['mobile_number']
    print(f'Success booked: {doctor_id},{patient_name},{appointment_date},{appointment_id},{patient_id},{email_id},{age},{gender}')
    doctor_records=DoctorTable.objects.get(doctor_id=doctor_id)
    doctor_name=doctor_records.doctor_name
    doctor_department=doctor_records.doctor_department
    patient_payment_mode='booking_by_admin'
    time_slots_id=request.POST.get('time_slots_id')
    print('time_slot_id',time_slots_id)
    get_schedule=AvailabilityIntradayScheduleMaster.objects.get(time_slot_id=time_slots_id)
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
    print('App_id',appointment_id)
    print('App_id',patient_id)
    if request.method=='POST':
        time_slots_id=request.POST.get('time_slots_id')
        patient_scheduled_id=time_slots_id
        records=BookedAppointments.objects.get_or_create(
        patient_id=patient_id,
        patient_name=patient_name,
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
        # patient_gender=gend
        )
    success='success'
    context={
    'success':success,'patient_id':patient_id,'patient_name':patient_name,'scheduled':scheduled,'gender':gender,'doctor_name':doctor_name,'doctor_department':doctor_department
    }
    return render(request,'patient/success_booked_by_admin.html',context)
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
def titile_master(request):
    title_master=TitleMaster.objects.all()
    context={
    'title_master':title_master
    }
    return render(request,'master_template/title_master.html',context)
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
        return render(request,'master_template/edit_title_master.html',context)
    context={
    'title_master':title_master,'form':form
    }
    return render(request,'master_template/edit_title_master.html',context)
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
        return render(request,'master_template/title_master.html',context)
    context={
    'form':form,'editing':editing
    }
    return render(request,'master_template/title_master.html',context)
def hospital_master(request):
    hospital_master=HospitalMaster.objects.all()
    form=HospitalMasterForm()
    if request.method=='POST':
        form=HospitalMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hospital-master')
    context={
    'hospital_master':hospital_master,'form':form,
    }
    return render(request,'general_master/hospital_master.html',context)
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
    return render(request,'master_template/edit_hospital_master.html',context)
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
        return render(request,'master_template/editing_hospital_master.html',context)
    context={
    'form':form,'editing':editing
    }
    return render(request,'master_template/editing_hospital_master.html',context)

#Master Related Url
# GENERAL_MASTER
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

def holiday_master(request):
    holiday_master=HolidayMaster.objects.all()
    form=HolidayMasterForm()
    if request.method=='POST':
        form=HolidayMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/holiday_master')
    context={
    'form':form,'holiday_master':holiday_master
    }
    return render(request,'general_master/holiday_master.html',context)
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


# def hospital_master(request):
#     return render(request,'general_master/hospital_master.html')
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

def title_master(request):
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
    'title_master':title_master,'form':form
    }
    return render(request,'general_master/title_master.html',context)
#================service Master================
def service_master(request):
    form=ServiceMasterForm()
    service_cat_obj=ServiceCategory.objects.all()
    service_sub_cat_obj=ServiceSubCategory.objects.all()
    records=None
    if request.method=='POST':
        form=ServiceMasterForm(request.POST)
        search=request.POST.get('searching')
        print('For Request')
        print('search',search)
        if search =='Search':
            service_category=request.POST.get('service_category')
            service_sub_category=request.POST.get('service_sub_category')
            records=ServiceMaster.objects.filter(service_category_id__in=service_category)&ServiceMaster.objects.filter(service_sub_category_id__in=service_sub_category)
        if form.is_valid():
            form.save()
            print('SAVED SuccessFully')
            return HttpResponseRedirect('/service_master')
    context={
    'form':form,'service_cat_obj':service_cat_obj,'service_sub_cat_obj':service_sub_cat_obj,'records':records,
    }
    return render(request,'general_master/service_master.html',context)
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
def corporate_master(request):
    corporate_master=CorporateMaster.objects.all()
    form=CorporateMasterForm()
    if request.method=='POST':
        form=CorporateMasterForm(request.POST)
        cor_id=randint(101,501)
        # corporate_ID=request.POST.get('corporate_ID')
        # corporate_Name=request.POST.get('corporate_Name')
        # valid_Upto=request.POST.get('valid_Upto')
        # contact_No=request.POST.get('contact_No')
        # email_ID=request.POST.get('email_ID')
        # remark=request.POST.get('remark')
        # inactive=request.POST.get('inactive')
        # Office_Location_Name=request.POST.get('Office_Location_Name')
        # Auth_Person=request.POST.get('Auth_Person')
        # Designation=request.POST.get('designation')
        # address=request.POST.get('address')
        # city=request.POST.get('City')
        # PinCode=request.POST.get('PinCode')
        # phone_no=request.POST.get('phone_no')
        # fax=request.POST.get('fax')
        # email=request.POST.get('email')
        corporate_ID=cor_id
        if form.is_valid():
            # CM=CorporateMaster(corporate_ID=cor_id,corporate_Name=corporate_Name,valid_Upto=valid_Upto,contact_No=contact_No,email_ID=email_ID,remark=remark,inactive=inactive,Office_Location_Name=Office_Location_Name,Auth_Person=Auth_Person,designation=Designation,address=address,City=city,PinCode=PinCode,phone_no=phone_no,fax=fax,email=email)
            form.save()
            return HttpResponseRedirect('/corporate_master')
    context={
    'corporate_master':corporate_master,'form':form
    }
    return render(request,'general_master/corporate_master.html',context)
def tariff_charge_master(request):
    tariff_charge_master=TariffChargeMaster.objects.all()
    tariff_master=TariffMaster.objects.all()
    service_department=ServiceDepartment.objects.all()
    service_sub_department=ServiceSubDepartment.objects.all()
    form=TariffChargeMasterForm()
    records=None
    if request.method=='POST':
        form=TariffChargeMasterForm(request.POST)
        searching=request.POST.get('search')
        submit=request.POST.get('submit')
        print('Search')
        if searching=='Search':
            service_department=request.POST.get('service_department')
            service_sub_department=request.POST.get('service_sub_department')
            print(f'{service_department},{service_sub_department}')
            records=ServiceMaster.objects.filter(service_department__in=service_department)&ServiceMaster.objects.filter(ServiceSubDepartment_id__in=service_sub_department)
        elif submit=='Save':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/tariff_charge_master')

    context={
    'tariff_charge_master':tariff_charge_master,'form':form,'tariff_master':tariff_master,'service_department':service_department,'service_sub_department':service_sub_department,'records':records
    }
    return render(request,'general_master/tariff_charge_master.html',context)
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
def master_dashboard(request):
    return render(request,'general_master/master_dashboard.html')
def add_service_master(request):
    form=ServiceCategoryForm()
    service_category='service_category'
    if request.method=='POST':
        form=ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/service-master')
    context={
    'form':form,'service_category':service_category
    }
    return render(request,'general_master/main_master.html',context)
def add_sub_service_master(request):
    form=ServiceSubCategoryForm()
    service_sub_category='service_sub_category'
    if request.method=='POST':
        form=ServiceSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_sub_service_master')
    context={
    'form':form,'service_category':service_sub_category
    }
    return render(request,'general_master/main_master.html',context)
def add_service_department(request):
    form=ServiceDepartmentForm()
    service_department='service_department'
    if request.method=='POST':
        form=ServiceDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_department')
    context={
    'form':form,'service_department':service_department
    }
    return render(request,'general_master/main_master.html',context)
def add_service_sub_department(request):
    form=ServiceSubDepartmentForm()
    service_sub_department='service_sub_department'
    if request.method=='POST':
        form=ServiceSubDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_service_sub_department')
    context={
    'form':form,'service_sub_department':service_sub_department
    }
    return render(request,'general_master/main_master.html',context)
def ward_category(request):
    form=WardCategoryForm()
    ward_category='ward_category'
    if request.method=='POST':
        form=WardCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ward_category')
    context={
    'form':form,'ward_category':ward_category
    }
    return render(request,'general_master/main_master.html',context)
def ward_type(request):
    form=WardTypeForm()
    ward_type='ward_type'
    if request.method=='POST':
        form=WardTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ward_type')
    context={
    'form':form,'ward_type':ward_type
    }
    return render(request,'general_master/main_master.html',context)
def designation(request):
    form=DesignationForm()
    ward_type='ward_type'
    if request.method=='POST':
        form=DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/designation')
    context={
    'form':form,'ward_type':ward_type
    }
    return render(request,'general_master/main_master.html',context)

#=================QMS========================
def token_master_configuration(request):
    form=TokenMasterConfigurationForm()
    if request.method=='POST':
        form=TokenMasterConfigurationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/token_master_configuration')
        context={
        'form':form
        }
        return render(request,'qms/token_master_configuration.html',context)
    tmc=TokenMasterConf.objects.all()
    context={
    'form':form,'tmc':tmc
    }
    return render(request,'qms/token_master_configuration.html',context)

from django.contrib import messages#import Messages
def token_creation2(request):
    form=TokenCreationForm2()
    if request.method=='POST':
        form=TokenCreationForm2(request.POST)
        if form.is_valid():
            Date=request.POST.get('Date')
            Doct_Name=request.POST.get('Doct_Name')
            D_Name=form.cleaned_data['Doct_Name']
            Pt_Id=request.POST.get('Pt_Id')
            print('Doct Name',Doct_Name)
            searching_patient_id=BookedAppointments.objects.filter(patient_id__iexact=Pt_Id)
            searching_doctor_id=DoctorTable.objects.filter(doctor_id__iexact=Doct_Name)
            for data in searching_doctor_id:
                doc_id=data.doctor_id
                doc_name=data.doctor_name
                doc_speciality=data.doctor_department
                request.session['Date']=Date
                request.session['doc_id']=doc_id
                request.session['doc_name']=doc_name
                request.session['doc_speciality']=doc_speciality
            doc_id=request.session['doc_id']
            doc_name=request.session['doc_name']
            doc_speciality=request.session['doc_speciality']
            if searching_patient_id.exists():
                for data in searching_patient_id:
                    request.session['pt_id']=data.patient_id
                    request.session['pt_name']=data.patient_name
                form=TokenCreationForm3()
                pt_id=request.session['pt_id']
                pt_name=request.session['pt_name']
                get_max_token=TokenMasterConf.objects.filter(Date=date.today())&TokenMasterConf.objects.filter(Doct_Name=doc_id)
                get_booked_token=TokenCreationDone.objects.filter(Date=date.today())&TokenCreationDone.objects.filter(Doct_id=doc_id)
                booked_token=[]
                if get_booked_token.exists():
                    for data in get_booked_token:
                        booked_token.append(int(data.Token_No))
                print('booked_token',booked_token)
                tokens=None
                if get_max_token.exists():
                    for data in get_max_token:
                        print('data',data.Doct_Name)
                        assigned_token=data.Max_Token_Assigned
                    tokens=[]
                    for data in range(1,assigned_token+1):
                        tokens.append(data)
                    #Login to removing item from two dirrent list
                    print(f'Available Tokens{tokens},booked token {booked_token}')
                    res=list(set(tokens)^set(booked_token))
                    tokens=res
                tc=TokenCreationDone.objects.filter(Date=date.today())
                context={
                'doc_id':doc_id,'doc_name':doc_name,'doc_speciality':doc_speciality,'pt_id':pt_id,'pt_name':pt_name,'form':form,'token':tokens,'tc':tc,
                }
                return render(request,'qms/token_creation3.html',context)
    tc=TokenCreationDone.objects.filter(Date=date.today())
    context={
    'form':form,'tc':tc,
    }
    return render(request,'qms/token_creation2.html',context)
def token_creation(request):
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
        tcd=TokenCreationDone(Date=Date,Doct_id=doc_id,Doct_Name=Doct_Name,speciality=doc_speciality,Pt_Id=pt_id,Pt_Name=pt_name,Token_No=Token_No,Room_No=Room_No)
        tcd.save()
        return HttpResponseRedirect('/token_creation')
    doc_id=request.session['doc_id']
    tc=TokenCreationDone.objects.filter(Date=date.today())
    mtc=TokenMasterConf.objects.filter(Date=date.today())&TokenMasterConf.objects.filter(Doct_Name=doc_id)
    context={
    'tc':tc
    }
    return render(request,'qms/token_creation.html',context)




def token_slip_generation(request,pk):
    tc=TokenCreationDone.objects.get(id=pk)
    context={
    'tc':tc,
    }
    return render(request,'qms/token_slip_generation.html',context)
def centralised_admin_view(request):
    form=CentralisedAdminViewForm()
    token_creation=TokenCreationDone.objects.filter(Date=date.today())
    if request.method=='POST':
        form=CentralisedAdminViewForm(request.POST)
        if form.is_valid():
            Date=request.POST.get('Date')
            # Room_No=request.POST.get('room_number')
            Room_No=form.cleaned_data['room_number']
            Doctor_Name=form.cleaned_data['Doc_Name']
            # Doctor_Name=request.POST.get('Doc_Name')
            Max_Token=request.POST.get('Max_Token')
            Token_Issued=request.POST.get('Token_Issued')
            current_in=request.POST.get('current_in')
            next_waiting=request.POST.get('next_waiting')
            CentralisedAdminView.objects.create(Date=Date,Doc_Name=Doctor_Name,room_number=Room_No,Max_Token=Max_Token,Token_Issued=Token_Issued,Current_In=current_in,Next_Waiting=next_waiting)
            return HttpResponseRedirect('/centralised_admin_view')
    cav=TokenCreationDone.objects.filter(Date=date.today())
    context={
    'form':form,'token_creation':token_creation,'cav':cav
    }
    return render(request,'qms/centralised_admin_view.html',context)
def opd_reception_view(request):
    records=TokenCreationDone.objects.filter(Date=date.today())
    context={
    'records':records
    }
    return render(request,'qms/opd_reception_view.html',context)
def qms_dashboard(request):
    return render(request,'qms/qms_dashboard.html')
def create_room(request):
    form=RoomNumberForm()
    if request.method=='POST':
        form=RoomNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create-room')
    create_room='create_room'
    context={
    'form':form,'create_room':create_room
    }
    return render(request,'qms/main_master.html',context)
