from django import forms
from django.forms import ModelForm , Textarea , DateTimeInput
from django.core.exceptions import ValidationError
from mezzanine.accounts.forms import ProfileForm
from django.core.mail import EmailMultiAlternatives
from .models import  Business_request, MyProfile , Pricing, Support_request,DesktopActivationReq,SendMails, BusinessTypeFile 

from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL

BUSINESS_TYPE=( ('SERVICE','SERVICES' ),('MANUFACTURING','MANUFACTURING'),('SALES','SALES'),('PERSONAL','PERSONAL'),('SOCIETY','SOCIETY' ),('SCHOOL','SCHOOL'),('SUPER MARKER','SUPER MARKET'),)

def file_size(value): # Check File Size
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

class ImportBusinessForm(ModelForm):
  businessType=forms.ModelChoiceField(queryset=BusinessTypeFile.objects.all(),empty_label=None,label="Business Type",help_text="Select Business Type")
  class Meta:
    model=Business
    fields=['name']
	
class DesktopLicenseReq(ModelForm):
	class Meta:
		model=DesktopActivationReq
		fields=['system_type',]

class SupportReqForm(ModelForm):
	class Meta:
		model=Support_request
		fields=['date_time','request_type','request_closed',]
		widgets = {'date_time': forms.DateInput(attrs={'class': 'datetimepicker12'})}
		


class BusinessRequestForm(ModelForm):
	class Meta:
		model=Business_request
		fields=['business_name','business_type','license_type','additional_details','tax_structure','sales_invoice','purchase_invoice','pay_slip','talley_file',]
		widgets = {'additional_details': Textarea(attrs={'cols': 80, 'rows': 20}),'tax_structure': Textarea(attrs={'cols': 80, 'rows': 20}) ,}
		
	def __init__(self,*args,**kwargs):
		self.request = kwargs.pop('request',None)
		super(BusinessRequestForm,self).__init__(*args,**kwargs)
		select_user=MyProfile.objects.get(user=self.request.user)
		price=Pricing.objects.all().filter(pricing_region=select_user.region).filter(target=select_user.sales_partner)
		self.fields['license_type'].queryset=price

class MyCustomProfileForm(ProfileForm):
	def save(self, *args, **kwargs):
		user = super(MyCustomProfileForm, self).save(*args, **kwargs)
		if self._signup:
			to=[]
			email_obj=SendMails.objects.all()
			for item in email_obj:
				to.append(item.email_id)
			passwd=self.cleaned_data.get('password1')
			name=self.cleaned_data.get('first_name')+' '+self.cleaned_data.get('last_name')
			username=self.cleaned_data.get('email')
			usr_create=manager_browser()
			#using email address for Name also. Which will assist in locating the user easily
			#when creating a business (business.managerapi)
			usr_create.create_user(name=username,username=username,password=passwd)
			#Error detection email sent below
			from_email='info@accountingbuddy.org'
			subject="AccountingBuddy.Org User Created   Name %s Username %s "  % (name,username)
			text_content="AccountingBuddy.Org User Created  Name %s Username %s "  % (name,username)
			html_content=" <h4> AccountingBuddy.Org User Created  Name %s Username %s  </h4>" % (name,username)
			#to = ['keeganpatrao@gmail.com',]
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			#Error detection emails sent below
		return user
