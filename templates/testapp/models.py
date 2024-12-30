from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class CustomeManager(models.Manager):
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
class DoctorTable(models.Model):
    today=timezone.now()
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
    doctor_id=models.IntegerField(primary_key=True)
    doctor_belogns_to=models.ForeignKey(BranchMaster,on_delete=models.CASCADE)
    doctor_email_address=models.EmailField(max_length=200)
    doctor_password=models.CharField(max_length=100)
    doctor_name=models.CharField(max_length=100)
    doctor_profile_image=models.ImageField(upload_to='images/')
    doctor_phone_no=models.BigIntegerField()
    doctor_appointment=models.DateField()
    doctor_address=models.CharField(max_length=500)
    doctor_date_of_birth=models.DateField()
    doctor_department=models.CharField(max_length=100)
    doctor_status=models.CharField(max_length=100,choices=status)
    doctor_registration_no=models.BigIntegerField()
    registration_exparing_date=models.DateField()
    doctor_register_by=models.CharField(max_length=200,choices=register_by)
    doctor_time_slot=models.IntegerField(choices=time_slot_lists)
    doctor_location=models.CharField(max_length=200)
    def __str__(self):
        return self.doctor_name
    objects=CustomeManager()
class DoctorScheduleTable(models.Model):
    today=timezone.now()
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
    schedule_time=(
    ('09:00','09:15'),
    ('21:00','21:00'),
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
    patient_id=models.CharField(max_length=200,primary_key=True)
    patient_name=models.CharField(max_length=200)
    patient_gender=models.CharField(max_length=200)
    patient_appointment_date=models.DateField()
    patient_appointment_id=models.CharField(max_length=200)
    patient_age=models.IntegerField()
    patient_mobile_number=models.BigIntegerField()
    patient_email_id=models.EmailField()
    patient_schedule_date_and_time=models.CharField(max_length=200)
    patient_scheduled_id=models.CharField(max_length=200)
    patient_payment_mode=models.CharField(max_length=200)
    doctor_name=models.CharField(max_length=200)
    doctor_department=models.CharField(max_length=200)
    def __str__(self):
        return '%s %s ' %(self.doctor_name,self.doctor_department)
class AddMembers(models.Model):
    reference_mobile_number=models.CharField(max_length=40)
    title_name=models.CharField(max_length=100)
    patient_name=models.CharField(max_length=100)
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
