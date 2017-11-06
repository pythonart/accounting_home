from django import forms
from django.forms import ModelForm 
from django.core.exceptions import ValidationError

from .models import  Business, MyProfile

MONTH_CHOICES=[('JAN','1'),('

class BusinessCreateForm(ModelForm):
  class Meta:
    model=Business
    fields=['name']
    
class GstOffLineGenForm(forms.Form):
  q=MyProfile.objects.all()
  business=forms.ModelChoiceField(queryset=q, empty_label=None)
  month=forms.MultipleChoiceField(choice=MONTH_CHOICES)

  
      

