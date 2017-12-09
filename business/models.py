from django.db import models

# Create your models here.

class Business(models.Model):
  name=models.CharField("Business Name",max_length=50)
  code=models.CharField("Code",max_length=200)
  user=models.ForeignKey("auth.User")
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return "%s" % self.name
  
class SalesInvoice(models.Model):
  IssueDate=models.DateField('Invoice Date')
  To=models.CharField("Customer",max_length=500)
  BillingAddress=models.CharField(label="Billing Address")
  DueDateType=models.ChoiceField(label="Due Date",choices=(("Net","Net"),("By","By")) )
  InvoiceSummary=models.CharField(label="Description",max_length=200)
  
  def __str__(self):
    return "%s" % self.IssueDate
  
  
class SalesInvoiceLine(models.Model):
  Description=models.CharField("Description",max_length=200)
  TaxCode=models.CharField("Tax",max_length=200)
  Qty=models.FloatField("Quantity")
  Item=models.CharField("Item",max_length=200) 
  Amount=models.FloatField("Amount")
  
  def __str__(self):
    return "%s" % self.Description
  
  
  
  
'''
class BusinessDetails(models.Model):
  businessName=models.ForeignKey(Business)
  businessContactInformation=models.CharField("Business Contact details", max_length=200,null=True,blank=True)
  businessIdentifier=models.CharField("Business Identifier",max_length=200,null=True,blank=True)
  
class BusinessCustomer(models.Model):
  name=models.CharField("Customer Name",max_length=200,null=True,blank=True)
  billingAddress=models.TextField("Billing Address",null=True,blank=True)
  email=models.CharField("Email",max_length=200,null=True,blank=True)
  businessIdentifier=models.CharField("Business Identifier",max_length=200,null=True,null=True)
  code=models.CharField("Customer Code",max_length=200,null=True,blank=True)
'''
  
  
  
  
  
  
  
  
  
  
