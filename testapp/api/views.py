from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from testapp.models import *
from testapp.serializers import *
from rest_framework.response import Response
from django.template.response import TemplateResponse
class Doctor(ListCreateAPIView):
    queryset=DoctorTable.objects.all()
    serializer_class=DoctorTableSerializer
class DoctorRUD(RetrieveUpdateDestroyAPIView):
    queryset=DoctorTable.objects.all()
    serializer_class=DoctorTableSerializer
class AppointmentList(APIView):
    def get(self,request,format=None):
        # print(2/0)
        qs=BookedAppointments.objects.all()
        serializer=BookedAppointmentsSerializer(qs,many=True)
        #To Convert QS To Python Native DT
        return Response(serializer.data)
class GroupMasterLC(ListCreateAPIView):
    queryset=GroupMaster.objects.all()
    serializer_class=GroupMasterSerializer
class BranchMasterLC(ListCreateAPIView):
    queryset=BranchMaster.objects.all()
    serializer_class=BranchMasterSerializer
class TitleMasterLC(ListCreateAPIView):
    queryset=TitleMaster.objects.all()
    serializer_class=TitleMasterSerializer
class HospitalMasterLC(ListCreateAPIView):
    queryset=HospitalMaster.objects.all()
    serializer_class=HospitalMasterSerializer
class HolidayMasterLC(ListCreateAPIView):
    queryset=HolidayMaster.objects.all()
    serializer_class=HolidayMasterSerializer
class GenderMaterLC(ListCreateAPIView):
    queryset=GenderMater.objects.all()
    serializer_class=GenderMaterSerializer
class DistrictMasterLC(ListCreateAPIView):
    queryset=DistrictMaster.objects.all()
    serializer_class=DistrictMasterSerializer
class CountryMasterLC(ListCreateAPIView):
    queryset=CountryMaster.objects.all()
    serializer_class=CountryMasterSerializer
class CityMasterLC(ListCreateAPIView):
    queryset=CityMaster.objects.all()
    serializer_class=CityMasterSerializer
class MostCommonDocumentTypeMasterLC(ListCreateAPIView):
    queryset=MostCommonDocumentTypeMaster.objects.all()
    serializer_class=MostCommonDocumentTypeMasterSerializer
class MaritalStatusMasterLC(ListCreateAPIView):
    queryset=MaritalStatusMaster.objects.all()
    serializer_class=MaritalStatusMasterSerializer
class RelationMasterLC(ListCreateAPIView):
    queryset=RelationMaster.objects.all()
    serializer_class=RelationMasterSerializer
class ServiceCategoryLC(ListCreateAPIView):
    queryset=ServiceCategory.objects.all()
    serializer_class=ServiceCategorySerializer
class ServiceSubCategoryLC(ListCreateAPIView):
    queryset=ServiceSubCategory.objects.all()
    serializer_class=ServiceSubCategorySerializer
class ServiceDepartmentLC(ListCreateAPIView):
    queryset=ServiceDepartment.objects.all()
    serializer_class=ServiceDepartmentSerializer
class ServiceSubDepartmentLC(ListCreateAPIView):
    queryset=ServiceSubDepartment.objects.all()
    serializer_class=ServiceSubDepartmentSerializer
class ServiceMasterLC(ListCreateAPIView):
    queryset=ServiceMaster.objects.all()
    serializer_class=ServiceMasterSerializer
class TariffMasterLC(ListCreateAPIView):
    queryset=TariffMaster.objects.all()
    serializer_class=TariffMasterSerializer
class DesignationLC(ListCreateAPIView):
    queryset=Designation.objects.all()
    serializer_class=DesignationSerializer
class CorporateMasterLC(ListCreateAPIView):
    queryset=CorporateMaster.objects.all()
    serializer_class=CorporateMasterSerializer
class WardTypeLC(ListCreateAPIView):
    queryset=WardType.objects.all()
    serializer_class=WardTypeSerializer
class WardCategoryLC(ListCreateAPIView):
    queryset=WardCategory.objects.all()
    serializer_class=WardCategorySerializer
class TariffChargeMasterLC(ListCreateAPIView):
    queryset=TariffChargeMaster.objects.all()
    serializer_class=TariffChargeMasterSerializer
class BillingGroupTariffLinkLC(ListCreateAPIView):
    queryset=BillingGroupTariffLink.objects.all()
    serializer_class=BillingGroupTariffLinkSerializer
class DoctorScheduleTableLC(ListCreateAPIView):
    queryset=DoctorScheduleTable.objects.all()
    serializer_class=DoctorScheduleTableSerializer
class AppointmentTableLC(ListCreateAPIView):
    queryset=AppointmentTable.objects.all()
    serializer_class=AppointmentTableSerializer
class PatientTableLC(ListCreateAPIView):
    queryset=PatientTable.objects.all()
    serializer_class=PatientTableSerializer
class AddMembersLC(ListCreateAPIView):
    queryset=AddMembers.objects.all()
    serializer_class=AddMembersSerializer
class DoctorScheduleLC(ListCreateAPIView):
    queryset=DoctorSchedule.objects.all()
    serializer_class=DoctorScheduleSerializer
