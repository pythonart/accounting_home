from django import forms
from django.forms import ModelForm , Textarea
from django.core.exceptions import ValidationError
from mezzanine.accounts.forms import ProfileForm
from django.core.mail import EmailMultiAlternatives
from .models import  Business_request, MyProfile , Pricing, Support_request
from datetimewidget.widgets import DateTimeWidget # For Date time widgets https://github.com/asaglimbeni/django-datetime-widget

from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL

BUSINESS_TYPE=( ('SERVICE','SERVICES' ),('MANUFACTURING','MANUFACTURING'),('SALES','SALES'),('PERSONAL','PERSONAL'),('SOCIETY','SOCIETY' ),('SCHOOL','SCHOOL'),('SUPER MARKER','SUPER MARKET'),)

def file_size(value): # Check File Size
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')  

class SupportReqForm(ModelForm):
	class Meta:
		model=Support_request
		fields=['date_time','request_type','request_closed',]
		widgets={'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3), }
		


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
			passwd=self.cleaned_data.get('password1')
			name=self.cleaned_data.get('first_name')+' '+self.cleaned_data.get('last_name')
			username=self.cleaned_data.get('email')
			usr_create=manager_browser()
			#using email address for Name also. Which will assist in locating the user easily
			#when creating a business (business.managerapi)
			usr_create.create_user(name=username,username=username,password=passwd)
			#Error detection email sent below
			from_email='info@accountingbuddy.org'
			subject="AccountingBuddy.Org User Created Password %s  Name %s Username %s "  % (passwd,name,username)
			text_content="AccountingBuddy.Org User Created Password %s  Name %s Username %s "  % (passwd,name,username)
			html_content=" <h4> AccountingBuddy.Org User Created Password %s  Name %s Username %s  </h4>" % (passwd,name,username)
			to = ['keeganpatrao@gmail.com',]
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			#Error detection emails sent below
		return user
