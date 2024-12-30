from django.db import models
import datetime
from django.utils import timezone
from random import *
from django.urls import reverse
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from datetime import *
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db.models import Count
from django_mysql.models import ListCharField
from mainapp.models import *

class LocationMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    location_name=models.CharField(max_length=50)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.location_name
# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
        qs=super().get_queryset().order_by('-doctor_id')
        return qs
class GroupMaster(models.Model):
    group_id=models.CharField(max_length=200,primary_key=True)
    group_name=models.CharField(max_length=200)
    def __str__(self):
        return self.group_id
class BranchMaster(models.Model):
    BRANCH_TYPE=(
    ('HOSPITAL','Hospital'),
    ('CLINIC','Clinic'),
    ('PHARMACY','Pharmacy'),
    ('LAB','Lab'),
    )
    group_id=models.ForeignKey(GroupMaster,on_delete=models.CASCADE)
    branch_id=models.CharField(max_length=200,primary_key=True)
    branch_name=models.CharField(max_length=200)
    branch_type=models.CharField(max_length=200,choices=BRANCH_TYPE)
    def __str__(self):
        return self.branch_name
class TitleMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    initial=models.CharField(max_length=50)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
class HospitalMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    hospital_name=models.CharField(max_length=500)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.hospital_name
class HolidayMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    holiday_id=models.CharField(max_length=20,blank=True,null=True)
    holiday_type=models.CharField(max_length=200)
    holiday_date=models.DateField()
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
class GenderMater(models.Model):
    Gender=models.CharField(max_length=200)
    status=models.CharField(max_length=50)
    description=models.TextField(blank=True,null=True)
class DistrictMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    district=models.CharField(max_length=500)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.district
class CountryMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    country=models.CharField(max_length=500)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
class CityMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    district=models.ForeignKey(DistrictMaster,on_delete=models.CASCADE)
    city=models.CharField(max_length=500)
    status=models.CharField(max_length=50,choices=STATUS,default='active',blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.city
class MostCommonDocumentTypeMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    document_type=models.CharField(max_length=200)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
class MaritalStatusMaster(models.Model):
    marital_status=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
class RelationMaster(models.Model):
    relation_name=models.CharField(max_length=200)
    status=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
#..............Service Master Start.............
class ServiceCategory(models.Model):
    service_category=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.service_category
class ServiceSubCategory(models.Model):
    service_sub_category=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.service_sub_category
class ServiceDepartment(models.Model):
    service_department=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.service_department
class ServiceSubDepartment(models.Model):
    service_sub_department=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.service_sub_department
class ServiceMaster(models.Model):
    SERVICE_TYPE=(
    ('type1','type_1'),
    ('type2','type_2'),
    ('type3','type_3'),
    ('type4','type_4'),
    )
    service_name=models.CharField(max_length=100,blank=True,null=True)
    service_category=models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
    service_sub_category=models.ForeignKey(ServiceSubCategory,on_delete=models.CASCADE)
    service_department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    ServiceSubDepartment=models.ForeignKey(ServiceSubDepartment,on_delete=models.CASCADE)
    service_title=models.CharField(max_length=100)
    service_short_name=models.CharField(max_length=100)
    unit=models.CharField(max_length=100)
    consent=models.BooleanField()
    consent_name=models.CharField(max_length=100)
    ipd=models.BooleanField()
    nursing_charges=models.BooleanField()
    opd=models.BooleanField()
    preventing_health_check_up=models.BooleanField()
    discount=models.BooleanField()
    outsource=models.BooleanField()
    emergency=models.BooleanField()
    emergency_percentage=models.CharField(max_length=100,blank=True,null=True)
    tally_ledger=models.BooleanField()
    inactive=models.BooleanField()
    due_not_allowed=models.BooleanField()
    isProcedure=models.BooleanField()
    Editable_Serv_Charge=models.BooleanField()
    Service_Type=models.CharField(max_length=100,choices=SERVICE_TYPE)
    Card_Discount_Per=models.CharField(max_length=100,blank=True,null=True)
    Billing_Group_Service_Code=models.CharField(max_length=100,blank=True,null=True)
    Charges=models.FloatField(blank=True,null=True,default=0)
    def __str__(self):
        return self.service_name


#..............Service Master End.............
#..............Tariff Master Start............
class TariffMaster(models.Model):
    status=(
    ('active','active'),
    ('inactive','inactive'),
    )
    tariff_name=models.CharField(max_length=255,unique=True)
    status=models.CharField(max_length=20,choices=status)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.tariff_name
#..............Tariff Master End....................
#..............Corporate  Master Start..............
class Designation(models.Model):
    designation=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.designation
class CorporateMaster(models.Model):
    corporate_ID=models.IntegerField()
    corporate_Name=models.CharField(max_length=255,unique=True)
    valid_Upto=models.DateField()
    contact_No=models.BigIntegerField()
    email_ID=models.EmailField(max_length=200)
    remark=models.CharField(max_length=200,blank=True,null=True)
    Cash_Credit=(
        ('Cash','Cash'),
        ('Credit','Credit'),
    )
    cash_credit=models.CharField(max_length=30,choices=Cash_Credit,blank=True,null=True)
    inactive=models.BooleanField()
    #Address Fields====================
    Office_Location_Name=models.CharField(max_length=200)
    Auth_Person=models.CharField(max_length=200)
    designation=models.ForeignKey(Designation,on_delete=models.CASCADE)
    address=models.CharField(max_length=500)
    City=models.ForeignKey(CityMaster,on_delete=models.CASCADE)
    PinCode=models.IntegerField()
    phone_no=models.BigIntegerField()
    fax=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.corporate_Name
#..............Corporate  Master End................
#..............Billing  Master Start................
class BillingGroup(models.Model):
    STATUS=(
        ('Active','Active'),
        ('In Active','In Active'),
    )
    billing_group_id=models.CharField(max_length=50,unique=True)
    billing_group=models.CharField(max_length=100)
    status=models.CharField(max_length=20,choices=STATUS,default='Active')
    def __str__(self):
        return self.billing_group
#..............Billing  Master End................


#..............Tariff Charge  Master Start................
class WardType(models.Model):
    type=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.type

class WardCategory(models.Model):
    category=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.category
class TariffChargeMaster(models.Model):
    tariff=models.ForeignKey(TariffMaster,on_delete=models.CASCADE)
    apply_From=models.DateField()
    Ward_Type=models.ForeignKey(WardType,on_delete=models.CASCADE)
    Ward_Category=models.ForeignKey(WardCategory,on_delete=models.CASCADE)

#..............Tariff Charge  Master End................
#..............Billing Group Tariff Link Start................
class BillingGroupTariffLink(models.Model):
    Tariff=models.ForeignKey(TariffMaster,on_delete=models.CASCADE)
    Billing_Group_Name=models.ForeignKey(BillingGroup,on_delete=models.CASCADE)
    inactive=models.BooleanField()
    def __str__(self):
        return str(self.Billing_Group_Name)
#..............Billing Group Tariff Link End..................
#..............Billing Group Corporate Start..................
class BillingGroupCorporateMaster(models.Model):
    Corporate_Name=models.ForeignKey(CorporateMaster,on_delete=models.CASCADE)
    Biiling_Group=models.ForeignKey(BillingGroup,on_delete=models.CASCADE)
    inactive = models.BooleanField()
#..............Billing Group Corporate End....................

class DoctorTable(models.Model):
    status=(
    ('active','active'),
    ('inactive','inactive'),
    )
    register_by=(
    ('IMC','Indian Medical Council'),
    ('SMC','State Medical Council'),
    )
    time_slot_lists=(
    (0,'09:00 - 09:30'),
    (1,'09:30 - 10:00'),
    (2,'10:00 - 11:30'),
    (3,'11:30 - 12:00'),
    (4,'12:00 - 12:30'),
    (5,'12:30 - 13:00'),
    )
    doctor_id=models.CharField(max_length=200,primary_key=True)
    doctor_belogns_to=models.ForeignKey(BranchMaster,on_delete=models.CASCADE)
    doctor_email_address=models.EmailField(max_length=200)
    doctor_name=models.CharField(max_length=100)
    doctor_profile_image=models.ImageField(upload_to='images/')
    doctor_sign_image=models.ImageField(upload_to='images/')
    doctor_phone_no=models.BigIntegerField(null=True,blank=True)
    doctor_appointment=models.DateField(null=True,blank=True)
    doctor_address=models.CharField(max_length=500)
    doctor_date_of_birth = models.DateField()
    doctor_department = models.CharField(max_length=100)
    doctor_status=models.CharField(max_length=100,choices=status)
    doctor_fee=models.FloatField()
    doctor_registration_no=models.CharField(max_length=200)
    registration_exparing_date=models.DateField()
    doctor_register_by=models.CharField(max_length=200,choices=register_by)
    # doctor_time_slot=models.IntegerField(choices=time_slot_lists)
    doctor_location=models.CharField(max_length=200)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.doctor_id
    
    def __str__(self):
        return self.doctor_name
    def get_absolute_url(self):
        return reverse('delete')
    objects=CustomManager()

class DoctorScheduleTable(models.Model):

    days=(
    ('0','Sunday'),
    ('1','Monday'),
    ('2','Tuesday'),
    ('3','Wednesday'),
    ('4','Thursday'),
    ('5','Friday'),
    ('6','Saturday'),
    )
    status=(
    ('active','active'),
    ('inactive','inactive'),
    )
    # doctor_schedule_id=models.IntegerField()
    select_doctor=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    doctor_schedule_date=models.DateField()
    doctor_schedule_start_time=models.TimeField()
    doctor_schedule_end_time=models.TimeField()
    average_consulting_time=models.TimeField()
    doctor_schedule_status=models.CharField(max_length=200,choices=status)
    def __str__(self):
        return self.select_doctor
class AppointmentTable(models.Model):
    patient_come_into_hospital=(
    ('Yes','Yes'),
    ('No','No'),
    )
    appointment_id=models.IntegerField()
    doctor_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    # patient_id=models.IntegerField()
    # doctor_schedule_id=models.ManyToManyField(DoctorScheduleTable)
    appointment_number=models.BigIntegerField()
    reason_for_appointment=models.CharField(max_length=200)
    appointment_time=models.TimeField()
    status=models.CharField(max_length=100)
    patient_come_into_hospital=models.CharField(max_length=100,choices=patient_come_into_hospital)
    doctor_comment=models.CharField(max_length=300)
class PatientTable(models.Model):
    gender=(
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
    )
    patient_id=models.IntegerField()
    patient_email_address=models.EmailField(max_length=200)
    patient_password=models.CharField(max_length=100)
    patient_first_name=models.CharField(max_length=100)
    patient_last_name=models.CharField(max_length=100)
    patient_date_of_birth=models.DateField()
    patient_gender=models.CharField(max_length=100,choices=gender)
    patient_address=models.CharField(max_length=200)
    patient_phone_number=models.CharField(max_length=100)
    patient_maritial_status=models.CharField(max_length=100)
    patient_added_on=models.DateTimeField()
    patient_verification_code=models.CharField(max_length=100)
    email_verify=models.CharField(max_length=100)

class BookedAppointments(models.Model):
    admin=models.CharField(max_length=200,blank=True,null=True)
    patient_id=models.CharField(max_length=200,primary_key=True)
    first_name=models.CharField(max_length=200)
    middle_name=models.CharField(max_length=200,blank=True)
    last_name=models.CharField(max_length=200,blank=True)
    patient_gender=models.CharField(max_length=200,blank=True)
    patient_appointment_date=models.DateField()
    patient_appointment_id=models.CharField(max_length=200)
    patient_age=models.IntegerField()
    patient_mobile_number=models.CharField(max_length=15)
    patient_email_id=models.EmailField()
    patient_schedule_date_and_time=models.CharField(max_length=200)
    patient_scheduled_id=models.CharField(max_length=200)
    patient_payment_mode=models.CharField(max_length=200)
    doctor_name=models.CharField(max_length=200)
    doctor_department=models.CharField(max_length=200)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=200,default="appointed",blank=True,null=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return '%s %s ' %(self.doctor_name,self.doctor_department)

class AddMembers(models.Model):
    reference_mobile_number=models.CharField(max_length=40)
    title_name=models.CharField(max_length=100)
    first_name=models.CharField(max_length=200)
    middle_name=models.CharField(max_length=200,blank=True)
    last_name=models.CharField(max_length=200,blank=True)
    gender=models.CharField(max_length=100)
    age=models.IntegerField()
    mobile_number=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
class DoctorSchedule(models.Model):
    doctor_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
#Availability_day_schedule_master_temp – table name
class AvailableDayScheduleMasterTemp(models.Model):
    doctor_id=models.CharField(max_length=100)
    dates_available=models.CharField(max_length=5000)
    schedule_id_of_each_slot=models.CharField(max_length=5000)
    time_slots=models.CharField(max_length=5000)
class AvailabilityIntradayScheduleMaster(models.Model):
    time_slot_id=models.CharField(max_length=100)
    time_slot_start_time=models.CharField(max_length=100)
    time_slot_end_time=models.CharField(max_length=100)
    doctor_id=models.CharField(max_length=100)
#++++++++++Patient Registration++++++++++++++++
class NameOfTheTitle(models.Model):
    title_name=(
    ('Mr','Mr.'),
    ('Mrs.','Mrs.'),
    ('Ms.','Ms.'),
    ('Dr','Dr.'),
    )
    title=models.CharField(max_length=100,choices=title_name)
    def __str__(self):
        return self.title
class BloodMaster(models.Model):
    blood_group_id=models.CharField(max_length=100)
    blood_group=models.CharField(max_length=100)
    blood_group_description=models.CharField(max_length=200)
class MartialStatus(models.Model):
    status=(
    ('Married','Married '),
    ('Widowed','Widowed'),
    ('Separated','Separated'),
    ('Divorced','Divorced'),
    ('Single','Single'),
    )
    martial_status=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
# class PatientRegistration(models.Model):
#     pass
class NewAppointmentByAdmin(models.Model):
    GENDER=(
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
    )
    appointment_id=models.CharField(max_length=200,primary_key=True)
    patient_id=models.CharField(max_length=200)
    first_name=models.CharField(max_length=200)
    middle_name=models.CharField(max_length=200,blank=True)
    last_name=models.CharField(max_length=200,blank=True)
    email_id=models.EmailField(max_length=200)
    age=models.CharField(max_length=200)
    gender=models.CharField(max_length=200,choices=GENDER)
    mobile_number=models.CharField(max_length=200)

class NewAppointmentByAdminChooseDoctor(models.Model):
    appointment_date=models.DateField()
    doctor_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
#QMS DATABASE
class RoomNumber(models.Model):
    room_no=models.IntegerField(unique=True)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return str(self.room_no)
from datetime import *
class TokenMasterConf(models.Model):
    STATUS=(
    ('IN','IN'),
    ('OUT','OUT'),
    )
    Date=models.DateField()
    Doct_Name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,related_name='DoctorTable')
    status=models.CharField(max_length=20,choices=STATUS)
    Room_No=models.ForeignKey(RoomNumber,on_delete=models.CASCADE)
    Max_Token_Assigned=models.IntegerField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class TokenCreations(models.Model):
    Date=models.DateField(default= datetime.now)
    Doct_id=models.CharField(max_length=100)
    Doct_Name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    speciality=models.CharField(max_length=100)
    Patient_Id=models.CharField(max_length=100)
    Patient_Name=models.CharField(max_length=200)
    Token_No=models.CharField(max_length=20)
    Room_No=models.ForeignKey(RoomNumber,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Token_No)

class TokenCreationDone(models.Model):
    Date=models.DateField(auto_now_add=True)
    Doct_id=models.CharField(max_length=100)
    Doct_Name=models.CharField(max_length=100)
    speciality=models.CharField(max_length=100)
    Pt_Id=models.CharField(max_length=100)
    Pt_Name=models.CharField(max_length=200)
    Token_No=models.CharField(max_length=20)
    Room_No=models.CharField(max_length=100)
    status = models.CharField(max_length=100,default="Waiting")
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class SlipCreation(models.Model):
    select_token_number=models.ForeignKey(TokenCreations,on_delete=models.CASCADE)
    patient_id=models.CharField(max_length=20)
    patient_name=models.CharField(max_length=200)
    Doctor_Name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    Room_No=models.ForeignKey(RoomNumber,on_delete=models.CASCADE)

class CentralisedAdminView(models.Model):
    Date=models.DateField(auto_now_add=True)
    room_number=models.ForeignKey(RoomNumber,on_delete=models.CASCADE)
    Doc_Name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    Max_Token=models.IntegerField()
    Token_Issued=models.IntegerField()
    Current_In=models.IntegerField()
    Next_Waiting=models.IntegerField()
# class TestCountrys(models.Model):
#     country_code=models.IntegerField(primary_key=True)
#     country_name=models.CharField(max_length=100)
    # def __str__(self):
    #     return '{country_code},{country_name}'.format(country_code=self.country_code,country_name=self.country_name)
# =====================Time Capturing====================
class TimeTaken(models.Model):
    doctor_name=models.CharField(max_length=200)
    patient_id=models.CharField(max_length=200)
    start_time=models.CharField(max_length=20)
    end_time=models.CharField(max_length=20)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class ReplicatedTokenMasterConf(models.Model):
    Date=models.DateField()
    Doct_Name=models.CharField(max_length=100)
    status=models.CharField(max_length=20)
    Room_No=models.IntegerField()
    Max_Token_Assigned=models.IntegerField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

