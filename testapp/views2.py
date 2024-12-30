from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from testapp.forms import *
from testapp.models import *
from django.http import HttpResponse,HttpResponseRedirect
import razorpay
from django.contrib.auth.decorators import login_required
from testapp.models import OpdPayment
from testapp.serializers import *
from usermanagementapp.models import *
from django.contrib.auth import authenticate, login, logout
from OpdManagement import utils as utils_response
from datetime import datetime
from django.contrib import messages
import random
from django.http import JsonResponse
from django.db.models import Sum,Q

def discharge_medi_delete(request,uhid_visit,id):
    DialysisDishchargeMedicine.objects.get(id=id).delete()
    return HttpResponseRedirect(f'/post_dialysis_discharge/{uhid_visit}')
def discharge_prescription_delete(request,uhid_visit,id):
    DialysisPrescription.objects.get(id=id).delete()
    return HttpResponseRedirect(f'/post_dialysis_discharge/{uhid_visit}')
def discharge_post_medi_delete(request,uhid_visit,id):
    PostDialysisDishchargeMedicine.objects.get(id=id).delete()
    return HttpResponseRedirect(f'/post_dialysis_discharge/{uhid_visit}')

def dialysis_report_chart(request,pk):
    uh_visit_id = pk.split('-')
    uhid_p = uh_visit_id[0]
    visit_id = uh_visit_id[1]
    difference_wt = None
    pat_details=PatientsRegistrationsAllInOne.objects.filter(uhid=uhid_p).extra(select={
    'pat_billing': 'Select billing_group from testapp_BillingGroup where id=testapp_patientsregistrationsallinone.billing_group',
    }).last()
    pre_dialysis=Pre_Dialysis_Details.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
    if pre_dialysis is not None:
        if pre_dialysis.measured_wt != '' and pre_dialysis.previous_wt != '':
            difference_wt=float(pre_dialysis.measured_wt)-float(pre_dialysis.previous_wt)
        else:
            difference_wt=''
    post_dialysis=Post_Dialysis_Details.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
    pre_equip_records=PreEquipPreparationPreDialysis.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
    if pre_equip_records is not None:
        a=pre_equip_records.name.all()
        listt=[data.name for data in a]
    else:
        listt=[]
    post_equip_intra=PostEquip_preparation.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
    assessment_records = PreDialysisAssessment.objects.filter(uhid=uhid_p,visit_id=visit_id).last()
    intra_records_per_hour = IntraDialysisPerHourInput.objects.filter(uhid=uhid_p,visit_id=visit_id)
    if intra_records_per_hour is not None:
        conductivity=intra_records_per_hour.last().conductivity
        start_time=intra_records_per_hour.first().time
        end_time=intra_records_per_hour.last().time
    else:
        conductivity=''
        start_time=''
        end_time=''
    post_add_drug = AddDrugs_Dialysis.objects.filter(uhid=uhid_p,visit_id=visit_id)
    print('conductivity---->,',conductivity)
    if post_equip_intra is not None:
        b=post_equip_intra.post_preparation.all()
        list2=[data.post_equip_name for data in b]
    else:
        list2=[]
    context={
        'pat_details':pat_details,'pre_dialysis':pre_dialysis,'post_dialysis':post_dialysis,'pre_equip_records':pre_equip_records,
        'listt':listt,'list2':list2,'assessment_records':assessment_records,'intra_records_per_hour':intra_records_per_hour,
        'post_add_drug':post_add_drug,'end_time':end_time,'conductivity':conductivity,'difference_wt':difference_wt,'start_time':start_time,
    }
    return render(request,'dialysis/dialysis_report_chart.html',context)

def view_packages_services(request,pid):
    package=OpdPackageService.objects.filter(package_id=pid)
    context={
        'package':package
    }
    return render(request,'general_master/opd_package/view_packages_services.html',context)

def opd_package_service_edit(request,pid):

    package_master=OpdPackageService_main.objects.get(package_id=pid)
    package_amount = package_master.after_total_amt
    service_master = ServiceMaster.objects.all()
    service_item = [data.service_name for data in service_master]
    profile_master = ProfileMaster.objects.all()
    profile_item = [data.profile_name for data in profile_master]
    records = OpdPackageService.objects.filter(package_id=pid)
    pack_name=records.first().package_name
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
    print('total', total, before_total)
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
        quantity = request.POST.getlist('quantity')
        discount = request.POST.getlist('discount')
        rate = request.POST.getlist('rate')
        net_amount = request.POST.getlist('n_amount')
        total_net_amount = request.POST.get('total_amount')
        records_getting = OpdPackageService_temp.objects.filter(id__in=service_name)
        total_discount = 0
        for data in discount:
            total_discount = int(data) + total_discount
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
            print()

            for dat in records_getting:
                opd_package_sub = OpdPackageService.objects.get_or_create(
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
            return HttpResponseRedirect('/opd_package_service')

        if preview == 'preview':
            if float(package_amount) == float(total_net_amount):
                records = ''

                preview_record = OpdPackageService.objects.filter(package_id=pid)
            else:
                messages.success(request, 'Total amount is not Balanced to package amoount....!')

    context = {
        'package_name': pack_name, 'service_item': service_item,'profile_item':profile_item,
        'total': total, 'tot_id_len': tot_id_len, 'id_start': id_start, 'id_count': id_count,
        'records_discount': records_discount, 'records_id': records_id,'pid':pid,
        'preview': preview_record, 'total_net_amount': total_net_amount, 'total_discount': total_discount,
        'before_total': before_total, 'package_amount': package_amount,'profile_master':profile_master,
        'msg': msg,'records':records,'service_master':service_master,
    }
    return render(request, 'general_master/opd_package/opd_package_service_edit.html', context)



def opd_package_service_add(request,serv,pid):
    edit=True
    service_name = ServiceMaster.objects.get(id=serv)
    service_master = ServiceMaster.objects.all()
    records = OpdPackageService.objects.filter(package_id=pid)
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        rate = request.POST.get('rate')
        net_amount = request.POST.get('net_amount')
        temp_data = OpdPackageService(
            package_id=pid,
            service_department_id=records.first().service_department.id,
            service_sub_department_id=records.first().service_sub_department.id,
            package_name_id=records.first().package_name.id,
            service_name_id=service_name,
            quantity=quantity,
            discount=discount,
            rate=rate,
            net_amount=net_amount,
            status='service_name',
        )
        temp_data.save()
        return HttpResponseRedirect(f'/opd_package_service_edit/{pid}')
    context = {
        'service_name': service_name,'package_name': records.first().package_name, 'service_master': service_master, 'records': records,
        'edit':edit
    }
    return render(request, 'general_master/opd_package/opd_package_service.html', context)


def opd_package_profile_add(request,serv,pid):
    edit=True
    profile_name = ProfileMaster.objects.get(id=serv)
    service_master_all = ServiceMaster.objects.all()
    item = [data.service_name for data in service_master_all]
    records = OpdPackageService.objects.filter(package_id=pid)

    if request.method == 'POST':
        prifiles_name = request.POST.get('service_name')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        rate = request.POST.get('rate')
        net_amount = request.POST.get('net_amount')
        temp_data = OpdPackageService(
            package_id=pid,
            service_department_id=records.first().service_department.id,
            service_sub_department_id=records.first().service_sub_department.id,
            package_name_id=records.first().package_name.id,
            profile_name_id=prifiles_name,
            quantity=quantity,
            discount=discount,
            rate=rate,
            net_amount=net_amount,
            status='profile_name',
        )
        temp_data.save()
        return HttpResponseRedirect(f'/opd_package_service_edit/{pid}')
    context = {
        'profile_name': profile_name, 'package_name': records.first().package_name, 'item': item, 'records': records,'edit':edit
    }
    return render(request, 'general_master/opd_package/opd_package_service.html', context)

def opd_service_delete(request,pk,pid):
    OpdPackageService.objects.get(id=pk).delete()
    return HttpResponseRedirect(f'/opd_package_service_edit/{pid}')

def previuos_dialysis_details(request):
    records=PostDialysisDischargeSheet.objects.all().order_by('-id').extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_PostDialysisDischargeSheet.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PostDialysisDischargeSheet.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PostDialysisDischargeSheet.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PostDialysisDischargeSheet.uhid',
            'visit_date': 'Select visit_date_time from testapp_PatientVisitMains where visit_id=testapp_PostDialysisDischargeSheet.visit_id',
        })
    return render(request,'dialysis/previuos_dialysis_details.html',{'records':records})

# lab_sales_report with group by
def lab_revenue_report(request):
    records = ''
    toatal = ''
    from_date=request.POST.get('b_start_date')
    to_date=request.POST.get('b_end_date')
    if from_date and to_date:
        from_date=request.POST.get('b_start_date').split("T")[0]
        to_date=request.POST.get('b_end_date').split("T")[0]
        billing_records=OpdBillingSub.objects.filter(location=request.location,service_category__in=['Investigation','Packages'],service_sub_category__in=['Lab Investigation','Package Charges'],bill_date_time__range=[from_date,to_date]).order_by('bill_no')
        bill_no_list=list(set([data.bill_no for data in billing_records]))
        records=[]
        department=ServiceSubDepartment.objects.all()
        toatal=0
        for dep in department:
            # for bill in bill_no_list:
            billing_record=OpdBillingSub.objects.filter(service_category__in=['Investigation','Packages'],service_sub_category__in=['Lab Investigation','Package Charges'],bill_date_time__range=[from_date,to_date]).order_by('service_id')
            for data in billing_record:
                # for dep in department:
                dict={}
                package=OpdPackageService.objects.filter(package_name__package_name__icontains=data.service_id,service_sub_department=dep).last()
                patient=PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
                profile=ProfileService.objects.filter(profile_name__exact=data.service_id,service_sub_department=dep).last()
                serivce=ServiceMaster.objects.filter(service_name__exact=data.service_id,ServiceSubDepartment=dep).last()
                if package or profile or serivce:
                    dict['uhid']=data.uhid
                    dict['bill_no']=data.bill_no
                    dict['bill_date_time']=data.bill_date_time
                    dict['visit_no']=data.visit_no
                    dict['charges']=int(data.charges)
                    toatal+=int(data.charges)
                    dict['discount']=data.discount
                    dict['first_name']=patient.first_name
                    dict['middle_name']=patient.middle_name
                    dict['last_name']=patient.last_name
                    dict['age']=str(patient.age )+ ' / ' + patient.gender[0]
                    if package:
                        dict['service_name']=package.package_name
                        dict['sub_department']=dep
                    elif profile:
                        dict['service_name']=data.service_id
                        dict['sub_department']=dep
                    elif serivce:
                        dict['service_name']=data.service_id
                        dict['sub_department']=dep

                    records.append(dict)

        return render(request, 'lab_module/lab_revenue_report.html',{'records':records,'toatal':toatal,'from_date':from_date,'to_date':to_date})
    return render(request, 'lab_module/lab_revenue_report.html')



# lab_sales_report without group by
def lab_sales_report(request):
    records = ''
    toatal = ''
    from_date=request.POST.get('b_start_date')
    to_date=request.POST.get('b_end_date')
    if from_date and to_date:
        from_date=request.POST.get('b_start_date').split("T")[0]
        to_date=request.POST.get('b_end_date').split("T")[0]
        billing_records=OpdBillingSub.objects.filter(location=request.location,service_category__in=['Investigation','Packages'],service_sub_category__in=['Lab Investigation','Package Charges'],bill_date_time__range=[from_date,to_date]).order_by('bill_no')
        bill_no_list=list(set([data.bill_no for data in billing_records]))
        records=[]
        department=ServiceSubDepartment.objects.all()
        toatal=0
        for dep in department:
            # for bill in bill_no_list:
            billing_record=OpdBillingSub.objects.filter(service_category__in=['Investigation','Packages'],service_sub_category__in=['Lab Investigation','Package Charges'],bill_date_time__range=[from_date,to_date]).order_by('service_id')
            for data in billing_record:
                # for dep in department:
                dict={}
                package=OpdPackageService.objects.filter(package_name__package_name__icontains=data.service_id,service_sub_department=dep).last()
                patient=PatientsRegistrationsAllInOne.objects.get(uhid=data.uhid)
                profile=ProfileService.objects.filter(profile_name__exact=data.service_id,service_sub_department=dep).last()
                serivce=ServiceMaster.objects.filter(service_name__exact=data.service_id,ServiceSubDepartment=dep).last()
                if package or profile or serivce:
                    dict['uhid']=data.uhid
                    dict['bill_no']=data.bill_no
                    dict['bill_date_time']=data.bill_date_time
                    dict['visit_no']=data.visit_no
                    dict['charges']=int(data.charges)
                    toatal+=int(data.charges)
                    dict['discount']=data.discount
                    dict['billing_dept']=data.department
                    dict['first_name']=patient.first_name
                    dict['middle_name']=patient.middle_name
                    dict['last_name']=patient.last_name
                    dict['age']=str(patient.age )+ ' / ' + patient.gender[0]
                    if package:
                        dict['service_name']=package.package_name
                        dict['sub_department']=dep
                        dict['department']=package.service_department
                    elif profile:
                        dict['service_name']=data.service_id
                        dict['sub_department']=dep
                        dict['department']=profile.service_department
                    elif serivce:
                        dict['service_name']=data.service_id
                        dict['sub_department']=dep
                        dict['department']=serivce.service_department

                    records.append(dict)

        return render(request, 'lab_module/lab_sales_report.html',{'records':records,'toatal':toatal,'from_date':from_date,'to_date':to_date})
    return render(request, 'lab_module/lab_sales_report.html')

    #========================= Some Code Transfer ===================================

