import time
from django.http import HttpResponse
from .models import *


class MiddlewareExecutionStart(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            if 'admin_location' in request.session:
                request.location = request.session['admin_location']
            else:
                request.location = ''
        elif request.user.is_authenticated and not request.user.is_superuser or request.user.is_staff :
            access = CreateUser.objects.filter(login_id=request.user).first()
            if access:
                request.location = access.location.id
                if access.store:
                    store = access.store.all()
                    store_list = [data.id for data in store]
                    request.store_id = store_list
                else:
                    request.store_id = []
            else:
                request.location = ''

        response = self.get_response(request)
        return response

    # def process_exception(self,request,exception):
    #     return HttpResponse('<h3>Currently We Are Facing Technical Isses</h3>')