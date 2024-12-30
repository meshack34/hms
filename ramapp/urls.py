from django.urls import path
from ramapp import views
urlpatterns=[
    path('',views.data_import , name= 'data_import'),
    path('auto-migrations',views.auto_migration,name='auto_migration'),
]