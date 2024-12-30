from django.urls import path,include
from usermanagementapp import views
urlpatterns=[
    path('user_management',views.user_management),
    path('user_management_acess/<pk>',views.user_management_acess),
    path('user_management_edit/<pk>',views.user_management_edit),
    path('user_management_details',views.user_management_details),
    path('user_management_delete/<pk>',views.user_management_delete),
    path('ward_access',views.ward_page),
    path('ward_search',views.ward_search),
    path('ward_access_edit/<pk>',views.ward_access_edit),
    path('lab_access',views.lab_access),
    path('lab_access_add/<pk>',views.lab_access_add),
    path('lab_search',views.lab_search),
    path('lab_doctor_search',views.lab_doctor_search),
    path('lab_access_add2/<pk>',views.lab_access_add2),
    #
    path('screen_access',views.screen_access,name='screen_access'),
    path('screen_access_view',views.screen_access_view,name='screen_access_view'),
    path('screen_access_edit/<pk>',views.screen_access_edit,name='screen_access_edit'),


]