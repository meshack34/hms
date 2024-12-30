#Exceptional Handeling
def exceptional_handeling():
    try:
       if request.user.is_superuser:
            return render(request,'clinical/dashboard.html')
        elif request.user.is_authenticated:
            access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
            context={
                'access':access
            }
            return render(request,'clinical/dashboard.html',context)
        else:
            return redirect('user_login_main')
        
    except Exception as error:
        print('Except Block ')
        print('Error ',error)
    else:
        print("'ELSE BLOCK: 'I'm always with try block")
    finally:
        print("'FINALLY BLOCK ', I'm sutable for try and except both,,, I don't have any restriction")
        
exceptional_handeling()

@login_required(login_url='/user_login')

access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'user_managemnet' in access.user_profile.screen_access:
        try:

except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

'access':access

{% endif %}
{% if 'patient_registration_add' in access.user_profile.screen_access or request.user.is_superuser %}
{% endif %}



try:
    except Exception as error:
        return render(request,'error.html',{'error':error})
    
    
    
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    
    created_by_id=request.user.id,location_id=request.location,
    
    location=request.location

