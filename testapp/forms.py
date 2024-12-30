from django import forms
from testapp.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from random import *
from mainapp.models import *

class CreateUser_EditForm(forms.ModelForm):
    class Meta:
        model = CreateUser
        fields = '__all__'
        widgets={
            'user_id':forms.HiddenInput(attrs={'class':'form-control'}),
            'login_id':forms.HiddenInput(attrs={'class':'form-control'}),
            'f_name':forms.TextInput(attrs={'class':'form-control'}),
            'middle_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            'user_profile':forms.Select(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'create_datatime':forms.widgets.DateTimeInput(attrs={'class':'form-control'}),
            'date_of_join':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'date_of_living':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreateUser_EditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CreateUser
        fields = '__all__'
        widgets={
            'user_id':forms.HiddenInput(attrs={'class':'form-control'}),
            'f_name':forms.TextInput(attrs={'class':'form-control'}),
            'middle_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            'user_profile':forms.Select(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'create_datatime':forms.widgets.DateTimeInput(attrs={'class':'form-control'}),
            'date_of_join':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'date_of_living':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'is_admin' : forms.CheckboxInput(attrs = {'class':'form-control'})

        }
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name']
        widgets={
            'username':forms.TextInput(attrs={'hidden':'hidden'}),
            'password1':forms.PasswordInput(attrs={'hidden':'hidden'}),
            'password2':forms.PasswordInput(attrs={'hidden':'hidden'}),
            'email':forms.EmailInput(attrs={'hidden':'hidden'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'hidden': 'hidden'})
        self.fields['password2'].widget.attrs.update({'hidden': 'hidden'})
        self.fields['first_name'].widget.attrs.update({'hidden': 'hidden'})


class DoctorTableForm(forms.ModelForm):
    class Meta:
        model=DoctorTable
        fields='__all__'
        widgets={
        'doctor_id':forms.HiddenInput(attrs={'value':'Null'}),
        'doctor_email_address':forms.EmailInput(attrs={'placeholder':'Enter Valid Doctor email address'}),
        'doctor_name':forms.TextInput(attrs={'placeholder':'Enter Valid Doctor Name'}),
        'doctor_phone_no':forms.NumberInput(attrs={'placeholder':'Enter Valid Doctor Phone Number'}),
        'doctor_registration_no':forms.HiddenInput(attrs={'value':'Null'}),
        'doctor_location':forms.TextInput(attrs={'placeholder':'Enter Valid Doctor Location'}),
        'doctor_date_of_birth':forms.NumberInput(attrs={'type':'date'}),
        'doctor_appointment':forms.NumberInput(attrs={'type':'date'}),
        'registration_exparing_date':forms.NumberInput(attrs={'type':'date'}),
        'doctor_address':forms.TextInput(attrs={'placeholder':'Enter Full Address'}),
        }
    # def clean(self):
    #     total_cleaned_data=super().clean()
    #     doctor_phone_no=total_cleaned_data['doctor_phone_no']
    #     if len(str(doctor_phone_no))==10:
    #         pass
    #     else:
    #         raise forms.ValidationError('Doctor Mobile Number Must Be 10 digits only')
class DoctorScheduleTableForm(forms.ModelForm):
    class Meta:
        model=DoctorScheduleTable
        fields='__all__'
        widgets={
        'doctor_schedule_date':forms.NumberInput(attrs={'type':'date'}),
        'doctor_schedule_start_time':forms.TimeInput(attrs={'type':'time'}),
        'doctor_schedule_end_time':forms.TimeInput(attrs={'type':'time'}),
        'average_consulting_time':forms.TimeInput(attrs={'type':'time','placeholder':'Enter Time format in minuts'}),
        }

class AppointmentTableForm(forms.ModelForm):
    class Meta:
        model=AppointmentTable
        fields='__all__'
class PatientTableForm(forms.ModelForm):
    class Meta:
        model=PatientTable
        fields='__all__'
class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model=DoctorSchedule
        fields='__all__'
        widgets={
        'start_date':forms.TextInput(attrs={'type':'date'}),
        'end_date':forms.TextInput(attrs={'type':'date'})
        }
# Available Day Schedule Master Temp Form
class AvailableDayScheduleMasterTemp(forms.Form):
    doctor_id=forms.CharField()
    dates_available=forms.CharField()
    time_slots=forms.CharField()
    schedule_id_of_each_slot=forms.CharField()
class BookedAppointmentsForm(forms.ModelForm):
    class Meta:
        model=BookedAppointments
        fields=['patient_scheduled_id']
class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
class NewAppointmentByAdminForm(forms.Form):
    GENDER=(
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
    )
    appointment_id=forms.CharField(max_length=200)
    patient_id=forms.CharField(max_length=200)
    patient_name=forms.CharField(max_length=200)
    email_id=forms.EmailField(max_length=200)
    age=forms.CharField(max_length=200)
    gender=forms.CharField(label='Gender',widget=forms.Select(choices=GENDER))
    mobile_number=forms.CharField(max_length=200)
    # class Meta:
    #     model=NewAppointmentByAdmin
    #     fields='__all__'
class NewAppointmentByAdminChooseDoctorForm(forms.ModelForm):
    class Meta:
        model=NewAppointmentByAdminChooseDoctor
        fields='__all__'
        widgets={
        'appointment_date':forms.NumberInput(attrs={'type':'date'})
        }

#Capering data from user

class TokenMasterConfigurationForm(forms.ModelForm):
    class Meta:
        model=TokenMasterConf
        fields='__all__'
        widgets = {
            'Date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control',}),
        }
        
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Date'].initial = datetime.now().date()
#MasterForm
class TitleMasterForm(forms.ModelForm):
    class Meta:
        model=TitleMaster
        fields='__all__'
class HospitalMasterForm(forms.ModelForm):
    class Meta:
        model=HospitalMaster
        fields='__all__'

class HolidayMasterForm(forms.ModelForm):
    class Meta:
        model=HolidayMaster
        fields='__all__'
        widgets={
        'holiday_date':forms.NumberInput(attrs={'type':'date'})
        }
class MostCommonDocumentTypeMasterForm(forms.ModelForm):
    class Meta:
        model=MostCommonDocumentTypeMaster
        fields='__all__'
        widgets={
        'holiday_date':forms.NumberInput(attrs={'type':'date'})
        }
