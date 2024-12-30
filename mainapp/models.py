from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    branch_location = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)
    def __str__(self): 
        return self.name

class Domain(DomainMixin):
    pass

class BranchRestrict(models.Model):
    branch_name = models.ForeignKey(Client,on_delete=models.CASCADE)
    branch_limit = models.CharField(max_length=100)
    user_limit = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)
    
    
