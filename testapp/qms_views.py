from django.http import HttpResponse
from rest_framework.views import APIView
from testapp.serializers import QmsSerializer
from django.shortcuts import render
import time
from rest_framework.response import Response
from testapp.models import DoctorTable
from testapp.serializers import DoctorTableSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
class Token_Master_Cofiguration_Class(ListCreateAPIView):
    queryset=DoctorTable.objects.all()
    serializer_class=DoctorTableSerializer
class Token_Master_Cofiguration_ClassRUD(RetrieveUpdateDestroyAPIView):
    queryset=DoctorTable.objects.all()
    serializer_class=DoctorTableSerializer
# class Token_Master_Cofiguration(APIView):
#     def get(self,request,*args,**kwargs):
#         form=TokenMasterConfigurationForm()
#         serializer_obj=QmsSerializer()
#         context={
#         'form':form
#         }
#         return render(request,'qms/index.html',context)
#     def post(self,request,*args,**kwargs):
#         # doc_id=request.POST.get('doc_id')
#         # doc_name=request.POST.get('doc_name')
#         # speciality=request.POST.get('speciality')
#         # status=request.POST.get('status')
#         # room_no=request.POST.get('room_no')
#         # max_token_assigned=request.POST.get('max_token_assigned')
#         # data=[doc_id,doc_name,speciality,status,room_no,max_token_assigned]
#         serializer=QmsSerializer(data=request.data)
#         if serializer.is_valid():
#             doc_id=serializer.data.get('doc_id')
#             doc_name=serializer.data.get('doc_name')
#             speciality=serializer.data.get('speciality')
#             status=serializer.data.get('status')
#             room_no=serializer.data.get('room_no')
#             max_token_assigned=serializer.data.get('max_token_assigned')
#             msg=' doctor id : {} , doctor name : {} , speciality : {} ,status : {}, room_no : {}, max_token_assigned : {}'.format(doc_id,doc_name,speciality,status,room_no,max_token_assigned)
#             return Response({'OutPut':msg})
#         else:
#             return Response(serializer.errors)
from rest_framework.generics import ListCreateAPIView
class Token_Master_Cofiguration_view(ListCreateAPIView):
    queryset=DoctorTable.objects.all()
    serializer_class=DoctorTableSerializer