def daily_billing_report(request):
    if request.method=="POST":
        bill_start_date=request.POST.get('b_start_date')
        bill_end_date=request.POST.get('b_end_date')
        records = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).order_by('-bill_no')
        cancel_bill_records = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],status='cancel',location=request.location).order_by('-bill_no').count()
        record=[]
        total_paid_amount=0
        for data in records:
            dict={}
            patient_record=PatientsRegistrationsAllInOne.objects.filter(uhid=data.uhid).last()
            patient_visit=PatientVisitMains.objects.filter(uhid=data.uhid,visit_id=data.visit_no).last()
            dict['uhid']=data.uhid
            dict['visit_no']=data.visit_no
            dict['patient_name']=patient_record.first_name + ' ' + patient_record.last_name
            if data.corporate_id == 'Cash':
                dict['billing_group']=data.corporate_id
            else:
                cop_record=CorporateMaster.objects.filter(id=data.corporate_id).last()
                dict['billing_group']=cop_record.corporate_Name
            dict['bill_no']=data.bill_no
            dict['net_amount']=data.net_amount
            #===================== New If ====================
            if patient_visit!= None:
                dict['department']=patient_visit.clinical_department
            else:
                dict['department'] = ''
            #====================== END =========================
            dict['lou_no']=data.lou_no
            if patient_record.referred_by == 'Walked By':
                dict['refer_by']=patient_record.referred_by
            else:
                refer_record=Refered_by_Master.objects.filter(id=patient_record.referred_by).last()
                dict['refer_by']=refer_record.Staff_name
            payment_record=OpdPayment.objects.filter(bill_id=data.bill_no).last()
            # print('payment_record--->,',payment_record)
            # if data.payment_mode == 'CASH':
            if payment_record is not None:
                dict['payment_mode']=payment_record.mode_type
                dict['paid_amount']=data.paid_amount
                dict['status']='Close'
                total_paid_amount+=int(data.paid_amount)
                dict['clam_no']=''
                dict['batch_no']=''
            else:
                dict['payment_mode']='CREDIT'
                dict['paid_amount']=data.paid_claim_amt
                dict['status']='Finalized'
                dict['clam_no']=data.claim_no
                if data.batch_no == None:
                    dict['batch_no']=''
                else:
                    dict['batch_no']=data.batch_no
                total_paid_amount+=int(data.paid_claim_amt)
            if data.status == 'cancel':
                dict['status'] = data.status
            visit=PatientVisitMains.objects.filter(uhid=data.uhid,visit_id=data.visit_no).last()
            #======================= New If ============================
            if visit != None:
                dict['doctor'] = visit.doctor
            else:
                dict['doctor'] = ''
            #================================ END =============================
            record.append(dict)
        temp_record = OpdBillingTemper.objects.filter(created_at__range=[bill_start_date,bill_end_date],location=request.location)
        patient_uhid=list(set([data.uhid for data in temp_record]))
        open_net_amount=0
        for data in patient_uhid:
            visit=temp_record.filter(uhid=data)
            vist_list=list(set([data.visit_no for data in visit]))
            for vst in vist_list:
                dict={}
                filnial_rcord=temp_record.filter(uhid=data,visit_no=vst).last()
                open_net_amount+=int(filnial_rcord.net_ammount)
                patient_record=PatientsRegistrationsAllInOne.objects.filter(uhid=filnial_rcord.uhid).last()
                dict['uhid']=filnial_rcord.uhid
                dict['patient_name']=patient_record.first_name + ' ' + patient_record.last_name
                if patient_record.nhif_ins_cor_name == 'Cash':
                    dict['billing_group']=patient_record.nhif_ins_cor_name
                    dict['payment_mode']='CASH'
                else:
                    cop_record=CorporateMaster.objects.filter(id=patient_record.nhif_ins_cor_name).last()
                    dict['billing_group']=cop_record.corporate_Name
                    dict['payment_mode']='CREDIT'

                dict['paid_amount']=0
                dict['status']='Open Bill'
                dict['clam_no']=''
                dict['batch_no']=''
                dict['bill_no']=filnial_rcord.Pr_Opd_sr_bill_no
                dict['net_amount']=filnial_rcord.net_ammount

                dict['lou_no']=''
                if patient_record.referred_by == 'Walked By':
                    dict['refer_by']=patient_record.referred_by
                else:
                    refer_record=Refered_by_Master.objects.filter(id=patient_record.referred_by).last()
                    dict['refer_by']=refer_record.Staff_name
                visit=PatientVisitMains.objects.filter(visit_id=vst).last()
                dict['doctor']=visit.doctor
                dict['department']=visit.clinical_department
                record.append(dict)

        #========================== To Calculate Total Amt 24/04/23 ======================================================
        net_amt = OpdBillingMain.objects.filter(bill_date_time__range=[bill_start_date,bill_end_date],location=request.location).exclude(status='cancel')\
            .aggregate(Sum('net_amount'))
        net_amt = net_amt['net_amount__sum']+open_net_amount
        #========================= For Pharmacy Bill 22/06/2023 =====================================
        pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash').extra(select={
            'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
            'reffered_by': 'Select referred_by from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
        }).order_by("-uhid")
        refer_by_list=[]
        for refer_by in pharmacy_records:
            if refer_by.reffered_by == 'Walked By' or refer_by.reffered_by == None  :
                refer_by_list.append('Walked By')
            else:
                refer=Refered_by_Master.objects.filter(id=refer_by.reffered_by).last()
                refer_by_list.append(refer.Staff_name)
        pharmacy_records_zip=zip(pharmacy_records,refer_by_list)
        #============================================= Total Amount Calculation Pharnacy ========================================
        net_amt_pharma = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash')\
            .aggregate(Sum('total_taxable_amount'))
        net_amt_pharma = net_amt_pharma['total_taxable_amount__sum']

        paid_amt_pharma = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash')\
            .aggregate(Sum('paid_amount'))
        paid_amt_pharma = paid_amt_pharma['paid_amount__sum']
        if net_amt == None:
            net_amt = 0
        if net_amt_pharma== None:
            net_amt_pharma = 0
        if total_paid_amount== None:
            total_paid_amount = 0
        if paid_amt_pharma == None:
            paid_amt_pharma = 0
        grand_net_amt=net_amt+net_amt_pharma
        grand_paid_amt=total_paid_amount+paid_amt_pharma
        #================================ END ====================================================================================
        context={
            'records_1':records,'net_amt':net_amt,'total_paid_amount':total_paid_amount,'record':record,'from_date':bill_start_date,'to_date':bill_end_date,
            'pharmacy_records':pharmacy_records_zip,'net_amt_pharma':net_amt_pharma,'paid_amt_pharma':paid_amt_pharma,'grand_net_amt':grand_net_amt,
            'grand_paid_amt':grand_paid_amt,
        }
        return render(request,'clinical/details_revenue_report2.html',context)
    return render(request,'clinical/details_revenue_report2.html')


def monthly_report(request):
    record_detail=''
    to_date=''
    from_date=''
    net_amount=0
    record_tempdetail = ''
    pharmacy_records = ''
    grand_total=0
    pharmacy_net_amt=0
    opd_main_data=0
    if request.method == 'POST':
        from_date=request.POST.get('b_start_date')
        to_date=request.POST.get('b_end_date')
        records = OpdBillingSub.objects.extra(select={
                'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingsub.uhid',
                'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingsub.uhid',
                'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingsub.uhid',
            }).filter(bill_date_time__range=[from_date,to_date],location=request.location)
        # record=[]
        sponsors=[]
        referred_by=[]
        national_id=[]
        payment_mode=[]
        bill_status=[]
        bill_status=[]
        opd_main_data=[]
        for data in records:
            patient_detail=PatientsRegistrationsAllInOne.objects.filter(uhid=data.uhid).last()
            payment_record=OpdPayment.objects.filter(bill_id=data.bill_no).last()
            opd_main=OpdBillingMain.objects.filter(bill_no=data.bill_no).last()
            opd_main_data.append(opd_main)
            if payment_record is not None:
                bill_status.append('Close')
            else:
                bill_status.append('Finalized')
            if data.status == 'cancel':
                bill_status.append(data.status)
            national_id.append(patient_detail.aadhar_card)
            if patient_detail.nhif_ins_cor_name == 'Cash':
                sponsors.append('Cash')
                payment_mode.append('Cash')
            else:
                spos=CorporateMaster.objects.filter(id=patient_detail.nhif_ins_cor_name).last()
                sponsors.append(spos.corporate_Name)
                payment_mode.append('Credit')
            if patient_detail.referred_by == 'Walked By':
                referred_by.append(patient_detail.referred_by)
            else:
                refer_record=Refered_by_Master.objects.filter(id=patient_detail.referred_by).last()
                referred_by.append(refer_record.Staff_name)
        temp_record = OpdBillingTemper.objects.extra(select={
                'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingtemper.uhid',
                'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingtemper.uhid',
                'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingtemper.uhid',
            }).filter(created_at__range=[from_date,to_date],location=request.location)
        patient_uhid=list(set([data.uhid for data in temp_record]))
        open_net_amount=0
        sponsors1=[]
        referred_by1=[]
        national_id1=[]
        payment_mode1=[]
        bill_status1=[]
        doctor1=[]
        deparment1=[]
        for data in patient_uhid:
            visit=temp_record.filter(uhid=data)
            vist_list=list(set([data.visit_no for data in visit]))
            for vst in vist_list:
                filnial_rcord=temp_record.filter(uhid=data,visit_no=vst).last()
                open_net_amount+=int(filnial_rcord.total_amount)
                patient_record=PatientsRegistrationsAllInOne.objects.filter(uhid=filnial_rcord.uhid).last()
                national_id1.append(patient_record.aadhar_card)
                if patient_record.nhif_ins_cor_name == 'Cash':
                    payment_mode1.append('CASH')
                    sponsors1.append('Cash')
                else:
                    payment_mode1.append('CREDIT')
                    spos=CorporateMaster.objects.filter(id=patient_record.nhif_ins_cor_name).last()
                    sponsors1.append(spos.corporate_Name)

                bill_status1.append('Open Bill')

                if patient_record.referred_by == 'Walked By':
                    referred_by1.append(patient_record.referred_by)
                else:
                    refer_record=Refered_by_Master.objects.filter(id=patient_record.referred_by).last()
                    referred_by1.append(refer_record.Staff_name)
                visit=PatientVisitMains.objects.filter(visit_id=vst).last()
                doctor1.append(visit.doctor)
                deparment1.append(visit.clinical_department)

        ps_parent = PS_CounterSale_Parent.objects.filter(sales_date__range=[from_date,to_date],location_id_id=request.location,panel='Cash').extra(select={
            'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
            'reffered_by': 'Select referred_by from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
            'national_id': 'Select aadhar_card from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
            'sponser': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_ps_countersale_parent.uhid',
        }).order_by("-uhid")
        refer_by_list=[]
        ps_child=[]
        sponsers=[]
        for data in ps_parent:
            ps_child.append(PS_CounterSale_child.objects.filter(Op_sales_no=data.Op_sales_no))
            pss_child=PS_CounterSale_child.objects.filter(Op_sales_no=data.Op_sales_no)
            for data1 in pss_child:
                pharmacy_net_amt+=float(data1.amount)
            if data.reffered_by == 'Walked By' or data.reffered_by == None  :
                refer_by_list.append('Walked By')
            elif data.reffered_by == 'AAA ' or data.reffered_by == 'BBB ':
                refer_by_list.append('Walked By')
            else:
                refer=Refered_by_Master.objects.filter(id=data.reffered_by).last()
                refer_by_list.append(refer.Staff_name)
            if data.sponser == 'Cash':
                sponsers.append('Cash')
            else:
                spos=CorporateMaster.objects.filter(id=data.sponser).last()
                if spos:
                    sponsers.append(spos.corporate_Name)
                else:
                    sponsers.append('')
        pharmacy_records = zip(ps_parent,ps_child,refer_by_list,sponsers)
        net_amt = OpdBillingSub.objects.filter(bill_date_time__range=[from_date,to_date],location=request.location).aggregate(Sum('paid_amount'))
        net_amount = net_amt['paid_amount__sum'] + open_net_amount
        grand_total = net_amount + pharmacy_net_amt
        record_detail = zip(records,sponsors,referred_by,national_id,payment_mode,bill_status)
        record_tempdetail = zip(temp_record,sponsors1,referred_by1,national_id1,payment_mode1,bill_status1,doctor1,deparment1)
    context={
            'record':record_detail,'from_date':from_date,'to_date':to_date,'net_amount':net_amount,'record_tempdetail':record_tempdetail,
            'pharmacy_records':pharmacy_records,'pharmacy_net_amt':pharmacy_net_amt,'grand_total':grand_total,'opd_main_data':opd_main_data,
        }
    return render(request,'clinical/monthly_report.html',context)

