from django.shortcuts import render,redirect
from mainapp.models import *
# Create your views
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from testapp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from testapp.forms import *
from mainapp.models import *

@login_required(login_url='/user_login')
def select_location(request):
    all_branch = Client.objects.all()
    if request.method=='POST':
        request.session['admin_location']= int(request.POST.get('location'))
    
        return HttpResponseRedirect('/dashboard')
 
    return render(request,'user_management/select_location.html',{'all_branch':all_branch,'request':request})

# this is a tenants and domain creation function
def create_tenants(request):
    system_location = request.session['admin_location']
    if BranchRestrict.objects.all():
        branch_restrict = BranchRestrict.objects.get(branch_name = system_location)
    desclimer = None
    tenant1 = Client.objects.all()
    tenant2 = tenant1.count()
    all_domain = Domain.objects.all()
    domain1 = Domain.objects.first()
    both_details = zip(tenant1,all_domain)
    save_tenant = request.POST.get("save_btn")
    
    if request.method == "POST":
        if int(branch_restrict.branch_limit) >= tenant2: 
            if save_tenant == "Save":
                schema = request.POST.get("Schema_Name")
                name = request.POST.get("Branch")
                tenant = Client(schema_name=schema,name=name)
                tenant.save()
                domain_name = f"{name}.{domain1.domain}"
                domain=Domain(domain=domain_name.lower(),tenant=tenant,is_primary=True)
                domain.save()
                return HttpResponseRedirect("create_tenants")
        else:
            desclimer = "Limited"
    
    context = {
        "both_details":both_details,"desclimer":desclimer
    }
    return render(request,"mainapp/create_tenants.html",context)

# super admin signin function
def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            login(request, user)
            return redirect('user_login')  # Redirect to the home page or any other desired page
    else:
        form = UserForm()
    super_admin = User.objects.filter(is_superuser = True)
    if super_admin:
        return redirect("user_login_main")
    else:
        return render(request,"user_management/signup.html",{'form':form} )
        

def user_login_main(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('userName')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None :
                get_user_location = CreateUser.objects.filter(user_id=user).last()
                get_username = User.objects.get(username = user )
                if get_user_location is not None or get_username.is_superuser == True:
                    login(request, user)
                    print("get_user_location",get_user_location)
                    if request.user.is_superuser or get_username.is_superuser == True:
                        return redirect('select_location')
                    else:
                        return HttpResponseRedirect('/dashboard')
            else:
                messages.warning(request, 'Enter Valid Username or password.')
        return render(request, 'user_management/user_login.html')
    except Exception as error:
        return render(request, 'error.html', {'error': error})
    
@login_required(login_url='/user_login')
def create_userprofile(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or request.user.is_staff:
        # try:
        all_branches_location = Client.objects.all()
        desclimer = None
        no_of_patient_registered=CreateUser.objects.all().count()
        today = date.today()
        today = today.strftime("%y%m%d")
        current_location = request.session['admin_location']
        if len(str(no_of_patient_registered))==1:
            uhid='US'+today+str(current_location)+str(no_of_patient_registered)
        elif len(str(no_of_patient_registered))==2:
            uhid='US'+today+str(current_location)+str(no_of_patient_registered)
        elif len(str(no_of_patient_registered))==3:
            uhid='US'+today+str(current_location)+str(no_of_patient_registered)
        else:
            uhid='US'+today+str(current_location)+str(no_of_patient_registered)
        form = CreateUserForm(initial={'user_id': uhid})
        userform = UserForm(initial={'username': uhid})
        if request.method=='POST':
            system_location = request.session['admin_location']
            branch_restrict = BranchRestrict.objects.get(branch_name = system_location)
            created_user = CreateUser.objects.all().count()
            
            if int(branch_restrict.user_limit) >= created_user:
                user_first_name=request.POST.get('first_name')
                form=CreateUserForm(request.POST,request.FILES)
                if form.is_valid():
                    userform = UserForm(request.POST)
                  
                    if userform.is_valid():
                        print("userform")
                        user = userform.save(commit=False)
                        user.username=uhid
                        user.is_superuser = form.cleaned_data['is_admin']
                        user.save()
                        form.save()
                        user_rec=User.objects.get(username=uhid)
                        crea_user=CreateUser.objects.get(user_id=uhid)
                        crea_user.login_id_id=user_rec.id
                        crea_user.save()
                        messages.success(request, 'Successfully Created.....')
                        return HttpResponseRedirect("/create_userprofile")
                    else:
                        print(userform.errors)
                else:
                    print(form.errors)
            else:
                desclimer = "You can Create only Limited User"
        return render (request,'user_management/create_user.html',{'form':form,'userform':userform,'access':access,'desclimer':desclimer,'all_branches_location':all_branches_location})
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
    
@login_required(login_url='/user_login')
def view_create_userprofile(request):
    access = CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or request.user.is_staff:
        try:
            name=request.session['Name']
            records=CreateUser.objects.all()
            return render (request,'user_management/view_create_user.html',{'records':records,'login_name':name})
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
    
@login_required(login_url='/user_login')
def edit_create_userprofile(request,pk):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'user_managemnet' in access.user_profile.screen_access:
        try:
            name=request.session['Name']
            records=CreateUser.objects.get(id=pk)
            form=CreateUser_EditForm(instance=records)
            if request.method=='POST':
                form=CreateUser_EditForm(request.POST,request.FILES,instance=records)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/view_create_userprofile')
                else:
                    print(form.errors)
            context={
            'form':form,'records':records,'login_name':name
            }
            return render (request,'user_management/edit_create_user.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
    
@login_required(login_url='/user_login')
def search_create_user(request):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'user_managemnet' in access.user_profile.screen_access:
        try:
            name=request.session['Name']
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
                    'records':records,'success_search':success_search,'login_name':name
                    }
                    return render(request,'clinical/patient_search.html',context)
                except Exception as e:
                    # raise e
                    pass
            context={
            'records1':records1,'login_name':name
            }
            return render(request,'user_management/search_create_user.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')
    
@login_required(login_url='/user_login')
def create_user_delete(request,pk):
    try:
        records=CreateUser.objects.get(id=pk)
        records.delete()
        return  HttpResponseRedirect('/search_create_user')
    except Exception as error:
        return render(request,'error.html',{'error':error})
    
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/user_login')


