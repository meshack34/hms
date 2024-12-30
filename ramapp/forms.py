from django import forms
from ramapp.get_model import get_model_name
class ReadCSV(forms.Form):
    all_model=get_model_name()
    model_choice=[('','---------')]+[(option,option) for option in all_model]
    Select_Table = forms.ChoiceField(choices=model_choice)
    upload_at = forms.FileField()