class RelationMasterForm(forms.ModelForm):
    class Meta:
        model=RelationMaster
        fields='__all__'
class GenderMaterForm(forms.ModelForm):
    class Meta:
        model=GenderMater
        fields='__all__'
class MaritalStatusMasterForm(forms.ModelForm):
    class Meta:
        model=MaritalStatusMaster
        fields='__all__'
class DistrictMasterForm(forms.ModelForm):
    class Meta:
        model=DistrictMaster
        fields='__all__'
class CountryMasterForm(forms.ModelForm):
    class Meta:
        model=CountryMaster
        fields='__all__'
class CityMasterForm(forms.ModelForm):
    class Meta:
        model=CityMaster
        fields='__all__'
#======Service Master===============
class ServiceMasterForm(forms.ModelForm):
    class Meta:
        model=ServiceMaster
        fields='__all__'
class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model=ServiceCategory
        fields=['service_category']
class ServiceSubCategoryForm(forms.ModelForm):
    class Meta:
        model=ServiceSubCategory
        fields=['service_sub_category']
class TariffMasterForm(forms.ModelForm):
    class Meta:
        model=TariffMaster
        fields='__all__'
class CorporateMasterForm(forms.ModelForm):
    class Meta:
        model=CorporateMaster
        fields='__all__'
        widgets={
        'corporate_ID':forms.HiddenInput(attrs={'value':'77707'}),
        'valid_Upto':forms.NumberInput(attrs={'type':'date'}),
        }
class TariffChargeMasterForm(forms.ModelForm):
    class Meta:
        model=TariffChargeMaster
        fields='__all__'
        widgets={
        'apply_From':forms.NumberInput(attrs={'type':'date'}),
        }
class CorporateMasterForm2(forms.ModelForm):
    class Meta:
        model=CorporateMaster
        exclude=('corporate_ID','corporate_Name')
        widgets={
        'corporate_ID':forms.HiddenInput(attrs={'value':'77707'}),
        'valid_Upto':forms.NumberInput(attrs={'type':'date'}),
        }
class BillingGroupTariffLinkForm(forms.ModelForm):
    class Meta:
        model=BillingGroupTariffLink
        fields='__all__'
class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model=ServiceCategory
        fields='__all__'
class ServiceSubCategoryForm(forms.ModelForm):
    class Meta:
        model=ServiceSubCategory
        fields='__all__'
class ServiceDepartmentForm(forms.ModelForm):
    class Meta:
        model=ServiceDepartment
        fields='__all__'
class ServiceSubDepartmentForm(forms.ModelForm):
    class Meta:
        model=ServiceSubDepartment
        fields='__all__'
class WardCategoryForm(forms.ModelForm):
    class Meta:
        model=WardCategory
        fields='__all__'
class WardTypeForm(forms.ModelForm):
    class Meta:
        model=WardType
        fields='__all__'
class BloodMasterForm(forms.ModelForm):
    class Meta:
        model=BloodMaster
        fields='__all__'
class DesignationForm(forms.ModelForm):
    class Meta:
        model=Designation
        fields='__all__'

class TokenCreationForm(forms.ModelForm):
    class Meta:
        model=TokenCreations
        exclude=('Token_No',)

class TokenCreationForm2(forms.ModelForm):
    class Meta:
        model=TokenCreations
        fields=['Date','Doct_Name','Patient_Id']

class TokenCreationForm3(forms.ModelForm):
    class Meta:
        model=TokenCreations
        fields=['Token_No','Room_No']

class CentralisedAdminViewForm(forms.ModelForm):
    class Meta:
        model=CentralisedAdminView
        exclude=('Current_In','Next_Waiting')
class RoomNumberForm(forms.ModelForm):
    class Meta:
        model=RoomNumber
        fields='__all__'
# For Replicated Start Date And End Date
class ReplicatedForm(forms.Form):
    # widget=forms.SelectDateWidget() == full calendar year month and date dropdown format
    start_date=forms.DateField(widget=forms.NumberInput(attrs={'type':'date'}))
    end_date=forms.DateField(widget=forms.NumberInput(attrs={'type':'date'}))

class PatientsRegistrationsAllInOneForm(forms.ModelForm):
    class Meta:
        model=PatientsRegistrationsAllInOne
        fields='__all__'
        widgets = {
            'uhid': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'created_by': forms.HiddenInput(),
            'location': forms.HiddenInput(),
        }
    title = forms.ChoiceField(choices=[])
    gender = forms.ChoiceField(choices=[])
    marital_status = forms.ChoiceField(choices=[])
    referred_by = forms.ChoiceField(choices=[])
    relationship = forms.ChoiceField(choices=[])
    billing_group = forms.ChoiceField(choices=[])
    nhif_ins_cor_name = forms.ChoiceField(choices=[])
    staff_member = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].choices = [(author.initial, author.initial) for author in TitleMaster.objects.all()]
        self.fields['gender'].choices = [(data.Gender, data.Gender) for data in GenderMater.objects.all()]
        self.fields['marital_status'].choices = [(data.marital_status, data.marital_status) for data in MaritalStatusMaster.objects.all()]
        self.fields['referred_by'].choices = [(data.id, data.Staff_name) for data in Refered_by_Master.objects.all()] + [('Walked By', 'Walked By')]
        self.fields['relationship'].choices = [(data.id, data.relation_name) for data in RelationMaster.objects.all()]
        self.fields['billing_group'].choices = [(data.id, data.billing_group) for data in BillingGroup.objects.all()]
        self.fields['nhif_ins_cor_name'].choices = [('Cash','Cash')]
        self.fields['nhif_ins_cor_name'].choices = [(data.id,data.corporate_Name) for data in CorporateMaster.objects.all()] + [('Cash', 'CASH')]
        self.fields['staff_member'].choices = [('Yes','Yes'),('No','No')]
        self.fields['father_or_husband_name'].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GroupMasterForm(forms.ModelForm):
    class Meta:
        model=GroupMaster
        fields='__all__'
class BranchMasterForm(forms.ModelForm):
    class Meta:
        model=BranchMaster
        fields='__all__'
