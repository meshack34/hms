from django.urls import path
from testapp.func_api import views
urlpatterns=[
    path('patient',views.PatientView.as_view()),
]
