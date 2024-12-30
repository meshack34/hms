from django.contrib.auth.models import User
from .models import *

def users_and_projects(request):
    if request.user.is_authenticated:
        #  user access
        access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
        # for pending vitals in clinical amangement
        pending_patient=0
        total_p=0
        prescrip_count = 0
        if request.location:
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
            pending_patient = records.count()
            total_p = VitalSign.objects.all().exclude(visit_id__in=PatientVisitMains.objects.values('visit_id').filter(status__in=['close','completed'])).count()
            prescrip_count = PreMedicine.objects.filter(status='pending').count()

            #  lab pendig investigation
            pending_investigation=PendingInvestigation_main.objects.filter(location=request.location)
            pending_investigation_count=len(set([data.PTID for data in pending_investigation]))
            return {'access': access,'pending_vitial_patient_counts':pending_patient,'total_patient_in_consultant_dashboard':total_p,'prescrip_count':prescrip_count,
                    'pending_investigation_count':pending_investigation_count
                    }
    else:
        access=''
    return {'access': access}