def service_charge_edit(request):
    tariff_master=TariffMaster.objects.all()
    service_master=ServiceMaster.objects.all()
    service_cat=ServiceCategory.objects.all()
    service_sub_cat=ServiceSubCategory.objects.all()
    if request.POST.get('search') == 'search':
        traffi=request.POST.get('tariff_id')
        category=request.POST.get('service_cat')
        sub_category=request.POST.get('service_sub_cat')
        service_id=request.POST.get('service_id')
        filters={}
        if traffi:
            filters['tariff_id'] = traffi
        if category:
            filters['service_category'] = category
        if sub_category:
            filters['service_sub_category'] = sub_category
        if service_id:
            filters['service_id'] = service_id
        service_charge_master=ServiceChargeMaster.objects.filter(**filters)
        context = {
            'tariff_master': tariff_master,'service_cat': service_cat,'service_sub_cat': service_sub_cat,'service_master':service_master,
            'service_charge_master':service_charge_master
        }
        return render(request,'general_master/service_charge_edit.html',context)
    if request.POST.get('save') == 'save':
        ids=request.POST.getlist('ids')
        for data in ids:
            record=ServiceChargeMasterServiceChargeMaster.objects.get(id=data)
            record.service_charge=request.POST.get(f'charge{data}')
            record.save()
        return redirect('service_charge_edit')
    context = {
        'tariff_master': tariff_master,'service_cat': service_cat,'service_sub_cat': service_sub_cat,'service_master':service_master,
    }
    return render(request,'general_master/service_charge_edit.html',context)

def package_charge_edit(request):
    tariff_master=TariffMaster.objects.all()
    service_cat=ServiceCategory.objects.all()
    service_sub_cat=ServiceSubCategory.objects.all()
    if request.POST.get('search') == 'search':
        traffi=request.POST.get('tariff_id')
        category=request.POST.get('service_cat')
        sub_category=request.POST.get('service_sub_cat')
        filters={}
        if traffi:
            filters['tariff_id'] = traffi
        if category:
            filters['ward_type'] = category
        if sub_category:
            filters['ward_category'] = sub_category
        service_charge_master=PackageChargeMaster.objects.filter(**filters)
        context = {
            'tariff_master': tariff_master,'service_cat': service_cat,'service_sub_cat': service_sub_cat,
            'service_charge_master':service_charge_master
        }
        return render(request,'general_master/package_charge_edit.html',context)
    if request.POST.get('save') == 'save':
        ids=request.POST.getlist('ids')
        for data in ids:
            record=PackageChargeMaster.objects.get(id=data)
            record.package_charge=request.POST.get(f'charge{data}')
            record.save()
        return redirect('package_charge_edit')
    context = {
        'tariff_master': tariff_master,'service_cat': service_cat,'service_sub_cat': service_sub_cat,
    }
    return render(request,'general_master/package_charge_edit.html',context)

def profile_charge_edit(request):
    tariff_master=TariffMaster.objects.all()
    service_cat=ServiceCategory.objects.all()
    service_sub_cat=ServiceSubCategory.objects.all()
    if request.POST.get('search') == 'search':
        traffi=request.POST.get('tariff_id')
        category=request.POST.get('service_cat')
        sub_category=request.POST.get('service_sub_cat')
        filters={}
        if traffi:
            filters['tariff_id'] = traffi
        if category:
            filters['ward_type'] = category
        if sub_category:
            filters['ward_category'] = sub_category
        service_charge_master=ProfileChargeMaster.objects.filter(**filters)
        context = {
            'tariff_master': tariff_master,'service_cat': service_cat,'service_sub_cat': service_sub_cat,
            'service_charge_master':service_charge_master
        }
        return render(request,'general_master/profile_charge_edit.html',context)
    if request.POST.get('save') == 'save':
        ids=request.POST.getlist('ids')
        for data in ids:
            record=ProfileChargeMaster.objects.get(id=data)
            record.profile_charge=request.POST.get(f'charge{data}')
            record.save()
        return redirect('profile_charge_edit')
    context = {
        'tariff_master': tariff_master,'service_cat': service_cat,'service_sub_cat': service_sub_cat,
    }
    return render(request,'general_master/profile_charge_edit.html',context)

def per_hour_delete(request,pk,id):
    records = IntraDialysisPerHourInput.objects.get(id=id).delete()
    return HttpResponseRedirect(f'/dialysis_details/{pk}')

def nhif_unpaidbill_report(request):
    records=OpdBillingMain.objects.extra(select={
        'insurance_name': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'member_id': 'Select nhif_ins_cor_id from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',}).filter(location=request.location).order_by("-bill_no")
    grand_total1=OpdBillingMain.objects.filter(location=request.location).aggregate(Sum('net_amount'))
    grand_total = grand_total1['net_amount__sum']
    records1 = []
    for data in records:
        if data.insurance_name == "Cash":
            records1.append("Cash")
        else:
            aa = CorporateMaster.objects.get(id = data.insurance_name)
            records1.append(aa.corporate_Name)
    records3 = zip(records,records1)
    from_date = request.POST.get("start_date")
    to_date = request.POST.get("end_date")
    billing_grp = request.POST.get("billing_grp")
    billing_group = BillingGroup.objects.all()
    if from_date and to_date and billing_grp:
        from_date = request.POST.get("start_date").split("T")[0]
        to_date = request.POST.get("end_date").split("T")[0]
        records=OpdBillingMain.objects.extra(select={
        'insurance_name': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'member_id': 'Select nhif_ins_cor_id from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        }).filter(location=request.location,bill_date_time__range = [from_date,to_date],billing_group_id = billing_grp).order_by("-bill_no")
        grand_total1=OpdBillingMain.objects.filter(location=request.location,bill_date_time__range = [from_date,to_date],billing_group_id = billing_grp).aggregate(Sum('net_amount'))
        grand_total = grand_total1['net_amount__sum']
        records1 = []
        for data in records:
            if data.insurance_name == "Cash":
                records1.append("Cash")
            else:
                aa = CorporateMaster.objects.get(id = data.insurance_name)
                records1.append(aa.corporate_Name)
        records3 = zip(records,records1)
    elif from_date and to_date:
        from_date = request.POST.get("start_date").split("T")[0]
        to_date = request.POST.get("end_date").split("T")[0]
        records=OpdBillingMain.objects.extra(select={
        'insurance_name': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'member_id': 'Select nhif_ins_cor_id from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        }).filter(location=request.location,bill_date_time__range = [from_date,to_date]).order_by("-bill_no")
        grand_total1=records.aggregate(Sum('net_amount'))
        grand_total = grand_total['net_amount__sum']
        records1 = []
        for data in records:
            if data.insurance_name == "Cash":
                records1.append("Cash")
            else:
                aa = CorporateMaster.objects.get(id = data.insurance_name)
                records1.append(aa.corporate_Name)
        records3 = zip(records,records1)
    elif billing_grp:
        records=OpdBillingMain.objects.extra(select={
        'insurance_name': 'Select nhif_ins_cor_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        'member_id': 'Select nhif_ins_cor_id from testapp_patientsregistrationsallinone where uhid=testapp_opdbillingmain.uhid',
        }).filter(location=request.location,billing_group_id = billing_grp).order_by("-bill_no")
        grand_total1=records.aggregate(Sum('net_amount'))
        grand_total = grand_total['net_amount__sum']
        records1 = []
        for data in records:
            if data.insurance_name == "Cash":
                records1.append("Cash")
            else:
                aa = CorporateMaster.objects.get(id = data.insurance_name)
                records1.append(aa.corporate_Name)
        records3 = zip(records,records1)
    context = {
        "records":records3,"billing_group":billing_group,"from_date":from_date,"to_date":to_date,"grand_total":grand_total,
    }
    return render(request,"Reports/nhif_unpaid_bill.html",context)
@login_required(login_url='/user_login')
def today_report_new(request):
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
                                }).order_by("-uhid")
            users=[data.created_by for data in records]
            user_details=CreateUser.objects.filter(login_id__in=users)
            pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],panel='Cash').extra(select={
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
                                }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location).aggregate(Sum('net_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location).aggregate(Sum('paid_amount'))
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
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='cash').aggregate(Sum('paid_amount'))
            p_amt_cash = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type__startswith='cash',panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_cash['paid_amount__sum']:
                amt_cash = amt_cash['paid_amount__sum'] + p_amt_cash['paid_amount__sum']
            else:
                amt_cash = amt_cash['paid_amount__sum']
            amt_debit = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='debit_credit_card').aggregate(Sum('paid_amount'))
            p_amt_debit = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type__startswith='debit_credit_card',panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_debit['paid_amount__sum']:
                amt_debit = amt_debit['paid_amount__sum'] + p_amt_debit['paid_amount__sum']
            else:
                amt_debit = amt_debit['paid_amount__sum']
            amt_m_pesa = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='m_pesa').aggregate(Sum('paid_amount'))
            p_amt_m_pesa = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type__startswith='m_pesa',panel='Cash').aggregate(Sum('paid_amount'))
            if p_amt_m_pesa['paid_amount__sum']:
                amt_m_pesa = amt_m_pesa['paid_amount__sum'] + p_amt_m_pesa['paid_amount__sum']
            else:
                amt_m_pesa = amt_m_pesa['paid_amount__sum']
            amt_bank = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='bank').aggregate(Sum('paid_amount'))
            amt_bank = amt_bank['paid_amount__sum']
            amt_eft = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='eft').aggregate(Sum('paid_amount'))
            amt_eft = amt_eft['paid_amount__sum']
            amt_cheque = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type__startswith='cheque').aggregate(Sum('paid_amount'))
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
                                }).order_by("-uhid")
            users=[data.created_by for data in records]
            pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,panel='Cash').extra(select={
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
                                }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,location=request.location).aggregate(Sum('net_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,location=request.location).aggregate(Sum('paid_amount'))
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
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type=mode_type).aggregate(Sum('paid_amount'))
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
                                }).order_by("-uhid")
            users=[data.created_by for data in records]
            user_details=CreateUser.objects.filter(login_id__in=users)
            pharmacy_records = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date,bill_end_date],type=mode_type,created_by=users_id,panel='Cash').extra(select={
                                'dept':'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
                                }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,created_by=users_id,location=request.location).aggregate(Sum('net_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],mode_type=mode_type,created_by=users_id,location=request.location).aggregate(Sum('paid_amount'))
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
            amt_cash = OpdPayment.objects.filter(date_time__range=[bill_start_date,bill_end_date],location=request.location,mode_type=mode_type,created_by=users_id).aggregate(Sum('paid_amount'))
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
            }).order_by("-uhid")
            users = [data.created_by for data in records]
            pharmacy_records = PS_CounterSale_Parent.objects.filter(
                sales_date__range=[bill_start_date, bill_end_date],created_by=users_id, panel='Cash').extra(select={
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_ps_countersale_parent.uhid',
            }).order_by("-uhid")
            ttl_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location).aggregate(Sum('paid_amount'))
            rcv_amt = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location).aggregate(Sum('paid_amount'))
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
                                                 location=request.location, mode_type__startswith='cash').aggregate(
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
                                                  mode_type__startswith='debit_credit_card').aggregate(
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
                                                   mode_type__startswith='m_pesa').aggregate(Sum('paid_amount'))
            p_amt_m_pesa = PS_CounterSale_Parent.objects.filter(sales_date__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                                type__startswith='m_pesa', panel='Cash').aggregate(
                Sum('paid_amount'))
            if p_amt_m_pesa['paid_amount__sum']:
                amt_m_pesa = amt_m_pesa['paid_amount__sum'] + p_amt_m_pesa['paid_amount__sum']
            else:
                amt_m_pesa = amt_m_pesa['paid_amount__sum']
            amt_bank = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],
                                                 location=request.location,created_by=users_id, mode_type__startswith='bank').aggregate(
                Sum('paid_amount'))
            amt_bank = amt_bank['paid_amount__sum']
            amt_eft = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                location=request.location, mode_type__startswith='eft').aggregate(
                Sum('paid_amount'))
            amt_eft = amt_eft['paid_amount__sum']
            amt_cheque = OpdPayment.objects.filter(date_time__range=[bill_start_date, bill_end_date],created_by=users_id,
                                                   location=request.location,
                                                   mode_type__startswith='cheque').aggregate(Sum('paid_amount'))
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


