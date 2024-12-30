from rest_framework import serializers
from testapp.models import *

class QmsSerializer(serializers.Serializer):
    doc_id=serializers.IntegerField()
    doc_name=serializers.CharField(max_length=10)
    speciality=serializers.CharField(max_length=200)
    status=serializers.CharField(max_length=100)
    room_no=serializers.IntegerField()
    max_token_assigned=serializers.IntegerField()
#Serializers of models
class DoctorTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorTable
        fields='__all__'
class BookedAppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookedAppointments
        fields='__all__'
class GroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupMaster
        fields='__all__'
    def validate_group_name(self,value):
        if len(value)<2:
            raise serializers.ValidationError('Sorry!!! Kindly Provide Valid Grout Name')
class BranchMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=BranchMaster
        fields='__all__'
class TitleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=TitleMaster
        fields='__all__'
class HospitalMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=HospitalMaster
        fields='__all__'
class HolidayMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=HolidayMaster
        fields='__all__'
class GenderMaterSerializer(serializers.ModelSerializer):
    class Meta:
        model=GenderMater
        fields='__all__'
class DistrictMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=DistrictMaster
        fields='__all__'
class CountryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CountryMaster
        fields='__all__'
class CityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CityMaster
        fields='__all__'
class MostCommonDocumentTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=MostCommonDocumentTypeMaster
        fields='__all__'
class MaritalStatusMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=MaritalStatusMaster
        fields='__all__'
class RelationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=RelationMaster
        fields='__all__'
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceCategory
        fields='__all__'
class ServiceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceSubCategory
        fields='__all__'
class ServiceDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceDepartment
        fields='__all__'
class ServiceSubDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceSubDepartment
        fields='__all__'
class ServiceMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceMaster
        fields='__all__'
class TariffMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=TariffMaster
        fields='__all__'
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Designation
        fields='__all__'
class CorporateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CorporateMaster
        fields='__all__'
class WardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=WardType
        fields='__all__'
class WardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=WardCategory
        fields='__all__'
class TariffChargeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=TariffChargeMaster
        fields='__all__'
class BillingGroupTariffLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillingGroupTariffLink
        fields='__all__'
#=================Scheduled Tables======================
class DoctorScheduleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorScheduleTable
        fields='__all__'
class AppointmentTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppointmentTable
        fields='__all__'
class PatientTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientTable
        fields='__all__'
class AddMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddMembers
        fields='__all__'
class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorSchedule
        fields='__all__'
class AvailableDayScheduleMasterTempSerializer(serializers.ModelSerializer):
    class Meta:
        model=AvailableDayScheduleMasterTemp
        fields='__all__'
class AvailabilityIntradayScheduleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=AvailabilityIntradayScheduleMaster
        fields='__all__'
class NameOfTheTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model=NameOfTheTitle
        fields='__all__'
class BloodMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=BloodMaster
        fields='__all__'
class NewAppointmentByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewAppointmentByAdmin
        fields='__all__'
class NewAppointmentByAdminChooseDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewAppointmentByAdminChooseDoctor
        fields='__all__'
class RoomNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoomNumber
        fields='__all__'
class TokenMasterConfSerializer(serializers.ModelSerializer):
    class Meta:
        model=TokenMasterConf
        fields='__all__'
class TokenCreationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=TokenCreations
        fields='__all__'
class TokenCreationDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=TokenCreationDone
        fields='__all__'
class CentralisedAdminViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=CentralisedAdminView
        fields='__all__'
from rest_framework.serializers import ModelSerializer
class TestCountrySerializer(ModelSerializer):
    pass

class PatienDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientsRegistrationsAllInOne
        fields=['uhid','title','first_name','middle_name','last_name','dob','age','gender','mobile_number']

class OpdBillingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpdBillingMain
        fields='__all__'
class DoctorAccountingSerilizer(serializers.ModelSerializer):
    class Meta:
        model=DoctorAccounting
        fields='__all__'

class OpdBillingSubSerializer(serializers.ModelSerializer):
    options = DoctorAccountingSerilizer(many=True, read_only=True)
    class Meta:
        model=OpdBillingSub
        fields='__all__'



