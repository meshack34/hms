import time
from django.http import HttpResponse
class ApiMiddlewareExecution(object):
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        print('pre-pro-req',request)
        """
        Pre-Processing of the request
        """
        response=self.get_response(request)
        """
        post processing of the request
        """
        return response
    def process_view(request,*args,**kwargs):
        #This Is Process View
        print('Process Views In Middleware')
        #If this view return None Then That's View Function Will Execute else this one only
        return None
    def process_exception(self,request,exception):
        return HttpResponse(f'<h3>Sorry!!<br> Exception Is:{exception.__class__.__name__}<br> The Exception Msg: {exception}</h3>')
    # def process_template_response(self,request,response):
    #     print("Process Template Response Middleware")
    #     response="hello"
    #     return response

# def api_middleware(get_response):
#     print('One Time Configurations and Initialization')
#     def middleware(request):
#         print('code to Be Executed Each Request')
#         response=get_response(request)
#         print('code to be executed each request/respone after')
#         return response
#     return middleware