#================================= new code 14/07/2023 =========================================
def user_collection_summary_new(request):
    context={}
    users_names = CreateUser.objects.all()
    if request.method=='POST':
        s_date=request.POST.get('b_start_date')
        e_date=request.POST.get('b_end_date')
        users_ids=request.POST.get('users_ids')
        if s_date != '' and e_date != '' and users_ids== '':
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
            pharmacy_records = PS_CounterSale_Parent.objects.extra(select={
                'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_PS_CounterSale_Parent.uhid',
            }).filter(sales_date__range=[s_date,e_date],location_id=request.location,panel='Cash').order_by('-id')
            mode_type=[data.mode_type for data in records]
            mode_types=set(mode_type)
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
            users=set(userr)
            user_table=CreateUser.objects.filter(user_id__in=users)
            datas_records=[data.f_name for data in user_table]
            ttl_amt = OpdPayment.objects.filter(date_time__range=[s_date,e_date],location=request.location).exclude(status='cancel').aggregate(
                Sum('net_amount'))
            ttl_net = ttl_amt['net_amount__sum']
            rcv_amt = OpdPayment.objects.filter(date_time__range=[s_date,e_date],location=request.location).exclude(status='cancel').aggregate(
                Sum('paid_amount'))
            paid_amt_cash = rcv_amt['paid_amount__sum']
            pharmacy_tot_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],panel='Cash',location_id=request.location).aggregate(
                Sum('paid_amount'))
            pharmacy_tot_amt = pharmacy_tot_amt['paid_amount__sum']
            #======================================== Here Both insurance and cash total calculation ========================
            if paid_amt_cash is None:
                paid_amt_cash=0
            if paid_amt_ins is None:
                paid_amt_ins=0
            if pharmacy_tot_amt is None:
                pharmacy_tot_amt=0
            paid_amt=paid_amt_cash+paid_amt_ins+pharmacy_tot_amt
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
                pharmacy_cash_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',type='cash', created_by=user.login_id.id,location_id=request.location).exclude(bill_status='Forward to OPD').aggregate(
                    Sum('total_taxable_amount'))
                pharmacy_cash_amt = pharmacy_cash_amt['total_taxable_amount__sum']
                if cash_cash is None:
                    cash_cash = 0
                if cash_ins is None:
                    cash_ins = 0
                if pharmacy_cash_amt is  None:
                    pharmacy_cash_amt = 0
                cash=cash_cash+cash_ins+pharmacy_cash_amt
                sub_total_summary=sub_total_summary+cash
                list_cash.append(cash)
                debits_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='debit_credit_card',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                debit_cash = debits_cash['paid_amount__sum']
                debits_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='debit_credit_card', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                debit_ins = debits_ins['paid_amount__sum']
                debits_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',type='debit_credit_card', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                debits_pharmacy = debits_pharmacy['paid_amount__sum']
                if debit_cash is None:
                    debit_cash = 0
                if debit_ins is None:
                    debit_ins = 0
                if debits_pharmacy is None:
                    debits_pharmacy = 0
                debit=debit_cash+debit_ins+debits_pharmacy
                sub_total_summary_debit=sub_total_summary_debit+debit
                list_debit.append(debit)
                efts_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='eft',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                eft_cash = efts_cash['paid_amount__sum']
                efts__ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='eft', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                eft__ins = efts__ins['paid_amount__sum']
                eft_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',type='eft', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                eft_pharmacy = eft_pharmacy['paid_amount__sum']
                if eft_cash is None:
                    eft_cash = 0
                if eft__ins is None:
                    eft__ins = 0
                if eft_pharmacy is None:
                    eft_pharmacy = 0
                eft=eft_cash+eft__ins+eft_pharmacy
                sub_total_summary_eft=sub_total_summary_eft+eft
                list_eft.append(eft)
                m_pesas_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='m_pesa',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                m_pesa_cash = m_pesas_cash['paid_amount__sum']
                m_pesas_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='m_pesa', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                m_pesa_ins = m_pesas_ins['paid_amount__sum']
                m_pesa_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',type='m_pesa', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                m_pesa_pharmacy = m_pesa_pharmacy['paid_amount__sum']
                if m_pesa_cash is None:
                    m_pesa_cash = 0
                if m_pesa_ins is None:
                    m_pesa_ins = 0
                if m_pesa_pharmacy is None:
                    m_pesa_pharmacy = 0
                m_pesa=m_pesa_cash+m_pesa_ins+m_pesa_pharmacy
                sub_total_summary_m_pesa=sub_total_summary_m_pesa+m_pesa
                list_m_pesa.append(m_pesa)
                banks_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='bank',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                bank_cash = banks_cash['paid_amount__sum']
                banks_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='bank', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                bank_ins = banks_ins['paid_amount__sum']
                bank_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',type='bank', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                bank_pharmacy = bank_pharmacy['paid_amount__sum']
                if bank_cash is None:
                    bank_cash = 0
                if bank_ins is None:
                    bank_ins = 0
                if bank_pharmacy is None:
                    bank_pharmacy = 0
                bank=bank_cash+bank_ins+bank_pharmacy
                sub_total_summary_bank=sub_total_summary_bank+bank
                list_bank.append(bank)
                cheques_cash = OpdPayment.objects.filter(date_time__range=[s_date,e_date],mode_type='cheque',created_by=user.login_id.id,location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                cheque_cash = cheques_cash['paid_amount__sum']
                cheques_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date,e_date],mode_type='cheque', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                cheque_ins = cheques_ins['paid_amount__sum']
                cheque_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',type='cheque', created_by=user.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                cheque_pharmacy = cheque_pharmacy['paid_amount__sum']
                if cheque_cash is None:
                    cheque_cash = 0
                if cheque_ins is None:
                    cheque_ins = 0
                if cheque_pharmacy is None:
                    cheque_pharmacy = 0
                cheque=cheque_cash+cheque_ins+cheque_pharmacy
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
                sub_total_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date,e_date],panel='Cash',created_by=sub.login_id.id,location_id=request.location).aggregate(
                    Sum('paid_amount'))
                sub_total_pharmacy = sub_total_pharmacy['paid_amount__sum']
                if sub_total_cash is None:
                    sub_total_cash = 0
                if sub_total_ins is None:
                    sub_total_ins = 0
                if sub_total_pharmacy is None:
                    sub_total_pharmacy = 0
                sub_total_both=sub_total_cash+sub_total_ins+sub_total_pharmacy
                grand_total=grand_total+sub_total_both
                sub_total_list.append(sub_total_both)
            #=================================== END =================================
            all_rec=zip(user_table,sub_total_list)
            context={
              'records':records,'ttl_net':ttl_net,'paid_amt':grand_total,'mode_types':mode_types,'users':users,'all_rec':all_rec,
                'user_table':user_table,'user_summary':user_summary,'payment_sub_total':payment_sub_total,'records2':records2,
                'sub_total_summary_cash_list':sub_total_summary,'sub_total_summary_debit_list':sub_total_summary_debit,
                'sub_total_summary_m_pesa_list':sub_total_summary_m_pesa,'sub_total_summary_bank_list':sub_total_summary_bank,
                'sub_total_summary_eft_list':sub_total_summary_eft,'sub_total_summary_cheque_list':sub_total_summary_cheque,
                'total_summary_list':sum_total_all,'grand_total_summary_list':sum_total_all,'pharmacy_records':pharmacy_records,
                'users_names':users_names,
            }
            return render(request,'Reports/user_collection_summary.html',context)
        #================= DATE RANGE WITH USER =================================================
        if s_date != '' and e_date !='' and  users_ids !='':
            records = OpdPayment.objects.extra(select={
                'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdPayment.uhid',
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                'disc': 'Select discount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
                'payable': 'Select pay_amount from testapp_opdbillingmain where uhid=testapp_OpdPayment.uhid',
            }).filter(date_time__range=[s_date, e_date],created_by=users_ids, location=request.location).order_by('created_by').exclude(
                status='cancel')
            records2 = Insurance_Payement_Detail.objects.extra(select={
                'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
                'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
                'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
                'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_Insurance_Payement_Detail.uhid',
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_Insurance_Payement_Detail.uhid',
                'disc': 'Select discount from testapp_opdbillingmain where uhid=testapp_Insurance_Payement_Detail.uhid',
                'payable': 'Select pay_amount from testapp_opdbillingmain where uhid=testapp_Insurance_Payement_Detail.uhid',
            }).filter(date_time__range=[s_date, e_date],created_by=users_ids, location_id=request.location).order_by('-id')
            pharmacy_records = PS_CounterSale_Parent.objects.extra(select={
                'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PS_CounterSale_Parent.uhid',
                'dept': 'Select department from testapp_opdbillingmain where uhid=testapp_PS_CounterSale_Parent.uhid',
            }).filter(sales_date__range=[s_date, e_date],created_by=users_ids, location_id=request.location, panel='Cash').order_by('-id')
            mode_type = [data.mode_type for data in records]
            mode_types = set(mode_type)
            userr_ins = [data.created_by for data in records2]
            users_ins = set(userr_ins)
            ttl_amt_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],created_by=users_ids,location_id=request.location).aggregate(Sum('net_amount'))
            ttl_amt_ins = ttl_amt_ins['net_amount__sum']
            rcv_amt_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],created_by=users_ids,location_id=request.location).aggregate(Sum('paid_amount'))
            paid_amt_ins = rcv_amt_ins['paid_amount__sum']
            # -================================= Here TO start cash Patient calculation ==================================
            userr = [data.created_by for data in records]
            users = set(userr)
            user_table = CreateUser.objects.filter(user_id__in=users)
            datas_records = [data.f_name for data in user_table]
            ttl_amt = OpdPayment.objects.filter(date_time__range=[s_date, e_date],created_by=users_ids,location=request.location).exclude(status='cancel').aggregate(Sum('net_amount'))
            ttl_net = ttl_amt['net_amount__sum']
            rcv_amt = OpdPayment.objects.filter(date_time__range=[s_date, e_date],created_by=users_ids,location=request.location).exclude(status='cancel').aggregate(Sum('paid_amount'))
            paid_amt_cash = rcv_amt['paid_amount__sum']
            pharmacy_tot_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],created_by=users_ids,panel='Cash',location_id=request.location).aggregate(Sum('paid_amount'))
            pharmacy_tot_amt = pharmacy_tot_amt['paid_amount__sum']
            # ======================================== Here Both insurance and cash total calculation ========================
            if paid_amt_cash is None:
                paid_amt_cash = 0
            if paid_amt_ins is None:
                paid_amt_ins = 0
            if pharmacy_tot_amt is None:
                pharmacy_tot_amt = 0
            paid_amt = paid_amt_cash + paid_amt_ins + pharmacy_tot_amt
            # ================= for user wise and payment modes wise total calculation ==========================
            list_cash = []
            list_debit = []
            list_eft = []
            list_m_pesa = []
            list_sum_total = []
            list_bank = []
            list_cheque = []
            sum_total_all = 0
            sub_total_summary = 0
            sub_total_summary_debit = 0
            sub_total_summary_m_pesa = 0
            sub_total_summary_bank = 0
            sub_total_summary_eft = 0
            sub_total_summary_cheque = 0
            sub_total_summary_cash_list = []
            sub_total_summary_debit_list = []
            sub_total_summary_m_pesa_list = []
            sub_total_summary_bank_list = []
            sub_total_summary_eft_list = []
            sub_total_summary_cheque_list = []
            total_summary_list = []
            grand_total_summary_list = []
            for user in user_table:
                cashs = OpdPayment.objects.filter(date_time__range=[s_date, e_date], mode_type='cash',
                                                  created_by=user.login_id.id, location=request.location).exclude(
                    status='cancel').aggregate(
                    Sum('paid_amount'))
                cash_cash = cashs['paid_amount__sum']
                cashs_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                     mode_type='cash', created_by=user.login_id.id,
                                                                     location_id=request.location).aggregate(
                    Sum('paid_amount'))
                cash_ins = cashs_ins['paid_amount__sum']
                pharmacy_cash_amt = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                         panel='Cash', type='cash',
                                                                         created_by=user.login_id.id,
                                                                         location_id=request.location).exclude(
                    bill_status='Forward to OPD').aggregate(
                    Sum('total_taxable_amount'))
                pharmacy_cash_amt = pharmacy_cash_amt['total_taxable_amount__sum']
                if cash_cash is None:
                    cash_cash = 0
                if cash_ins is None:
                    cash_ins = 0
                if pharmacy_cash_amt is None:
                    pharmacy_cash_amt = 0
                cash = cash_cash + cash_ins + pharmacy_cash_amt
                sub_total_summary = sub_total_summary + cash
                list_cash.append(cash)
                debits_cash = OpdPayment.objects.filter(date_time__range=[s_date, e_date],
                                                        mode_type='debit_credit_card', created_by=user.login_id.id,
                                                        location=request.location).exclude(
                    status='cancel').aggregate(
                    Sum('paid_amount'))
                debit_cash = debits_cash['paid_amount__sum']
                debits_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                      mode_type='debit_credit_card',
                                                                      created_by=user.login_id.id,
                                                                      location_id=request.location).aggregate(
                    Sum('paid_amount'))
                debit_ins = debits_ins['paid_amount__sum']
                debits_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                       panel='Cash', type='debit_credit_card',
                                                                       created_by=user.login_id.id,
                                                                       location_id=request.location).aggregate(
                    Sum('paid_amount'))
                debits_pharmacy = debits_pharmacy['paid_amount__sum']
                if debit_cash is None:
                    debit_cash = 0
                if debit_ins is None:
                    debit_ins = 0
                if debits_pharmacy is None:
                    debits_pharmacy = 0
                debit = debit_cash + debit_ins + debits_pharmacy
                sub_total_summary_debit = sub_total_summary_debit + debit
                list_debit.append(debit)
                efts_cash = OpdPayment.objects.filter(date_time__range=[s_date, e_date], mode_type='eft',
                                                      created_by=user.login_id.id,
                                                      location=request.location).exclude(status='cancel').aggregate(
                    Sum('paid_amount'))
                eft_cash = efts_cash['paid_amount__sum']
                efts__ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                     mode_type='eft', created_by=user.login_id.id,
                                                                     location_id=request.location).aggregate(
                    Sum('paid_amount'))
                eft__ins = efts__ins['paid_amount__sum']
                eft_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                    panel='Cash', type='eft',
                                                                    created_by=user.login_id.id,
                                                                    location_id=request.location).aggregate(
                    Sum('paid_amount'))
                eft_pharmacy = eft_pharmacy['paid_amount__sum']
                if eft_cash is None:
                    eft_cash = 0
                if eft__ins is None:
                    eft__ins = 0
                if eft_pharmacy is None:
                    eft_pharmacy = 0
                eft = eft_cash + eft__ins + eft_pharmacy
                sub_total_summary_eft = sub_total_summary_eft + eft
                list_eft.append(eft)
                m_pesas_cash = OpdPayment.objects.filter(date_time__range=[s_date, e_date], mode_type='m_pesa',
                                                         created_by=user.login_id.id,
                                                         location=request.location).exclude(
                    status='cancel').aggregate(
                    Sum('paid_amount'))
                m_pesa_cash = m_pesas_cash['paid_amount__sum']
                m_pesas_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                       mode_type='m_pesa',
                                                                       created_by=user.login_id.id,
                                                                       location_id=request.location).aggregate(
                    Sum('paid_amount'))
                m_pesa_ins = m_pesas_ins['paid_amount__sum']
                m_pesa_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                       panel='Cash', type='m_pesa',
                                                                       created_by=user.login_id.id,
                                                                       location_id=request.location).aggregate(
                    Sum('paid_amount'))
                m_pesa_pharmacy = m_pesa_pharmacy['paid_amount__sum']
                if m_pesa_cash is None:
                    m_pesa_cash = 0
                if m_pesa_ins is None:
                    m_pesa_ins = 0
                if m_pesa_pharmacy is None:
                    m_pesa_pharmacy = 0
                m_pesa = m_pesa_cash + m_pesa_ins + m_pesa_pharmacy
                sub_total_summary_m_pesa = sub_total_summary_m_pesa + m_pesa
                list_m_pesa.append(m_pesa)
                banks_cash = OpdPayment.objects.filter(date_time__range=[s_date, e_date], mode_type='bank',
                                                       created_by=user.login_id.id,
                                                       location=request.location).exclude(
                    status='cancel').aggregate(
                    Sum('paid_amount'))
                bank_cash = banks_cash['paid_amount__sum']
                banks_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                     mode_type='bank', created_by=user.login_id.id,
                                                                     location_id=request.location).aggregate(
                    Sum('paid_amount'))
                bank_ins = banks_ins['paid_amount__sum']
                bank_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                     panel='Cash', type='bank',
                                                                     created_by=user.login_id.id,
                                                                     location_id=request.location).aggregate(
                    Sum('paid_amount'))
                bank_pharmacy = bank_pharmacy['paid_amount__sum']
                if bank_cash is None:
                    bank_cash = 0
                if bank_ins is None:
                    bank_ins = 0
                if bank_pharmacy is None:
                    bank_pharmacy = 0
                bank = bank_cash + bank_ins + bank_pharmacy
                sub_total_summary_bank = sub_total_summary_bank + bank
                list_bank.append(bank)
                cheques_cash = OpdPayment.objects.filter(date_time__range=[s_date, e_date], mode_type='cheque',
                                                         created_by=user.login_id.id,
                                                         location=request.location).exclude(
                    status='cancel').aggregate(
                    Sum('paid_amount'))
                cheque_cash = cheques_cash['paid_amount__sum']
                cheques_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                       mode_type='cheque',
                                                                       created_by=user.login_id.id,
                                                                       location_id=request.location).aggregate(
                    Sum('paid_amount'))
                cheque_ins = cheques_ins['paid_amount__sum']
                cheque_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                       panel='Cash', type='cheque',
                                                                       created_by=user.login_id.id,
                                                                       location_id=request.location).aggregate(
                    Sum('paid_amount'))
                cheque_pharmacy = cheque_pharmacy['paid_amount__sum']
                if cheque_cash is None:
                    cheque_cash = 0
                if cheque_ins is None:
                    cheque_ins = 0
                if cheque_pharmacy is None:
                    cheque_pharmacy = 0
                cheque = cheque_cash + cheque_ins + cheque_pharmacy
                sub_total_summary_cheque = sub_total_summary_cheque + cheque
                list_cheque.append(cheque)
                if cash is None:
                    cash = 0
                if debit is None:
                    debit = 0
                if eft is None:
                    eft = 0
                if m_pesa is None:
                    m_pesa = 0
                if bank is None:
                    bank = 0
                if cheque is None:
                    cheque = 0
                sum_total = cash + debit + eft + m_pesa + bank + cheque
                list_sum_total.append(sum_total)
                sum_total_all = sum_total_all + sum_total
            sub_total_summary_cash_list.append(sub_total_summary)
            sub_total_summary_debit_list.append(sub_total_summary_debit)
            sub_total_summary_eft_list.append(sub_total_summary_eft)
            sub_total_summary_m_pesa_list.append(sub_total_summary_m_pesa)
            sub_total_summary_bank_list.append(sub_total_summary_bank)
            sub_total_summary_cheque_list.append(sub_total_summary_cheque)
            total_summary_list.append(sum_total_all)
            grand_total_summary_list.append(sum_total_all)
            user_summary = zip(user_table, list_cash, list_debit, list_eft, list_m_pesa, list_bank, list_cheque,
                               list_sum_total)
            # ======================================= End ==================================================
            mode_wise_total = []
            mode_list = []
            for users in user_table:
                for mode_sub in mode_types:
                    sub_total_mode = OpdPayment.objects.filter(date_time__range=[s_date, e_date],
                                                               mode_type=mode_sub, created_by=users.login_id.id,
                                                               location=request.location).exclude(
                        status='cancel').aggregate(
                        Sum('paid_amount'))
                    total_mode_wise = sub_total_mode['paid_amount__sum']
                    mode_wise_total.append(total_mode_wise)
                    mode_list.append(mode_sub)
                    # print('mode_sub--->',mode_sub)
            payment_sub_total = zip(mode_list, mode_wise_total)
            # ==================================== Here For user wise sum total =============================================
            sub_total_list = []
            sub_total_both = 0
            grand_total = 0
            for sub in user_table:
                sub_total_cash = OpdPayment.objects.filter(date_time__range=[s_date, e_date],
                                                           created_by=sub.login_id.id,
                                                           location=request.location).exclude(
                    status='cancel').aggregate(
                    Sum('paid_amount'))
                sub_total_cash = sub_total_cash['paid_amount__sum']
                sub_total_ins = Insurance_Payement_Detail.objects.filter(date_time__range=[s_date, e_date],
                                                                         created_by=sub.login_id.id,
                                                                         location_id=request.location).aggregate(
                    Sum('paid_amount'))
                sub_total_ins = sub_total_ins['paid_amount__sum']
                sub_total_pharmacy = PS_CounterSale_Parent.objects.filter(sales_date__range=[s_date, e_date],
                                                                          panel='Cash', created_by=sub.login_id.id,
                                                                          location_id=request.location).aggregate(
                    Sum('paid_amount'))
                sub_total_pharmacy = sub_total_pharmacy['paid_amount__sum']
                if sub_total_cash is None:
                    sub_total_cash = 0
                if sub_total_ins is None:
                    sub_total_ins = 0
                if sub_total_pharmacy is None:
                    sub_total_pharmacy = 0
                sub_total_both = sub_total_cash + sub_total_ins + sub_total_pharmacy
                grand_total = grand_total + sub_total_both
                sub_total_list.append(sub_total_both)
            # =================================== END =================================
            all_rec = zip(user_table, sub_total_list)
            context = {
                'records': records, 'ttl_net': ttl_net, 'paid_amt': grand_total, 'mode_types': mode_types,
                'users': users, 'all_rec': all_rec,
                'user_table': user_table, 'user_summary': user_summary, 'payment_sub_total': payment_sub_total,
                'records2': records2,
                'sub_total_summary_cash_list': sub_total_summary,
                'sub_total_summary_debit_list': sub_total_summary_debit,
                'sub_total_summary_m_pesa_list': sub_total_summary_m_pesa,
                'sub_total_summary_bank_list': sub_total_summary_bank,
                'sub_total_summary_eft_list': sub_total_summary_eft,
                'sub_total_summary_cheque_list': sub_total_summary_cheque,
                'total_summary_list': sum_total_all, 'grand_total_summary_list': sum_total_all,
                'pharmacy_records': pharmacy_records,
                'users_names': users_names,
            }
            return render(request, 'Reports/user_collection_summary.html', context)
    context={
        'users_names':users_names
    }
    return render(request,'Reports/user_collection_summary.html',context)

