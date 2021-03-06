from django.db import models
from business.models import Business
from datetime import date

# Create your models here.

class Invoice(models.Model):
  number=models.CharField("Invoice No",max_length=200)
  amount=models.FloatField("Amount")
  discount=models.FloatField("Discount")
  totalAmount=models.FloatField("Total Amount")
  
  def __str__(self):
    return self.number
 

class Agent(models.Model):
  name=models.CharField("Agent Name",max_length=200)
  dateRegistered=models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
class SubscriptionType(models.Model):
  type=models.CharField("Type",max_length=200)
  cost=models.FloatField("Cost")
  
  def __str__(self):
    return self.type
  
class Subscription(models.Model):
  #user=models.ForeignKey("auth.User")
  business=models.ForeignKey(Business)
  type=models.ForeignKey(SubscriptionType)
  fromDate=models.DateField("Start Date")
  to=models.DateField("End Date")
  invoiceNo=models.ForeignKey(Invoice)
  agent=models.ForeignKey(Agent)
  
  def __str__(self):
    return "Type: %s  Ends: %s" % (self.type,self.to)
  
  @property
  def active(self):
    if to > date.today():
      True
    else:
      False 
    
  

  

  
  