# Patient Registrations Relates DB Table Stuff
class PatientRegistrationMains(models.Model):
    uhid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    dob = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=50, null=False, blank=False)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class PatientRegistrationSub(models.Model):
    uhid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    registration_date_and_time = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    blood_group = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=False, blank=False)
    father_or_husband_name = models.CharField(max_length=100, null=False, blank=False)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=300, null=False, blank=False)
    referred_by = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    pin_code = models.CharField(max_length=8, null=False, blank=False)
    aadhar_card = models.CharField(max_length=100, editable=False, null=True, blank=True)
    pan_card = models.CharField(max_length=100, editable=False, null=True, blank=True)
    emergency_contact_person = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_num = models.CharField(max_length=20, null=True, blank=True)
    alternate_contact_number = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    staff_member = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    allow_photo_at_nursing_station = models.CharField(max_length=100, editable=False, null=True, blank=True)
    notable = models.CharField(max_length=100, null=True, editable=False, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class PatientBillingInfos(models.Model):
    uhid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    in_cash = models.CharField(max_length=100, null=True, blank=True)
    is_senior_citizen = models.CharField(max_length=100, null=True, blank=True)
    billing_group = models.CharField(max_length=100, null=False, blank=False)
    nhif_ins_cor_name = models.CharField(max_length=100, null=True, blank=True)
    nhif_ins_cor_id = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=100,null=True,blank=True)
    relation = models.CharField(max_length=100,blank=True)
    valid_upto = models.DateTimeField(auto_now=True, null=True, blank=True)
    sum_insured_amount = models.CharField(max_length = 100,blank=True)
    is_inactive = models.CharField(max_length=100, null=True, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class PatientsRegistrationsAllInOne(models.Model):
    # 41 fields
    uhid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    dob = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=50, null=False, blank=False)
    patient_profile = models.ImageField(upload_to='images/',null=True, blank=True)
    registration_date_and_time = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    blood_group = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=False, blank=False)
    father_or_husband_name = models.CharField(max_length=100, null=False, blank=False)
    mother_name = models.CharField(max_length=100 , null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=300, null=False, blank=False)
    referred_by = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    pin_code = models.CharField(max_length=8, null=False, blank=False)
    aadhar_card = models.CharField(max_length=100, editable=False, null=True, blank=True)
    pan_card = models.CharField(max_length=100, editable=False, null=True, blank=True)
    next_of_kin = models.CharField(max_length=100, null=True, blank=True)
    next_of_kin_mob_no = models.CharField(max_length=20, null=True, blank=True)
    alternate_contact_number = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    staff_member = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    allow_photo_at_nursing_station = models.CharField(max_length=100, editable=False, null=True, blank=True)
    notable = models.CharField(max_length=100, null=True, editable=False, blank=True)
    in_cash = models.CharField(max_length=100, null=True, blank=True)
    is_senior_citizen = models.CharField(max_length=100, null=True, blank=True)
    billing_group = models.CharField(max_length=100,blank=False)
    nhif_ins_cor_name = models.CharField(max_length=100,blank=True,default='Cash')
    nhif_ins_cor_id = models.CharField(max_length=100,blank=True,null=True)
    card_number = models.CharField(max_length=100,null=True,blank=True)
    relation = models.CharField(max_length=100,blank=True)
    valid_upto = models.DateField(null=True, blank=True)
    sum_insured_amount = models.CharField(max_length = 100,blank=True,default='0')
    ins_doc_upload = models.ImageField(upload_to='ins_document/',blank=True)
    ins_id_upload = models.ImageField(upload_to='ins_id_document/',blank=True)
    is_inactive = models.CharField(max_length=100, null=True, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    appointment_id = models.CharField(max_length=100,blank=True,null=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    update_status = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.uhid

class PatientBarCode(models.Model):
    uhid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    barcode = models.ImageField(upload_to='barcodes/',null=True, blank=True)
    def __str__(self):
        return self.uhid
	# Overriding save....
    def save(self,*args,**kwargs):

        COD128=barcode.get_barcode_class('code128')
        rv=BytesIO()
        code=COD128(self.uhid,writer=ImageWriter()).write(rv)
        self.barcode.save(f'{self.uhid}.png',File(rv),save=False)
        return super().save(*args,**kwargs)
class PatientImages(models.Model):
      p_images=models.ImageField(upload_to='images/')
class PatientProfile(models.Model):
      uhid = models.CharField(max_length=50, unique=True, null=False, blank=False)
      p_images=models.ImageField(upload_to='profile/')
class ClinicalOrDepartment(models.Model):
    clinical_department=models.CharField(max_length=100)
    description=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.clinical_department
# Visit Master
class VisitTyoeMaster(models.Model):
    visit_type=models.CharField(max_length=100,unique=True)
    description=models.CharField(max_length=300)
    def __str__(self):
        return self.visit_type
class PatientVisitMains(models.Model):
    uhid = models.CharField(max_length=50, null=False, blank=False)
    visit_date_time = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    visit_id=models.CharField(max_length=50)
    visit_type = models.ForeignKey(VisitTyoeMaster,on_delete=models.CASCADE)
    description = models.CharField(max_length=500,null=True,blank=True)
    # 23/12/22 MANTU ========== This is for dialysis =============================================
    claim_no = models.CharField(max_length=500, null=True, blank=True,default='Not Initiated')
    batch_no = models.CharField(max_length=500, null=True, blank=True)
    #======================= for clinical management its update =======================
    status = models.CharField(max_length=500, null=True, blank=True,default='open')
    #======================= for Tariff and Insurance ======================
    billing_group=models.ForeignKey(BillingGroup,on_delete=models.CASCADE,null=True, blank=True)
    insurance_name=models.CharField(max_length=50,null=True, blank=True)
    # ========================= END ========================
    doctor = models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True, blank=True)
    clinical_department = models.ForeignKey(ClinicalOrDepartment,on_delete=models.CASCADE)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    #================ For Uniqe visit id 20-06-23 ====================
    uv_id=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return  self.visit_id

class OpdPaymentMode(models.Model):
    payment_mode=models.CharField(max_length=100)
    description=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.payment_mode
class BankMaster(models.Model):
    STATUS=(
        ('active','active'),
        ('inactive','inactive')
    )
    bank_id=models.CharField(max_length=100)
    bank_name=models.CharField(max_length=100)
    bank_created_by=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50,choices=STATUS,default='active')
    def __str__(self):
        return self.bank_name

class OpdBillingService(models.Model):
    uhid=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50)
    action_date_time = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    service_name=models.CharField(max_length=50)
    doctor=models.CharField(max_length=50)
    amount=models.FloatField()
    discount=models.IntegerField()
    unit=models.IntegerField()
    net_amount=models.FloatField()
    co_pay=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100)
    patient_amount=models.FloatField()
    receive_amount=models.FloatField()

class OpdBillingMain(models.Model):
    STATUS=(
        ('active','active'),
        ('inactive','inactive')
    )

    bill_no=models.CharField(max_length=50,blank=False,null=False)
    bill_id=models.CharField(max_length=50,blank=False,null=False)
    bill_date_time=models.DateTimeField(auto_now_add=True,editable=False,blank=False,null=False)
    uhid=models.CharField(max_length=50)
    temp_bill_no=models.CharField(max_length=50,null=True,blank=True)
    department=models.CharField(max_length=50,null=True,blank=True)
    doctor_name=models.CharField(max_length=50,null=True,blank=True)
    visit_no=models.CharField(max_length=50,blank=False,null=False)
    corporate_id=models.CharField(max_length=50,blank=True,null=True)
    billing_group_id=models.CharField(max_length=50,blank=True,null=True)
    package_profile_id=models.CharField(max_length=50,blank=True,null=True)
    net_amount=models.CharField(max_length=50,blank=False,null=False)
    discount=models.CharField(max_length=50,blank=False,null=False)
    pay_amount=models.CharField(max_length=50,blank=False,null=False)
    paid_amount=models.CharField(max_length=50,blank=False,null=False)
    outstanding_amount=models.CharField(max_length=50,blank=False,null=False)
    payment_mode=models.CharField(max_length=50,blank=True,null=True)
    paid_amt=models.CharField(max_length=50,blank=True,null=True)
    paid_amt_update_date=models.CharField(max_length=50,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50,default='active',blank=False,null=False)
    checklist_status=models.CharField(max_length=50,blank=True,null=True,default='pending')
    claim_status=models.CharField(max_length=50,blank=True,null=True,default='pending')
    claim_amt=models.CharField(max_length=50,blank=True,null=True,default='pending')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    #====== for insurance ============================================
    lou_no=models.CharField(max_length=50,blank=True,null=True)
    claim_no=models.CharField(max_length=50,blank=True,null=True)
    batch_no =models.CharField(max_length=50,blank=True,null=True)
    paid_claim_amt=models.IntegerField(blank=True,null=True,default=0)
    insurance_amt =models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.bill_no

class OpdBillingSub(models.Model):
    STATUS = (
        ('active', 'active'),
        ('inactive', 'inactive')
    )
    bill_no=models.CharField(max_length=50,blank=True,null=True)
    bill_id=models.CharField(max_length=50,blank=False,null=False)
    uhid=models.CharField(max_length=50,null=True,blank=True)
    temp_bill_no=models.CharField(max_length=50,null=True,blank=True)
    package_profile_id=models.CharField(max_length=50,blank=True,null=True)
    package_profile_amt=models.CharField(max_length=50,blank=True,null=True)
    bill_date_time=models.DateTimeField(auto_now_add=True,editable=False,blank=True,null=True)
    department=models.CharField(max_length=50,null=True,blank=True)
    doctor_name=models.CharField(max_length=50,null=True,blank=True)
    visit_no=models.CharField(max_length=50,null=True,blank=True)
    corporate_id=models.CharField(max_length=50,null=True,blank=True)
    billing_group_id=models.CharField(max_length=50,null=True,blank=True)
    service_id=models.CharField(max_length=50,blank=False,null=False)
    charges=models.FloatField(blank=False,null=False)
    unit=models.IntegerField(blank=False,null=False)
    pay_amount=models.FloatField(blank=True,null=True)
    paid_amount=models.FloatField(blank=True,null=True)
    outstanding_amount=models.FloatField(blank=True,null=True)
    payment_mode=models.CharField(max_length=50,null=True,blank=True)
    total_amount=models.FloatField(blank=False,null=False)
    discount=models.FloatField(blank=False,null=False)
    status=models.CharField(max_length=20,choices=STATUS,default='active',blank=False,null=False)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    service_category=models.CharField(max_length=50,null=True,blank=True)
    service_sub_category=models.CharField(max_length=50,null=True,blank=True)
    order_id=models.CharField(max_length=500,blank=True,null=True)

