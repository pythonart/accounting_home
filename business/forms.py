from django import forms
from django.forms import ModelForm 
from django.core.exceptions import ValidationError

from .models import  Business

class BusinessCreateForm(ModelForm):
  class Meta:
    model=Business
    fields=['name']
    
class GstOffLineGenForm(forms.Form):
  pass

  
      