class PatientVisitMainForm(forms.ModelForm):
    class Meta:
        model=PatientVisitMains
        fields='__all__'
        widgets = {
            'uhid': forms.HiddenInput(attrs={'value': 'Null'}),
            'visit_id': forms.HiddenInput(attrs={'value': 'Null'}),
        }
class ClinicalOrDepartmentForm(forms.ModelForm):
    class Meta:
        model=ClinicalOrDepartment
        fields="__all__"
class VisitTyoeMasterForm(forms.ModelForm):
    class Meta:
        model=VisitTyoeMaster
        fields="__all__"
# Opd Billing form
from testapp.models import PatientVisitMains
from django.forms.models import ModelChoiceField
class VisitForm(forms.Form):
    uhid=forms.CharField(max_length=50)
    # visit_no=forms.ModelChoiceField(PatientVisitMains.objects,required=False)
    # search_visit_no=forms.CharField(required=False)
# Billing Opd Form 2
class BillingCreationForm(forms.Form):
    service_master=forms.CharField()
    doctor=forms.CharField()
    amount=forms.CharField()
    discount=forms.CharField()
    unit=forms.CharField()
    net_amount=forms.CharField()
    co_pay=forms.CharField()
    company_name=forms.CharField()
    patient_amount=forms.CharField()
    receive_amount=forms.CharField()
    view=forms.CharField()
class BillingGroupCorporateForm1(forms.ModelForm):
    class Meta:
        model=BillingGroupCorporateMaster
        fields='__all__'
    # Corporate_Name=(
    #     ('name1','xxx'),
    #     ('name2','yyy'),
    #     ('name3','zzz'),
    # )
    # Billing_Group=(
    #     ('grp1','grp1'),
    #     ('grp2','grp2'),
    #     ('grp3','grp3'),
    # )
    # corporate_name=forms.ChoiceField(choices=Corporate_Name)
    # billing_group=forms.ChoiceField(choices=Billing_Group)
class BillingGroupForm(forms.ModelForm):
    class Meta:
        model=BillingGroup
        fields='__all__'
# class OpdPaymentForm(forms.ModelForm):
#     class Meta:
#         model=OpdPayment
#         fields='__all__'
#================= By mantu ========================
class OpdPaymentCashForm(forms.ModelForm):
    class Meta:
        model=OpdPayment
        fields='__all__'
class OpdPaymentCreditForm(forms.ModelForm):
    class Meta:
        model=OpdPayment
        fields='__all__'
class OpdPaymentWalletForm(forms.ModelForm):
    class Meta:
        model=OpdPayment
        fields='__all__'
class OpdPaymentUPIForm(forms.ModelForm):
    class Meta:
        model=OpdPayment
        fields='__all__'
# ==============IPD and Pharmacy======================
class MaterialIndentForm(forms.Form):
    SUB_STORE = (
        ('store1', 'store1'),
        ('store2', 'store2'),
        ('store3', 'store3'),
        ('store4', 'store4'),
    )
    Priority = (
        ('priority1', 'priority1'),
        ('priority2', 'Priority2'),
        ('priority3', 'Priority3'),
        ('priority4', 'Priority4'),
    )
    Item_name = (
        ('item1', 'Item1'),
        ('item2', 'Item2'),
        ('item3', 'Item3'),
        ('item4', 'Item4'),
    )
    Item_code = (
        ('code1', 'code1'),
        ('code2', 'code2'),
        ('code3', 'code3'),
        ('code4', 'code4'),
    )
    Item_Belongs_to = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )

    indent_no = forms.CharField(max_length=100)
    indent_datetime = forms.DateTimeField()
    sub_store = forms.ChoiceField(choices=SUB_STORE)
    priority = forms.ChoiceField(choices=Priority)
    item_name = forms.ChoiceField(choices=Item_name)
    quantity = forms.CharField(max_length=100)
    item_code = forms.ChoiceField(choices=Item_code)
    item_belongs_to = forms.ChoiceField(choices=Item_Belongs_to)
    remark = forms.CharField(max_length=250)


class IndentInboxForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    sub_store = forms.CharField(max_length=50)


class ItemIssueForm(forms.Form):
    Issue_Store = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )
    Receiving_Store = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )
    Priority = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )
    Item_Name = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
    )
    indent_no = forms.CharField()
    issuing_store = forms.ChoiceField(choices=Issue_Store)
    receiving_store = forms.ChoiceField(choices=Receiving_Store)
    datetime = forms.DateTimeField()
    approved_by = forms.CharField(max_length=100)
    priority = forms.ChoiceField(choices=Priority)

    # right side above table
    barcode = forms.CharField()
    item_name = forms.ChoiceField(choices=Item_Name)
    batch_serial = forms.CharField()
    expiry_date = forms.CharField()
    available_qty = forms.CharField()
    issue_qty = forms.CharField()
    remarks = forms.CharField(max_length=250)


class IssueInboxForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    store = forms.CharField(max_length=50)


class ChallanBillForm(forms.Form):
    Document_type = (
        ('document1', 'document1'),
        ('document2', 'document2'),
        ('document3', 'document3'),
    )
    Store = (
        ('store1', 'store1'),
        ('store2', 'store2'),
        ('store3', 'store3'),
    )
    purchase_no = forms.CharField()
    vendor_name = forms.CharField()
    date = forms.DateField()
    document_type = forms.ChoiceField(choices=Document_type)
    bill_date = forms.DateField()
    bill_number = forms.CharField()
    bill_amount = forms.CharField()
    discount = forms.CharField()
    remark = forms.CharField()
    store = forms.ChoiceField(choices=Store)

    # Item Info
    Item_Name = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
    )
    Packing = (
        ('pack1', 'pack1'),
        ('pack2', 'pack2'),
        ('pack3', 'pack3'),
    )
    GST = (
        ('gst1', '5%'),
        ('gst2', '10%'),
        ('gst3', '25%'),
    )
    item_name = forms.ChoiceField(choices=Item_Name)
    HSN_code = forms.CharField()
    Packing = forms.ChoiceField(choices=Packing)
    Batch_Number = forms.CharField()
    MFG_Date = forms.CharField()
    Expiry_Date = forms.CharField()
    Paid_Qty = forms.CharField()
    Free_Qty = forms.CharField()
    MRP = forms.CharField()
    Sale_level1 = forms.CharField()
    Sale_level2 = forms.CharField()
    Rate = forms.CharField()
    Item_Disc = forms.CharField()
    Disc_Amt = forms.CharField()
    GST = forms.ChoiceField(choices=GST)
    GST_Amt = forms.CharField()
    CGST = forms.CharField()
    SGST = forms.CharField()
    IGST = forms.CharField()
    CGST_Amt = forms.CharField()
    SGST_Amt = forms.CharField()
    IGST_Amt = forms.CharField()
    Net_Rate = forms.CharField()
    Total_Amount = forms.CharField()

    message = forms.CharField()
    Total_CGST = forms.CharField()
    Total_Product_Amt = forms.CharField()
    Total_SGST = forms.CharField()
    Item_Disc = forms.CharField()
    Bill_Disc = forms.CharField()
    Total_IGST = forms.CharField()
    Total_GST = forms.CharField()
    Other_Adj_Amount = forms.CharField()
    Net_Amount = forms.CharField()


