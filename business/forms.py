from django import forms
from django.forms import ModelForm 
from django.core.exceptions import ValidationError
import calendar


from accountingbuddy.models import   MyProfile 
from business.models import Business
from .models import  Business

MONTH_CHOICES=[(str(k),calendar.month_abbr[k]) for k in range(1,13)]
YEAR_CHOICES=[(str(k),str(k)) for k in range(2015,2051)]
#[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')]

class BusinessCreateForm(ModelForm):
  class Meta:
    model=Business
    fields=['name']
    
class GstOffLineGenForm(forms.Form):
  q=Business.objects.all()
  business=forms.ModelChoiceField(queryset=q, empty_label=None)
  month=forms.ChoiceField(label='Select Month',choices=MONTH_CHOICES)
  year=forms.ChoiceField(label='Select Year',choices=YEAR_CHOICES)
  
  def __int__(self,*args,**kwargs):
    self.request = kwargs.pop('request',None)
    super(GstOffLineGenForm,self).__init__(*args,**kwargs)
    select_user=MyProfile.objects.get(user=self.request.user)
    q=Business.objects.all().filter(user=select_user)
    self.fields['business'].queryset=q
      

  
      

