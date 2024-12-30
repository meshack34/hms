from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from testapp.models import *
from usermanagementapp.forms import *
from usermanagementapp.models import *
from encrypt_util import *
from django.contrib.auth.decorators import login_required

# Create your views here.

#  karan 18-03-2023
@login_required(login_url='/user_login')
def screen_access_view(request):
    records = ScreenAccess.objects.all()
    return render(request,'user_management/screen_access_view.html',{'records':records})

@login_required(login_url='/user_login')
def screen_access(request):
    if request.method=='POST':
        ScreenAccess.objects.create(
            group_name=request.POST.get('group_name'),
            screen_access=request.POST.getlist('access'),
            status='Active'
        )
        return redirect('screen_access_view')
    return render(request,'user_management/screen_access.html')

@login_required(login_url='/user_login')
def screen_access_edit(request,pk):
    record=ScreenAccess.objects.get(id=pk)
    if request.method=='POST':
        record.screen_access=request.POST.getlist('access')
        record.save()
        return redirect('screen_access_view')
    return render(request,'user_management/screen_access_edit.html',{'record':record})
#  end 18-03-2023

@login_required(login_url='/user_login')
def user_management(request):

    form = UserMangementForm()
    return render(request,"user_management/user_management.html",{'form':form})


@login_required(login_url='/user_login')
def user_management_acess(request,pk):

    create_user_records = CreateUser.objects.get(user_id=pk)
    ad=UserMangement.objects.all()
    ad_uhid=[data.user_id for data in ad]
    print()
    if pk in ad_uhid:
        records=UserMangement.objects.get(user_id=pk)
        form=UserMangementForm(instance=records)
        if request.method=='POST':
            form=UserMangementForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/usermanagementapp/user_management')
    else:
        user_id=create_user_records.user_id
        user_name=create_user_records.first_name
        dob=create_user_records.date_of_birth
        DOB=dob.strftime("%y%m%d")
        cap_name=user_name.upper()
        user_password=cap_name[:4]+DOB
        print(user_password)
        form = UserMangementForm(initial={'user_id': user_id,'user':user_name,'password':encrypt(user_password)})
        if request.method=='POST':
            form=UserMangementForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/usermanagementapp/user_management')
            else:
                print(form.errors)
    context={
        'form':form
    }
    return render(request,"user_management/user_management.html",context)

@login_required(login_url='/user_login')
def user_management_edit(request,pk):

    records=UserMangement.objects.get(id=pk)
    print('records',records)
    form=UserMangementForm(instance=records)
    if request.method=='POST':
        form=UserMangementForm(request.POST,instance=records)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/usermanagementapp/user_management')
    context={
    'form':form,'records':records
    }
    return render (request,'user_management/user_management.html',context)

@login_required(login_url='/user_login')
def user_management_details(request):

    records = UserMangement.objects.all()
    print(records)
    return render (request,'user_management/user_management_details.html',{'records':records})

@login_required(login_url='/user_login')
def user_management_delete(request,pk):
    records = UserMangement.objects.get(id=pk)
    records.delete()
    return HttpResponseRedirect('/usermanagementapp/user_management_details')

@login_required(login_url='/user_login')
def ward_search(request):

    records1=CreateUser.objects.all()
    if request.method=='POST':
        uhid=request.POST.get('uhid')
        patient_name=request.POST.get('patient_name')
        get_dob=request.POST.get('dob')
        mobile_number=request.POST.get('mobile_number')
        if uhid == '':
            uhid="Not Provided"
        if patient_name == '':
            patient_name="Not Provided"
        if get_dob == '':
            get_dob=date.today()
        if mobile_number == '':
            mobile_number="Not Provided"
        try:
            records=CreateUser.objects.filter(Q(uhid__exact=uhid)|Q(dob__exact=get_dob)|Q(mobile_number__exact=mobile_number))
            print('records',records.count())
            success_search='success'
            context={
            'records':records,'success_search':success_search
            }
            return render(request,'clinical/patient_search.html',context)
        except Exception as e:
            # raise e
            pass
    context={
    'records1':records1
    }
    return render(request,'user_management/ward_access_search.html',context)

@login_required(login_url='/user_login')
def ward_page(request):

    records=UserMangement_ward.objects.all()
    form=UserMangement_wardForm()
    if request.method=='POST':
        form=UserMangement_wardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/usermanagementapp/ward_access')
    context={
    'form':form,'records':records
    }
    return render (request,'user_management/ward_access.html',context)