class BillingGroupCorporateForm(forms.Form):
    Corporate_Name = (
        ('name1', 'xxx'),
        ('name2', 'yyy'),
        ('name3', 'zzz'),
    )
    Billing_Group = (
        ('grp1', 'grp1'),
        ('grp2', 'grp2'),
        ('grp3', 'grp3'),
    )

    corporate_name = forms.ChoiceField(choices=Corporate_Name)
    billing_group = forms.ChoiceField(choices=Billing_Group)


class StockEntryForm(forms.Form):
    Item = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
    )
    GST = (
        ('gst1', '5%'),
        ('gst2', '10%'),
        ('gst3', '25%'),
    )
    Store = (
        ('Store1', 'Store1'),
        ('Store2', 'Store2'),
        ('Store3', 'Store3'),
    )
    item = forms.ChoiceField(choices=Item)
    from_date = forms.CharField()
    to_date = forms.CharField()

    item = forms.ChoiceField(choices=Item)
    Store = forms.ChoiceField(choices=Store)
    Batch_Number = forms.CharField()
    MRP = forms.CharField()
    Expiry_Date = forms.CharField()
    Pysical_Qty = forms.CharField()
    GST = forms.ChoiceField(choices=GST)
    CGST = forms.CharField()
    SGST = forms.CharField()
    IGST = forms.CharField()
    Remark = forms.CharField()


class ItemDetailForm(forms.Form):
    Indent = (
        ('indent1', '001'),
        ('indent2', '002'),
        ('indent3', '003'),
    )
    VendorName = (
        ('vendor1', 'vendor1'),
        ('vendor1', 'vendor2'),
        ('vendor1', 'vendor3'),

    )
    Priority = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )
    Belongs = (
        ('belongs1', 'belongs1'),
        ('belongs2', 'belongs2'),
        ('belongs3', 'belongs3'),
        ('belongs4', 'belongs4'),
    )
    Item_Code = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )
    Item_Name = (
        ('item1', 'item1'),
        ('item2', 'item2'),
        ('item3', 'item3'),
        ('item4', 'item4 '),
    )
    Packing = (
        ('pack1', 'pack1'),
        ('pack2', 'pack2'),
        ('pack3', 'pack3'),
    )
    indent_no = forms.ChoiceField(choices=Indent)
    Suggested_vendor_name = forms.ChoiceField(choices=VendorName)
    priority = forms.ChoiceField(choices=Priority)
    Remark = forms.CharField()

    item_belongs_to = forms.ChoiceField(choices=Belongs)
    item_code = forms.ChoiceField(choices=Item_Code)
    item_name = forms.ChoiceField(choices=Item_Name)
    packing = forms.ChoiceField(choices=Packing)
    quantity = forms.CharField()


class IpdFrontDeskForm(forms.Form):
    Admission_type = (
        ('add1', 'add1'),
        ('add2', 'add2'),
        ('add3', 'add3'),
    )
    admission_datetime = forms.CharField()
    admission_type = forms.ChoiceField(choices=Admission_type)
    request_ward_type = forms.CharField()
    request_ward_category = forms.CharField()
    infected = forms.BooleanField()
    mlc = forms.BooleanField()
    mlc_no = forms.CharField()

    # Doctor Detail
    Primary_Doctor = (
        ('p1', 'doc1'),
        ('p2', 'doc2'),
        ('p3', 'doc3'),
    )
    Department = (
        ('dept1', 'dept1'),
        ('dept2', 'dept2'),
        ('dept3', 'dept3'),
    )
    Ref_Hospital = (
        ('hos1', 'hos1'),
        ('hos2', 'hos2'),
        ('hos3', 'hos3'),
    )

    primary_doctor = forms.ChoiceField(choices=Primary_Doctor)
    Department = forms.ChoiceField(choices=Department)
    Secondary_doctor = forms.CharField()
    Ref_hospital = forms.ChoiceField(choices=Ref_Hospital)

    bed_no = forms.CharField()


class SearchAdmittedPatientForm(forms.Form):
    patient_name = forms.CharField()
    mobile_number = forms.CharField()


class BedShiftingIntimationForm(forms.Form):
    WING = (
        ('WING1', 'WING1'),
        ('WING2', 'WING2'),
    )
    FLOOR = (
        ('floor1', 'floor1'),
        ('floor2', 'floor2'),
    )
    RequestedCategory = (
        ('req1', 'req1'),
        ('req1', 'req1'),
    )
    AllotedCategory = (
        ('allot1', 'allot1'),
        ('allot2', 'allot2'),
    )
    WardType = (
        ('Ward1', 'Ward1'),
        ('Ward2', 'Ward2'),
    )
    BedNo = (
        ('bed1', 'bed1'),
        ('bed2', 'bed2'),
    )

    wing = forms.ChoiceField(choices=WING)
    floor = forms.ChoiceField(choices=FLOOR)
    requested_category = forms.ChoiceField(choices=RequestedCategory)
    alloted_category = forms.ChoiceField(choices=AllotedCategory)
    ward_type = forms.ChoiceField(choices=WardType)
    bed_no = forms.ChoiceField(choices=BedNo)
    higher_category_remark = forms.CharField()
    remark_for_cancel = forms.CharField()


