from django.views.generic.edit import UpdateView , CreateView, DeleteView
from django.shortcuts import render, render_to_response

from django.shortcuts import get_object_or_404 , get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import UpdateView , CreateView, DeleteView
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

from business.models import Business
from business.forms import BusinessCreateForm

from business.managerapi import manager_browser, manager_object, USER_NAME,PASSWORD,ROOT_URL
from accountingbuddy.models import MyProfile
  
@login_required  
def BusinessCreateView(request):
  if request.method=="POST":
    form=BusinessCreateForm(request.POST,request.FILES)
    if form.is_valid():
      business_create=form.save(commit=False)
      business_create.user=request.user
      #create the business in Manager
      bus=manager_browser()
      name=form.cleaned_data['name']
      code=bus.create_business(name=name)
      bus.activate_tabs()
      #completed creating the business
      #Adding user to business
      user_link=bus.browser.get_link(text='users')
      bus.browser.follow_link(user_link)
      select_user=MyProfile.objects.get(user=self.request.user)
      user_name=select_user.user.username
      usr_name_link=bus.browser.get_link(text=user_name)
      bus.browser.follow_link(usr_name_link)
      
      #completed adding user
      business_create.code=code
      business_create.save()
      return HttpResponseRedirect(reverse('accountingbuddy:pricing-india'))
  else:
    form=BusinessCreateForm()
  return render(request,'form.html',{'form':form})
      
  
  
      
  