class OpdPayment(models.Model):
    MODE_TYPE=(
        ('CASH','CASH'),
        ('DEBIT/CREDIT CARD','DEBIT/CREDIT CARD'),
        ('WALLET','WALLET'),
        ('UPI','UPI'),
    )
    BANK=(
        ('NA','N/A'),
        ('SBI','SATATE BANK OF INDIA'),
        ('ICICI','ICICI'),
        ('PNB','PUNJAB NATIONAL BACK'),
        ('OTHER','OTHER'),
    )
    uhid=models.CharField(max_length=50,null=True,blank=True)
    date_time=models.CharField(max_length=50,null=True,blank=True)
    bill_id=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50)
    mode_type=models.CharField(max_length=30)
    net_amount=models.FloatField(blank=True,null=True)
    paid_amount=models.FloatField(blank=True,null=True)
    pending_amount=models.FloatField(blank=True,null=True)
    bank_no=models.CharField(max_length=100,blank=True,null=True)
    card_no=models.CharField(max_length=100,blank=True,null=True)
    paid_by=models.CharField(max_length=100,blank=True,null=True)
    ref_number=models.CharField(max_length=100,blank=True,null=True)
    mobile_nummber=models.CharField(max_length=100,blank=True,null=True)
    card_holder_name=models.CharField(max_length=100,blank=True,null=True)
    date_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    receipt_no=models.CharField(max_length=100,blank=True,null=True)
    type=models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class OpdBillingTemp(models.Model):
    bill_no = models.CharField(max_length=50, blank=True, null=True)
    bill_id = models.CharField(max_length=50, blank=True, null=True)
    bill_date_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    uhid = models.CharField(max_length=50,blank=True, null=True)
    visit_no = models.CharField(max_length=50, blank=True, null=True)
    service_name = models.CharField(max_length=50,blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    unit = models.IntegerField(blank=True, null=True)
    net_ammount = models.FloatField(blank=True, null=True)
    outstanding_amount = models.FloatField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    receive_amount = models.FloatField(blank=True, null=True)

class OpdBillingTemper(models.Model):
    uhid = models.CharField(max_length=500,blank=True, null=True)
    visit_no = models.CharField(max_length=500, blank=True, null=True)
    temp_bill_no = models.CharField(max_length=500, blank=True, null=True)
    Pr_Opd_sr_bill_no = models.CharField(max_length=500, blank=True, null=True)
    package_profile_id=models.CharField(max_length=50,blank=True,null=True,default='None')
    package_profile_amt=models.CharField(max_length=50,blank=True,null=True,default='None')
    service_name = models.CharField(max_length=500,blank=True, null=True)
    rate = models.CharField(max_length=500,blank=True, null=True)
    discount = models.CharField(max_length=500,blank=True, null=True)
    unit = models.CharField(max_length=500,blank=True, null=True)
    net_ammount = models.CharField(max_length=500,blank=True, null=True)
    outstanding_amount = models.CharField(max_length=500,blank=True, null=True)
    total_amount = models.CharField(max_length=500,blank=True, null=True)
    receive_amount = models.CharField(max_length=500,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True, null=True)
    status=models.CharField(max_length=500,default='Open',blank=True, null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    service_category=models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,null=True,blank=True)
    service_sub_category=models.ForeignKey(ServiceSubCategory,on_delete=models.CASCADE,null=True,blank=True)
    order_id=models.CharField(max_length=500,blank=True, null=True)

# Clinical Management
#=====================================================
# =========Clinical Management/Vital Signs============
class VitalSign(models.Model):
    AVPU=(
        ('A','A'),
        ('V','V'),
        ('P','P'),
        ('U','U'),
    )
    TRAUMA=(
        ('TRAUMA1','TRAUMA1'),
        ('TRAUMA2','TRAUMA2'),
        ('TRAUMA3','TRAUMA3'),
        ('TRAUMA4','TRAUMA4'),
    )
    MOBILITY=(
        ('MOBILITY1','MOBILITY1'),
        ('MOBILITY2','MOBILITY2'),
        ('MOBILITY3','MOBILITY3'),
        ('MOBILITY4','MOBILITY4'),
    )
    OXYZEN=(
        ('OXYZEN1','OXYZEN1'),
        ('OXYZEN2','OXYZEN2'),
        ('OXYZEN3','OXYZEN3'),
        ('OXYZEN4','OXYZEN4'),
    )
    COMMENT=(
        ('COMMENT1','COMMENT1'),
        ('COMMENT2','COMMENT2'),
        ('COMMENT3','COMMENT3'),
        ('COMMENT4','COMMENT4'),
    )
    # visit_id = models.ForeignKey(Visit, on_delete=models.SET(1), null=False, blank=False)
    uhid=models.CharField(max_length=50, null=True, blank=True)
    bill_id=models.CharField(max_length=50,unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    sys_bp = models.CharField(max_length=100, null=False, blank=False)
    dia_bp = models.CharField(max_length=100, null=False, blank=False)
    temp = models.CharField(max_length=100, null=False, blank=False)
    weight = models.IntegerField(null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    bmi = models.CharField(max_length=100, null=False, blank=False)
    resp_rate = models.CharField(max_length=100, null=True, blank=True)
    heart_rate = models.CharField(max_length=100, null=True, blank=True)
    urine_output = models.CharField(max_length=100, null=True, blank=True)
    blood_sugar_f = models.CharField(max_length=100, null=True, blank=True)
    blood_sugar_r = models.CharField(max_length=100, null=True, blank=True)
    spo2 = models.CharField(max_length=100, null=True, blank=True)
    avpu = models.CharField(max_length=100, null=True, blank=True,choices=AVPU)
    trauma = models.CharField(max_length=100, null=True, blank=True,choices=TRAUMA)
    mobility = models.CharField(max_length=100, null=True, blank=True,choices=MOBILITY)
    oxygen_supplementation = models.CharField(max_length=100, null=True, blank=True,choices=OXYZEN)
    comments = models.TextField(null=True, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    gcs = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(blank=True,null=True,auto_now_add=True)

    def __str__(self):
        return "{visit},{comment}".format(visit=self.visit_id, comment=self.comments)

class PreMedicine(models.Model):
    FREQUENCY=(
        ('1.5','1.5'),
        ('2.5','2.5'),
        ('3.5','3.5'),
        ('4.5','4.5'),
        ('5.5','5.5'),
    )
    FOOD_RALATION=(
        ('R1','R1'),
        ('R1','R1'),
        ('R1','R1'),
    )
    ROUTE=(
        ('route1','route1'),
        ('route2','route2'),
        ('route3','route3'),
    )
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    medicine=models.ForeignKey('testapp.Inventory_ItemMaster',on_delete=models.CASCADE)
    dosage=models.CharField(max_length=100)
    frequency=models.CharField(max_length=500,null=True, blank=True)
    no_of_days=models.IntegerField()
    food_relations=models.CharField(max_length=50,null=True, blank=True)
    route=models.CharField(max_length=50,null=True, blank=True)
    instruction=models.CharField(max_length=500)
    prescribe_date=models.DateField()
    prescribed_date=models.DateField(null=True, blank=True,auto_now_add=True)
    end_date=models.DateField()
    status = models.CharField(max_length=100,null=True, blank=True,default='pending')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class DiagnosisMaster(models.Model):
    diagnosis_id=models.CharField(max_length=50,unique=True)
    diagnosis_name=models.CharField(max_length=200,unique=True)
    icd_10_code=models.CharField(max_length=50)
    icd_11_code=models.CharField(max_length=50)
    def __str__(self):
        return self.diagnosis_name
class Diagnosis(models.Model):
    ATTANDANCE=(
        ('EMERGENCY_ACUTE','EMERGENCY_ACUTE'),
    )
    TYPE=(
        ('PRINCIPAL','PRINCIPAL'),
    )
    CATEGORY=(
        ('PRIMARY','PRIMARY'),
    )
    STATE_OF_DIAGNOSIS=(
        ('PRINCIPAL','PRINCIPAL'),
    )
    ADVERSE_EFFECT=(
        ('PRIMARY','PRIMARY'),
    )
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    attendance=models.CharField(max_length=100,choices=ATTANDANCE)
    type=models.CharField(max_length=100,choices=TYPE)
    category=models.CharField(max_length=100,choices=CATEGORY)
    diagnosis=models.CharField(max_length=100, null=True, blank=True)
    D_GRG_Code=models.CharField(max_length=100)
    state_of_diagnosis=models.CharField(max_length=100,choices=STATE_OF_DIAGNOSIS)
    adverse_effect=models.CharField(max_length=100,choices=ADVERSE_EFFECT)
    visit_date = models.CharField(max_length=100, null=True, blank=True)

class HistoryAndExamination(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    general_examination=models.CharField(max_length=500)
    # systemetic_examination=models.CharField(max_length=500)
    Cardiovascular=models.CharField(max_length=500)
    Respiration=models.CharField(max_length=500)
    gastrointestinal_system = models.CharField(max_length=500)
    genitourinary_system = models.CharField(max_length=500)
    Musculoskeletal=models.CharField(max_length=500)
    integumentary = models.CharField(max_length=500)
    central_nervous_system = models.CharField(max_length=500)
    ENT = models.CharField(max_length=500)

class History(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    Past_Medical_Surgical=models.CharField(max_length=500)
    Family_History=models.CharField(max_length=500)
    Paediatric_History=models.CharField(max_length=500)
    Gynaec_Obstetric_History=models.CharField(max_length=500)
    socioeconomic_history = models.CharField(max_length=500)
    # Vaginal_Examination =models.CharField(max_length=500)

class InvestigationProcedure(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    investigation_and_procedure=models.CharField(max_length=200)
    status=models.BooleanField()
    result_status=models.CharField(max_length=50,blank=True,null=True)
    ot_required=models.CharField(max_length=50,blank=True,null=True)
class Advice(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    advice=models.TextField()
    follow_up_date=models.DateField()
    follow_check_box=models.CharField(max_length=500)


class PresentingComplaint(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    visit_date = models.DateField(auto_now_add=True, null=True, blank=True)
    presenting_comp=models.CharField(max_length=50)
    initial_comp=models.TextField()

class MedicalCertificates(models.Model):
    TEMP_CONS=(
        ('In Patient Medical Certificate','In Patient Medical Certificate'),
        ('Medical Examination Form','Medical Examination Form'),
        ('Out Patient Certificate','Out Patient Certificate'),
    )
    AUTH_DOC=(
        ('DOCT1','DOCT1'),
        ('DOCT2','DOCT2'),
        ('DOCT3','DOCT3'),
    )
    mc_templates=models.CharField(max_length=100)
    authorize_dr=models.CharField(max_length=100)
    finalized=models.BooleanField()

# Inventory Start
class ItemManufact(models.Model):
    MANUFACTURERS = (
        ('manufacturers1', 'manufacturers1'),
        ('manufacturers2', 'manufacturers2'),
    )
    manufactures = models.CharField(max_length=100, choices=MANUFACTURERS)


class ItemSupplier(models.Model):
    Suppliers = (
        ('suppliers1', 'Suppliers1'),
        ('suppliers2', 'Suppliers2'),
    )
    suppliers = models.CharField(max_length=100, choices=Suppliers)




class PackagigMaster(models.Model):
    item_packing = models.CharField(max_length=100, )

    def __str__(self)-> str:
        return self.item_packing


class ItemUnitMaster(models.Model):
    unit = models.CharField(max_length=100, )

    def __str__(self) -> str:
        return self.unit


class ItemManufacturer(models.Model):
    manufacturers = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.manufacturers


# class StoreMaster(models.Model):
#     ParentStore = (
#         ('store1', 'store1'),
#         ('store2', 'store2'),
#     )
#     Wing = (
#         ('store1', 'Store1'),
#         ('store2', 'Store2'),
#     )
#     Floor = (
#         ('store1', 'Store1'),
#         ('store2', 'Store2'),
#     )
#     LocationName = (
#         ('store1', 'Store1'),
#         ('store2', 'Store2'),
#     )
#     StoreType = (
#         ('store1', 'Store1'),
#         ('store2', 'Store2'),
#     )
#     store_Id = models.CharField(max_length=100, )
#     store_name = models.CharField(max_length=100, )
#     parent_store = models.CharField(max_length=100, choices=ParentStore)
#     wing = models.CharField(max_length=100, choices=Wing)
#     floor = models.CharField(max_length=100, choices=Floor)
#     location_name = models.CharField(max_length=100, choices=LocationName)
#     store_type = models.CharField(max_length=100, choices=StoreType)
#     main_store = models.BooleanField()
#     inactive = models.BooleanField()


# class VendorMasterr(models.Model):
#     City = (
#         ('city1', 'Chennai'),
#         ('city2', 'Salem'),
#     )
#     District = (
#         ('district1', 'Chennai'),
#         ('district2', 'Salem'),
#     )
#     Rating = (
#         ('1', '1'),
#         ('2', '2'),
#     )

#     vendor_id = models.CharField(max_length=100, )
#     vendor_name = models.CharField(max_length=100, )
#     vendor_short_name = models.CharField(max_length=100, )
#     contact_person = models.CharField(max_length=100, )
#     address = models.CharField(max_length=100, )
#     city = models.CharField(max_length=100, choices=City)
#     district = models.CharField(max_length=100, choices=District)
#     pincode = models.CharField(max_length=100, )
#     phone1 = models.CharField(max_length=100, )
#     phone2 = models.CharField(max_length=100, )
#     fax_no = models.CharField(max_length=100, )
#     email = models.CharField(max_length=100, )
#     website = models.CharField(max_length=100, )
#     tax_id = models.CharField(max_length=100, )
#     rating = models.CharField(max_length=100, choices=Rating)
#     afc_code = models.CharField(max_length=100, )
#     type_char = models.CharField(max_length=100, )
#     inactive = models.BooleanField()


class StoreNursingCounter(models.Model):
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
    storelinkId = models.CharField(max_length=100, )
    store = models.CharField(max_length=100, choices=Store)
    nursingcounter = models.CharField(max_length=100, choices=NursingCounter)
    department = models.CharField(max_length=100, choices=Department)


class ItemLocation(models.Model):
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
    location_Id = models.CharField(max_length=100, )
    Item_name = models.CharField(max_length=100, choices=ItemName)
    store_name = models.CharField(max_length=100, choices=StoreName)
    location = models.CharField(max_length=100, choices=Location)
    remark = models.CharField(max_length=100, )
    inactive = models.BooleanField()





class ManufactureTempTable(models.Model):
    manufacture = models.CharField(max_length=50)


class SuppliersTempTable(models.Model):
    supplier = models.CharField(max_length=50)
# Inventory Ends

# OPD Trasactions------By Mantu --------------------
class Cash(models.Model):
    net_payable_amt=models.FloatField()
    paid_amt=models.FloatField()

class Credit(models.Model):
    bill_no = models.CharField(max_length=50, blank=True, null=True)
    bill_date_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    uhid = models.CharField(max_length=50,blank=True, null=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    visit_no = models.CharField(max_length=50, blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    net_payable_amt=models.FloatField(blank=True, null=True)
    paid_amt=models.FloatField(blank=True, null=True)
    patient_paid_amt=models.FloatField(blank=True, null=True,default=0)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,null=True,blank=True)

class ServiceChargeMaster(models.Model):
    tariff_id=models.ForeignKey(TariffMaster,on_delete=models.CASCADE)
    service_id=models.ForeignKey(ServiceMaster,on_delete=models.CASCADE)
    service_charge=models.CharField(max_length=50)
    applicable_date=models.DateField()
    #============= for service category=======================
    # ward_type=models.ForeignKey('IPDapp.AdmissionWardType',on_delete=models.CASCADE,null=True,blank=True)
    # ward_category=models.ForeignKey('IPDapp.AdmissionWardCate',on_delete=models.CASCADE,null=True,blank=True)
    service_category=models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,null=True,blank=True)
    service_sub_category=models.ForeignKey(ServiceSubCategory,on_delete=models.CASCADE,null=True,blank=True)
    desc = models.CharField(max_length=100,null=True,blank=True)
    ipd_opd = models.CharField(max_length=100,null=True,blank=True)
    inactive = models.BooleanField(default=False,null=True,blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) -> str:
        return  self.service_id.service_name

class Adv_Visit_Creation(models.Model):
    uhid=models.CharField(max_length=50)
    advance_pay=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

class AdvPatientVisitMains(models.Model):
    uhid = models.CharField(max_length=50, null=False, blank=False)
    visit_date_time = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    visit_id=models.CharField(max_length=50)
    visit_type = models.ForeignKey(VisitTyoeMaster,on_delete=models.CASCADE)
    description = models.CharField(max_length=500,null=True,blank=True)
    nurse_doctor = models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    clinical_department = models.ForeignKey(ClinicalOrDepartment,on_delete=models.CASCADE)
    def __str__(self):
        return  self.visit_id

class Temporary_Table(models.Model):
    bill_no=models.CharField(max_length=50,blank=False,null=False)
    bill_id=models.CharField(max_length=50,blank=False,null=False)
    bill_date_time=models.CharField(max_length=50)
    uhid=models.CharField(max_length=50)
    department=models.CharField(max_length=50,null=True,blank=True)
    doctor_name=models.CharField(max_length=50,null=True,blank=True)
    visit_no=models.CharField(max_length=50,blank=False,null=False)
    corporate_id=models.CharField(max_length=50,blank=True,null=True)
    billing_group_id=models.CharField(max_length=50,blank=True,null=True)
    net_amount=models.CharField(max_length=50,blank=False,null=False)
    discount=models.CharField(max_length=50,blank=False,null=False)
    pay_amount=models.CharField(max_length=50,blank=False,null=False)
    paid_amount=models.CharField(max_length=50,blank=False,null=False)
    outstanding_amount=models.CharField(max_length=50,blank=False,null=False)
    payment_mode=models.CharField(max_length=50,blank=True,null=True)
class OPDBillSettlement(models.Model):
    Status=(
        ('active','active'),
        ('inactive','inactive'),
    )
    uhid=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50)
    bill_no=models.CharField(max_length=50)
    bill_date=models.CharField(max_length=50)
    bill_amt=models.CharField(max_length=50)
    claim_no = models.CharField(max_length=300, blank=True, null=True)
    batch_no = models.CharField(max_length=300, blank=True, null=True)
    refrence_id = models.CharField(max_length=300, blank=True, null=True)
    net_payable_amt=models.FloatField()
    paid_amt=models.FloatField()
    payment_amt=models.FloatField()
    payment_mode=models.CharField(max_length=50)
    status=models.BooleanField(choices=Status)

class OPDBillSettlementTemp(models.Model):
    Status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    Status2 = (
        ('partialy', 'partialy'),
        ('fully', 'fully'),
    )
    uhid = models.CharField(max_length=500)
    visit_id = models.CharField(max_length=500)
    bill_no = models.CharField(max_length=500)
    bill_date = models.CharField(max_length=500)
    bill_amt = models.CharField(max_length=500)
    payer = models.CharField(max_length=500)
    tax = models.CharField(max_length=500)
    paymennt_mode = models.CharField(max_length=500,blank=True,null=True)
    cheque_no = models.CharField(max_length=500,blank=True,null=True)
    receivable_amt = models.CharField(max_length=500,blank=True,null=True)
    received_amt = models.CharField(max_length=500,blank=True,null=True)
    outstanding_amt = models.CharField(max_length=500,blank=True,null=True)
    settle_date_time = models.DateTimeField(auto_now_add=True,editable=False,blank=False,null=False)
    status= models.CharField(max_length=500,null=True,blank=True)
    status2= models.CharField(max_length=500,null=True,blank=True)
    # 23/12/22 ================================ mantu ========================
    claim_no = models.CharField(max_length=300, blank=True, null=True)
    batch_no = models.CharField(max_length=300, blank=True, null=True)
    refrence_id = models.CharField(max_length=300, blank=True, null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)


# ====================== karan ==============================
class CreateUser(models.Model):
    st=(
        ('active','Active'),
        ('inactive','Inactive')
    )
    login_id=models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)
    user_id=models.CharField(max_length=100)
    f_name=models.CharField('Item Description',max_length=100)
    middle_name=models.CharField(max_length=100,blank=True)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    user_profile=models.ForeignKey('usermanagementapp.ScreenAccess',on_delete=models.CASCADE,related_name='create_user_profile')
    location=models.ForeignKey(Client,on_delete=models.CASCADE)
    store=models.ManyToManyField('testapp.StoreMaster',related_name='create_user_store',blank=True)
    create_datatime=models.DateTimeField(default=datetime.now)
    signature=models.ImageField(upload_to='user_sign/')
    status=models.CharField(max_length=100,choices=st)
    date_of_join=models.DateField(default=datetime.now)
    date_of_living=models.DateField(blank=True,null=True)
    is_admin=models.BooleanField(blank=True,null=True)

class CreateAdmin(models.Model):
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=1000)
    email=models.EmailField(blank=True)

#  ========== ward module ===================

class ProcedureTemp(models.Model):
    service_name=models.CharField(max_length=100)
    service_category=models.CharField(max_length=100)
    service_sub_category=models.CharField(max_length=100)
    service_department=models.CharField(max_length=100)
    service_sub_department=models.CharField(max_length=100)
    service_charge=models.CharField(max_length=100)

class Procedure_main(models.Model):
    uhid=models.CharField(max_length=100)
    admission_ID=models.CharField(max_length=100)
    procedure_id=models.CharField(max_length=100)
    service_name=models.CharField(max_length=100)
    service_category=models.CharField(max_length=100)
    service_sub_category=models.CharField(max_length=100)
    service_department=models.CharField(max_length=100)
    service_sub_department=models.CharField(max_length=100)
    service_charge=models.CharField(max_length=100)
    pro_date=models.DateField()

#=========================== OPD Packages =======================
class OpdPackageMaster(models.Model):
    STATUS=(
        ('active','active'),
        ('inactive','inactive'),
    )
    package_name=models.CharField(max_length=500)
    package_amount=models.FloatField(blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.package_name

class OpdPackageService(models.Model):
    package_id=models.CharField(max_length=100,null=True,blank=True)
    service_department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE,null=True,blank=True)
    service_sub_department=models.ForeignKey(ServiceSubDepartment,on_delete=models.CASCADE,null=True,blank=True)
    package_name=models.ForeignKey(OpdPackageMaster,on_delete=models.CASCADE,null=True,blank=True)
    service_name=models.ForeignKey(ServiceMaster,on_delete=models.CASCADE,null=True,blank=True)
    profile_name=models.ForeignKey('testapp.ProfileMaster',on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField()
    discount=models.IntegerField()
    rate=models.FloatField()
    net_amount=models.FloatField()
    status=models.CharField(max_length=50,null=True,blank=True)


class OpdPackageService_temp(models.Model):
    package_id=models.CharField(max_length=100,null=True,blank=True)
    service_department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE,null=True,blank=True)
    service_sub_department=models.ForeignKey(ServiceSubDepartment,on_delete=models.CASCADE,null=True,blank=True)
    package_name=models.ForeignKey(OpdPackageMaster,on_delete=models.CASCADE,null=True,blank=True)
    service_name=models.ForeignKey(ServiceMaster,on_delete=models.CASCADE,null=True,blank=True)
    profile_name=models.ForeignKey('testapp.ProfileMaster',on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField()
    discount=models.IntegerField()
    rate=models.FloatField()
    net_amount=models.FloatField()
    status=models.CharField(max_length=50,null=True,blank=True)

class OpdPackageService_main(models.Model):
    package_id=models.CharField(max_length=100)
    package_name=models.ForeignKey(OpdPackageMaster,on_delete=models.CASCADE,null=True,blank=True)
    total_services=models.CharField(max_length=100)
    before_total_amt=models.CharField(max_length=100)
    total_discount=models.CharField(max_length=100)
    after_total_amt=models.CharField(max_length=100)

#=============== For Bed charge ==============================
class BedCharge(models.Model):
    ward_type=models.CharField(max_length=100)
    ward_cat=models.CharField(max_length=100)
    bed_no=models.CharField(max_length=100)
    bed_charge=models.CharField(max_length=100)

class BedChargeSlip(models.Model):
    uhid=models.CharField(max_length=100)
    admission_ID=models.CharField(max_length=100)
    ward_type=models.CharField(max_length=100)
    ward_cat=models.CharField(max_length=100)
    bed_no=models.CharField(max_length=100)
    bed_charge=models.CharField(max_length=100)
    datetime=models.DateTimeField()
    status=models.CharField(default='generated',max_length=100)

class discharge(models.Model):
    STATUS=(
        ('LAMA','LAMA'),
        ('DAMA','DAMA'),
        ('expired','Expired'),
        ('Normal','Normal'),
    )
    uhid=models.CharField(max_length=100)
    admission_id=models.CharField(max_length=100)
    status=models.CharField(max_length=100,choices=STATUS)
    discharge_datetime=models.DateTimeField()
# ====================END BED CHAEGE ================

class TarifLinkOpdPackage(models.Model):
    tariff_id=models.CharField(max_length=100)
    opd_package_id=models.CharField(max_length=100)
    apply_date=models.CharField(max_length=100)

#===========Doctor Accounting============ 02/12/2022 ================
class DoctorAccounting(models.Model):
    service_name=models.CharField(max_length=300,blank=True,null=True)
    service_rate=models.CharField(max_length=300,blank=True,null=True)
    tariff_id=models.CharField(max_length=300,blank=True,null=True)
    doctor_id=models.CharField(max_length=300,blank=True,null=True)
    doctor_share=models.CharField(max_length=300)
    hospital_share=models.CharField(max_length=300)
    date=models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class OpdBillingGetDelete(models.Model):
    STATUS = (
        ('active', 'active'),
        ('inactive', 'inactive')
    )
    bill_no=models.CharField(max_length=50,blank=True,null=True)
    bill_id=models.CharField(max_length=50,blank=False,null=False)
    uhid=models.CharField(max_length=50,null=True,blank=True)
    bill_date_time=models.DateTimeField(auto_now_add=True,editable=False,blank=True,null=True)
    department=models.CharField(max_length=50,null=True,blank=True)
    visit_no=models.CharField(max_length=50,null=True,blank=True)
    corporate_id=models.CharField(max_length=50,null=True,blank=True)
    billing_group_id=models.CharField(max_length=50,null=True,blank=True)
    service_id=models.CharField(max_length=50,blank=False,null=False)
    charges=models.FloatField(blank=False,null=False)
    unit=models.IntegerField(blank=False,null=False)
    pay_amount=models.FloatField(blank=True,null=True)
    paid_amount=models.FloatField(blank=True,null=True)
    outstanding_amount=models.FloatField(blank=True,null=True)
    payment_mode=models.CharField(max_length=50,null=True,blank=True)
    total_amount=models.FloatField(blank=False,null=False)
    discount=models.FloatField(blank=False,null=False)
    status=models.CharField(max_length=20,choices=STATUS,default='active',blank=False,null=False)

# for Doctor Accounting Report :
class DoctorAccountingTemp(models.Model):
    uhid = models.CharField(max_length=50)
    p_name=models.CharField(max_length=50,blank=False,null=False)
    p_age=models.CharField(max_length=50,blank=False,null=False)
    p_gender=models.CharField(max_length=50,blank=False,null=False)
    dr_share1=models.CharField(max_length=50,null=True,blank=True)
    dr_share2=models.CharField(max_length=50,null=True,blank=True)
    dr_share3=models.CharField(max_length=50,null=True,blank=True)
    bill_no=models.CharField(max_length=50,blank=False,null=False)
    bill_date_time=models.CharField(max_length=50)
    service_name=models.CharField(max_length=50,null=True,blank=True)
    service_charge=models.CharField(max_length=50,null=True,blank=True)
    dr_share=models.CharField(max_length=50,null=True,blank=True)

# Profile Master 13/12/22
class ProfileMaster(models.Model):
    STATUS=(
        ('active','active'),
        ('inactive','inactive'),
    )
    profile_name=models.CharField(max_length=500)
    profile_amount=models.FloatField(blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.profile_name

# Some changes in fields 16/12/22 ===================
class ProfileService(models.Model):
    profile_id=models.CharField(max_length=100)
    service_department=models.CharField(max_length=100)
    service_sub_department=models.CharField(max_length=100)
    profile_name=models.CharField(max_length=100)
    service_name=models.CharField(max_length=100)
    infant_range = models.CharField(max_length=100, blank=True, null=True)
    chield_range = models.CharField(max_length=100, blank=True, null=True)
    male_range = models.CharField(max_length=100, blank=True, null=True)
    female_range = models.CharField(max_length=100, blank=True, null=True)
    units = models.CharField(max_length=100 ,blank=True, null=True)
    outsource=models.BooleanField(default=False)

class ProfileService_temp(models.Model):
    service_name=models.CharField(max_length=100)
    infant_range = models.CharField(max_length=100, blank=True, null=True)
    chield_range = models.CharField(max_length=100, blank=True, null=True)
    male_range = models.CharField(max_length=100, blank=True, null=True)
    female_range = models.CharField(max_length=100, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)

class ProfileServiceSub(models.Model):
    service_name=models.CharField(max_length=100)
    infant_range = models.CharField(max_length=100, blank=True, null=True)
    chield_range = models.CharField(max_length=100, blank=True, null=True)
    male_range = models.CharField(max_length=100, blank=True, null=True)
    female_range = models.CharField(max_length=100, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)

class ProfileService_main(models.Model):
    profile_id=models.CharField(max_length=100,blank=True,null=True)
    service_department=models.CharField(max_length=100)
    service_sub_department=models.CharField(max_length=100)
    total_services=models.CharField(max_length=100,blank=True,null=True)
    outsource=models.BooleanField(default=False)

# 14/12/22 afternoon ============================
class Service_Test(models.Model):
    test_name=models.ForeignKey('testapp.ServiceMaster',on_delete=models.CASCADE,null=True,blank=True)
    service_category=models.CharField(max_length=100)
    service_sub_category=models.CharField(max_length=100)
    service_department=models.CharField(max_length=100)
    ServiceSubDepartment=models.CharField(max_length=100)
    infant_range = models.CharField(max_length=100,blank=True,null=True)
    chield_range = models.CharField(max_length=100,blank=True,null=True)
    male_range = models.CharField(max_length=100,blank=True,null=True)
    female_range = models.CharField(max_length=100,blank=True,null=True)
    units=models.CharField(max_length=100)
    methodology=models.CharField(max_length=100)

class ServiceTest_records(models.Model):
    test_name=models.CharField(max_length=100)
    service_category=models.CharField(max_length=100)
    service_sub_category=models.CharField(max_length=100)
    service_department=models.CharField(max_length=100)
    ServiceSubDepartment=models.CharField(max_length=100)
    infant_range = models.CharField(max_length=100,blank=True,null=True)
    chield_range = models.CharField(max_length=100,blank=True,null=True)
    male_range = models.CharField(max_length=100,blank=True,null=True)
    female_range = models.CharField(max_length=100,blank=True,null=True)
    units=models.CharField(max_length=100)
    date_time=models.DateTimeField()
    logged_name=models.CharField(max_length=100)
    methodology=models.CharField(max_length=100)
# 16/12/22 ===================
class ProfileMasterlinkTarrif(models.Model):
    tariff_id=models.CharField(max_length=100)
    profile_id=models.CharField(max_length=100)
    apply_date=models.CharField(max_length=100)

#  ============ karan =========
class PendingInvestigation_main(models.Model):
    PTID=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100)
    uhid=models.CharField(max_length=100)
    visit_no=models.CharField(max_length=100)
    bill_no=models.CharField(max_length=100)
    profile_id=models.CharField(max_length=100)
    profile_name=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    sub_department=models.CharField(max_length=100)
    outsource=models.BooleanField(default=False)
    date_time=models.DateTimeField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class LabResultEntry(models.Model):
    STATUS=(
    ('in_range','in_range'),
    ('out_range','out_range'),
    )
    PTID=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100)
    profile_id=models.CharField(max_length=100,null=True,blank=True)
    profile_name=models.CharField(max_length=100)
    service_name=models.CharField(max_length=100)
    range = models.CharField(max_length=100,null=True,blank=True)
    value = models.CharField(max_length=100,null=True,blank=True)
    units = models.CharField(max_length=100,null=True,blank=True)
    outsource=models.BooleanField(default=False)
    status=models.CharField(max_length=100,choices=STATUS,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class SampleMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    sample_name=models.CharField(max_length=100)
    status=models.CharField(max_length=100,choices=STATUS)
    description=models.TextField(blank=True,null=True)

class VolumeMaster(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    volume=models.CharField(max_length=100)
    status=models.CharField(max_length=100,choices=STATUS)
    description=models.TextField(blank=True,null=True)

class SampleCollection(models.Model):
    PTID=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100)
    lab_service_name=models.CharField(max_length=100)
    type_of_sample=models.CharField(max_length=100)
    Volume=models.CharField(max_length=100)
    technician_name=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class SampleCollected(models.Model):
    STATUS=(
    ('waiting','waiting'),
    ('completed','completed'),
    )
    PTID=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100)
    uhid=models.CharField(max_length=100)
    visit_no=models.CharField(max_length=100)
    bill_no=models.CharField(max_length=100)
    profile_id=models.CharField(max_length=100)
    profile_name=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now_add=True)
    department=models.CharField(max_length=100)
    sub_department=models.CharField(max_length=100)
    status=models.CharField(max_length=100,choices=STATUS)
    source_status=models.CharField(max_length=100,blank=True,null=True)
    validated_by=models.ForeignKey('testapp.CreateUser',on_delete=models.CASCADE, blank=True,null=True)
    validated_at=models.DateTimeField(blank=True,null=True)
    result_entry_by=models.ForeignKey('testapp.CreateUser',on_delete=models.CASCADE, related_name='result_entry_by' ,blank=True,null=True)
    result_entry_at=models.DateTimeField(blank=True,null=True)
    doctor_id=models.CharField(max_length=100)
    outsource=models.BooleanField(default=False)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

# 19/12/22 ===================
class OPDBillingPackage(models.Model):
    uhid=models.CharField(max_length=100)
    visit_no=models.CharField(max_length=100)
    bill_no=models.CharField(max_length=100)
    package_id=models.CharField(max_length=100)
    package_name=models.CharField(max_length=100)
    date_time=models.DateTimeField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class ServiceTestlinkTarrif(models.Model):
    tariff_id=models.CharField(max_length=100)
    service_test_id=models.CharField(max_length=100)
    apply_date=models.CharField(max_length=100)

class ServiceTest(models.Model):
    test_name=models.CharField(max_length=100)
    infant_range = models.CharField(max_length=100,blank=True,null=True)
    chield_range = models.CharField(max_length=100,blank=True,null=True)
    male_range = models.CharField(max_length=100,blank=True,null=True)
    female_range = models.CharField(max_length=100,blank=True,null=True)
    units=models.CharField(max_length=100)
    test_charges=models.CharField(max_length=100,blank=True,null=True,default=0)

class LabResultEntry_records(models.Model):
    STATUS=(
    ('in_range','in_range'),
    ('out_range','out_range'),
    )
    PTID=models.CharField(max_length=100,blank=True,null=True)
    test_id=models.CharField(max_length=100,blank=True,null=True)
    profile_id=models.CharField(max_length=100,blank=True,null=True)
    profile_name=models.CharField(max_length=100,blank=True,null=True)
    service_name=models.CharField(max_length=100,blank=True,null=True)
    range = models.CharField(max_length=100,blank=True,null=True)
    value = models.CharField(max_length=100,blank=True,null=True)
    units = models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=100,choices=STATUS)
    updated_by=models.CharField(max_length=100,blank=True,null=True)
    upadated_date_time=models.DateTimeField(auto_now_add=True)

class Validation_record(models.Model):
    PTID=models.CharField(max_length=100)
    uhid=models.CharField(max_length=100)
    validated_by=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100)

    #================== 02/01/2022 ==========================
class ProfileChargeMaster(models.Model):
    tariff_id=models.ForeignKey(TariffMaster,on_delete=models.CASCADE)
    profile_id=models.ForeignKey(ProfileMaster,on_delete=models.CASCADE)
    profile_charge=models.CharField(max_length=50)
    applicable_date=models.DateField()
    # ============= for service category=======================
    # ward_type=models.ForeignKey('IPDapp.AdmissionWardType',on_delete=models.CASCADE,null=True,blank=True)
    # ward_category=models.ForeignKey('IPDapp.AdmissionWardCate',on_delete=models.CASCADE,null=True,blank=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, blank=True)
    service_sub_category = models.ForeignKey(ServiceSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    ipd_opd = models.CharField(max_length=100, null=True, blank=True)
    inactive = models.BooleanField(default=False, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(LocationMaster, on_delete=models.CASCADE, null=True, blank=True)

class PackageChargeMaster(models.Model):
    tariff_id=models.ForeignKey(TariffMaster,on_delete=models.CASCADE)
    package_id=models.ForeignKey(OpdPackageMaster,on_delete=models.CASCADE)
    package_charge=models.CharField(max_length=50)
    applicable_date=models.DateField()
    # ============= for service category=======================
    # ward_type=models.ForeignKey('IPDapp.AdmissionWardType',on_delete=models.CASCADE,null=True,blank=True)
    # ward_category=models.ForeignKey('IPDapp.AdmissionWardCate',on_delete=models.CASCADE,null=True,blank=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, blank=True)
    service_sub_category = models.ForeignKey(ServiceSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    ipd_opd = models.CharField(max_length=100, null=True, blank=True)
    inactive = models.BooleanField(default=False, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(LocationMaster, on_delete=models.CASCADE, null=True, blank=True)

class BedChargeSlip_main(models.Model):
    uhid = models.CharField(max_length=100)
    admission_ID = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=100)
    ward_cat = models.CharField(max_length=100)
    bed_no = models.CharField(max_length=100)
    bed_charge = models.CharField(max_length=100)
    datetime = models.DateTimeField()



# ================ For POST DIALYSIS 30/01/2023 ========================

class CannulationNurse(models.Model):
    nurse_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.nurse_name
class Post_Dialysis_Details(models.Model):
    uhid=models.CharField(max_length=50)
    visit_id = models.CharField(max_length=50,null=True,blank=True)
    #==== For Session Details =====================
    status=models.CharField(max_length=50)
    closing_attendent=models.CharField(max_length=50)
    completion_status=models.CharField(max_length=50)
    end_time=models.CharField(max_length=50)
    duration=models.CharField(max_length=50)
    next_day_dialysis=models.CharField(max_length=50)
    shift=models.CharField(max_length=50)
    #===== for Patient Condition ====================
    bp_sitting_max=models.CharField(max_length=50)
    bp_sitting_min=models.CharField(max_length=50)
    bp_standing_max=models.CharField(max_length=50)
    bp_standing_min=models.CharField(max_length=50)
    respiration=models.CharField(max_length=50)
    pulse_sitting=models.CharField(max_length=50)
    pulse_standing=models.CharField(max_length=50)
    tempreture=models.CharField(max_length=50)
    measured_wt=models.CharField(max_length=50)
    wheelchair_wt=models.CharField(max_length=50)
    prosthetic_wt=models.CharField(max_length=50)
    condition_assessment=models.CharField(max_length=50)
    prolonged_bleeding_at_punctured_sites=models.CharField(max_length=50)
    #========= for Dialysis Details ===================
    weight_lost=models.CharField(max_length=50)
    fluid_removed=models.CharField(max_length=50)
    uf_rate=models.CharField(max_length=50)
    heparin_Left=models.CharField(max_length=50)
    total_heparin_infused=models.CharField(max_length=50)
    dialyzer_rating=models.CharField(max_length=50)
    bruit_thrill=models.CharField(max_length=50)
    minimum_BP_max=models.CharField(max_length=50)
    minimum_BP_min=models.CharField(max_length=50)
    minimum_BP_time=models.CharField(max_length=50)
    dialysis_odometer_end_eading=models.CharField(max_length=50)
    completion_notes=models.TextField()
    next_pre_dialysis_notes=models.TextField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class Pre_Dialysis_Details(models.Model):
    # 60 fields==========
    uhid=models.CharField(max_length=30)
    visit_id = models.CharField(max_length=50,null=True,blank=True)
    #==== for Prev Post Dialysis 30/01/2023 ====================
    pre_post_dialysis=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    # pre_equip_preparation=models.CharField(max_length=100)
    physian=models.CharField(max_length=100)
    primary_dialysis_theraphy=models.CharField(max_length=100)
    secondry_dialysis_theraphy=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    cannulation_nurse =models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    machine_name=models.CharField(max_length=100,null=True,blank=True)
    asset_type=models.CharField(max_length=100,null=True,blank=True)
    bruit_thrill=models.CharField(max_length=100,null=True,blank=True)
    cannulation_name=models.CharField(max_length=100,null=True,blank=True)
    access_site=models.CharField(max_length=100,null=True,blank=True)
    access_site_infection=models.CharField(max_length=100,null=True,blank=True)
    iso_uf=models.CharField(max_length=100,null=True,blank=True)
    any_remark=models.CharField(max_length=100,null=True,blank=True)
    dialysis_type=models.CharField(max_length=100,null=True,blank=True)
    other_staff=models.CharField(max_length=100,null=True,blank=True)
    completion_status=models.CharField(max_length=100,null=True,blank=True)
    needle_type=models.CharField(max_length=100,null=True,blank=True)
    #======== for Dialyzer Reuse =========================
    dialyser=models.CharField(max_length=100,null=True,blank=True)
    bundle_volume=models.CharField(max_length=100,null=True,blank=True)
    reprocess_number=models.CharField(max_length=100,null=True,blank=True)
    reprocessed_date=models.CharField(max_length=100,null=True,blank=True)
    rating=models.CharField(max_length=100,null=True,blank=True)
    single_used_dialyzer=models.CharField(max_length=100,null=True,blank=True)
    #======== for Patient Condition =========================
    bp_sitting_max = models.CharField(max_length=50,null=True,blank=True)
    bp_sitting_min = models.CharField(max_length=50,null=True,blank=True)
    bp_standing_max = models.CharField(max_length=50,null=True,blank=True)
    bp_standing_min = models.CharField(max_length=50,null=True,blank=True)
    respiration = models.CharField(max_length=50,null=True,blank=True)
    pulse_sitting = models.CharField(max_length=50,null=True,blank=True)
    pulse_standing = models.CharField(max_length=50,null=True,blank=True)
    tempreture = models.CharField(max_length=50,null=True,blank=True)
    measured_wt = models.CharField(max_length=50,null=True,blank=True)
    wheelchair_wt = models.CharField(max_length=50,null=True,blank=True)
    prosthetic_wt = models.CharField(max_length=50,null=True,blank=True)
    condition_assessment = models.CharField(max_length=100,null=True,blank=True)
    assessment = models.CharField(max_length=100,null=True,blank=True)
    current_wt = models.CharField(max_length=100,null=True,blank=True)
    previous_wt = models.CharField(max_length=100,null=True,blank=True)
    weight_change = models.CharField(max_length=100,null=True,blank=True)
    #======== for Dialysis Details =========================
    dry_wt_date=models.CharField(max_length=100,null=True,blank=True)
    target_wt=models.CharField(max_length=100,null=True,blank=True)
    excess=models.CharField(max_length=100,null=True,blank=True)
    duration=models.CharField(max_length=100,null=True,blank=True)
    target_UF_Vol_kg=models.CharField(max_length=100,null=True,blank=True)
    target_UFR_vol_kg_hr=models.CharField(max_length=100,null=True,blank=True)
    anticoagulation=models.CharField(max_length=100,null=True,blank=True)
    heparin_type=models.CharField(max_length=100,null=True,blank=True)
    initial_dose=models.CharField(max_length=100,null=True,blank=True)
    interim_Dose=models.CharField(max_length=100,null=True,blank=True)
    total_heparin_bolus=models.CharField(max_length=100,null=True,blank=True)
    hourly=models.CharField(max_length=100,null=True,blank=True)
    unit_in_syringe=models.CharField(max_length=100,null=True,blank=True)
    dialysis_odometer_str_reading=models.CharField(max_length=100,null=True,blank=True)
    pre_dialysis_assessment=models.CharField(max_length=100,null=True,blank=True)
    notes_pre_dialysis_session=models.CharField(max_length=100,null=True,blank=True)
    fluids_volume_ml=models.CharField(max_length=100,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location_id=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)


# ===== for Dialysis_Details ============================
class Dialysis_Details(models.Model):
    uhid=models.CharField(max_length=100)
    # ======== for Session Details ===============
    dialysis_start=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    start_attendant=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    machine=models.CharField(max_length=100)
    machine_status=models.CharField(max_length=100)
    min_bp_time=models.CharField(max_length=100)
    min_bp=models.CharField(max_length=100)
    average_pulse=models.CharField(max_length=100)
    average_vp=models.CharField(max_length=100)
    avg_dial_pressure=models.CharField(max_length=100)
    server_time=models.CharField(max_length=100)
    post_equip_preparation=models.CharField(max_length=100)
    completion_status=models.CharField(max_length=100)

#============ For CHEMOTHERAPY TREATMENT SHEET =========================
class Chemotherapy_treatment_sheet(models.Model):
    uhid=models.CharField(max_length=30)
    patient_name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    stage=models.CharField(max_length=100)
    weight=models.CharField(max_length=100)
    height=models.CharField(max_length=100)
    BSA=models.CharField(max_length=100)
    histology=models.CharField(max_length=100)
    drugs=models.CharField(max_length=100)
    dose_m2=models.CharField(max_length=100)
    notes=models.CharField(max_length=100)

class Chemotherapy_treatment_sheet_sub(models.Model):
    uhid=models.CharField(max_length=30)
    date=models.CharField(max_length=100)
    bp=models.CharField(max_length=100)
    p_temp=models.CharField(max_length=100)
    wht=models.CharField(max_length=100)
    wbc=models.CharField(max_length=100)
    hb=models.CharField(max_length=100)
    plt=models.CharField(max_length=100)
    uec=models.CharField(max_length=100)
    remark1=models.CharField(max_length=100)
    remark2=models.CharField(max_length=100)
    remark3=models.CharField(max_length=100)
    remark4=models.CharField(max_length=100)

#====== for Nursing Notes 01/02/2023 ===============================
class Nursing_Notes(models.Model):
    uhid=models.CharField(max_length=30)
    patient_name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    diagnosis=models.CharField(max_length=100)
    hosp_no=models.CharField(max_length=100)
    chemotherapy_protocol=models.CharField(max_length=100)

class Nursing_Notes_sub(models.Model):
    uhid=models.CharField(max_length=30)
    date_time=models.CharField(max_length=100)
    nursing_notes=models.CharField(max_length=100)
    name_sign=models.CharField(max_length=100)

#==== Foe Dialysis Master  01/02/2023 ================
class Status(models.Model):
    status=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class Primary_dialysis_theropist(models.Model):
    pri_dial_therop=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class Secondry_dialysis_theropist(models.Model):
    sec_dial_therop=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class Machine_name(models.Model):
    machine_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class Asset_type(models.Model):
    asset_type=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class Bruit_thrill(models.Model):
    bruit_thrill=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class Access_site(models.Model):
    access_site=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    def __str__(self):
        return self.access_site

class Dialysate_Type(models.Model):
    dialysis_type=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class Completion_Status_Master(models.Model):
    completion_Status=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class Needle_type(models.Model):
    needle_type=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class Dialyzer(models.Model):
    dialyzer = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
class Rating(models.Model):
    rating = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
class Anticoagulation(models.Model):
    anticoagulation_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
class Heparin_Type(models.Model):
    heparine_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class Closing_Attendent(models.Model):
    closing_attendent=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class Shift(models.Model):
    shift_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    def __str__(self):
        return self.shift_name
#===== End Master For Dialysis =====
#========= For Estimate Bill =======================
class Estimate_bill_mains(models.Model):
    uhid = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30)
    age = models.CharField(max_length=30)
    sex = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=30)
    services = models.CharField(max_length=300)
    services_rate = models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)


class Estimate_bill_sub(models.Model):
    uhid=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=30)
    age=models.CharField(max_length=30)
    sex=models.CharField(max_length=30)
    contact_no=models.CharField(max_length=30)
    billing_group=models.ForeignKey(BillingGroup,on_delete=models.CASCADE)
    services=models.CharField(max_length=300,null=True,blank=True)
    services_rate=models.CharField(max_length=300,null=True,blank=True)

class Estimate_bill_temp(models.Model):
    uhid=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=30)
    age=models.CharField(max_length=30)
    sex=models.CharField(max_length=30)
    contact_no=models.CharField(max_length=30)
    services=models.CharField(max_length=300)
    services_rate=models.CharField(max_length=300)


class Schedule_Master(models.Model):
    schedule_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class Maintanence_Deatils(models.Model):
    schedule_name=models.CharField(max_length=100)
    item_sub_id=models.CharField(max_length=100)
    item_id=models.CharField(max_length=100,null=True,blank=True)
    item_model_no=models.CharField(max_length=100)
    created_at=models.CharField(max_length=100)
    due_date=models.CharField(max_length=30,null=True,blank=True)
    description=models.CharField(max_length=100)

#================= 08/02/2023 ====================
class Unplanned_Maintanence(models.Model):
    item_sub_id=models.CharField(max_length=100)
    item_id=models.CharField(max_length=100,null=True,blank=True)
    item_model_no=models.CharField(max_length=100)
    done_by=models.CharField(max_length=100)
    problem_occure_date=models.CharField(max_length=100)
    problem_name=models.CharField(max_length=30)
    resolve_date=models.CharField(max_length=30,null=True,blank=True)
    remark=models.CharField(max_length=100)

class Preventory_Maintanence(models.Model):
    item_sub_id=models.CharField(max_length=100)
    item_id=models.CharField(max_length=100,null=True,blank=True)
    item_model_no=models.CharField(max_length=100)
    done_by=models.CharField(max_length=100)
    done_date=models.CharField(max_length=100)
    due_date=models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    remark=models.CharField(max_length=100)
    delay_days=models.CharField(max_length=30,null=True,blank=True)

class Validation_Calibration(models.Model):
    item_sub_id=models.CharField(max_length=100)
    item_id=models.CharField(max_length=100,null=True,blank=True)
    item_model_no=models.CharField(max_length=100)
    done_by=models.CharField(max_length=100)
    schedule_name=models.CharField(max_length=100)
    dispensive=models.CharField(max_length=100)
    date_time=models.CharField(max_length=100)
    validation_date=models.CharField(max_length=100)
    remark=models.CharField(max_length=100)
#=========================== 06/03/23 ============================

class Ins_Document(models.Model):
    doc_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class PatientInsDocType(models.Model):
    uhid=models.CharField(max_length=100)
    billing_group=models.CharField(max_length=100,blank=True,null=True)
    nhif_ins_corp_name=models.CharField(max_length=100,blank=True,null=True)
    doc_type=models.CharField(max_length=100)

class CancelOpdBillingMain(models.Model):
    bill_no=models.CharField(max_length=50,blank=False,null=False)
    bill_id=models.CharField(max_length=50,blank=False,null=False)
    bill_date_time=models.CharField(max_length=50,blank=False,null=False)
    uhid=models.CharField(max_length=50)
    temp_bill_no=models.CharField(max_length=50,null=True,blank=True)
    department=models.CharField(max_length=50,null=True,blank=True)
    doctor_name=models.CharField(max_length=50,null=True,blank=True)
    visit_no=models.CharField(max_length=50,blank=False,null=False)
    corporate_id=models.CharField(max_length=50,blank=True,null=True)
    billing_group_id=models.CharField(max_length=50,blank=True,null=True)
    package_profile_id=models.CharField(max_length=50,blank=True,null=True)
    net_amount=models.CharField(max_length=50,blank=False,null=False)
    discount=models.CharField(max_length=50,blank=False,null=False)
    pay_amount=models.CharField(max_length=50,blank=False,null=False)
    paid_amount=models.CharField(max_length=50,blank=False,null=False)
    outstanding_amount=models.CharField(max_length=50,blank=False,null=False)
    payment_mode=models.CharField(max_length=50,blank=True,null=True)
    paid_amt=models.CharField(max_length=50,blank=True,null=True)
    paid_amt_update_date=models.CharField(max_length=50,blank=True,null=True)
    updated_at = models.CharField(max_length=50,blank=True,null=True)
    status=models.CharField(max_length=50,blank=False,null=False)


#=========================================== THIS IS FOR SOME FORM ===============================
class ConsentChemotherapy(models.Model):
    uhid=models.CharField(max_length=100)
    patient_name=models.CharField(max_length=100)
    patient_nhif_id=models.CharField(max_length=100)
    patient_national_id=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
    patient_email=models.CharField(max_length=100)
    diagnosis=models.TextField(max_length=200)
    chemotherapy_protocol=models.TextField(max_length=500)
    inform_by_dr=models.CharField(max_length=100)
    i_have=models.CharField(max_length=100)
    language=models.CharField(max_length=100)
    patient_sign=models.CharField(max_length=100)
    patient_relative_sign=models.CharField(max_length=100)
    witness=models.CharField(max_length=100)

class Refferal_notes(models.Model):
    uhid=models.CharField(max_length=100)
    date=models.CharField(max_length=100,null=True,blank=True)
    dr=models.CharField(max_length=100)
    re=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    diagnosis=models.TextField(max_length=500)

class CaseSummery(models.Model):
    uhid=models.CharField(max_length=100)
    patient_name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    hosp_no=models.CharField(max_length=100)
    tel_no=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    d_o_a=models.CharField(max_length=100)
    d_o_d=models.CharField(max_length=100)
    consultant=models.CharField(max_length=100)
    dept=models.CharField(max_length=100)
    medical_history=models.CharField(max_length=100)
    physi_find=models.CharField(max_length=100)
    investigation=models.CharField(max_length=100)
    management=models.CharField(max_length=100)
    treat_discharge=models.CharField(max_length=100)
    recommendation=models.CharField(max_length=100)
    follow_up=models.CharField(max_length=100)
    day=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
    name_sign=models.CharField(max_length=100)
    doctor_notes=models.CharField(max_length=100)

#==================== kennedy in clinical management ============================

class PatientAllergy(models.Model):
    allergy_choices = (
        ('Drug', 'Drug'),
        ('Food', 'Food'),
        ('Insect', 'Insect'),
        ('Latex', 'Latex'),
        ('Mold', 'Mold'),
    )
    allergen_choices = (
        ('Drug', 'Drug'),
        ('Food', 'Food'),
        ('Insect', 'Insect'),
        ('Latex', 'Latex'),)
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True,choices=allergy_choices)
    allergen = models.CharField(max_length=100, null=True, blank=True,choices=allergen_choices)
    reaction = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.allergen

