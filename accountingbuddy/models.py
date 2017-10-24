from django.db import models

# Create your models here.

REGION_CHOICES=(('USA','USA'),('GULF','GULF'),('ASIA','ASIA'),('EUROPE','EUROPE'),)
CURRENCY_CHOICES=(('USD','US DOLLARS'),('INR','INDIAN RUPEES'),('AED','DIRHAMS'),)
SALES_PARTNER_CHOICES=(('SALESPARTNER','SALESPARTNER'),('INDIVIDUAL','INDIVIDUAL'))
BUSINESS_TYPE=( ('SERVICE','SERVICES' ),('MANUFACTURING','MANUFACTURING'),('SALES','SALES'),('PERSONAL','PERSONAL'),('SOCIETY','SOCIETY' ),('SCHOOL','SCHOOL'),('SUPER MARKER','SUPER MARKET'),)



class MyProfile(models.Model):
	user=models.OneToOneField("auth.User")
	company_name=models.CharField("Company Name",max_length=200,)
	phone_no=models.CharField("Contact No",max_length=200, help_text="Include country code   00-91-PhoneNo")
	sales_partner=models.CharField("Sales Partner or Individual",max_length=200,choices=SALES_PARTNER_CHOICES,help_text="Select Sales Partner, only  if your intrested in  becoming a  Sales partner")
	region=models.CharField("Select Region", max_length=200,choices=REGION_CHOICES,help_text="Select your Region")

	def __str__(self):
		return  "%s" % self.user

class  Pricing(models.Model):
	PLAN_CHOICES=(('INDIVIDUAL','INDIVIDUAL'),('SILVER','SILVER'),('GOLD','GOLD'),('DIAMOND','DIAMOND'),)
	pricing_region=models.CharField("Select Region",max_length=200,choices=REGION_CHOICES,help_text="Select Region  Price is Applicable for ")
	plan=models.CharField("Select Plan",max_length=200,choices=PLAN_CHOICES,help_text="Select Plan")
	price=models.IntegerField("Enter Price",help_text="Enter Price")
	currency=models.CharField("Select Currency",max_length=200,choices=CURRENCY_CHOICES,help_text="Select Currency")
	target=models.CharField("Select User Type",max_length=200,choices=SALES_PARTNER_CHOICES,help_text="Select Type of User")
	scope=models.CharField("Enter Customer Scope",max_length=200,help_text="E.G Profesionals , Companies, Etc")	

	def  __str__(self):
		return  "%s" % (self.target+' '+self.plan+' '+self.pricing_region+' '+str(self.price))


class Business_request(models.Model):
	user=models.ForeignKey("auth.User")
	business_name=models.CharField("Name of Business Required",max_length=200,help_text="Enter the name of the business")
	business_type=models.CharField("Select Business Type",max_length=200,choices=BUSINESS_TYPE,help_text="If your business type is not present,enter in additional details and select the closest type here")
	license_type=models.ForeignKey(Pricing)
	tax_structure=models.CharField("Tax Structure",max_length=200,help_text="Describe your Tax Structure",blank=True)
	additional_details=models.CharField("Enter any additional details",max_length=200,blank=True)
	sales_invoice=models.FileField(upload_to='businessReqForm',null=True,blank=True)
	purchase_invoice=models.FileField(upload_to='businessReqForm',null=True,blank=True)
	pay_slip=models.FileField(upload_to='businessReqForm',null=True,blank=True)
	talley_file=models.FileField(upload_to='businessReqForm',null=True,blank=True)
	
	def __str__(self):
		return  "%s  %s" % (self.user , self.business_name)
	
class SupportTypes(models.Model):
	support_reason=models.CharField("Support Type",max_length=200)
	
	def __str__(self):
	   return self.support_reason	
	
class Support_request(models.Model):
	user=models.ForeignKey("auth.User")
	date_time=models.DateTimeField("Enter Appointment Date/ Time")
	request_type=models.ForeignKey(SupportTypes)
	date_created=models.DateTimeField(auto_now=True)
	request_closed=models.CharField("Request Status",choices=(('OPEN','OPEN'),('CLOSED','CLOSED')),default='OPEN')
	
	def __str__(self):
	    return self.user + " " + self.date_time
			
	   
			       
class SendMails(models.Model):
	email_id=models.EmailField("Email Address",help_text="Emails of Business Request Will be Sent To")
	
	def __str__(self):
	    return " %s " % self.email_id
	
