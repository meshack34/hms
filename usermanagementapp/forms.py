from usermanagementapp.models import *
from django import forms

class UserMangementForm(forms.ModelForm):
    class Meta:
        model=UserMangement
        fields='__all__'
        widgets={
        'password':forms.HiddenInput(),
         }

    def __init__(self, *args, **kwargs):
        super(UserMangementForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserMangement_wardForm(forms.ModelForm):
    class Meta:
        model=UserMangement_ward
        fields='__all__'
        widgets={
            'user_id':forms.TextInput(attrs={'class':'form-control'}),
            'user':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.HiddenInput(attrs={'class':'form-control'}),
            'ward_cat':forms.TextInput(attrs={'class':'form-control'}),
         }


class LabAccessForm(forms.ModelForm):
    class Meta:
        model=LabAccess
        fields='__all__'
        widgets={
            'user_id':forms.TextInput(attrs={'class':'form-control'}),
            'user':forms.TextInput(attrs={'class':'form-control'}),
            'service_department':forms.CheckboxSelectMultiple(attrs={}),
         }