class TriageInfo(models.Model):
    social_status_choices = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    )
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    social_status = models.CharField(choices=social_status_choices, max_length=100,null=True, blank=True)
    # alcohol/ Tobacco info
    tobacco = models.BooleanField(default=False, null=True, blank=True)
    tobacco_frequency = models.CharField(max_length=100, null=True, blank=True)
    alcohol = models.BooleanField(default=False, null=True, blank=True)
    alcohol_frequency = models.CharField(max_length=100, null=True, blank=True)
    # Visual Acuity
    OU= models.BooleanField(default=False, null=True, blank=True)
    OU_corrected = models.BooleanField(default=False, null=True, blank=True)
    OS= models.BooleanField(default=False, null=True, blank=True)
    OS_corrected = models.BooleanField(default=False, null=True, blank=True)
    OD= models.BooleanField(default=False, null=True, blank=True)
    OD_corrected = models.BooleanField(default=False, null=True, blank=True)
    # Family History\
    heart_disease = models.BooleanField(default=False, null=True, blank=True)
    diabetes = models.BooleanField(default=False, null=True, blank=True)
    cancer = models.BooleanField(default=False, null=True, blank=True)
    other_family_disease = models.CharField(max_length=100, null=True, blank=True)
    # Mental Status
    alert = models.BooleanField(default=False, null=True, blank=True)
    awake = models.BooleanField(default=False, null=True, blank=True)
    oriented = models.BooleanField(default=False, null=True, blank=True)
    unresponsive = models.BooleanField(default=False, null=True, blank=True)
    response_to_pain = models.BooleanField(default=False, null=True, blank=True)
    # Physical Examination
    color_pink = models.BooleanField(default=False, null=True, blank=True)
    color_palle = models.BooleanField(default=False, null=True, blank=True)
    color_cyanosis = models.BooleanField(default=False, null=True, blank=True)
    skin_warm= models.BooleanField(default=False, null=True, blank=True)
    skin_cold = models.BooleanField(default=False, null=True, blank=True)
    skin_hot = models.BooleanField(default=False, null=True, blank=True)
    skin_dry = models.BooleanField(default=False, null=True, blank=True)
    # Past Medical history
    past_HTN = models.BooleanField(default=False, null=True, blank=True)
    past_heart_disease = models.BooleanField(default=False, null=True, blank=True)
    past_diabetes = models.BooleanField(default=False, null=True, blank=True)
    past_cancer = models.BooleanField(default=False, null=True, blank=True)
    past_HIV = models.BooleanField(default=False, null=True, blank=True)
    past_TB = models.BooleanField(default=False, null=True, blank=True)
    past_other_disease = models.CharField(max_length=100, null=True, blank=True)
    # Past Surgery
    past_surgery_gall_bladder = models.BooleanField(default=False, null=True, blank=True)
    past_surgery_appendix = models.BooleanField(default=False, null=True, blank=True)
    past_surgery_hernia = models.BooleanField(default=False, null=True, blank=True)
    past_surgery_other = models.CharField(max_length=100, null=True, blank=True)
    # Bleeding
    bleeding = models.BooleanField(default=False, null=True, blank=True)
    # Skin
    skin_intact= models.BooleanField(default=False, null=True, blank=True)
    skin_other= models.CharField(max_length=100, null=True, blank=True)
    # Cardiovascular
    shortness_of_breath = models.BooleanField(default=False, null=True, blank=True)
    Coughing = models.BooleanField(default=False, null=True, blank=True)
    visit_date= models.DateTimeField(auto_now_add=True, null=True,blank=True)
    vital_bp= models.CharField(max_length=100, null=True, blank=True)
    vital_pulse= models.CharField(max_length=100, null=True, blank=True)
    vital_temp= models.CharField(max_length=100, null=True, blank=True)
    patient_name= models.CharField(max_length=100, null=True, blank=True)