#================================ OUTSTANDING AMT 21/07/2023 ==========================================
def list_cash_outstanding_amt(request):
    start_date = date(2023, 4, 1)
    end_date = date(2023, 4, 30)
    opdbill_records=OpdBillingMain.objects.filter(billing_group_id='1',location_id=request.location).exclude(outstanding_amount__in=['0','']).exclude(status='cancel').exclude(bill_date_time__range=[start_date,end_date]).order_by('-id').extra(select={
                'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
                'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
    })
    context={
        'opdbill_records':opdbill_records,
    }
    return render(request,'clinical/opd_bill/list_cash_outstanding_amt.html',context)

@login_required(login_url='/user_login')
def cash_settle(request,pk):
    data_records=pk.split('-')
    pay_m_uhid=data_records[0]
    pay_m_visit_id=data_records[1]
    pay_m_bill_nos=data_records[2]
    tatol_package_amt=0
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
                created_by_id = request.user.id,location_id=request.location,receipt_no=receipt_no,type=types,
            )
            update_pay_amt = OpdBillingMain.objects.filter( bill_no=pay_m_bill_nos).last()
            amount_paid=update_pay_amt.paid_amount
            amount_paid_plus=int(amount_paid)+int(cash_pay_amount)
            update_pay_amt.paid_amount=amount_paid_plus
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
            update_pay_amt = OpdBillingMain.objects.filter(bill_no=pay_m_bill_nos).last()
            amount_paid = update_pay_amt.paid_amount
            amount_paid_plus = int(amount_paid) + int(card_pay_amount)
            update_pay_amt.paid_amount = amount_paid_plus
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
            update_pay_amt = OpdBillingMain.objects.filter( bill_no=pay_m_bill_nos).last()
            amount_paid=update_pay_amt.paid_amount
            amount_paid_plus=int(amount_paid)+int(mpesa_pay_amount)
            update_pay_amt.paid_amount=amount_paid_plus
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
            update_pay_amt = OpdBillingMain.objects.filter( bill_no=pay_m_bill_nos).last()
            amount_paid=update_pay_amt.paid_amount
            amount_paid_plus=int(amount_paid)+int(bank_pay_amount)
            update_pay_amt.paid_amount=amount_paid_plus
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
            update_pay_amt = OpdBillingMain.objects.filter( bill_no=pay_m_bill_nos).last()
            amount_paid=update_pay_amt.paid_amount
            amount_paid_plus=int(amount_paid)+int(eft_pay_amount)
            update_pay_amt.paid_amount=amount_paid_plus
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
            update_pay_amt = OpdBillingMain.objects.filter( bill_no=pay_m_bill_nos).last()
            amount_paid=update_pay_amt.paid_amount
            amount_paid_plus=int(amount_paid)+int(cheque_pay_amount)
            update_pay_amt.paid_amount=amount_paid_plus
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
        services_que = ServiceChargeMaster.objects.filter(service_id__in=services_name)
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
            ttl_amt = OpdBillingSub.objects.filter(bill_no=pay_m_bill_nos,
                                                   service_category=inv.service_category).aggregate(Sum('charges'))
            net_amount = ttl_amt['charges__sum']
            sub_list.append(net_amount)
        # ============================ Here total Amount payment table ==============================
        payment_ttl_amt = OpdPayment.objects.filter(uhid=pay_m_uhid, bill_id=pay_m_bill_nos, visit_id=pay_m_visit_id).aggregate(Sum('paid_amount'))
        payment_ttl_amt = payment_ttl_amt['paid_amount__sum']
        # ============================ Here total Amount  ==============================
        net_amount = OpdBillingSub.objects.filter(bill_no=pay_m_bill_nos).aggregate(Sum('paid_amount'))
        net_amount = net_amount['paid_amount__sum']
        # ================= END =================================================
        for visit_detail in visit_detail:
            visit_date_time = visit_detail.visit_date_time
        all_data = zip(ins_records, sub_list)

        context = {
            'pay_m_visit_id': pay_m_visit_id,'amount':amount,'pay_m_uhid':pay_m_uhid,'bill_no':bill_no,
            'patinet_name':patinet_name,'mobile_number':mobile_number,'address':address,'visit_detail':visit_detail,
            'default_unit':default_unit,'default_discount':default_discount,'patient_detail':patient_detail,'all_data':all_data,
            'visit_date_time':visit_date_time,'temp_records':temp_records,'temp_record':temp_record,
            'net_amount':net_amount,'date_time':date_time,'exact_bill_no':exact_bill_no,'mode_of_payment':mode_of_payment,
            'mode_of_bank':mode_of_bank,'tatol_package_amt':tatol_package_amt,'payment_ttl_amt':payment_ttl_amt,
            'billing_groups':billing_groups,'sponsors':sponsors,'payment_details':payment_details,'reffered_by':reffered_by,
        }
        return render(request, 'clinical/opd_billing_receipt_cash.html', context)
    net_amount = OpdBillingMain.objects.filter(bill_no=pay_m_bill_nos).aggregate(Sum('outstanding_amount'))
    net_amount = net_amount['outstanding_amount__sum']
    print('net_amount----->,',net_amount)
    context={
        'pay_m_uhid':pay_m_uhid,'pay_m_visit_id':pay_m_visit_id,'net_amount':net_amount,
    }
    return render(request,'clinical/opd_bill/cash_settle.html',context)
