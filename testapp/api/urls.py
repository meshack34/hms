from django.urls import path
from testapp.api import views
urlpatterns=[
    #These All Ends point
    path('doctor/',views.Doctor.as_view()),
    path('doctor/<pk>',views.DoctorRUD.as_view()),
    path('appointment/',views.AppointmentList.as_view()),
    path('group-master/',views.GroupMasterLC.as_view()),
    path('branch-master/',views.BranchMasterLC.as_view()),
    path('title-master/',views.TitleMasterLC.as_view()),
    path('hospital-master/',views.HospitalMasterLC.as_view()),
    path('holiday-master/',views.HolidayMasterLC.as_view()),
    path('gender-master/',views.GenderMaterLC.as_view()),
    path('district-master/',views.DistrictMasterLC.as_view()),
    path('country-master/',views.CountryMasterLC.as_view()),
    path('city-master/',views.CityMasterLC.as_view()),
    path('most-common-document-master/',views.MostCommonDocumentTypeMasterLC.as_view()),
    path('msm-master/',views.MaritalStatusMasterLC.as_view()),
    path('relation-master/',views.RelationMasterLC.as_view()),
    path('service-category/',views.ServiceCategoryLC.as_view()),
    path('service-sub-category/',views.ServiceSubCategoryLC.as_view()),
    path('service-department/',views.ServiceDepartmentLC.as_view()),
    path('service-sub-department/',views.ServiceSubDepartmentLC.as_view()),
    path('service-master/',views.ServiceMasterLC.as_view()),
    path('designation/',views.DesignationLC.as_view()),
    path('corporate-master/',views.CorporateMasterLC.as_view()),
    path('ward-type/',views.WardTypeLC.as_view()),
    path('ward-category/',views.WardCategoryLC.as_view()),
    path('tariff-charge-master/',views.TariffChargeMasterLC.as_view()),
    path('billing-group-tariff-link/',views.BillingGroupTariffLinkLC.as_view()),
    path('doctor-schedule-table/',views.DoctorScheduleTableLC.as_view()),
    path('appointment-table/',views.AppointmentTableLC.as_view()),
    path('patient-table/',views.PatientTableLC.as_view()),
    path('add-members/',views.AddMembersLC.as_view()),
    path('doctor-schedule/',views.DoctorScheduleLC.as_view()),
    path('avl-intday-sche-mas/',views.AvailabilityIntradayScheduleMasterLC.as_view()),
    path('name-of-the-title/',views.NameOfTheTitleLC.as_view()),
    path('new-appointment-by-admin/',views.NewAppointmentByAdminLC.as_view()),
    path('room-master/',views.RoomNumberLC.as_view()),
    path('token-master-conf/',views.TokenMasterConfLC.as_view()),
    path('token-creations/',views.TokenCreationsLC.as_view()),
    path('token-creation-done/',views.TokenCreationDoneLC.as_view()),
    path('centralised-admin-view/',views.CentralisedAdminViewLC.as_view()),
    path('centralised-admin-view/<pk>',views.CentralisedAdminViewRUD.as_view()),
    path('country/',views.TestCountryViewLC.as_view()),
    path('country/<pk>',views.TestCountryViewRUD.as_view()),
    path('countrys/',views.country),
    path('country-list/',views.CountryList.as_view()),
    path('patient-details',views.patient_details,name='patient_details'),
    path('patient-details/<str:uhid>',views.patient_details,name='patient_details'),
    path('patient-admission-info',views.patient_admission_info, name='patient_admission_info'),
]