# 23/04/2022 Pharmacy
class SoaForm(forms.Form):
    ItemName = (
        ('Item1', 'Item1'),
        ('Item2', 'Item2'),
    )
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)
    item_name = forms.ChoiceField(choices=ItemName)
    search_by_anything = forms.CharField(max_length=50, required=False)


class VendorForm(forms.Form):
    ItemName = (
        ('Item1', 'Item1'),
        ('Item2', 'Item2'),
    )
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)
    search_here = forms.CharField(max_length=50, required=False)


class PoForm(forms.Form):
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)
    po_no = forms.CharField(required=False)
    vendor_name = forms.CharField(required=False)


class GatePassForm(forms.Form):
    IssuingStore = (
        ('Item1', 'Item1'),
        ('Item2', 'Item2'),
    )
    VendorName = (
        ('vendor1', 'vendor1'),
        ('vendor1', 'vendor2'),
        ('vendor1', 'vendor3'),
    )
    AuthorizedName = (
        ('name1', 'name1'),
        ('name2', 'name2'),
    )
    Manufacture = (
        ('name1', 'name1'),
        ('name2', 'name2'),
    )
    ItemName = (
        ('Item1', 'Item1'),
        ('Item2', 'Item2'),
    )
    Packing = (
        ('pack1', 'pack1'),
        ('pack2', 'pack2'),
        ('pack3', 'pack3'),
    )
    gatepass_no = forms.CharField(required=False)
    datetime = forms.DateField(required=False)
    issuing_store = forms.ChoiceField(choices=IssuingStore)
    vendor_name = forms.ChoiceField(choices=VendorName)
    authorized_name = forms.ChoiceField(choices=AuthorizedName)
    manufacture = forms.ChoiceField(choices=Manufacture)
    item_name = forms.ChoiceField(choices=ItemName)
    batch_serial_no = forms.CharField()
    item_code = forms.CharField()
    qty = forms.CharField()
    packing = forms.ChoiceField(choices=Packing)
    reason = forms.CharField()

    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)


class DetailsOfReceiverForm(forms.Form):
    DocumentType = (
        ('doc1', 'doc1'),
        ('doc2', 'doc2'),
        ('doc3', 'doc3'),
    )
    Store = (
        ('Store1', 'Store1'),
        ('Store2', 'Store2'),
        ('Store3', 'Store3'),
    )
    document_type = forms.ChoiceField(choices=DocumentType)
    store = forms.ChoiceField(choices=Store)

    returndate = forms.DateField(required=False)
    returnnumber = forms.DateField(required=False)
    againstinvoice = forms.CharField(required=False)
    invoicedate = forms.DateField(required=False)

    gstin = forms.CharField(required=False)
    address = forms.CharField(required=False)
    state = forms.CharField(required=False)

    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)

    paid_qty = forms.CharField(required=False)
    free_qty = forms.CharField(required=False)
    rate = forms.CharField(required=False)
    bill_disc = forms.CharField(required=False)
    item_disc = forms.CharField(required=False)
    disc_amt = forms.CharField(required=False)
    gst = forms.CharField(required=False)
    gst_amt = forms.CharField(required=False)
    cgst = forms.CharField(required=False)
    cgst_amt = forms.CharField(required=False)
    sgst = forms.CharField(required=False)
    sgst_amt = forms.CharField(required=False)
    igst = forms.CharField(required=False)
    igst_amt = forms.CharField(required=False)

    total_amt_before_tax = forms.CharField(required=False)
    total_bill_disc = forms.CharField(required=False)
    total_item_disc = forms.CharField(required=False)
    net_amt = forms.CharField(required=False)
    total_cgst = forms.CharField(required=False)
    total_sgst = forms.CharField(required=False)
    total_tax_amt = forms.CharField(required=False)
    total_amt_after_tax = forms.CharField(required=False)


class DueBillForm(forms.Form):
    Bank = (
        ('bank1', 'bank1'),
        ('bank2', 'bank2'),
        ('bank3', 'bank3'),
    )
    vendors_name = forms.CharField(required=False)

    total_amt_to_paid = forms.CharField(required=False)
    total_paying_amt = forms.CharField(required=False)

    vendor_no = forms.CharField(required=False)
    vendor_date = forms.CharField(required=False)
    total_amount = forms.CharField(required=False)
    paid_amount = forms.CharField(required=False)
    remarks = forms.CharField(required=False)

    cash_amount = forms.CharField()
    bank = forms.ChoiceField(choices=Bank)
    transaction_id = forms.CharField()
    amount = forms.CharField(required=False)
    cheque_no = forms.CharField()
    date = forms.CharField()
    amount = forms.CharField(required=False)


class IndentDetailForm(forms.Form):
    ItemName = (
        ('Item1', 'Item1'),
        ('Item2', 'Item2'),
    )
    GST = (
        ('gst1', 'Gst1'),
        ('gst2', 'Gst2'),
    )

    purchase_order_number = forms.CharField(required=False)
    date = forms.DateField()
    vendor_code = forms.CharField()
    vendor_name = forms.CharField()
    bill_disc = forms.CharField(required=False)

    item_name = forms.ChoiceField(choices=ItemName)
    hsn_code = forms.CharField()
    indent_qty = forms.CharField()
    paid_qty = forms.CharField()
    free_qty = forms.CharField()
    total_qty = forms.CharField()
    rate = forms.CharField()
    item_disc = forms.CharField()
    disc_amt = forms.CharField()
    gst = forms.ChoiceField(choices=GST)
    gst_amt = forms.CharField()
    net_amt = forms.CharField()
    cgst = forms.CharField()
    sgst = forms.CharField()
    igst = forms.CharField()
    cgst_amt = forms.CharField()
    sgst_amt = forms.CharField()
    igst_amt = forms.CharField()

    indent_number = forms.CharField()

    total_amt = forms.CharField(required=False)
    total_disc_amt = forms.CharField(required=False)
    total_gst_amt = forms.CharField(required=False)
    total_net_amt = forms.CharField(required=False)
    packaging_forwarding = forms.CharField(required=False)
    other_expenses = forms.CharField(required=False)
    bill_disc_amt = forms.CharField(required=False)
    net_payable_amt = forms.CharField(required=False)