class AvailableDayScheduleMasterTempLC(ListCreateAPIView):
    queryset=AvailableDayScheduleMasterTemp.objects.all()
    serializer_class=AvailableDayScheduleMasterTempSerializer
class AvailabilityIntradayScheduleMasterLC(ListCreateAPIView):
    queryset=AvailabilityIntradayScheduleMaster.objects.all()
    serializer_class=AvailabilityIntradayScheduleMasterSerializer
class NameOfTheTitleLC(ListCreateAPIView):
    queryset=NameOfTheTitle.objects.all()
    serializer_class=NameOfTheTitleSerializer
class BloodMasterLC(ListCreateAPIView):
    queryset=BloodMaster.objects.all()
    serializer_class=BloodMasterSerializer
class NewAppointmentByAdminLC(ListCreateAPIView):
    queryset=NewAppointmentByAdmin.objects.all()
    serializer_class=NewAppointmentByAdminSerializer
class NewAppointmentByAdminChooseDoctorLC(ListCreateAPIView):
    queryset=NewAppointmentByAdminChooseDoctor.objects.all()
    serializer_class=NewAppointmentByAdminChooseDoctorSerializer
class RoomNumberLC(ListCreateAPIView):
    queryset=RoomNumber.objects.all()
    serializer_class=RoomNumberSerializer
class TokenMasterConfLC(ListCreateAPIView):
    queryset=TokenMasterConf.objects.all()
    serializer_class=TokenMasterConfSerializer
class TokenCreationsLC(ListCreateAPIView):
    queryset=TokenCreations.objects.all()
    serializer_class=TokenCreationsSerializer
class TokenCreationDoneLC(ListCreateAPIView):
    queryset=TokenCreationDone.objects.all()
    serializer_class=TokenCreationDoneSerializer
class CentralisedAdminViewLC(ListCreateAPIView):
    queryset=CentralisedAdminView.objects.all()
    serializer_class=CentralisedAdminViewSerializer
    # return TemplateResponse('Hello')
class CentralisedAdminViewRUD(RetrieveUpdateDestroyAPIView):
    queryset=CentralisedAdminView.objects.all()
    serializer_class=CentralisedAdminViewSerializer
    # return TemplateResponse('Hello')
from rest_framework import mixins
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
class TestCountryViewLC(ListCreateAPIView):
    pass
    # queryset=TestCountry.objects.all()
    # serializer_class=TestCountrySerializer
    # def retrieve(request,*args,**kwargs):
    #     data=request.data
    #     print(data)
    # return TemplateResponse('Hello')
class TestCountryViewRUD(RetrieveUpdateDestroyAPIView):
    pass
    # queryset=TestCountry.objects.all()
    # print('queryset',queryset)
    # serializer_class=TestCountrySerializer
    # return TemplateResponse('Hello')
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from testapp import utils as project_utils
import json
@api_view(["POST"])
def country(request):
    serializer=TestCountrySerializer(data=request.data)
    print('POST Serializer',serializer)
    serializer.is_valid(raise_exception=True)
    return Response(project_utils.success_response(data=serializer.data,msg="Country Created",status_code=200))
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
class CountryList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='api/county_list.html'
    def get(self, request):
        queryset =TestCountry.objects.all()
        queryset_data=[]
        for data in queryset:
            country_code=data.country_code
            country_name=data.country_name
            data2=str(country_code)+'-'+country_name
            queryset_data.append(data2)
        print(queryset_data)
        return Response({'country': queryset})
def server_client_common_api_function(request,request_id_stream):
    pass
@api_view(['GET'])
def patient_details(request,uhid=None):
    if request.method == 'GET':
        if uhid == None:
            patient_details=PatientsRegistrationsAllInOne.objects.all()
            serializer=PatienDetailSerializer(patient_details,many=True)
            return Response(project_utils.success_response(status_code=200,data=serializer.data))
        else:
            patient_details=PatientsRegistrationsAllInOne.objects.filter(uhid=uhid)
            if patient_details.exists():
                serializer=PatienDetailSerializer(patient_details,many=True)
                return Response(project_utils.success_response(status_code=200,data=serializer.data))
            else:
                return Response(project_utils.success_response(status_code=404,msg="Please Provide Valid UHID Of The Patient...!!!"))

@api_view(['GET'])
def patient_admission_info(request):
    if request.method == 'GET':
        records = AdmissionInfos.objects.all()
        patient_details = PatientsRegistrationsAllInOne.objects.all()
        serializer1 = PatienDetailSerializer(patient_details, many=True)
        serializer2 = AdmissionInfosSerializer(records,many = True)
        data1=serializer1.data
        data2=serializer2.data
        # print(type(data1),list(data1))
        # print(type(data2),list(data2))
        l1=[]
        for d1 in data1:
            for d2 in data2:
                if d1['uhid'] == d2['uhid']:
                    r_d1=dict(d1)
                    r_d2=dict(d2)
                    # result=r_d1 | r_d2
                    r_d1.update(r_d2)
                    l1.append(r_d1)
        ResultSerializer=serializer1.data + serializer2.data# its concadinating
        return Response(project_utils.success_response(status_code=200, data=l1))