#========================= FOR EDITING OPD BILL ======================================
def list_all_bill(request):
    opd_bill_records=OpdBillingMain.objects.all().exclude(status='cancel').order_by('-id').extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
        })
    context={
        'opd_bill_records':opd_bill_records,
    }
    return render(request, 'clinical/opd_bill/list_all_bill.html',context)

#====================== Searching Sevices =============================
def search_services(request):
    service_name=request.GET.get('service_name')
    payload=[]
    tariff_names=request.session['tariff_names']
    if service_name and len(service_name)>0:
        fake_address_objs=ServiceChargeMaster.objects.filter(service_id__icontains=service_name,tariff_id__in=tariff_names)
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.service_id))
        fake_address_objs=ProfileChargeMaster.objects.filter(profile_id__icontains=service_name,tariff_id__in=tariff_names)
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.profile_id))
        fake_address_objs=PackageChargeMaster.objects.filter(package_id__package_name__icontains=service_name,tariff_id__in=tariff_names)
        for fake_address_obj in fake_address_objs:
            payload.append(str(fake_address_obj.package_id))
    return JsonResponse({'status':200,'data':payload})

def update_opd_bill(request,pk,serv=None):
    all_data=''
    #=================================== For SEPARATING UHID, VISIT ID AND BILL NO =========================================
    uh_visit_id = pk.split('-')
    uhid_p = uh_visit_id[0]
    visit_id_p = uh_visit_id[1]
    bill_id_p=uh_visit_id[2]
    billing_g=BillingGroup.objects.all()
    insurance=CorporateMaster.objects.all()
    #================================= For Patient Heading Data ==========================================
    records_opd=OpdBillingMain.objects.filter(uhid=uhid_p,visit_no=visit_id_p,bill_no=bill_id_p).extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'billing_group': 'Select billing_group from testapp_BillingGroup where id=testapp_OpdBillingMain.billing_group_id',
            'corporate_name': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_OpdBillingMain.corporate_id',
    }).last()
    #============================ For Passint Tariff ID In Search Address Views Function, For Getting tariff Related Data =======================================
    request.session['tariff_names']=records_opd.billing_group_id
    #======================== For Displaying Sub Table Data in for Loop Front end ================================
    records_sub = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p).exclude(status='inactive')
    #======================== For Displaying Temp Table Data in for Loop Front end ================================
    records_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p)
    # =================================== For Calculating OPD Billing Sub Table AMT ============================
    rate_amt = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('charges'))
    rate_amt = rate_amt['charges__sum']
    rcv_amt = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('pay_amount'))
    rcv_amt = rcv_amt['pay_amount__sum']
    nt_amt = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('paid_amount'))
    nt_amt = nt_amt['paid_amount__sum']
    nt_disc =  OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('discount'))
    nt_disc = nt_disc['discount__sum']
    ttl_unit =  OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('unit'))
    ttl_unit = ttl_unit['unit__sum']
    # ========================= For Calculating Temp Table AMT ==============================================
    ttl_rate_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('rate'))
    ttl_rate_temp = ttl_rate_temp['rate__sum']
    ttl_qty_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('unit'))
    ttl_qty_temp = ttl_qty_temp['unit__sum']
    ttl_dics_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('discount'))
    ttl_dics_temp = ttl_dics_temp['discount__sum']
    ttl_net_amt_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('net_ammount'))
    ttl_net_amt_temp = ttl_net_amt_temp['net_ammount__sum']
    ttl_amt_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('total_amount'))
    ttl_amt_temp = ttl_amt_temp['total_amount__sum']
    # ============================ For Adding Data Both Tables AMT =========================================
    if rate_amt == None:
        rate_amt=0
    if ttl_unit == None:
        ttl_unit = 0
    if nt_disc == None:
        nt_disc=0
    if rcv_amt == None:
        rcv_amt = 0
    if nt_amt == None:
        nt_amt = 0
    if ttl_rate_temp == None:
        ttl_rate_temp=0
    if ttl_qty_temp == None:
        ttl_qty_temp = 0
    if ttl_dics_temp == None:
        ttl_dics_temp=0
    if ttl_net_amt_temp == None:
        ttl_net_amt_temp = 0
    if ttl_amt_temp == None:
        ttl_amt_temp = 0
    add_rate=rate_amt+ttl_rate_temp
    add_unit=ttl_unit+ttl_qty_temp
    add_disc=nt_disc+ttl_dics_temp
    add_net_amt=rcv_amt+ttl_net_amt_temp
    add_total_amt=nt_amt+ttl_amt_temp
    # ================================= Here Searching Services =============================================================
    intell_search = serv
    request.session['intell_search'] = intell_search
    service_charge = ServiceChargeMaster.objects.all()
    service_charge_list = [data.service_id for data in service_charge]
    profile_data = OpdPackageMaster.objects.all()
    profile_list = [data.package_name for data in profile_data]
    service_test_data = ServiceTest.objects.all()
    test_list = [data.test_name for data in service_test_data]
    if intell_search:
        if str(intell_search) in service_charge_list:
            service_ids = intell_search
            get_service = ServiceChargeMaster.objects.filter(service_id=service_ids, tariff_id__in=records_opd.billing_group_id)
            intell_search_ser_name = [data.service_id for data in get_service]
            intell_search_ser_charges = [data.service_charge for data in get_service]
            intell_search_ser_cate = [data.ward_type for data in get_service]
            intell_search_ser_sub_cat = [data.ward_category for data in get_service]
            intell_search_ser_qty = ['1']
            intell_search_ser_disc = ['0']
            intell_search_ser_total_amt = [data.service_charge for data in get_service]
        elif str(intell_search) in profile_list:
            get_services1 = PackageChargeMaster.objects.filter(package_id__package_name__icontains=intell_search,
                                                               tariff_id__in=records_opd.billing_group_id)
            package_id = [data.id for data in get_services1]
            package_amt = [data.package_charge for data in get_services1]
            intell_search_ser_name = [data.package_id for data in get_services1]
            intell_search_ser_charges = [data.package_charge for data in get_services1]
            intell_search_ser_qty = '1'  # [data.quantity for data in get_services]
            intell_search_ser_disc = '0'  # [data.discount for data in get_services]
            intell_search_ser_total_amt = [data.package_charge for data in get_services1]
            intell_search_ser_cate = [data.ward_type for data in get_services1]
            intell_search_ser_sub_cat = [data.ward_category for data in get_services1]
        elif str(intell_search) in test_list:
            get_services = ServiceTest.objects.filter(test_name__icontains=intell_search)
            intell_search_ser_name = [data.test_name for data in get_services]
            intell_search_ser_charges = [data.test_charges for data in get_services]
            intell_search_ser_qty = '1'
            intell_search_ser_disc = '0'
            intell_search_ser_total_amt = [data.test_charges for data in get_services]
        else:
            get_services1 = ProfileChargeMaster.objects.filter(profile_id__icontains=intell_search,
                                                               tariff_id__in=records_opd.billing_group_id)
            intell_search_ser_name = [data.profile_id for data in get_services1]
            intell_search_ser_charges = [data.profile_charge for data in get_services1]
            intell_search_ser_cate = [data.ward_type for data in get_services1]
            intell_search_ser_sub_cat = [data.ward_category for data in get_services1]
            intell_search_ser_qty = '1'
            intell_search_ser_disc = '0'
            intell_search_ser_total_amt = [data.profile_charge for data in get_services1]
        # ================================== For Passing All value in Zip ============================================
        all_data = zip(intell_search_ser_name, intell_search_ser_charges, intell_search_ser_qty,intell_search_ser_disc,
                       intell_search_ser_total_amt, intell_search_ser_sub_cat, intell_search_ser_cate)
    # ======================================= Saving Data In Temp Table =======================================
    change_tariff = request.POST.get('change_tariff')
    insert = request.POST.get('insert')
    extra_data=''
    if change_tariff == 'To_Change_Tariff':
        billing_name = request.POST.get('billing_name')
        insurance_name = request.POST.get('insurance_name')
        print('To change tariff successfully----->,',billing_name,insurance_name)
        get_tariff=BillingGroupTariffLink.objects.filter(Billing_Group_Name=billing_name).last()
        tariff_master = TariffMaster.objects.get(tariff_name=get_tariff.Tariff)
        records_sub = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p)
        for i in records_sub:
            print('this is sub table data',i.service_id)
            get_service = ServiceChargeMaster.objects.filter(service_id__service_name=i.service_id,
                                                             tariff_id=tariff_master, ipd_opd='OPD').last()
            get_packages = PackageChargeMaster.objects.filter(package_id__package_name=i.service_id,
                                                               tariff_id=tariff_master, ipd_opd='OPD').last()
            get_profile = ProfileChargeMaster.objects.filter(profile_id__profile_name=i.service_id,
                                                               tariff_id=tariff_master, ipd_opd='OPD').last()
            if get_service:
                print('get_service---->,',get_service.service_id)
                print('get_service---->,',get_service.service_charge)
                records_subs = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p,service_id=i.service_id).last()
                records_subs.service_id=get_service.service_id.service_name
                records_subs.charges=get_service.service_charge
                records_subs.save()
            elif get_packages:
                print('get_service---->,',get_packages.package_id)
                print('get_service---->,',get_packages.package_charge)
                records_subs = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p,service_id=i.service_id).last()
                records_subs.service_id=get_packages.package_id
                records_subs.charges=get_packages.package_charge
                records_subs.save()
            elif get_profile:
                print('get_service---->,',get_profile.profile_id)
                print('get_service---->,',get_profile.profile_charge)
                records_subs = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p,service_id=i.service_id).last()
                records_subs.service_id=get_profile.profile_id
                records_subs.charges=get_profile.profile_charge
                records_subs.save()
            else:
                print('data is not there',i.service_id)
                extra_data=i.service_id

            # records_sub = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p)
    if insert == 'Save_Data':
        print('Data Saved successfully------>,')
        service_name=request.POST.get('service_name')
        package_profile_id = request.POST.get('package_profile_id')
        package_profile_amt = request.POST.get('package_profile_amt')
        amount = request.POST.get('amount')
        discount = request.POST.get('discount')
        unit = request.POST.get('unit')
        net_amount = request.POST.get('net_amount')
        outstanding_amount = request.POST.get('outstanding_amount')
        total_amount = request.POST.get('total_amount')
        service_category = request.POST.get('service_category')
        service_sub_category = request.POST.get('service_sub_category')
        receive_amount = request.POST.get('receive_amount')
        temp_opd_billing = OpdBillingTemper(
            uhid=uhid_p,
            visit_no=visit_id_p,
            temp_bill_no=bill_id_p,
            package_profile_id=package_profile_id,
            package_profile_amt=package_profile_amt,
            service_name=service_name,
            rate=amount,
            discount=discount,
            unit=unit,
            net_ammount=net_amount,
            outstanding_amount=outstanding_amount,
            total_amount=total_amount,
            service_category_id=service_category,
            service_sub_category_id=service_sub_category,
            receive_amount=receive_amount,
            created_by_id=request.user.id,
            location_id=request.location,
        )
        temp_opd_billing.save()
        return HttpResponseRedirect(f'/update_opd_bill/{pk}')
    # ===================================== End ==============================================
    context={
        'dat':records_opd,'records_sub':records_sub,'pk':pk,'all_data':all_data,'records_temp':records_temp,
        'ttl_amt':add_total_amt,'rate_amt':add_rate,'rcv_amt':rcv_amt,'nt_amt':add_net_amt,'nt_disc':add_disc,'ttl_unit':add_unit,
        'ttl_rate_temp':ttl_rate_temp,'ttl_qty_temp':ttl_qty_temp,'ttl_dics_temp':ttl_dics_temp,'ttl_net_amt_temp':ttl_net_amt_temp,
        'ttl_amt_temp':ttl_amt_temp,'billing_g':billing_g,"insurance":insurance,'extra_data':extra_data,
    }
    return render(request, 'clinical/opd_bill/update_opd_bill.html',context)