class EmrInfo(models.Model):
    record_type_choices= (
        ('OPD', 'OPD'),
        ('IPD', 'IPD'),
    )
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    visit_date= models.DateTimeField(null=True,blank=True)
    patient_name= models.CharField(max_length=100, null=True, blank=True)
    age= models.CharField(max_length=100, null=True, blank=True)
    gender= models.CharField(max_length=100, null=True, blank=True)
    record_type= models.CharField(max_length=100, null=True, blank=True,choices=record_type_choices)

class EmrInfoRecord(models.Model):
    medical_record_type_choices = (
        ('nurse_notes', 'nurse_notes'),
        ('doctor_prescription', 'doctor_prescription'),
        ('lab_report', 'lab_report'),
        ('patient_history', 'patient_history'),
        ('clinical_notes', 'clinical_notes'),
        ('consultant_notes', 'consultant_notes'),
        ('consultant_order', 'consultant_order'),
        ('medical_details', 'medical_details'),
    )
    emrinfo= models.ForeignKey(EmrInfo, on_delete=models.CASCADE, null=True, blank=True, related_name='emrinfo_record')
    medical_record_type = models.CharField(max_length=100, null=True, blank=True,choices=medical_record_type_choices)
    medical_record_file = models.FileField(upload_to='medical_record/', null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)

class LabReportStore(models.Model):
    uhid=models.CharField(max_length=100)
    bill_no=models.CharField(max_length=100)
    report=models.FileField(upload_to='lab_report/')

###--Insurance Module---###

class Insurance_CheckList_Master(models.Model):
    checklist_name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    status=models.CharField(max_length=50,blank=True,null=True,editable=False)