# date - 02-05-2022
class ItemMasterForm(forms.Form):
    BelongsTo = (
        ('1', '1'),
        ('2', '2'),
    )
    Item_Category = (
        ('1', '1'),
        ('2', '2'),
    )
    Packing = (
        ('pack1', 'Pack1'),
        ('pack2', 'Pack2'),
    )
    Unit = (
        ('unit1', 'Unit1'),
        ('unit2', 'Unit2'),
    )
    GST = (
        ('gst1', 'Gst1'),
        ('gst2', 'Gst2'),
    )
    MANUFACTURERS = (
        ('manufacturers1', 'manufacturers1'),
        ('manufacturers2', 'manufacturers2'),
    )
    Suppliers = (
        ('suppliers1', 'Suppliers1'),
        ('suppliers2', 'Suppliers2'),
    )
    Generic = (
        ('gen1', 'gen1'),
        ('gen2', 'gen2'),
    )
    num_of_reuse = forms.CharField()
    serial_batch_control = forms.CharField()
    reusable_rate = forms.CharField()

    belongs_to = forms.ChoiceField(choices=BelongsTo)
    item_category = forms.ChoiceField(choices=Item_Category)
    item_name = forms.CharField(required=False)
    shortcode = forms.CharField()
    packing = forms.ChoiceField(choices=Packing)
    contain = forms.CharField(required=False)
    unit = forms.ChoiceField(choices=Unit)
    conversion_factor = forms.CharField(required=False)
    hsn_code = forms.CharField()
    hospital_item_code = forms.CharField(required=False)
    remark = forms.CharField(required=False)
    Gst = forms.ChoiceField(choices=GST)

    min_quantity = forms.CharField()
    max_quantity = forms.CharField()
    re_order_level = forms.CharField()

    manufacturers = forms.ChoiceField(choices=MANUFACTURERS)
    suppliers = forms.ChoiceField(choices=Suppliers)
    generic = forms.ChoiceField(choices=Generic)


class StoreNursingCounterForm(forms.Form):
    Store = (
        ('store1', 'Store1'),
        ('store2', 'Store2'),
    )
    NursingCounter = (
        ('counter1', 'Counter1'),
        ('counter2', 'Counter2'),
    )
    Department = (
        ('dept1', 'Dept1'),
        ('dept2', 'Dept2'),
    )
    storelinkId = forms.CharField()
    store = forms.ChoiceField(choices=Store)
    nursingcounter = forms.ChoiceField(choices=NursingCounter)
    department = forms.ChoiceField(choices=Department)


class ItemLocationForm(forms.Form):
    StoreName = (
        ('store1', 'Store1'),
        ('store2', 'Store2'),
    )
    ItemName = (
        ('counter1', 'Counter1'),
        ('counter2', 'Counter2'),
    )
    Location = (
        ('dept1', 'Dept1'),
        ('dept2', 'Dept2'),
    )
    location_Id = forms.CharField()
    Item_name = forms.ChoiceField(choices=ItemName)
    store_name = forms.ChoiceField(choices=StoreName)
    location = forms.ChoiceField(choices=Location)
    remark = forms.CharField()


class StoreMasterForm(forms.Form):
    ParentStore = (
        ('store1', 'store1'),
        ('store2', 'store2'),
    )
    Wing = (
        ('store1', 'Store1'),
        ('store2', 'Store2'),
    )
    Floor = (
        ('store1', 'Store1'),
        ('store2', 'Store2'),
    )
    LocationName = (
        ('store1', 'Store1'),
        ('store2', 'Store2'),
    )
    StoreType = (
        ('store1', 'Store1'),
        ('store2', 'Store2'),
    )
    store_Id = forms.CharField()
    store_name = forms.CharField()
    parent_store = forms.ChoiceField(choices=ParentStore)
    wing = forms.ChoiceField(choices=Wing)
    floor = forms.ChoiceField(choices=Floor)
    location_name = forms.ChoiceField(choices=LocationName)
    store_type = forms.ChoiceField(choices=StoreType)


class VendorMasterrForm(forms.Form):
    City = (
        ('city1', 'Chennai'),
        ('city2', 'Salem'),
    )
    District = (
        ('district1', 'Chennai'),
        ('district2', 'Salem'),
    )
    Rating = (
        ('1', '1'),
        ('2', '2'),
    )

    vendor_Id = forms.CharField()
    vendor_name = forms.CharField()
    vendor_short_name = forms.CharField()
    contact_person = forms.CharField()
    address = forms.CharField()
    city = forms.ChoiceField(choices=City)
    district = forms.ChoiceField(choices=District)
    pincode = forms.CharField()
    phone1 = forms.CharField()
    phone2 = forms.CharField()
    fax_no = forms.CharField()
    email = forms.CharField()
    website = forms.CharField()
    tax_id = forms.CharField()
    rating = forms.ChoiceField(choices=Rating)
    afc_code = forms.CharField()
    type_char = forms.CharField()

# Vital Sign
class VitalSignForm(forms.ModelForm):
    class Meta:
        model=VitalSign
        fields='__all__'
        widgets={
            'comments':forms.Textarea(attrs={'rows':1,'cols':18}),
            'weight':forms.NumberInput(attrs={'class':'num1 key'}),
            'height':forms.NumberInput(attrs={'class':'num2 key'}),
            'bmi':forms.NumberInput(attrs={'class':'sum'}),
        }
class PrescriptionMedicineForm(forms.ModelForm):
    class Meta:
        model=PreMedicine
        fields="__all__"
        widgets={
            'prescribe_date':forms.TextInput(attrs={'type':'date'}),
            'end_date':forms.TextInput(attrs={'type':'date'}),
        }
class DiagnosisForm(forms.ModelForm):
    class Meta:
        model=Diagnosis
        fields="__all__"
class DiagnosisMasterForm(forms.ModelForm):
    class Meta:
        model=DiagnosisMaster
        fields="__all__"
# Inventory Master Start
class ItemMasterForm(forms.ModelForm):
    class Meta:
        model = ItemMaster
        fields = '__all__'

class Inventory_ItemMasterForm(forms.ModelForm):
    class Meta:
        model=Inventory_ItemMaster
        fields='__all__'

class Generic_MasterForm(forms.ModelForm):
    class Meta:
        model=Generic_Master
        fields='__all__'