from django.shortcuts import redirect
# ============================ this is using in OPD Bill Update Delete data =============================================
def sub_service_removing(request,pk,id):
    data=OpdBillingSub.objects.get(id=id)
    data.status= 'inactive'
    data.save()
    bill_no=data.bill_no
    sub_rate=data.charges
    sub_dis=data.discount
    sub_pay_amount=data.pay_amount
    sub_paid_amount=data.paid_amount
    print('sub amount--->,',sub_rate,sub_dis,sub_pay_amount,sub_paid_amount)
    main_data=OpdBillingMain.objects.filter(bill_no=bill_no).last()
    main_rate=main_data.net_amount
    main_discount=main_data.discount
    main_pay_amount=main_data.pay_amount
    main_paid_amount=main_data.paid_amount
    print('main amount--->,',main_rate,main_discount,main_pay_amount,main_paid_amount)
    update_rate=int(main_rate)-int(sub_rate)
    update_disc=int(main_discount)-int(sub_dis)
    update_pay_amount=int(main_pay_amount)-int(sub_pay_amount)
    update_paid_amoun=int(main_paid_amount)-int(sub_paid_amount)
    print('main amount--->,',update_rate,update_disc,update_pay_amount,update_paid_amoun)
    main_data.net_amount=update_paid_amoun
    main_data.discount=update_disc
    main_data.pay_amount=update_pay_amount
    main_data.paid_amount=update_paid_amoun
    main_data.save()
    return HttpResponseRedirect(f'/update_opd_bill/{pk}')
# ============================ this is using in OPD Bill Update Delete data =============================================
def temp_service_deleting(request,pk,id):
    OpdBillingTemper.objects.get(id=id).delete()
    return HttpResponseRedirect(f'/update_opd_bill/{pk}')
# ============================================ For Updating OPD Billing Main Table ========================================
def update_bill_main(request,pk):
    all_data=''
    #=================================== For SEPARATING UHID, VISIT ID AND BILL NO =========================================
    uh_visit_id = pk.split('-')
    uhid_p = uh_visit_id[0]
    visit_id_p = uh_visit_id[1]
    bill_id_p=uh_visit_id[2]
    #================================= For Patient Heading Data ==========================================
    records_opd=OpdBillingMain.objects.filter(uhid=uhid_p,visit_no=visit_id_p,bill_no=bill_id_p).extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_OpdBillingMain.uhid',
            'billing_group': 'Select billing_group from testapp_BillingGroup where id=testapp_OpdBillingMain.billing_group_id',
            'corporate_name': 'Select corporate_Name from testapp_CorporateMaster where id=testapp_OpdBillingMain.corporate_id',
    }).last()
    #============================ For Passint Tariff ID In Search Address Views Function, For Getting tariff Related Data =======================================
    request.session['tariff_names']=records_opd.billing_group_id
    #======================== For Displaying Sub Table Data in for Loop Front end ================================
    records_sub = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p, bill_no=bill_id_p).exclude(status='inactive')
    #======================== For Displaying Temp Table Data in for Loop Front end ================================
    records_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p)
    # =================================== For Calculating OPD Billing Sub Table AMT ============================
    rate_amt = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('charges'))
    rate_amt = rate_amt['charges__sum']
    rcv_amt = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('pay_amount'))
    rcv_amt = rcv_amt['pay_amount__sum']
    nt_amt = OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('paid_amount'))
    nt_amt = nt_amt['paid_amount__sum']
    nt_disc =  OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('discount'))
    nt_disc = nt_disc['discount__sum']
    ttl_unit =  OpdBillingSub.objects.filter(uhid=uhid_p, visit_no=visit_id_p,bill_no=bill_id_p).exclude(status='inactive').aggregate(Sum('unit'))
    ttl_unit = ttl_unit['unit__sum']
    # ========================= For Calculating Temp Table AMT ==============================================
    ttl_rate_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('rate'))
    ttl_rate_temp = ttl_rate_temp['rate__sum']
    ttl_qty_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('unit'))
    ttl_qty_temp = ttl_qty_temp['unit__sum']
    ttl_dics_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('discount'))
    ttl_dics_temp = ttl_dics_temp['discount__sum']
    ttl_net_amt_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('net_ammount'))
    ttl_net_amt_temp = ttl_net_amt_temp['net_ammount__sum']
    ttl_amt_temp = OpdBillingTemper.objects.filter(uhid=uhid_p, visit_no=visit_id_p, temp_bill_no=bill_id_p).aggregate(Sum('total_amount'))
    ttl_amt_temp = ttl_amt_temp['total_amount__sum']
    # ============================ For Adding Data Both Tables AMT =========================================
    if ttl_rate_temp == None:
        ttl_rate_temp=0
    if ttl_qty_temp == None:
        ttl_qty_temp = 0
    if ttl_dics_temp == None:
        ttl_dics_temp=0
    if ttl_net_amt_temp == None:
        ttl_net_amt_temp = 0
    if ttl_amt_temp == None:
        ttl_amt_temp = 0
    add_rate=rate_amt+ttl_rate_temp
    add_unit=ttl_unit+ttl_qty_temp
    add_disc=nt_disc+ttl_dics_temp
    add_net_amt=rcv_amt+ttl_net_amt_temp
    add_total_amt=nt_amt+ttl_amt_temp
    # ======================================= Saving Data In Temp Table =======================================
    if request.method == 'POST':
        service_name=request.POST.get('service_name')
        package_profile_id = request.POST.get('package_profile_id')
        package_profile_amt = request.POST.get('package_profile_amt')
        amount = request.POST.get('amount')
        discount = request.POST.get('discount')
        unit = request.POST.get('unit')
        net_amount = request.POST.get('net_amount')
        outstanding_amount = request.POST.get('outstanding_amount')
        total_amount = request.POST.get('total_amount')
        service_category = request.POST.get('service_category')
        service_sub_category = request.POST.get('service_sub_category')
        receive_amount = request.POST.get('receive_amount')
        temp_opd_billing = OpdBillingTemper(
            uhid=uhid_p,
            visit_no=visit_id_p,
            temp_bill_no=bill_id_p,
            package_profile_id=package_profile_id,
            package_profile_amt=package_profile_amt,
            service_name=service_name,
            rate=amount,
            discount=discount,
            unit=unit,
            net_ammount=net_amount,
            outstanding_amount=outstanding_amount,
            total_amount=total_amount,
            service_category_id=service_category,
            service_sub_category_id=service_sub_category,
            receive_amount=receive_amount,
            created_by_id=request.user.id,
            location_id=request.location,
        )
        temp_opd_billing.save()
        return HttpResponseRedirect(f'/update_opd_bill/{pk}')
    # ===================================== End ==============================================
    context={
        'dat':records_opd,'records_sub':records_sub,'pk':pk,'all_data':all_data,'records_temp':records_temp,
        'ttl_amt':add_total_amt,'rate_amt':add_rate,'rcv_amt':rcv_amt,'nt_amt':add_net_amt,'nt_disc':add_disc,'ttl_unit':add_unit,
        'ttl_rate_temp': ttl_rate_temp, 'ttl_qty_temp': ttl_qty_temp, 'ttl_dics_temp': ttl_dics_temp,
        'ttl_net_amt_temp': ttl_net_amt_temp,
        'ttl_amt_temp': ttl_amt_temp,
    }
    return render(request, 'clinical/opd_bill/update_bill_main.html',context)

#========================= FOR DIALYSIS ===========================================
def dialys_prescription_list(request):
    prescription_records = PrescriptionDialysis.objects.all().extra(select={
            'title': 'Select title from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'f_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'm_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'l_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'dob': 'Select dob from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
            'registration_date_and_time': 'Select registration_date_and_time from testapp_patientsregistrationsallinone where uhid=testapp_PrescriptionDialysis.uhid',
    })
    context={
        'prescription_records':prescription_records,
    }
    return render(request,'dialysis/dialys_prescription_list.html',context)