class Insurance_Checklist_Parent(models.Model):
    checklist_no=models.CharField(max_length=255)
    checklist_date=models.DateField()
    bill_no=models.CharField(max_length=255)
    lou_no=models.CharField(max_length=255)
    claim_no=models.CharField(max_length=255)
    batch_no=models.CharField(max_length=255)
    bill_datetime=models.DateTimeField()
    uhid=models.CharField(max_length=50)
    bill_amt=models.CharField(max_length=50)
    net_amt=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class Insurance_Checklist_Child(models.Model):
    checklist_no=models.CharField(max_length=255)
    checklist_date=models.DateField()
    document_name=models.CharField(max_length=255)
    prepare_status=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class Insurance_Claim_Acknowledge(models.Model):
    bill_no=models.CharField(max_length=255)
    bill_datetime=models.DateTimeField()
    uhid=models.CharField(max_length=50)
    bill_amt=models.CharField(max_length=50)
    net_amt=models.CharField(max_length=50)
    claim_amt=models.CharField(max_length=50)
    acknowledge=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class Insurance_Payement_Detail(models.Model):
    receipt_no=models.CharField(max_length=50,null=True,blank=True)
    pay_type=models.CharField(max_length=50,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location_id=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)
    uhid=models.CharField(max_length=50,null=True,blank=True)
    date_time=models.CharField(max_length=50,null=True,blank=True)
    bill_id=models.CharField(max_length=50)
    mode_type=models.CharField(max_length=30)
    net_amount=models.FloatField(blank=True,null=True)
    paid_amount=models.FloatField(blank=True,null=True)
    pending_amount=models.FloatField(blank=True,null=True)
    bank_no=models.CharField(max_length=100,blank=True,null=True)
    card_no=models.CharField(max_length=100,blank=True,null=True)
    paid_by=models.CharField(max_length=100,blank=True,null=True)
    ref_number=models.CharField(max_length=100,blank=True,null=True)
    mobile_nummber=models.CharField(max_length=100,blank=True,null=True)
    card_holder_name=models.CharField(max_length=100,blank=True,null=True)
    date_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status=models.CharField(max_length=100)

class Insurance_Raising_Queries(models.Model):
    bill_no=models.CharField(max_length=255)
    bill_datetime=models.DateTimeField()
    uhid=models.CharField(max_length=50)
    bill_amt=models.CharField(max_length=50)
    net_amt=models.CharField(max_length=50)
    question=models.CharField(max_length=50)
    answer=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)


# Gohila pharmacy




class ItemBelongsToMaster(models.Model):
    belongs_to = models.CharField(max_length=100)

    def __str__(self):
        return self.belongs_to

class ItemCategoryMaster(models.Model):
    item_category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.item_category

class ItemMaster(models.Model):
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
    num_of_reuse = models.CharField(max_length=100, )
    serial_batch_control = models.CharField(max_length=100, )
    reusable_rate = models.CharField(max_length=100, )

    belongs_to = models.ForeignKey(ItemBelongsToMaster, on_delete=models.CASCADE)
    item_category = models.ForeignKey(ItemCategoryMaster, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100, )
    shortcode = models.CharField(max_length=100, )
    packing = models.ForeignKey(PackagigMaster, on_delete=models.CASCADE)
    contain = models.CharField(max_length=100, )
    unit = models.ForeignKey(ItemUnitMaster, on_delete=models.CASCADE)
    conversion_factor = models.CharField(max_length=100, )
    hsn_code = models.CharField(max_length=100, )
    hospital_item_code = models.CharField(max_length=100, )
    remark = models.CharField(max_length=100, )
    Gst = models.CharField(max_length=100, choices=GST)

    min_quantity = models.CharField(max_length=100, )
    max_quantity = models.CharField(max_length=100, )
    re_order_level = models.CharField(max_length=100, )


class VendorMaster(models.Model):

    Rating = (
        ('1', '1'),
        ('2', '2'),
        ('3','3'),
        ('4','4'),
    )
    vendor_name = models.CharField(max_length=100)
    vendor_short_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=100)
    phone2 = models.CharField(max_length=100)
    fax_no = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=100)
    rating = models.CharField(max_length=100, choices=Rating)
    afc_code = models.CharField(max_length=100,blank=True,null=True)
    type_char = models.CharField(max_length=100,blank=True,null=True)
    payment_mode = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    inactive = models.BooleanField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.strftime('%d-%m-%Y')}"
    def __str__(self):
        return f"{self.updated_at.strftime('%d-%m-%Y')}"
    def __str__(self):
        return self.payment_terms
    def __str__(self):
        return self.vendor_name

class ItemsubcategoryMaster(models.Model):
    itemcategory=models.ForeignKey(ItemCategoryMaster,on_delete=models.CASCADE)
    itemsubcategory=models.CharField(max_length=50)
    description=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.itemsubcategory

class Generic_Master(models.Model):
    generic_name=models.CharField(max_length=50)
    description=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.generic_name

class Inventory_ItemMaster(models.Model):
    # GST = (
    #     ('10%', '10%'),
    #     ('18%', '18%'),
    #     ('22%', '22%'),
    #     ('28%', '28%'),
    # )
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
    belongs_to = models.CharField(max_length=100)
    item_category =models.CharField(max_length=100)
    item_subcategory =models.ForeignKey(ItemsubcategoryMaster,on_delete=models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=100)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE,null=True,blank=True)
    generic_id=models.ForeignKey(Generic_Master,on_delete=models.CASCADE,null=True,blank=True)
    shortcode = models.CharField(max_length=100, )
    packing = models.CharField(max_length=100)
    contain = models.CharField(max_length=100, )
    unit =models.CharField(max_length=100)
    conversion_factor = models.CharField(max_length=100, )
    hsn_code = models.CharField(max_length=100, )
    hsn_item_code = models.CharField(max_length=100, )
    remark = models.CharField(max_length=100, )
    tax = models.CharField(max_length=100)
    num_of_reuse = models.CharField(max_length=100, )
    serial_batch_control = models.CharField(max_length=100, )
    reusable_rate = models.CharField(max_length=100)
    min_quantity = models.CharField(max_length=100)
    max_quantity = models.CharField(max_length=100)
    re_order_level = models.CharField(max_length=100)
    status = models.CharField(max_length=100,blank=True)
    assets = models.CharField(max_length=100,blank=True)
    expiry = models.CharField(max_length=100)
    create_by= models.DateField(null=True,blank=True)
    updated_by= models.DateField(null=True,blank=True)
    is_reusable=models.CharField(max_length=100)
    tpa=models.CharField(max_length=100)
    service_charge=models.CharField(max_length=100)
    autointent=models.CharField(max_length=100)

    def __str__(self):
        return self.item_name

class StoreMaster(models.Model):
    STORE_TYPE=(
    ('0','CPC'),
    ('1','MainStore'),
    ('2','SubStore')
    )
    store_name = models.CharField(max_length=100, )
    parent_store = models.CharField(max_length=100)
    wing = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    location_id = models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    department_id=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    store_type = models.CharField(max_length=100,choices=STORE_TYPE)
    inactive = models.BooleanField()

    def __str__(self):
        return self.store_name

class PurchaseOrder_Temp(models.Model):
    item_ID=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    unit_id=models.CharField(max_length=50)
    vendor_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE,blank=True,null=True)
    location_id = models.ForeignKey(LocationMaster,on_delete=models.CASCADE,blank=True,null=True)
    free_qty=models.CharField(max_length=50,blank=True,null=True)
    stock_qty=models.IntegerField()
    rate=models.CharField(max_length=50)
    selling_rate=models.CharField(max_length=50,blank=True,null=True)
    schema=models.CharField(max_length=100,blank=True,null=True)
    discount=models.CharField(max_length=50,blank=True,null=True)
    discount_amt=models.CharField(max_length=500,blank=True,null=True)
    amount=models.CharField(max_length=50)
    tax_details=models.CharField(max_length=500)
    status=models.CharField(max_length=500)

class PurchaseOrder_Parent(models.Model):
    PO_id=models.CharField(max_length=50)
    PO_datetime=models.DateField()
    vendar_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE)
    Department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    Location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    po_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='po_location_name')
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,blank=True,null=True)
    net_amount=models.CharField(max_length=50)
    basic_amt=models.CharField(max_length=50)
    PO_status=models.CharField(max_length=50)
    purpose=models.CharField(max_length=50,blank=True,null=True)
    deliver_date=models.DateField(blank=True,null=True)
    approval_status=models.CharField(max_length=50)
    issue_status=models.CharField(max_length=50)
    delete_status=models.CharField(max_length=50,blank=True,null=True,default='active')

class PurchaseOrder_Child(models.Model):
    PO_Id=models.CharField(max_length=50)
    PO_datetime=models.DateField()
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    qty=models.IntegerField()
    unit_id=models.CharField(max_length=50)
    free_qty=models.CharField(max_length=50,blank=True,null=True)
    stocy_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    selling_rate=models.CharField(max_length=50,blank=True,null=True)
    schema=models.CharField(max_length=50,blank=True,null=True)
    discount=models.CharField(max_length=50,blank=True,null=True)
    discount_amt=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=50)
    tex_details=models.CharField(max_length=500)
    received_qty=models.IntegerField()
    issued_qty=models.IntegerField()
    status=models.CharField(max_length=50)
    issue_status=models.CharField(max_length=50)
    approval_status=models.CharField(max_length=50)
    assets=models.CharField(max_length=50)
    delete_status=models.CharField(max_length=50,blank=True,null=True,default='active')

class StockEntry_Parent(models.Model):
    GRN_id=models.CharField(max_length=50)
    GRN_datetime=models.DateField()
    PO_id=models.CharField(max_length=50)
    PO_datetime=models.CharField(max_length=50)
    invoice_no=models.CharField(max_length=50)
    invoice_upload = models.FileField(upload_to='uploads/',blank=True,null=True)
    vendar_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE,blank=True,null=True)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    po_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='se_location_name')
    basic_amount=models.CharField(max_length=50)
    GRN_amount=models.CharField(max_length=50)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    net_amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    paid_amount=models.CharField(max_length=50)
    Payment_status=models.CharField(max_length=50)

class StockEntry_Child(models.Model):
    GRN_id=models.CharField(max_length=50)
    GRN_datetime=models.DateTimeField()
    PO_id=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    item_qty=models.CharField(max_length=50)
    serial_batch=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    expiry_date=models.DateField()
    physical_qty=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    free_qty=models.CharField(max_length=50,blank=True,null=True)
    stock_qty=models.CharField(max_length=50)
    schema=models.CharField(max_length=50,blank=True,null=True)
    discount=models.CharField(max_length=50,blank=True,null=True)
    discount_amt=models.CharField(max_length=50,blank=True,null=True)
    tax_details=models.CharField(max_length=500)
    remark=models.CharField(max_length=500,blank=True,null=True)
    status=models.CharField(max_length=50,blank=True,null=True)
    movement_status=models.CharField(max_length=50)
    issue_qty=models.IntegerField(default=0,blank=True,null=True)

class StockEntry_Temp(models.Model):
    PO_id=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    serial_batch=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    expiry_date=models.DateField()
    physical_qty=models.CharField(max_length=50)
    free_qty=models.CharField(max_length=50,blank=True,null=True)
    stock_qty=models.CharField(max_length=50)
    schema=models.CharField(max_length=50,blank=True,null=True)
    discount=models.CharField(max_length=50,blank=True,null=True)
    discount_amt=models.CharField(max_length=50,blank=True,null=True)
    tax_details=models.CharField(max_length=500)
    remark=models.CharField(max_length=500,blank=True,null=True)
    status=models.CharField(max_length=50,blank=True,null=True)

class Stock_BatchWise(models.Model):
    GRN_id=models.CharField(max_length=50)
    GRN_datetime=models.DateField()
    PO_id=models.CharField(max_length=50)
    PO_datetime=models.DateField(blank=True,null=True)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    batch_no=models.CharField(max_length=50)
    expiry_date=models.DateField()
    received_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    vendar_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE,blank=True,null=True)
    department_id=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    po_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='stb_location_name')
    available_qty=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    adjust_qty=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    total_consume_qty=models.CharField(max_length=50)


class Vendor_Payment(models.Model):
    vendor_payment_no=models.CharField(max_length=50)
    payment_datetime=models.DateField()
    invoice_no=models.CharField(max_length=50)
    grn_no=models.CharField(max_length=50)
    grn_datetime=models.CharField(max_length=50,blank=True,null=True)
    po_no=models.CharField(max_length=50,blank=True,null=True)
    po_datetime=models.CharField(max_length=50,blank=True,null=True)
    vendor_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    department_id=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    po_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='vp_location_name')
    grn_amount=models.CharField(max_length=50)
    paid_amount=models.CharField(max_length=50,blank=True,null=True)
    status=models.CharField(max_length=50,blank=True,null=True)

class Material_Intent_Parent(models.Model):
    intent_id=models.CharField(max_length=50)
    intent_datetime=models.DateField()
    substore_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='material_indent_store')
    main_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    total_amount=models.CharField(max_length=50)
    p_status=models.CharField(max_length=50)
    approval_status = models.CharField(max_length=50)

class Material_Intent_Child(models.Model):
    intent_id=models.CharField(max_length=50)
    intent_datetime=models.DateField()
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    received_qty=models.CharField(max_length=50)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE,blank=True,null=True)
    item_code=models.CharField(max_length=50)
    item_belongs_to=models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)


class Material_Intent_Temp(models.Model):
    intent_id=models.CharField(max_length=50)
    intent_datetime=models.DateField()
    substore_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='material_temp_store')
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    main_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    item_code=models.CharField(max_length=50)
    item_belongs_to=models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50,blank=True,null=True)

class Item_Issue_Temp(models.Model):
    intent_no=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    priority=models.CharField(max_length=50)
    barcode=models.CharField(max_length=50,blank=True,null=True)
    serial_batch=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    available_qty=models.CharField(max_length=50)
    issued_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    intent_qty=models.CharField(max_length=50)
    remaining_qty=models.CharField(max_length=50)
    remark=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=50)

class Item_Issue_Parent(models.Model):
    item_issue_no=models.CharField(max_length=50)
    intent_no=models.CharField(max_length=50)
    item_issue_date=models.DateTimeField()
    issued_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='material_indent_store1')
    received_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    issue_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='issue_location')
    receive_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='receive_location')
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    approved_by=models.CharField(max_length=50)
    total_amount=models.CharField(max_length=50)
    transfer_status=models.CharField(max_length=50,blank=True,null=True)
    p_status=models.CharField(max_length=50)

class Item_Transfer_Issue_Temp(models.Model):
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    barcode=models.CharField(max_length=50,blank=True,null=True)
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    available_qty=models.CharField(max_length=50)
    issued_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    remark=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=50)

class Item_Issue_Child(models.Model):
    item_issue_no=models.CharField(max_length=50)
    intent_no=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    item_issue_date=models.DateTimeField()
    barcode=models.CharField(max_length=50,blank=True,null=True)
    serial_batch=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    available_qty=models.CharField(max_length=50)
    issued_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    intent_qty=models.CharField(max_length=50)
    total_amount=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    remark=models.CharField(max_length=50,blank=True,null=True)
    priority=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    transfer_status=models.CharField(max_length=50,blank=True,null=True)
    movement_status=models.CharField(max_length=50,blank=True,null=True)


class Item_Return_Parent(models.Model):
    item_return_no=models.CharField(max_length=50)
    return_date=models.DateTimeField()
    return_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='item_return_store')
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    receiving_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)

class Item_return_Child(models.Model):
    item_return_no=models.CharField(max_length=50)
    return_date=models.DateTimeField()
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    return_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    movable_status=models.CharField(max_length=50,blank=True,null=True)

class Item_Return_Supplier_Parent(models.Model):
    supplier_return_no=models.CharField(max_length=50)
    return_date=models.DateField()
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    vendor_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)

class Item_Return_Supplier_Child(models.Model):
    supplier_return_no=models.CharField(max_length=50)
    return_date=models.DateField()
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    return_qty=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    return_amount=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    movement_status=models.CharField(max_length=50,blank=True,null=True)


class MakeItem_return_Temp(models.Model):
    date=models.DateField()
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    total_qty=models.CharField(max_length=50)
    batch_no=models.CharField(max_length=50,blank=True,null=True)
    expiry_date=models.CharField(max_length=50,blank=True,null=True)
    rate=models.CharField(max_length=50,blank=True,null=True)
    total_amt=models.CharField(max_length=50)
    status=models.CharField(max_length=50)


class Item_Status_Report_Temp(models.Model):
    item=models.CharField(max_length=50)
    date=models.DateTimeField()
    particular=models.CharField(max_length=50,blank=True,null=True)
    opening_balance=models.CharField(max_length=50)
    transaction=models.CharField(max_length=50)
    closing_qty=models.CharField(max_length=50)

class Item_Status_Particular_Temp(models.Model):
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    date=models.DateTimeField()
    particular=models.CharField(max_length=50,blank=True,null=True)
    opening_balance=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    transaction_cost = models.CharField(max_length=50)
    purchase_qty=models.CharField(max_length=50)
    issue_qty=models.CharField(max_length=50)
    return_qty=models.CharField(max_length=50)
    closing_cost=models.CharField(max_length=50)
    closing_balance=models.CharField(max_length=50)

class StockLegder_Temp(models.Model):
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    date=models.DateTimeField()
    particular=models.CharField(max_length=50,blank=True,null=True)
    opening_balance=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50,blank=True,null=True)
    transaction_cost = models.CharField(max_length=50,blank=True,null=True)
    purchase_qty=models.CharField(max_length=50)
    issue_qty=models.CharField(max_length=50)
    return_qty=models.CharField(max_length=50)
    closing_cost=models.CharField(max_length=50,blank=True,null=True)
    closing_balance=models.CharField(max_length=50)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE,blank=True,null=True)
    vendor_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE,blank=True,null=True)
    purchase_rate=models.CharField(max_length=50,blank=True,null=True)

class Purchase_Intent_Parent(models.Model):
    intent_id=models.CharField(max_length=50)
    intent_datetime=models.DateField()
    cpc_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='purchase_indent_store')
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    main_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    total_amount=models.CharField(max_length=50)
    p_status=models.CharField(max_length=50)
    approval_status=models.CharField(max_length=50)

class Purchase_Intent_Child(models.Model):
    intent_id=models.CharField(max_length=50)
    intent_datetime=models.DateField()
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    item_code=models.CharField(max_length=50)
    item_belongs_to=models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    approval_status=models.CharField(max_length=50)


class Purchase_Intent_Temp(models.Model):
    intent_id=models.CharField(max_length=50)
    intent_datetime=models.DateField()
    cpc_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='purchase_temp_store')
    main_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    item_code=models.CharField(max_length=50)
    item_belongs_to=models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50,blank=True,null=True)