# class ItemManufactForm(forms.ModelForm):
#     class Meta:
#         model=ItemManufact
#         fields='_all_'


class StoreNursingCounterForm(forms.ModelForm):
    class Meta:
        model = StoreNursingCounter
        fields = '__all__'


class ItemLocationForm(forms.ModelForm):
    class Meta:
        model = ItemLocation
        fields = '__all__'


class VendorMasterrForm(forms.ModelForm):
    class Meta:
        model = VendorMaster
        fields = '__all__'


class ItemCategoryMasterForm(forms.ModelForm):
    class Meta:
        model = ItemCategoryMaster
        fields = '__all__'


class ItemBelongsToMasterForm(forms.ModelForm):
    class Meta:
        model = ItemBelongsToMaster
        fields = '__all__'


class PackagigMasterForm(forms.ModelForm):
    class Meta:
        model = PackagigMaster
        fields = '__all__'


class ItemUnitMasterForm(forms.ModelForm):
    class Meta:
        model = ItemUnitMaster
        fields = '__all__'


class ItemManufacturerForm(forms.ModelForm):
    class Meta:
        model = ItemManufacturer
        fields = '__all__'


class ItemSupplierForm(forms.ModelForm):
    class Meta:
        model = ItemSupplier
        fields = '__all__'


class StoreMasterForm(forms.ModelForm):
    class Meta:
        model = StoreMaster
        fields = '__all__'
# Inventory Master Ends

# OPD Transaction by mantu
class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = '__all__'

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'

# class ServiceChargeMasterForm(forms.ModelForm):
#     class Meta:
#         model = ServiceChargeMaster
#         fields = '__all__'
# class OpdBillingTempForm(forms.ModelForm):
#     class Meta:
#         model=OpdBillingTempsec
#         fields='__all__'

class OpdPaymentModeForm(forms.ModelForm):
    class Meta:
        model=OpdPaymentMode
        fields='__all__'
class BankMasterForm(forms.ModelForm):
    class Meta:
        model=BankMaster
        fields='__all__'
class AdvPatientVisitMainForm(forms.ModelForm):
    class Meta:
        model=AdvPatientVisitMains
        fields='__all__'
        widgets = {
            'uhid': forms.HiddenInput(attrs={'value': 'Null'}),
            'visit_id': forms.HiddenInput(attrs={'value': 'Null'}),
        }
class OpdBillingMainForm(forms.ModelForm):
    class Meta:
        model=OpdBillingMain
        fields='__all__'

#=================== OPD Package ================================
class OpdPackageMasterForm(forms.ModelForm):
    class Meta:
        model = OpdPackageMaster
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OpdPackageMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProfileMasterForm(forms.ModelForm):
    class Meta:
        model=ProfileMaster
        fields='__all__'

class ServiceTestForm(forms.ModelForm):
    class Meta:
        model=ServiceTest
        fields='__all__'