@login_required(login_url='/user_login')
def main_dashboard(request):
    records = AdmissionInfos.objects.all()
    if records:
        month = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sep','Oct','Nov','Dec']
        month_count = [1,2,3,4,5,6,7,8,9,10,11,12]
        register_count=[]
        admiss_count=[]
        admit_count = AdmissionInfos.objects.filter(status__in=['admitted','discharge']).count()
        total_staff = User.objects.all().count()
        total_room = RoomNumber.objects.all().count()
        total_doctor = DoctorTable.objects.all().count()
        current_date = datetime.now()
        opd_payment = OpdPayment.objects.all().aggregate(Sum('paid_amount'))
        opd_income = opd_payment['paid_amount__sum']
        grn_payment = StockEntry_Parent.objects.all().aggregate(Sum('GRN_amount'))
        grn_expense = grn_payment['GRN_amount__sum']
        pharma_payment = PS_CounterSale_Parent.objects.all().aggregate(Sum('paid_amount'))
        pharma_income = pharma_payment['paid_amount__sum']
        consum_payment = Department_Consumption.objects.all().aggregate(Sum('total_amount'))
        consum_income = consum_payment['total_amount__sum']
        if consum_income == None:
            consum_income = 0
            
        income = int(opd_income) + int(pharma_income) + int(consum_income)

        admission_detail = AdmissionInfos.objects.extra(select={
            'first_name':'Select first_name from testapp_patientsregistrationsallinone where uhid=IPDapp_admissioninfos.uhid',
            'middle_name':'Select middle_name from testapp_patientsregistrationsallinone where uhid=IPDapp_admissioninfos.uhid',
            'last_name':'Select last_name from testapp_patientsregistrationsallinone where uhid=IPDapp_admissioninfos.uhid',
            'age':'Select age from testapp_patientsregistrationsallinone where uhid=IPDapp_admissioninfos.uhid',
            'gender':'Select gender from testapp_patientsregistrationsallinone where uhid=IPDapp_admissioninfos.uhid',
        }).all()
        for data in month_count:
            reg = PatientsRegistrationsAllInOne.objects.filter(registration_date_and_time__month=data)
            admiss = AdmissionInfos.objects.filter(admission_datetime__month=data)
            if admiss:
                admiss_count.append(admiss.count())
            else:
                admiss_count.append(0)
            if reg:
                register_count.append(reg.count())
            else:
                register_count.append(0)
        patient_reg=zip(month,register_count)
        patient_admiss = zip(month,admiss_count)
        context={
            'patient_reg':patient_reg,'patient_admiss':patient_admiss,'admit_count':admit_count,'income':income,'grn_expense':grn_expense,
            'total_staff':total_staff,'total_room':total_room,'total_doctor':total_doctor,'admission_detail':admission_detail
        }
        return render(request,'clinical/main_dashboard.html',context)
    else:
        return render(request,'clinical/main_dashboard.html')

@login_required(login_url='/user_login')
def incident_type(request):
    records=Incident_Type_Master.objects.all()
    incident_type_master_form =Incident_Type_MasterForm()
    if request.method=='POST':
        incident_type_master_form=Incident_Type_MasterForm(request.POST)
        if incident_type_master_form.is_valid():
            incident_type_master_form.save()
            return HttpResponseRedirect('/incident_type')
    context={
        'incident_type_master_form':incident_type_master_form,'records':records
    }
    return render(request,"incident/master/incident_type.html",context)

@login_required(login_url='/user_login')
def contributing_factor(request):
    records=Contributing_Factors_Master.objects.all()
    contributing_factor_form =Contributing_Factors_MasterForm()
    if request.method=='POST':
        contributing_factor_form=Contributing_Factors_MasterForm(request.POST)
        if contributing_factor_form.is_valid():
            contributing_factor_form.save()
            return HttpResponseRedirect('/contributing_factor')
    context={
        'contributing_factor_form':contributing_factor_form,'records':records
    }
    return render(request,"incident/master/contributing_factor.html",context)    

@login_required(login_url='/user_login')
def incident_creation_form(request):
    incident_type = Incident_Type_Master.objects.all()
    if request.method =='POST':
        incident_count=Incident_Creation_Form.objects.all().count()
        today=date.today()
        today_date=today.strftime("%d%m%y")
        incident_id='INF'+today_date+str(incident_count)

        incident_creation=Incident_Creation_Form(
            incident_id=incident_id,
            submitter_name=request.POST.get('submitter_name'),
            incident_reported_date=request.POST.get('reported_date'),
            incident_date=request.POST.get('incident_date'),
            incident_type_id=request.POST.get('incident_type'),
            incident_location=request.POST.get('incident_location'),
            affected_people=request.POST.get('affected_people'),
            responsible_dept=request.POST.get('responsible_dept'),
            incident_description=request.POST.get('incident_desc'),
            status='open',
        )
        incident_creation.save()
        return HttpResponseRedirect('/incident_creation_form')
    context = {
        'incident_type':incident_type,'contributing_factor':contributing_factor
    }
    return render(request,"incident/incident_creation_form.html",context)

@login_required(login_url='/user_login')
def investigation_form(request):
    contributing_factor = Contributing_Factors_Master.objects.all()
    incident_details = Incident_Creation_Form.objects.filter(status='open')
    context = {
        'incident_details':incident_details,'contributing_factor':contributing_factor
    }
    return render(request,"incident/investigation_form.html",context)

@login_required(login_url='/user_login')
def investigation_creation_form(request,pk):
    contributing_factor = Contributing_Factors_Master.objects.all()
    incident_details = Incident_Creation_Form.objects.filter(incident_id=pk).first()
    if request.method =='POST':
        invest_count=Incident_Creation_Form.objects.all().count()
        today=date.today()
        today_date=today.strftime("%d%m%y")
        investigation_id='INVF'+today_date+str(invest_count)

        investigation_save=Investigation_Form(
            investigation_id=investigation_id,
            incident_id_id=request.POST.get('incident_id'),
            investigation_date=datetime.now(),
            supervisor_name=request.POST.get('supervisor_name'),
            comments_by_supervisor=request.POST.get('comments_by_supervisor'),
            comments_by_quality_manager=request.POST.get('comments_by_qm'),
            risk_assessment_score=request.POST.get('risk_ass_score'),
            contributing_factors_id=request.POST.get('contributing_factor'),
            investigation_done_by=request.POST.get('invest_done_by'),
            investigation_outcome=request.POST.get('invest_outcomes'),
            final_summary=request.POST.get('final_summary'),
        )
        investigation_save.save()

        incident_update = Incident_Creation_Form.objects.filter(incident_id=pk).first()
        incident_update.status = 'closed'
        incident_update.save()
        return HttpResponseRedirect('/investigation_form')
    context = {
        'incident_details':incident_details,'contributing_factor':contributing_factor
    }
    return render(request,"incident/investigation_creation_form.html",context)

@login_required(login_url='/user_login')
def incident_list_report(request):
    incident_details = Incident_Creation_Form.objects.all()
    context = {
        'incident_details':incident_details
    }
    return render(request,"incident/reports/incident_list_report.html",context)

@login_required(login_url='/user_login')
def investigation_list(request,pk):
    investigation_details = Investigation_Form.objects.filter(incident_id=pk)
    context = {
        'investigation_details':investigation_details
    }
    return render(request,"incident/reports/investigation_list.html",context)

@login_required(login_url='/user_login')
def detailed_incident_list_report(request):
    investigation_details = Investigation_Form.objects.select_related('incident_id')
    print('investigation_details',investigation_details.last().incident_id.submitter_name)
    context = {
        'investigation_details':investigation_details
    }
    return render(request,"incident/reports/detailed_incident_list_report.html",context)    

@login_required(login_url='/user_login')
def incident_dashboard(request):
    incident_type = Incident_Type_Master.objects.all()
    total_incident = Incident_Creation_Form.objects.all().count()
    incident_list = [data.incident_type for data in incident_type]
    incident_closed = Incident_Creation_Form.objects.filter(status='closed').count()
    incident_open = Incident_Creation_Form.objects.filter(status='open').count()
    incident_count =[]
    incid_close = []
    incid_open = []
    status_total = []
    grand_total = 0
    for data in incident_type:
        incident_count.append(Incident_Creation_Form.objects.filter(incident_type_id=data.id).count())
        incid_close.append(Incident_Creation_Form.objects.filter(incident_type_id=data.id,status='closed').count())
        incid_open.append(Incident_Creation_Form.objects.filter(incident_type_id=data.id,status='open').count())
        grand_total += Incident_Creation_Form.objects.filter(incident_type_id=data.id).count()
        status_tot = Incident_Creation_Form.objects.filter(incident_type_id=data.id,status='closed').count() + Incident_Creation_Form.objects.filter(incident_type_id=data.id,status='open').count()
        status_total.append(status_tot)
    incident_count_detail = zip(incident_type,incident_count)
    count_total = incident_closed + incident_open
    incident_detail = zip(incident_type,incid_close,incid_open,status_total)
    js = zip(incident_type,incid_open)
    js1 = zip(incident_type,incid_close)
    print('incid_close',incid_close)
    print('incid_open',incid_open)
    context = {
        'incident_count_detail':incident_count_detail,'incident_count':incident_count,'incident_list':incident_list,
        'incident_closed':incident_closed,'incident_open':incident_open,'grand_total':grand_total,'count_total':count_total,
        'incident_detail':incident_detail,'incid_close':incid_close,'incid_open':incid_open,'js':js,'js1':js1,'total_incident':total_incident
    }
    return render(request,"incident/incident_dashboard.html",context)     

#==================== Lab Report for clinical management doctor ==========================================
@login_required(login_url='/user_login')
def current_report(request,pk):
    access=CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'lab_report' in access.user_profile.screen_access:
        try:
            records_cl = SampleCollected.objects.filter(uhid=pk).extra(select={
                'first_name': 'Select first_name from testapp_patientsregistrationsallinone where uhid=testapp_samplecollected.uhid LIMIT 1',
                'middle_name': 'Select middle_name from testapp_patientsregistrationsallinone where uhid=testapp_samplecollected.uhid LIMIT 1',
                'last_name': 'Select last_name from testapp_patientsregistrationsallinone where uhid=testapp_samplecollected.uhid LIMIT 1',
                'pat_gender': 'Select gender from testapp_patientsregistrationsallinone where uhid=testapp_samplecollected.uhid LIMIT 1',
                'pat_age': 'Select age from testapp_patientsregistrationsallinone where uhid=testapp_samplecollected.uhid LIMIT 1',
                }).exclude(status__in=['waiting','completed',]).order_by('-date_time')
            context={
                'records_cl':records_cl
            }
            return render(request,'lab_module/current_report.html',context)
        except Exception as error:
            return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

#  new lab report code
@login_required(login_url='/user_login')
def final_lab_report_clinical(request,pk):
    pap_records=PAPSMEAR.objects.all()
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
            order_id=data.visit_no
            history=Validation_record.objects.filter(PTID=data.test_id).last()
            record=LabResultEntry.objects.filter(test_id=data.test_id)
            tem=LabTemplateMaster.objects.filter(profile_name=data.profile_name)
            tem2=RadiologyTemplateMaster.objects.filter(service__service_name=data.profile_name)
            pap_template=PAPSMEAR.objects.filter(test_id=data.test_id).last()
            if pap_template:
                template=pap_template.template
            elif tem:
                template=tem.first()
            elif tem2:
                template=tem2.first()
            else:
                template=''
            List.append([data,record,template,history])
        records.append([dep,List])
    context={
        'records':records,'patient_record':patient_record,'barcode':barcode,'referred_by':referred_by,
        'pap_records':pap_records,
        }
    return render(request,'lab_module/final_lab_report_clinical.html',context)
#=========================== END ==================================================   
#========================== Report for doctor Schedule ================================
@login_required(login_url='/user_login')
def dr_schedule_report(request):
    dr_list=DoctorTable.objects.all()
    total_schedule = None
    dr_schedule_records = None
    if request.method=='POST':
        get_dr_id=request.POST.get('dr_id')
        dr_schedule_records=AvailabilityIntradayScheduleMaster.objects.filter(doctor_id=get_dr_id)
        total_schedule=dr_schedule_records.count()
    context = {
        'dr_list': dr_list,'total_schedule':total_schedule,'dr_schedule_records':dr_schedule_records
    }
    return render(request,'admin1/dr_schedule_report.html',context)
@login_required(login_url='/user_login')
def discount_report(request):
    if request.method=="POST":
        s_date=request.POST.get('b_start_date')
        e_date=request.POST.get('b_end_date')
        records_disc=OPDBillDiscountRemark.objects.filter(created_at__range=[s_date,e_date])
        list_bill=[data.bill_no for data in records_disc]
        opd_main=OpdBillingMain.objects.filter(bill_no__in=list_bill)
        both_data=zip(records_disc,opd_main)
        context={
            'records_disc':records_disc,'both_data':both_data,
        }
        return render(request,'clinical/opd_bill/discount_report.html',context)
    return render(request,'clinical/opd_bill/discount_report.html')

@login_required(login_url='/user_login')
def auth_person_disc(request):
    access = CreateUser.objects.select_related('user_profile').filter(login_id=request.user).first()
    if request.user.is_superuser or 'master' in access.user_profile.screen_access:
        try:
            auth_master=AuthorizedPerson.objects.all()
            form=AuthorizedPersonForm()
            if request.method=="POST":
                form=AuthorizedPersonForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/auth_person_disc')
                else:
                    print('Error',form.errors)
                context={
                    'form':form
                }
            context={
            'auth_master':auth_master,'form':form,'access':access
            }
            return render(request,'general_master/auth_person_disc.html',context)
        except Exception as error:
           return render(request,'error.html',{'error':error})
    else:
        return redirect('dashboard')

