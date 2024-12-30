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
# from django.core.mail import send_mail
# Create your views here.
# def email_sending(request):
#     send_mail(
#     'Django Testing mail',
#     'Here is the message from django, Just Testing Purpose Im sending this',
#     'vikashkr1887@gmail.com',
#     ['ram.asfera2021@gmail.com'],
#     fail_silently=False,
#     )
#     return HttpResponse('<h1>Send Successfully</h1>')
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
        records=(DoctorTable.objects.filter(doctor_name__icontains=doctor_or_speciality)|DoctorTable.objects.filter(doctor_department=doctor_or_speciality))|DoctorTable.objects.filter(doctor_location__icontains=location)

        count=0
        if records.exists():
            for data in records:
                doctor_name=data.doctor_name
                doctor_id=data.doctor_id
                doctor_department=data.doctor_department
                doctor_location=data.doctor_location
                doctor_profile_image=data.doctor_profile_image
                doctor_appointment=data.doctor_appointment
                doctor_time_slot=data.doctor_time_slot
                count+=1
            context={'form':form,'doctor':doctor_or_speciality,'location':location,'calendars':calendars,'nmm':nmm,'pmm':pmm,'records':records,'no_of_doctor':count,'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment}
            response=render(request,'testapp/book_appointment.html',context)
            # response.set_cookie(doctor_location,doctor_department)
            request.session['doctor_id']=doctor_id
            request.session['doctor_name']=doctor_name
            request.session['doctor_department']=doctor_department
            request.session['doctor_location']=doctor_location
            request.session['doctor_profile_image']=str(doctor_profile_image)
            request.session['doctor_time_slot']=str(doctor_time_slot)
            return response
        else:
            records=DoctorTable.objects.all()
            for data in records:
                doctor_name=data.doctor_name
                doctor_id=data.doctor_id
                doctor_department=data.doctor_department
                doctor_location=data.doctor_location
                doctor_profile_image=data.doctor_profile_image
                doctor_appointment=data.doctor_appointment
                doctor_time_slot=data.doctor_time_slot
                count+=1
            context={'form':form,'doctor':doctor_or_speciality,'location':location,'calendars':calendars,'nmm':nmm,'pmm':pmm,'records':records,'no_of_doctor':count,'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment}
            response=render(request,'testapp/book_appointment.html',context)
            # response.set_cookie(doctor_location,doctor_department)
            request.session['doctor_id']=doctor_id
            request.session['doctor_name']=doctor_name
            request.session['doctor_department']=doctor_department
            request.session['doctor_location']=doctor_location
            request.session['doctor_profile_image']=str(doctor_profile_image)
            request.session['doctor_time_slot']=str(doctor_time_slot)
            return response
    return render(request,'testapp/book_appointment.html')
def mobile_register(request):
    doctor_appointment=request.POST.get('doctor_appointment')
    choose_doctor=request.POST.get('choose_doctor')
    if choose_doctor is not None:
        records=DoctorTable.objects.get(doctor_id=choose_doctor)
        doctor_id=records.doctor_id
        doctor_name=records.doctor_name
        doctor_department=records.doctor_department
        doctor_location=records.doctor_location
        doctor_profile_image=records.doctor_profile_image
        # response.set_cookie(doctor_location,doctor_department)
        request.session['doctor_id']=doctor_id
        request.session['doctor_name']=doctor_name
        request.session['doctor_department']=doctor_department
        request.session['doctor_location']=doctor_location
        request.session['doctor_profile_image']=str(doctor_profile_image)
    request.session['doctor_appointment']=str(doctor_appointment)
    doctor_name=request.session['doctor_name']
    doctor_department=request.session['doctor_department']
    doctor_location=request.session['doctor_location']
    doctor_profile_image=request.session['doctor_profile_image']
    doctor_appointment=request.session['doctor_appointment']
    doctor_id=request.session['doctor_id']
    today=date.today()
    context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment}
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
    doctor_time_slot=request.session['doctor_time_slot']
    mobile_number=request.session['mobile_number']
    name=request.session['name']
    records=AvailabilityIntradayScheduleMaster.objects.filter(doctor_id=doctor_id)
    records2=BookedAppointments.objects.all().only('patient_scheduled_id')
    records3=[]
    records4=[]
    for data in records:
        data=data.time_slot_id
        records3.append(data)
    for data2 in records2:
        data=data2.patient_scheduled_id
        records4.append(data)
    #Generate Schedule
    fresh_schedule=[]
    for item in records3:
        if item not in records4:
            fresh_schedule.append(item)
    records=AvailabilityIntradayScheduleMaster.objects.filter(time_slot_id__in=fresh_schedule)
    time_slot_lists='time_slots'
    context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'doctor_time_slot':doctor_time_slot,'name':name,'time_slots':time_slot_lists,'records':records}
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
    context={'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'scheduled':scheduled, 'mobile_number':mobile_number,'name':name}
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
    reference_mobile_number=mobile_number
    base_price=700
    without_discount=700
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
            if no_of_member !=0:
                without_discount=base_price*(no_of_member+1)
                with_discount=without_discount*(90/100)
            base_price=700
            without_discount=700
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
    base_price=700
    without_discount=700
    with_discount=630
    context={
    'doctor_name':doctor_name,'doctor_department':doctor_department,'doctor_location':doctor_location,'doctor_profile_image':doctor_profile_image,'doctor_appointment':doctor_appointment,'records_of_members':records_of_members, 'mobile_number':mobile_number,'name':name,'scheduled':scheduled,'without_discount':without_discount,'with_discount':with_discount,
    }
    return render(request,'testapp/booking_detail.html',context)
def doctor_view(request):
    form=DoctorTableForm()
    records=DoctorTable.objects.all()
    success='success'
    if request.method=='POST':
        form=DoctorTableForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
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
class DoctorDeleteView(DeleteView):
    model=DoctorTable
    template_name='patient/doctortable_confirm_delete.html'
    success_url=reverse_lazy('delete')
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
    form=BookedAppointmentsForm(instance=records_patient_id)
    if request.method=='POST':
        form=BookedAppointmentsForm(request.POST,instance=records_patient_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/appointment_table')
    return render(request,'patient/cancel_appointment.html',{'form':form})

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
    return render(request,'patient/admin_list_table.html')
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
    p_ids= randint(111111,999999)
    appointment_id=randint(100000000,9999999999)
    patient_id='patient'+str(p_ids)
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
    for data in scheduled_date_list:
        count=0
        for times in get_time_list:
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
        print(f'consultant:=> {consultant}, department:=> {department}')
        filtering_records=BookedAppointments.objects.filter(Q(doctor_name=consultant)|Q(doctor_department=department))
        filtered='filter'
        context={
        'records':records,'filtered':filtered,'filtering_records':filtering_records,
        }
        return render(request,'testapp/shorting_filter.html',context)
    context={
    'records':records
    }
    return render(request,'testapp/shorting_filter.html',context)
def appointment_detail_reports(request):
    records=BookedAppointments.objects.all()
    context={
    'records':records,
    }
    return render(request,'testapp/appointment_detail_reports.html',context)
#Updated
def login(request):
    return render(request,'interface/login.html')
def box(request):
    return render(request,'interface/box.html')
def modal(request):
    return render(request,'interface/modal.html')
def table(request):
    return render(request,'interface/table.html')
#doctor admdin pannel
def doctor_admin_pannel(request):
    return HttpResponseRedirect('/accounts/login')
