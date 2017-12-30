from django.views.generic.edit import UpdateView , CreateView, DeleteView
from django.shortcuts import render, render_to_response

from django.shortcuts import get_object_or_404 , get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import UpdateView , CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail , BadHeaderError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMultiAlternatives

from business.models import Business, SalesInvoiceMod, SalesInvoiceLineMod
from accountingbuddy.modles import SendMails
from business.forms import BusinessCreateForm, GstOffLineGenForm, SalesInvoiceForm, SalesInvoiceLineForm, SalesInvModForm, SalesInvoiceLineModForm

from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL
from accountingbuddy.models import MyProfile
from business.manager_collect import *
import calendar
from django.forms import inlineformset_factory
  
@login_required  
def BusinessCreateView(request):
  if request.method=="POST":
    form=BusinessCreateForm(request.POST,request.FILES)
    if form.is_valid():
      to=[]
      email_obj=SendMails.objects.all()
      for item in email_obj:
        to.append(item.email_id)
      business_create=form.save(commit=False)
      business_create.user=request.user
      #create the business in Manager
      bus=manager_browser()
      name=form.cleaned_data['name']
      code=bus.create_business(name=name)
      bus.activate_tabs()
      #completed creating the business
      #Adding user to business
      select_user=MyProfile.objects.get(user=request.user)
      user_name=select_user.user.email
      bus.add_bus_user(req_user=user_name,code=code)
      #completed adding user
      business_create.code=code
      business_create.save()
      from_email='info@accountingbuddy.org'
      subject="AccountingBuddy.Org Business %s Created by User %s Username %s "  % (name,user_name)
      text_content="AccountingBuddy.Org Business %s Created by User %s Username %s "  % (name,user_name)
      html_content=" <h4> AccountingBuddy.Org Business %s Created by User %s Username %s " % (name,username)
      #to = ['keeganpatrao@gmail.com',]
      msg = EmailMultiAlternatives(subject, text_content, from_email, to)
      msg.attach_alternative(html_content, "text/html")
      msg.send()
      return HttpResponseRedirect(reverse('accountingbuddy:pricing-india'))
  else:
    form=BusinessCreateForm()
  return render(request,'form.html',{'form':form})

class BusinessListView(LoginRequiredMixin, generic.ListView):
  template_name='list.html'
  context_object_name='business'
  paginate_by=10
  
  def get_queryset(self):
    if self.request.user.is_staff:
      return Business.objects.all()
    else:
      return get_list_or_404(Business,user=self.request.user)
  
#@login_required
def GstOffLineView(request):
  if request.method=="POST":
    form=GstOffLineGenForm(request.POST,request.FILES,request=request)
    if form.is_valid():
      business_form=form.cleaned_data['business']
      month=form.cleaned_data['month']
      year=form.cleaned_data['year']
      month=int(month)
      year=int(year)
      invoice_type=form.cleaned_data['invoice_type']
      from_date=str(1)+'/'+str(month)+'/'+str(year)
      k,v=calendar.monthrange(year,month)
      to_date=str(v)+'/'+str(month)+'/'+str(year)
      business=Business.objects.get(id=business_form.id)
      #try:
      response=GstBusiness(fm_date=from_date,to_date=to_date,inv_type=invoice_type,business=business.name).gstOffline()
      return response
      #except Exception as err:
      #return render(request,'error.html',{'error':err})
  else:
    form=GstOffLineGenForm(request=request)
  return render(request,'business/form.html',{'form':form}) 


def SalesInvoiceCreate(request):
  if request.method=="POST":
    form=SalesInvModForm(request.POST,request.FILES)
    if form.is_valid():
      print(form)
  else:
    form=SalesInvModForm()
  return render(request,'business/form.html',{'form':form})

def SalesInvoiceLine(request):
  if request.method=="POST":
    form=SalesInvoiceLineModForm(request.POST,request.FILES)
    if form.is_valid():
      print(form)
  else:
    form=SalesInvoiceLineModForm()
  return render(request,'business/form.html',{'form':form})  
    
def SalesInvoiceFormSetView(request,pk):
  salesinvoice=SalesInvoiceMod.objects.get(pk=pk)
  #SalesInvoiceLineFormSet=inlineformset_factory(SalesInvoiceMod,SalesInvoiceLineMod,fields=('SalesInvoice','Description','TaxCode','Qty','Item','Amount'))  
  SalesInvoiceLineFormSet=inlineformset_factory(SalesInvoiceMod,SalesInvoiceLineMod,form=SalesInvoiceLineModForm) 
  if request.method=="POST":
    formset=SalesInvoiceLineFormSet(request.POST,request.FILES,instance=salesinvoice)
    if formset.is_valid():
      print(formset)
      formset.save()
  else:
    formset=SalesInvoiceLineFormSet(instance=salesinvoice)
  return   render(request,'business/test.html',{'formset': formset}) 
      
      
  