class Makepo_PI_Temp(models.Model):
    datetime=models.DateField()
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    unit_id=models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    stock_qty = models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    total_amount=models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class Manual_Stock_Adjustment(models.Model):
    adjustment_id=models.CharField(max_length=50)
    adjustment_date=models.DateTimeField()
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    available_qty=models.CharField(max_length=50)
    adjust_qty=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    remark=models.CharField(max_length=50)

class Transfer_Intent_Parent(models.Model):
    trnasfer_indent_no=models.CharField(max_length=50)
    intent_date=models.DateField()
    cpc_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='trnasfer_indent_store')
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    main_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    total_amount=models.CharField(max_length=50)
    p_status=models.CharField(max_length=50)
    approval_status=models.CharField(max_length=50)

class Transfer_Intent_Child(models.Model):
    trnasfer_indent_no=models.CharField(max_length=50)
    intent_date=models.DateField()
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    item_code=models.CharField(max_length=50)
    item_belongs_to=models.CharField(max_length=50)
    received_qty = models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    approval_status=models.CharField(max_length=50)

class Transfer_Intent_Temp(models.Model):
    trnasfer_indent_no=models.CharField(max_length=50)
    intent_date=models.DateField()
    cpc_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='trnasfer_temp_store')
    main_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    item_code=models.CharField(max_length=50)
    item_belongs_to=models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50,blank=True,null=True)

class Transfer_Request_Mainstore_Parent(models.Model):
    request_no = models.CharField(max_length=50)
    request_date = models.DateField()
    transfer_indent_no=models.CharField(max_length=50)
    transfer_return_no=models.CharField(max_length=50)
    item_issue_no = ListCharField(base_field=models.CharField(max_length=100), size=10, max_length=(10 * 101),blank=True,null=True)
    intent_date= models.CharField(max_length=50)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    indent_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    request_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='transfer_request_store')
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    receive_status=models.CharField(max_length=50)

class Transfer_Request_Mainstore_Child(models.Model):
    request_no=models.CharField(max_length=50)
    request_date=models.DateField()
    priority=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    issued_qty = models.CharField(max_length=50)
    remark=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    receive_status=models.CharField(max_length=50)


class PS_CounterSale_Parent(models.Model):
    Op_sales_no=models.CharField(max_length=50)
    sales_date=models.DateTimeField()
    uhid=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50)
    patient_name=models.CharField(max_length=50)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,blank=True,null=True)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,blank=True,null=True)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE,blank=True,null=True)
    consultant_type=models.CharField(max_length=50,blank=True,null=True)
    consultant_name=models.CharField(max_length=50,blank=True,null=True)
    mobile=models.CharField(max_length=50)
    age=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    panel=models.CharField(max_length=50,blank=True,null=True)
    type=models.CharField(max_length=50,blank=True,null=True)
    patient_type=models.CharField(max_length=50,blank=True,null=True)
    opd_no=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    total_taxable_amount=models.CharField(max_length=50)
    p_status=models.CharField(max_length=50)
    paid_amount=models.IntegerField(default=0)
    reason=models.CharField(max_length=50,blank=True,null=True)
    bill_status=models.CharField(max_length=50,blank=True,null=True)
    return_status=models.CharField(max_length=50,blank=True,null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class PS_CounterSale_child(models.Model):
    Op_sales_no=models.CharField(max_length=50)
    sales_date=models.DateTimeField()
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    generic_id=models.ForeignKey(Generic_Master,on_delete=models.CASCADE,null=True,blank=True)
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    mrp=models.CharField(max_length=50,blank=True,null=True)
    qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    before_disc_amount=models.CharField(max_length=50)
    discount=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50,blank=True,null=True)
    total_cost=models.CharField(max_length=50,blank=True,null=True)
    opening_cost=models.CharField(max_length=50,blank=True,null=True)
    status=models.CharField(max_length=50)
    moment_status=models.CharField(max_length=50)
    reason=models.CharField(max_length=50,blank=True,null=True)
    grn_consume_hand_qty = models.CharField(max_length=50)
    bill_status=models.CharField(max_length=50,blank=True,null=True)
    return_status=models.CharField(max_length=50,blank=True,null=True)
    return_qty=models.CharField(max_length=50,blank=True,null=True,default=0)
    return_amount=models.CharField(max_length=50,blank=True,null=True,default=0)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    #=========================== 02/08/2023 ===========================
    order_id=models.CharField(max_length=50)


class PS_Sales_Payement_Detail(models.Model):
    op_sale_no=models.CharField(max_length=50,null=True,blank=True)
    sale_date=models.DateTimeField()
    mode_type=models.CharField(max_length=30)
    bill_amt=models.FloatField(blank=True,null=True)
    paid_amount=models.FloatField(blank=True,null=True)
    pending_amount=models.FloatField(blank=True,null=True)
    bank_no=models.CharField(max_length=100,blank=True,null=True)
    card_no=models.CharField(max_length=100,blank=True,null=True)
    paid_by=models.CharField(max_length=100,blank=True,null=True)
    ref_number=models.CharField(max_length=100,blank=True,null=True)
    mobile_nummber=models.CharField(max_length=100,blank=True,null=True)
    card_holder_name=models.CharField(max_length=100,blank=True,null=True)
    date_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status=models.CharField(max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class PS_CounterSale_Temp(models.Model):
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    uhid=models.CharField(max_length=50,blank=True,null=True)
    visit_id=models.CharField(max_length=50,blank=True,null=True)
    generic_id=models.ForeignKey(Generic_Master,on_delete=models.CASCADE,null=True,blank=True)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,blank=True,null=True)
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    mrp=models.CharField(max_length=50,blank=True,null=True)
    qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    before_disc_amount=models.CharField(max_length=50)
    discount=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    moment_status=models.CharField(max_length=50)
    reason=models.CharField(max_length=50,blank=True,null=True)

class PS_CounterSale_Temp_OTC(models.Model):
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    generic_id=models.ForeignKey(Generic_Master,on_delete=models.CASCADE,null=True,blank=True)
    batch_no=models.CharField(max_length=50)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,blank=True,null=True)
    mob_no=models.CharField(max_length=50,blank=True,null=True)
    expiry_date=models.CharField(max_length=50)
    mrp=models.CharField(max_length=50,blank=True,null=True)
    qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    before_disc_amount=models.CharField(max_length=50)
    discount=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    moment_status=models.CharField(max_length=50)
    reason=models.CharField(max_length=50,blank=True,null=True)

class PS_sales_return_Child(models.Model):
    sales_return_id = models.CharField(max_length=50)
    sales_return_date = models.DateTimeField()
    sales_no = models.CharField(max_length=50,blank=True,null=True)
    item_id = models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    batch_no=models.CharField(max_length=50,blank=True,null=True)
    expiry_date=models.CharField(max_length=50,blank=True,null=True)
    sale_qty = models.CharField(max_length=50)
    return_qty = models.CharField(max_length=50)
    sale_amount = models.CharField(max_length=50)
    return_amount = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    discount = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class PS_sales_return_Parent(models.Model):
    sales_no = models.CharField(max_length=50)
    sales_return_id = models.CharField(max_length=50)
    sales_date = models.CharField(max_length=50)
    sales_return_date = models.DateTimeField()
    uhid=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50,blank=True,null=True)
    reason = models.CharField(max_length=50,blank=True,null=True)
    total_amount= models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class PS_sales_return(models.Model):
    sales_no = models.CharField(max_length=50)
    sales_return_id = models.CharField(max_length=50)
    sales_date = models.CharField(max_length=50)
    sales_return_date = models.DateTimeField()
    item_id = models.CharField(max_length=50)
    sale_qty = models.CharField(max_length=50)
    return_qty = models.CharField(max_length=50)
    sale_amount = models.CharField(max_length=50)
    return_amount = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    discount = models.CharField(max_length=50)
    reason = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class Department_Consumption(models.Model):
    consumption_No =models.CharField(max_length=50)
    consumption_date =models.DateTimeField(auto_now_add=True)
    batch_no =models.CharField(max_length=50)
    item_id =models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    expiry_date =models.CharField(max_length=50)
    store_id =models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    consumption_qty =models.CharField(max_length=50)
    inhand_qty =models.CharField(max_length=50)
    rate =models.CharField(max_length=50)
    total_amount =models.CharField(max_length=50)
    remark =models.CharField(max_length=500)
    status =models.CharField(max_length=50)
    total_qty = models.CharField(max_length=50)
    opening_balance = models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50,blank=True,null=True)
    total_cost=models.CharField(max_length=50,blank=True,null=True)
    opening_cost=models.CharField(max_length=50,blank=True,null=True)
    grn_consume_hand_qty =models.CharField(max_length=50)
    movement_status=models.CharField(max_length=50,null=True,blank=True,default='Consume Entry')

class Detailed_ItemStatus_Temp(models.Model):
    item_id = models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    date_time =models.DateTimeField()
    opening_balance = models.CharField(max_length=50)
    opening_cost = models.CharField(max_length=50)
    transaction_cost = models.CharField(max_length=50)
    closing_balance = models.CharField(max_length=50)
    closing_cost = models.CharField(max_length=50)
    purchase_qty = models.CharField(max_length=50)
    consume_qty = models.CharField(max_length=50)
    in_hand_qty = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


#============================ For Clinical Management temp table Start 27/03/2023 ===================================
class PresentingComplaintTemp(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    visit_date = models.DateField(auto_now_add=True, null=True, blank=True)
    presenting_comp=models.CharField(max_length=50)
    initial_comp=models.TextField()

class PresentingComplaintSub(models.Model):
    main_id=models.ForeignKey(PresentingComplaint,on_delete=models.CASCADE)
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    visit_date = models.DateField(auto_now_add=True, null=True, blank=True)
    presenting_comp=models.CharField(max_length=50)
    initial_comp=models.TextField()

class DiagnosisTemp(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50,null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    diagnosis=models.CharField(max_length=50,null=True, blank=True)
    D_GRG_Code=models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

class DiagnosisSub(models.Model):
    main_id=models.ForeignKey(Diagnosis,on_delete=models.CASCADE)
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    diagnosis=models.CharField(max_length=50,null=True, blank=True)
    D_GRG_Code=models.CharField(max_length=100,null=True, blank=True)
    visit_date=models.DateField(auto_now_add=True)

class InvestigationProcedureTemp(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    investigation_and_procedure=models.CharField(max_length=200)
    status=models.BooleanField()
    result_status=models.CharField(max_length=50,blank=True,null=True)
    ot_required=models.CharField(max_length=50,blank=True,null=True)

class InvestigationProcedureSub(models.Model):
    main_id=models.ForeignKey(Diagnosis,on_delete=models.CASCADE)
    uhid = models.CharField(max_length=50, null=True, blank=True)
    bill_id = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    investigation_and_procedure=models.CharField(max_length=200)
    status=models.BooleanField()
    result_status=models.CharField(max_length=50,blank=True,null=True)
    ot_required=models.CharField(max_length=50,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

#  karan


#  RIS
class RIS_PendingInvestigation_main(models.Model):
    bill_no=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100)
    uhid=models.ForeignKey("testapp.PatientsRegistrationsAllInOne",on_delete=models.CASCADE)
    visit_no=models.CharField(max_length=100)
    service=models.ForeignKey('testapp.ServiceMaster',on_delete=models.CASCADE)
    status=models.CharField(max_length=100,default='active')
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class RIS_Report(models.Model):
    RIS_PendingInvestigation=models.ForeignKey("testapp.RIS_PendingInvestigation_main",on_delete=models.CASCADE)
    discerption=models.TextField()
    conclusion=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class RadiologyTemplateMaster(models.Model):
    service=models.ForeignKey('testapp.ServiceMaster',on_delete=models.CASCADE)
    content=models.TextField()
    status=models.CharField(max_length=100)

class LabTemplateMaster(models.Model):
    profile=models.ForeignKey('testapp.ProfileMaster',on_delete=models.CASCADE)
    profile_name=models.CharField(max_length=100)
    content=models.TextField()
    status=models.CharField(max_length=100)


class PrescriptionDialysis(models.Model):
  #==== 47 fields ============================
    uhid = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    dr_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    drid=models.CharField(max_length=100, null=True, blank=True)
    prescription_date=models.CharField(max_length=100, null=True, blank=True)
    status=models.CharField(max_length=100,null=True, blank=True)
    s_date=models.CharField(max_length=100,null=True, blank=True)
    e_date=models.CharField(max_length=100,null=True, blank=True)
    dry_weight=models.CharField(max_length=100,null=True, blank=True)
    dry_weight_date=models.CharField(max_length=100,null=True, blank=True)
    diagnosis=models.CharField(max_length=100,null=True, blank=True)
    day1=models.CharField(max_length=100,null=True, blank=True)
    shift1=models.CharField(max_length=100,null=True, blank=True)
    duration=models.CharField(max_length=100,null=True,blank=True)
    day2=models.CharField(max_length=100,null=True,blank=True)
    weekly=models.CharField(max_length=100,null=True,blank=True)
    shift2=models.CharField(max_length=100,null=True,blank=True)
    day3=models.CharField(max_length=100,null=True,blank=True)
    shift3=models.CharField(max_length=100,null=True,blank=True)
    dialysis_membrane=models.CharField(max_length=100,null=True,blank=True)
    day4=models.CharField(max_length=100,null=True,blank=True)
    shift4 =models.CharField(max_length=100,null=True,blank=True)
    day5=models.CharField(max_length=100,null=True,blank=True)
    shift5=models.CharField(max_length=100,null=True,blank=True)
    dialysis_type=models.ForeignKey(Dialysate_Type,on_delete=models.CASCADE)
    dialyzer=models.ForeignKey(Dialyzer,on_delete=models.CASCADE)
    dialysate_temp=models.CharField(max_length=100,null=True,blank=True)
    k_meql=models.CharField(max_length=100,null=True,blank=True)
    ca_meal=models.CharField(max_length=100,null=True,blank=True)
    mg_meal=models.CharField(max_length=100,null=True,blank=True)
    glucose=models.CharField(max_length=100,null=True,blank=True)
    target_bvp=models.CharField(max_length=100,null=True,blank=True)
    dialysate_flow=models.CharField(max_length=100,null=True,blank=True)
    profile1=models.CharField(max_length=100,null=True,blank=True)
    blood_flow=models.CharField(max_length=100,null=True,blank=True)
    profile2=models.CharField(max_length=100,null=True,blank=True)
    bicarb=models.CharField(max_length=100,null=True,blank=True)
    profile3=models.CharField(max_length=100,null=True,blank=True)
    na_meql=models.CharField(max_length=100,null=True,blank=True)
    profile4=models.CharField(max_length=100,null=True,blank=True)
    uf_rate=models.CharField(max_length=100,null=True,blank=True)
    ufr_profile=models.CharField(max_length=100,null=True,blank=True)
    heparin_type=models.ForeignKey(Heparin_Type,on_delete=models.CASCADE,null=True,blank=True)
    initial_dose=models.CharField(max_length=100,null=True,blank=True)
    interim_dose=models.CharField(max_length=100,null=True,blank=True)
    total_heparin_bolus=models.CharField(max_length=100,null=True,blank=True)
    hourly=models.CharField(max_length=100,null=True,blank=True)
    cut_off_time=models.CharField(max_length=100,null=True,blank=True)
    heparin_profile=models.CharField(max_length=100,null=True,blank=True)
    comments=models.CharField(max_length=500,null=True,blank=True)
    notes=models.CharField(max_length=500,null=True,blank=True)

    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)



class Item_Issue_ToSubStore_Parent(models.Model):
    item_issue_no=models.CharField(max_length=50)
    intent_no=models.CharField(max_length=50)
    item_issue_date=models.DateTimeField()
    issued_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='issued_store1')
    received_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    issue_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='issue_location1')
    receive_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='receive_location1')
    department=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    approved_by=models.CharField(max_length=50)
    total_amount=models.CharField(max_length=50)
    p_status=models.CharField(max_length=50)

class Item_Issue_ToSubStore_Child(models.Model):
    item_issue_no=models.CharField(max_length=50)
    intent_no=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    issued_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    item_issue_date=models.DateTimeField()
    barcode=models.CharField(max_length=50,blank=True,null=True)
    serial_batch=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    available_qty=models.CharField(max_length=50)
    issued_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    purchase_rate=models.CharField(max_length=50,blank=True,null=True)
    intent_qty=models.CharField(max_length=50)
    total_amount=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    remark=models.CharField(max_length=50,blank=True,null=True)
    priority=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    movement_status=models.CharField(max_length=50,blank=True,null=True)

class Stock_BatchWise_Mainstore(models.Model):
    item_issue_no=models.CharField(max_length=50)
    item_issue_date=models.DateTimeField()
    intent_no=models.CharField(max_length=50)
    indent_date=models.CharField(max_length=50,blank=True,null=True)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    received_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    vendor_id=models.ForeignKey(VendorMaster,on_delete=models.CASCADE,blank=True,null=True)
    department_id=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    receive_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='stbm_location_name')
    available_qty=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    adjust_qty=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    total_consume_qty=models.CharField(max_length=50)
    transfer_status=models.CharField(max_length=50,blank=True,null=True)

class Stock_BatchWise_Substore(models.Model):
    item_issue_no=models.CharField(max_length=50)
    item_issue_date=models.DateTimeField()
    intent_no=models.CharField(max_length=50)
    indent_date=models.CharField(max_length=50,blank=True,null=True)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    serial_batch=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    received_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    purchase_rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    store_id=models.ForeignKey(StoreMaster,on_delete=models.CASCADE)
    department_id=models.ForeignKey(ServiceDepartment,on_delete=models.CASCADE)
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    receive_location=models.ForeignKey(LocationMaster,on_delete=models.CASCADE,related_name='Stock_BatchWise_Substore_location_name')
    available_qty=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    adjust_qty=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    total_consume_qty=models.CharField(max_length=50)