class SampleMasterForm(forms.ModelForm):
    class Meta:
        model = SampleMaster
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SampleMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class VolumeMasterForm(forms.ModelForm):
    class Meta:
        model = VolumeMaster
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VolumeMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CreateUser
        fields = '__all__'
        widgets={
            'user_id':forms.HiddenInput(attrs={'class':'form-control'}),
            'f_name':forms.TextInput(attrs={'class':'form-control'}),
            'middle_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            'user_profile':forms.Select(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'create_datatime':forms.widgets.DateTimeInput(attrs={'class':'form-control'}),
            'date_of_join':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'date_of_living':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateUser_EditForm(forms.ModelForm):
    class Meta:
        model = CreateUser
        fields = '__all__'
        widgets={
            'user_id':forms.HiddenInput(attrs={'class':'form-control'}),
            'login_id':forms.HiddenInput(attrs={'class':'form-control'}),
            'f_name':forms.TextInput(attrs={'class':'form-control'}),
            'middle_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            'user_profile':forms.Select(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'create_datatime':forms.widgets.DateTimeInput(attrs={'class':'form-control'}),
            'date_of_join':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'date_of_living':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreateUser_EditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class CreateAdminForm(forms.ModelForm):
    class Meta:
        model = CreateAdmin
        fields = '__all__'

#================= BED CHARGE SLIP ===================
class BedChargeSlipForm(forms.ModelForm):
    class Meta:
        model = BedChargeSlip
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BedChargeSlipForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#=================== FOR DIALYSIS 01/02/2023 ===============================
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Primary_dialysis_theropistForm(forms.ModelForm):
    class Meta:
        model = Primary_dialysis_theropist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Primary_dialysis_theropistForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Secondry_dialysis_theropistForm(forms.ModelForm):
    class Meta:
        model = Secondry_dialysis_theropist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Secondry_dialysis_theropistForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Machine_nameForm(forms.ModelForm):
    class Meta:
        model = Machine_name
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Machine_nameForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Asset_typeForm(forms.ModelForm):
    class Meta:
        model = Asset_type
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Asset_typeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Bruit_thrillForm(forms.ModelForm):
    class Meta:
        model = Bruit_thrill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Bruit_thrillForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Access_siteForm(forms.ModelForm):
    class Meta:
        model = Access_site
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Access_siteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Dialysate_TypeForm(forms.ModelForm):
    class Meta:
        model = Dialysate_Type
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Dialysate_TypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Completion_Status_MasterForm(forms.ModelForm):
    class Meta:
        model = Completion_Status_Master
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Completion_Status_MasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Needle_typeForm(forms.ModelForm):
    class Meta:
        model = Needle_type
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Needle_typeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DialyzerForm(forms.ModelForm):
    class Meta:
        model = Dialyzer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DialyzerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AnticoagulationForm(forms.ModelForm):
    class Meta:
        model = Anticoagulation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AnticoagulationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Heparin_TypeForm(forms.ModelForm):
    class Meta:
        model = Heparin_Type
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Heparin_TypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Closing_AttendentForm(forms.ModelForm):
    class Meta:
        model = Closing_Attendent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Closing_AttendentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
#======= Schedule_Master 06/02/2023 ==================
class Schedule_MasterForm(forms.ModelForm):
    class Meta:
        model = Schedule_Master
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Schedule_MasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#===== End Master For Dialysis =====================
#======= Inventory Item Master 04/02/2023 ================
# class Inventory_ItemMasterForm(forms.ModelForm):
#     class Meta:
#         model=Inventory_ItemMaster
#         fields='__all__'



class Ins_DocumentForm(forms.ModelForm):
    class Meta:
        model = Ins_Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Ins_DocumentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#========================= kenedy clinical management 12/03/2023 ========================
class PatientAllergyForm(forms.ModelForm):
    class Meta:
        model=PatientAllergy
        fields='__all__'
        widgets={
            'type':forms.Select(attrs={'class':'type'}),
           'allergen':forms.Select(attrs={'class':'allergen'}),
            'reaction':forms.TextInput(attrs={'class':'reaction'}),
        }

class TriageInfoForm(forms.ModelForm):
    class Meta:
        model= TriageInfo
        fields = '__all__'

class EmrInfoRecordForm(forms.ModelForm):
    class Meta:
        model= EmrInfoRecord
        fields = ['medical_record_type','medical_record_file']

class EmrInfoForm(forms.ModelForm):
    class Meta:
        model= EmrInfo
        fields = ['record_type']

class HistoryAndExaminationForm(forms.ModelForm):
    class Meta:
        model= HistoryAndExamination
        fields = '__all__'

class Insurance_CheckList_MasterForm(forms.ModelForm):
    class Meta:
        model=Insurance_CheckList_Master
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(Insurance_CheckList_MasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class ItemsubcategoryMasterForm(forms.ModelForm):
    class Meta:
        model=ItemsubcategoryMaster
        fields='__all__'



#  karan
class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name']
        widgets={
            'username':forms.TextInput(attrs={'hidden':'hidden'}),
            'password1':forms.PasswordInput(attrs={'hidden':'hidden'}),
            'password2':forms.PasswordInput(attrs={'hidden':'hidden'}),
            'email':forms.EmailInput(attrs={'hidden':'hidden'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'hidden': 'hidden'})
        self.fields['password2'].widget.attrs.update({'hidden': 'hidden'})
        self.fields['first_name'].widget.attrs.update({'hidden': 'hidden'})

class LocationMasterForm(forms.ModelForm):
    class Meta:
        model=LocationMaster
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(LocationMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PrescriptionDialysisForm(forms.ModelForm):
    class Meta:
        model = PrescriptionDialysis
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PrescriptionDialysisForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Permanent_Access_MasterForm(forms.ModelForm):
    class Meta:
        model=Permanent_Access_Master
        fields='__all__'


class IntraDialysisPerHourInputForm(forms.ModelForm):
    class Meta:
        model = IntraDialysisPerHourInput
        fields = '__all__'


#======================= For Dialysis 07/06/2023 ===================================
class PostEquip_preparationForm(forms.ModelForm):
    class Meta:
        model = PostEquip_preparation
        fields = '__all__'
        widgets={
            'uhid': forms.HiddenInput(attrs={'value': 'Null'}),
            'visit_id': forms.HiddenInput(attrs={'value': 'Null'}),
            'post_preparation': forms.CheckboxSelectMultiple(),
        }
class PreDialysisAssessmentForm(forms.ModelForm):
    class Meta:
        model = PreDialysisAssessment
        fields = '__all__'
        widgets={
            'uhid': forms.HiddenInput(attrs={'value': 'Null'}),
            'visit_id': forms.HiddenInput(attrs={'value': 'Null'}),
            'chest_auscultation_clear': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
            'peripheral_edema': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
            'pressure_limit_set': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
            'Physical_Chest_pain_discompfort': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
            'recent_surgery_injuries_trauma_bleeding': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
            'intra_dialysis': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
            'breakfast': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'}),
        }

#-=========================== END ======================================

# class PostEquip_preparationForm(forms.ModelForm):
#     class Meta:
#         model = PostEquip_preparation
#         fields = '__all__'

class SessionNoteForm(forms.ModelForm):
    class Meta:
        model = SessionNote
        fields = ['uhid', 'visit_id', 'time', 'plan', 'intervention', 'evalution']

    def __init__(self, *args, **kwargs):
        super(SessionNoteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Refered_by_MasterForm(forms.ModelForm):
    class Meta:
        model=Refered_by_Master
        fields='__all__'

class RelationForm(forms.ModelForm):
    class Meta:
        model=Relation
        fields='__all__'

class PreEquipPreparationMasterForm(forms.ModelForm):
    class Meta:
        model=PreEquipPreparationMaster
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(PreEquipPreparationMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class PreEquipPreparationPreDialysisForm(forms.ModelForm):
    class Meta:
        model=PreEquipPreparationPreDialysis
        fields='__all__'
        widgets={
            'uhid': forms.HiddenInput(attrs={'value': 'Null'}),
            'visit_id': forms.HiddenInput(attrs={'value': 'Null'}),
            'name':forms.CheckboxSelectMultiple(),
        }


class CannulationNurseForm(forms.ModelForm):
    class Meta:
        model=CannulationNurse
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(CannulationNurseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#####incident form #############
class Incident_Type_MasterForm(forms.ModelForm):
    class Meta:
        model=Incident_Type_Master
        fields='__all__'  
        # widgets={
        #     'date':forms.NumberInput(attrs={'type':'datetime-local'}),
        # }       
    def __init__(self, *args, **kwargs):
        super(Incident_Type_MasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'        

class Contributing_Factors_MasterForm(forms.ModelForm):
    class Meta:
        model=Contributing_Factors_Master
        fields='__all__'  
          
    def __init__(self, *args, **kwargs):
        super(Contributing_Factors_MasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AuthorizedPersonForm(forms.ModelForm):
    class Meta:
        model=AuthorizedPerson
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(AuthorizedPersonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OPDBillDiscountRemarkForm(forms.ModelForm):
    class Meta:
        model=OPDBillDiscountRemark
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(OPDBillDiscountRemarkForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CancelBillRemarkForm(forms.ModelForm):
    class Meta:
        model=CancelBillRemark
        exclude=('bill_no','status','created_by','location')

    def __init__(self, *args, **kwargs):
        super(CancelBillRemarkForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BranchRestrictForm(forms.ModelForm):
    class Meta:
        model = BranchRestrict
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(BranchRestrictForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'