@login_required(login_url='/user_login')
def ward_access_edit(request,pk):

    ward_records=DummyForm()
    create_user_records = CreateUser.objects.get(user_id=pk)
    ad=UserMangement_ward.objects.all()
    ad_uhid=[data.user_id for data in ad]
    print()
    if pk in ad_uhid:
        records=UserMangement_ward.objects.get(user_id=pk)
        form=UserMangement_wardForm(instance=records)
        if request.method=='POST':
            form=UserMangement_wardForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/usermanagementapp/ward_access')
    else:
        user_name=create_user_records.f_name
        dob=create_user_records.date_of_birth
        DOB=dob.strftime("%y%m%d")
        cap_name=user_name.upper()
        user_password=cap_name[:4]+DOB
        form = UserMangement_wardForm(initial={'user_id': create_user_records.user_id,'user':create_user_records.f_name,'password':encrypt(user_password)})
        if request.method=='POST':
            user_id=request.POST.get('user_id')
            user=request.POST.get('user')
            password=request.POST.get('password')
            ward_cat=request.POST.getlist('ward_cat')
            data=UserMangement_ward(user_id=user_id,user=user,password=password,ward_cat=ward_cat)
            data.save()
            return HttpResponseRedirect('/usermanagementapp/ward_access')
        else:
            print(form.errors)
    context={
        'form':form,'ward_records':ward_records
    }
    return render(request,"user_management/ward_access.html",context)

@login_required(login_url='/user_login')
def lab_access(request):

    form=LabAccessForm()
    if request.method=='POST':
        form=LabAccessForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/usermanagementapp/lab_access')
    context={
        'form':form
    }
    return render(request,"user_management/lab_access.html",context)


@login_required(login_url='/user_login')
def lab_search(request):

    records1=CreateUser.objects.all()
    if request.method=='POST':
        uhid=request.POST.get('uhid')
        patient_name=request.POST.get('patient_name')
        get_dob=request.POST.get('dob')
        mobile_number=request.POST.get('mobile_number')
        if uhid == '':
            uhid="Not Provided"
        if patient_name == '':
            patient_name="Not Provided"
        if get_dob == '':
            get_dob=date.today()
        if mobile_number == '':
            mobile_number="Not Provided"
        try:
            records=CreateUser.objects.filter(Q(uhid__exact=uhid)|Q(dob__exact=get_dob)|Q(mobile_number__exact=mobile_number))
            print('records',records.count())
            success_search='success'
            context={
            'records':records,'success_search':success_search
            }
            return render(request,'clinical/patient_search.html',context)
        except Exception as e:
            # raise e
            pass
    context={
    'records1':records1
    }
    return render(request,'user_management/lab_search.html',context)

@login_required(login_url='/user_login')
def lab_doctor_search(request):

    records1=DoctorTable.objects.all()
    context={
    'records1':records1
    }
    return render(request,'user_management/doctor_search.html',context)

@login_required(login_url='/user_login')
def lab_access_add(request,pk):

    ad=LabAccess.objects.all()
    ad_uhid=[data.user_id for data in ad]
    create_user_records = CreateUser.objects.get(user_id=pk)
    if pk in ad_uhid:
        print('if')
        records=LabAccess.objects.get(user_id=pk)
        form=LabAccessForm(instance=records)
        if request.method=='POST':
            form=LabAccessForm(request.POST,instance=records)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/usermanagementapp/lab_access')
    else:
        print('else')
        form = LabAccessForm(initial={'user_id': create_user_records.user_id,'user':create_user_records.f_name})
        if request.method=='POST':
            print('if 1')
            form=LabAccessForm(request.POST)
            if form.is_valid():
                print('if 2')
                form.save()
                return HttpResponseRedirect('/usermanagementapp/lab_access')
            else:
                print(form.errors)
    context={
        'form':form
    }
    return render(request,"user_management/lab_access.html",context)

@login_required(login_url='/user_login')
def lab_access_add2(request,pk):

    ad=LabAccess.objects.all()
    ad_uhid=[data.user_id for data in ad]
    doctor_records = DoctorTable.objects.get(doctor_id=pk)
    if pk in ad_uhid:
        print('if')
        records=LabAccess.objects.get(user_id=pk)
        form=LabAccessForm(instance=records)
        if request.method=='POST':
            form=LabAccessForm(request.POST,instance=records)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/usermanagementapp/lab_access')
    else:
        print('else')
        form = LabAccessForm(initial={'user_id': doctor_records.doctor_id,'user':doctor_records.doctor_name})
        if request.method=='POST':
            print('if 1')
            form=LabAccessForm(request.POST)
            if form.is_valid():
                print('if 2')
                form.save()
                return HttpResponseRedirect('/usermanagementapp/lab_access')
            else:
                print(form.errors)
    context={
        'form':form
    }
    return render(request,"user_management/lab_access.html",context)