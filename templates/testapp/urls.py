from django.urls import path
from testapp import  views
urlpatterns=[
    path('',views.patient_view),
    # path('',views.email_sending),
    path('book-appointment',views.book_appointment),
    path('book-appointment/<int:npp>',views.book_appointment),
    path('mobile_register',views.mobile_register),
    path('date_time',views.date_time),
    path('appointment_detail',views.appointment_detail),
    path('booking_detail',views.booking_detail),
    path('doctor-view',views.doctor_view),
    path('doctor-schedule-view',views.doctor_schedule_view),
    path('appointment-view',views.appointment_view),
    path('patient-view',views.patient_view_detail),
    path('admin-dashboard',views.patient_dashboard),
    path('admin_list_table',views.admin_list_table),
    path('appointment_table',views.AppoitmentView.as_view(),name='delete-appointment'),
    path('patient_table',views.patient_table),
    path('doctor_table',views.DoctorDashbordView.as_view(),name='delete'),
    path('delete-doctor/<int:pk>',views.DoctorDeleteView.as_view()),
    path('detail-doctor/<int:pk>',views.DoctorDetailView.as_view()),
    path('delete-appointment/<str:pk>',views.AppointmentDeleteView.as_view()),
    path('detail-appointment/<str:pk>',views.AppointmentDetailView.as_view()),
    path('success-booked',views.success_booked),
    path('doctor-schedule',views.doctor_schedule_view),
    path('schedule-date',views.schedule_date),
    path('time-scheduling',views.time_scheduling),
    path('scheduled_time',views.scheduled_time),
    path('patient-registrations',views.patient_registraions),
    #cancel appointment
    path('cancel-appointment/<str:patient_id>',views.cancel_appointment),
    #Appointment_dashboard
    path('doctor_dash',views.doctor_dash),
    path('doctor_appointment',views.doctor_appointment),
    path('prescription',views.prescription),
    path('appointment_list',views.appointment_list),
    path('patient_list',views.patient_list),
    #Interface
    path('interface_dashboard',views.interface_dashboard),
    path('patient',views.patient),
    path('login',views.login),
    path('box',views.box),
    path('modal',views.modal),
    path('table',views.table),
    #reports
    path('reports',views.reports),
    path('cancellation-reports',views.cancellation_reports),
    path('shorting-filter',views.shorting_filter),
    path('appointment-detail-reports',views.appointment_detail_reports),
    #admin Pannel


]