class MakeItem_return_ToCPC_Temp(models.Model):
    date=models.DateField()
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    batch_no=models.CharField(max_length=50,blank=True,null=True)
    total_qty=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50,blank=True,null=True)
    rate=models.CharField(max_length=50,blank=True,null=True)
    total_amt=models.CharField(max_length=50)
    status=models.CharField(max_length=50)

class Item_Return_ToCPC_Child(models.Model):
    return_no=models.CharField(max_length=50)
    return_date=models.DateTimeField()
    batch_no=models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    item_id=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE)
    return_qty=models.CharField(max_length=50)
    rate=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    total_qty=models.CharField(max_length=50)
    opening_balance=models.CharField(max_length=50)
    transaction_cost=models.CharField(max_length=50)
    total_cost=models.CharField(max_length=50)
    opening_cost=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    stock_transfer=models.CharField(max_length=50)
    movable_status=models.CharField(max_length=50,blank=True,null=True)

class Item_Return_ToCPC_Parent(models.Model):
    return_no=models.CharField(max_length=50)
    return_date=models.DateTimeField()
    return_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='item_return_cpc_store')
    location_id=models.ForeignKey(LocationMaster,on_delete=models.CASCADE)
    receiving_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='item_return_receive_store')
    indent_store=models.ForeignKey(StoreMaster,on_delete=models.CASCADE,related_name='indent_store',blank=True,null=True)
    request_no=models.CharField(max_length=50,blank=True,null=True)
    stock_transfer=models.CharField(max_length=50)
    status=models.CharField(max_length=50)

class Patient_Feedback(models.Model):
    feedback_id = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    uhid = models.CharField(max_length=50)
    visit_id = models.CharField(max_length=50,blank=True,null=True)
    facility = models.CharField(max_length=50)
    state_on_condition = models.CharField(max_length=50)
    doctor_knowledge = models.CharField(max_length=50)
    doctor_kindness = models.CharField(max_length=50)
    nurse_patience = models.CharField(max_length=50)
    nurse_knowledge = models.CharField(max_length=50)
    waiting_time = models.CharField(max_length=50)
    hygiene = models.CharField(max_length=50)
    improve_service = models.CharField(max_length=255)

class Permanent_Access_Master(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500,blank=True)
    def __str__(self):
        return self.name

#========================== For Dialysis Precriptions 04/04/2023 ========================================
class Temp_Access(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    temp_aces=models.CharField(max_length=500)
    date_initiation=models.CharField(max_length=500)
    doctor_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    access_site=models.ForeignKey(Access_site,on_delete=models.CASCADE)
    date_removal=models.CharField(max_length=500)
    remark=models.CharField(max_length=500)
    hospital_name=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)

class Permanent_Access(models.Model):
    uhid = models.CharField(max_length=50, null=True, blank=True)
    visit_id = models.CharField(max_length=100, null=True, blank=True)
    prim_aces=models.ForeignKey(Permanent_Access_Master,on_delete=models.CASCADE)
    date_initiation=models.CharField(max_length=500)
    doctor_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE)
    access_site=models.ForeignKey(Access_site,on_delete=models.CASCADE)
    date_failure=models.CharField(max_length=500)
    remark=models.CharField(max_length=500)
    hospital_name=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)

class IntraDialysisPerHourInput(models.Model):
    uhid = models.CharField(max_length=50)
    visit_id = models.CharField(max_length=100)
    time=models.CharField(max_length=50)
    bp_mmhg1=models.CharField(max_length=50)
    bp_mmhg2=models.CharField(max_length=50)
    bp_time=models.CharField(max_length=50)
    pulse=models.CharField(max_length=50)
    total_uf_removal=models.CharField(max_length=50)
    uf_rate=models.CharField(max_length=50)
    blood_pump_flow_rate=models.CharField(max_length=50)
    heparine_pump_infusion_rate=models.CharField(max_length=50)
    dialysate_temp=models.CharField(max_length=50)
    conductivity=models.CharField(max_length=50)
    venus_pressure=models.CharField(max_length=50)
    dialysate_pressure=models.CharField(max_length=50)
    tmp=models.CharField(max_length=50)
    dialysis_time=models.CharField(max_length=50)
    dialysis_flow_rate=models.CharField(max_length=50)

#=================== for intra dialysis 07/06/2023 ==================
class PostEquip_preparationMaster(models.Model):
    post_equip_name = models.CharField(max_length=100)
    description=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.post_equip_name

# class PostEquip_preparation(models.Model):
#     uhid=models.CharField(max_length=50)
#     visit_id=models.CharField(max_length=50)
#     post_preparation=models.ManyToManyField('testapp.PostEquip_preparationMaster')

class PreDialysisAssessment(models.Model):
    uhid=models.CharField(max_length=100)
    visit_id=models.CharField(max_length=100)
    chest_auscultation_clear = models.BooleanField(default=False)
    peripheral_edema = models.BooleanField(default=False)
    pressure_limit_set = models.BooleanField(default=False)
    Physical_Chest_pain_discompfort = models.BooleanField(default=False)
    recent_surgery_injuries_trauma_bleeding = models.BooleanField(default=False)
    intra_dialysis = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
#===================== END =====================================

class PostEquip_preparation(models.Model):
    Post_Equipment=(
        ('1','Air Detector Armed'),
        ('2','Saline Clamped'),
        ('3','Pressure Limit Set'),
        ('4','Nurses Round'),
        ('5','Dialysate Counter Flow'),
    )
    uhid=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50)
    post_preparation=models.ManyToManyField('testapp.PostEquip_preparationMaster')
    # post_preparation=models.CharField(max_length=50,choices=Post_Equipment)

class IntraDialysis(models.Model):
    uhid=models.CharField(max_length=30)
    visit_id=models.CharField(max_length=30)
    status=models.CharField(max_length=30)
    completion_status=models.CharField(max_length=30)

class SessionNote(models.Model):
    uhid=models.CharField(max_length=50)
    visit_id=models.CharField(max_length=50)
    time=models.TimeField()
    plan=models.TextField()
    intervention=models.TextField()
    evalution=models.TextField()

class Refered_by_Master(models.Model):
    Staff_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500,blank=True)

class Relation(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

class AddDrugs_Dialysis(models.Model):
    uhid=models.CharField(max_length=100)
    visit_id=models.CharField(max_length=100)
    medicine_name=models.CharField(max_length=200)
    rout=models.CharField(max_length=200,blank=True,null=True)
    dosage_pr_adm=models.CharField(max_length=200)
    remark=models.CharField(max_length=200,blank=True,null=True)
    batch_no=models.CharField(max_length=200,blank=True,null=True)
    expiry_date=models.CharField(max_length=200,blank=True,null=True)
    quantity=models.CharField(max_length=200,blank=True,null=True)
    administered_by=models.CharField(max_length=200,blank=True,null=True)
    doctor=models.CharField(max_length=200,blank=True,null=True)
    date_time=models.DateTimeField(auto_now_add=True)
#====================== Post Dialysis Dishcharge Summery Form 10/05/2023 ================================
class PostDialysisDischargeSheet(models.Model):
    uhid=models.CharField(max_length=100)
    visit_id=models.CharField(max_length=100)
    cause_ESRD=models.CharField(max_length=100)
    d_of_d=models.CharField(max_length=100)
    cc=models.CharField(max_length=100)
    access=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    bp=models.CharField(max_length=100)
    kt_v=models.CharField(max_length=100)
    acc_qb=models.CharField(max_length=100)
    out_come=models.CharField(max_length=100)
    recommendant=models.CharField(max_length=100)
    tca=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    nephrologist=models.TextField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)

class DialysisDishchargeMedicine(models.Model):
    main_id=models.ForeignKey(PostDialysisDischargeSheet,on_delete=models.CASCADE)
    med_name=models.CharField(max_length=100,null=True,blank=True)
    dosage=models.CharField(max_length=100,null=True,blank=True)


class PostDialysisDishchargeMedicine(models.Model):
    main_id=models.ForeignKey(PostDialysisDischargeSheet,on_delete=models.CASCADE)
    post_med_name=models.ForeignKey(Inventory_ItemMaster,on_delete=models.CASCADE,null=True,blank=True)
    outs_ource_med_name=models.CharField(max_length=100,null=True,blank=True)

class DialysisPrescription(models.Model):
    main_id=models.ForeignKey(PostDialysisDischargeSheet,on_delete=models.CASCADE)
    namw1=models.CharField(max_length=100)
    name2=models.CharField(max_length=100)
#============================================== END ====================================
#================= For PreEquipPreparation in PreDialysis 15/05/2023=========================
class PreEquipPreparationMaster(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.name
class PreEquipPreparationPreDialysis(models.Model):
    uhid=models.CharField(max_length=100)
    visit_id=models.CharField(max_length=100)
    name=models.ManyToManyField('testapp.PreEquipPreparationMaster',blank=True)

#========================== For IPD Dialysis 03/08/2023 ===========================
class DialysisSchedule(models.Model):
    STATUS=(
    ('active','active'),
    ('inactive','inactive'),
    )
    uhid=models.CharField(max_length=100)
    schedule_id=models.CharField(max_length=100,unique=True)
    department=models.CharField(max_length=100)
    sub_dept=models.CharField(max_length=100)
    shifting_date=models.DateField()
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    status=models.CharField(max_length=100,choices=STATUS,default='active')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.schedule_id

class Doctor_Notes(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    date = models.DateTimeField()
    diagnosis = models.CharField(max_length=1000, blank=True,null=True)
    duration_on_dialysis = models.CharField(max_length=1000, blank=True,null=True)
    current_medications = models.CharField(max_length=1000, blank=True,null=True)
    general_status = models.CharField(max_length=500, blank=True,null=True)
    access_site = models.CharField(max_length=500, blank=True,null=True)
    bp = models.CharField(max_length=500, blank=True,null=True)
    QB_rate = models.CharField(max_length=500, blank=True,null=True)
    ultrafiltration = models.CharField(max_length=500, blank=True,null=True)
    investication = models.CharField(max_length=500, blank=True,null=True)
    plan = models.CharField(max_length=5000, blank=True,null=True)


class Pre_Procedural_Checklist(models.Model):
    reffering_doctor = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    age =models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    cause_kidney_disease = models.CharField(max_length=1000)
    Comorbidities = models.CharField(max_length=1000)
    type1 = models.CharField(max_length=1000)
    site = models.CharField(max_length=1000)
    duration_use = models.CharField(max_length=1000)
    others = models.CharField(max_length=1000)
    reason_last_accesss_failure = models.CharField(max_length=1000)
    current_intend_access = models.CharField(max_length=1000)
    reason_for_current_intended = models.CharField(max_length=1000)
    procedure_notes= models.CharField(max_length=1000)
    final_access_site = models.CharField(max_length=1000)
    surgeon_name = models.CharField(max_length=100)
    signature = models.CharField(max_length=100,blank=True,null=True)
    created_by = models.DateTimeField(auto_now_add = True)

class Refferal_Form(models.Model):
    reffering_doctor = models.CharField(max_length=100,blank=True,null=True)
    refferal_hospital = models.CharField(max_length=100,blank=True,null=True)
    patient_last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    duration_dialysis = models.CharField(max_length=100)
    cause_kidney = models.CharField(max_length=1000)
    comorbidities = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    current_medication = models.CharField(max_length=1000,blank=True,null=True)
    dosage = models.CharField(max_length=1000,blank=True,null=True)
    duration =models.CharField(max_length=1000,blank=True,null=True)
    others = models.CharField(max_length=1000,blank=True,null=True)
    procedural_notes = models.CharField(max_length=1000,blank=True,null=True)
    doctor_name = models.CharField(max_length=1000,blank=True,null=True)
    created_by = models.DateTimeField(auto_now_add=True)

class Consent_KidneyDialysis(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_address = models.CharField(max_length=600)
    age = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    admission_no = models.CharField(max_length=100)
    name1 = models.CharField(max_length=100)
    blood_sample = models.CharField(max_length=100,blank=True,null=True)
    PO_box_no =  models.CharField(max_length=100,blank=True,null=True)
    name2 = models.CharField(max_length=100)
    signature = models.CharField(max_length=100,blank=True,null=True)
    id_no = models.CharField(max_length=100,blank=True,null=True)
    next_kin = models.CharField(max_length=100,blank=True,null=True)
    mobile_no = models.CharField(max_length=100,blank=True,null=True)
    witnessed_admitted_nurse =  models.CharField(max_length=200,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    time = models.CharField(max_length=100,blank=True,null=True)
    created_by = models.DateTimeField(auto_now_add=True)

class Informed_Consent(models.Model):
    date =  models.CharField(max_length=100,blank=True,null=True)
    time = models.CharField(max_length=100,blank=True,null=True)
    mental_state = models.CharField(max_length=1000,blank=True,null=True)
    doctor_performing = models.CharField(max_length=1000,blank=True,null=True)
    description = models.CharField(max_length=2000,blank=True,null=True)
    explain_parent_patient = models.CharField(max_length=1000,blank=True,null=True)
    intened_benefits = models.CharField(max_length=1000,blank=True,null=True)
    serious_risk = models.CharField(max_length=1000,blank=True,null=True)
    extra_procedure = models.CharField(max_length=1000,blank=True,null=True)
    alternative_treatment = models.CharField(max_length=1000,blank=True,null=True)
    date2 =  models.CharField(max_length=100,blank=True,null=True)
    time2 = models.CharField(max_length=100,blank=True,null=True)
    mental_state2 = models.CharField(max_length=1000,blank=True,null=True)
    administering_sedation = models.CharField(max_length=1000,blank=True,null=True)
    mode_of_anasthesia = models.CharField(max_length=100,blank=True,null=True)
    doctor_name = models.CharField(max_length=100,blank=True,null=True)
    dr_explain_procedure = models.CharField(max_length=1000,blank=True,null=True)
    benefites_mode_anasthesia = models.CharField(max_length=1000,blank=True,null=True)
    alternative = models.CharField(max_length=100,blank=True,null=True)
    patient_qstn = models.CharField(max_length=100,blank=True,null=True)
    patient_explain = models.CharField(max_length=1000,blank=True,null=True)
    name_of_doctor = models.CharField(max_length=100,blank=True,null=True)
    doctor_signature = models.CharField(max_length=100,blank=True,null=True)
    date3 =  models.CharField(max_length=100,blank=True,null=True)
    time3 = models.CharField(max_length=100,blank=True,null=True)
    patient_accept_procedure = models.CharField(max_length=100,blank=True,null=True)
    patient_signature = models.CharField(max_length=100,blank=True,null=True)
    date4 =  models.CharField(max_length=100,blank=True,null=True)
    time4 = models.CharField(max_length=100,blank=True,null=True)
    patient_upderstand_procedure = models.CharField(max_length=100,blank=True,null=True)
    signature_self = models.CharField(max_length=100,blank=True,null=True)
    date5 =  models.CharField(max_length=100,blank=True,null=True)
    time5 = models.CharField(max_length=100,blank=True,null=True)
    signature_guardian = models.CharField(max_length=100,blank=True,null=True)
    date6 =  models.CharField(max_length=100,blank=True,null=True)
    time6 = models.CharField(max_length=100,blank=True,null=True)

class Incident_Type_Master(models.Model):
    incident_type=models.CharField(max_length=50)
    description=models.CharField(max_length=50)

    def __str__(self):
        return self.incident_type

class Contributing_Factors_Master(models.Model):
    contributing_factor=models.CharField(max_length=50)
    description=models.CharField(max_length=50)    

    def __str__(self):
        return self.contributing_factor

class Incident_Creation_Form(models.Model):
    incident_id=models.CharField(max_length=50)
    submitter_name=models.CharField(max_length=50)
    incident_reported_date=models.CharField(max_length=50)  
    incident_date=models.CharField(max_length=50)  
    incident_type=models.ForeignKey(Incident_Type_Master,on_delete=models.CASCADE,related_name='incident_creation')
    incident_location=models.CharField(max_length=50)
    affected_people=models.CharField(max_length=50)
    responsible_dept=models.CharField(max_length=50)
    incident_description=models.CharField(max_length=255)
    status=models.CharField(max_length=50)

    def __str__(self):
        return self.incident_id

class Investigation_Form(models.Model):
    investigation_id=models.CharField(max_length=50)
    incident_id=models.ForeignKey(Incident_Creation_Form,on_delete=models.CASCADE,related_name='inves_incident_no')
    investigation_date=models.DateField(max_length=50)
    supervisor_name=models.CharField(max_length=50)
    comments_by_supervisor=models.CharField(max_length=50)  
    comments_by_quality_manager=models.CharField(max_length=50)  
    risk_assessment_score=models.CharField(max_length=50)  
    contributing_factors=models.ForeignKey(Contributing_Factors_Master,on_delete=models.CASCADE,related_name='inves_contributing_factor')
    investigation_done_by=models.CharField(max_length=50)
    investigation_outcome=models.CharField(max_length=50)
    final_summary=models.CharField(max_length=255)

class PAPSMEAR(models.Model):
    uhid_id=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100)
    template=models.TextField()

#========================== For Bill Discount =============================
class AuthorizedPerson(models.Model):
    auth_name = models.CharField(max_length=100)
    department = models.ForeignKey(ClinicalOrDepartment,on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField( blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.auth_name

class OPDBillDiscountRemark(models.Model):
    authorised_by = models.ForeignKey(AuthorizedPerson, on_delete=models.CASCADE, related_name='authorised_discount_remarks')
    bill_no = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_discount_remarks')
    location = models.ForeignKey('testapp.LocationMaster', on_delete=models.CASCADE, null=True, blank=True)

class CancelBillRemark(models.Model):
    bill_no=models.ForeignKey(OpdBillingMain,on_delete=models.CASCADE,blank=True,null=True)
    reason=models.CharField(max_length=100,blank=False,null=False)
    comment=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,default='active')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    location=models.ForeignKey('testapp.LocationMaster',on_delete=models.CASCADE,null=True,blank=True)



    