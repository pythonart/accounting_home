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

from accountingbuddy.models import MyProfile, Pricing, Business_request, SendMails,Support_request,Advert
from .forms import BusinessRequestForm , SupportReqForm,DesktopLicenseReq

# Create your views here.

@login_required
def desktopActivationReqView(request):
	to=[]
	if request.method=="POST":
		form=DesktopLicenseReq(request.POST)
		if form.is_valid():
			actreq=form.save(commit=False)
			actreq.user=request.user
			actreq.save()
			user=request.user
			from_email='info@accountingbuddy.org'
			subject="AccountingBuddy.Org Activation Code Fm %s" % user.first_name
			text_content=" Thank you for Downloading AccountingBuddy Software. Your Activation Code For Your Business is 684 - 371 - 827 "
			html_content=" <h4>Activation Code Generated </h4> <br> <p> Thank you for Downloading AccountingBuddy Desktop Software. Your Activation code is as below </p> <br> <h4> 684 - 371 - 827 </h4>"
			#to = ['keeganpatrao@gmail.com',]
			to +=[user.email,]
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			return HttpResponseRedirect(reverse('accountingbuddy:thanks_activation')) # Change Template
	else :
		form=DesktopLicenseReq()
	return render(request,'business_request_form.html', {'form': form})  # Change Template 	
	

def  pricing_india(request):
	if  request.user.is_authenticated:
		user=MyProfile.objects.get(user=request.user) 
		price=Pricing.objects.all().filter(pricing_region=user.region).filter(target=user.sales_partner)
		if price.count() > 0:		
			context={'price':price, }
		else :
			not_logged_in="True"
			context={'not_logged_in':not_logged_in,}
	else :
		not_logged_in="True"
		context={'not_logged_in':not_logged_in,  }	

	
	template_name="accountingbuddy/sales_price.html"
	return render(request,template_name,context)


@login_required
def businessRequestFormView(request):
	to=[]
	email_obj=SendMails.objects.all()
	for item in email_obj:
		to.append(item.email_id)
	if request.method == 'POST':
		form=BusinessRequestForm(request.POST,request.FILES,request=request)
		if form.is_valid():
			#s=Business_request(user=request.user)
			busreq=form.save(commit=False)
			busreq.user=request.user
			busreq.save()
			user=request.user
			from_email='info@accountingbuddy.org'
			subject="AccountingBuddy.Org Business Setup Request Fm %s" % user.first_name
			text_content="Business Name : %s , Business Type: %s , License Type: %s, Additional Details : %s , User %s , Phone %s, Email %s" % (busreq.business_name,busreq.business_type,busreq.license_type, busreq.additional_details, request.user,user.myprofile.phone_no,user.email)
			html_content=" <h4> Business Set Up Request </h4> <br> <ul> <li> Business Name : %s  </li> <li> Business Type : %s  </li> <li> License Type : %s  </li> <li> Additional Details : %s  </li><li> User : %s  </li><li> Phone : %s  </li><li> Email : %s  </li> </ul>" % (busreq.business_name,busreq.business_type,busreq.license_type, busreq.additional_details, request.user,user.myprofile.phone_no,user.email)
			#to = ['keeganpatrao@gmail.com',]
			to +=[user.email,]
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			if busreq.sales_invoice :
				msg.attach_file(busreq.sales_invoice.path)
			if busreq.purchase_invoice :
				msg.attach_file(busreq.purchase_invoice.path)
			if busreq.pay_slip :
				msg.attach_file(busreq.pay_slip.path)
			if busreq.talley_file :
				msg.attach_file(busreq.talley_file.path)	
			msg.send()
			return HttpResponseRedirect(reverse('accountingbuddy:thanks'))
	else:
		form = BusinessRequestForm(request=request)
	return render(request, 'business_request_form.html', {'form': form})

@login_required
def supportRequestCreate(request):
	to=[]
	email_obj=SendMails.objects.all()
	for item in email_obj:
		to.append(item.email_id)
	if request.method == 'POST':
		form=SupportReqForm(request.POST,request.FILES)
		if form.is_valid():
			supportreq=form.save(commit=False)
			supportreq.user=request.user
			supportreq.save()
			user=request.user
			from_email='info@accountingbuddy.org'
			subject="AccountingBuddy.Org Support Request Fm %s" % user.first_name
			text_content="Appointment Date and Time : %s , Request Type: %s , Request Status: %s" % (supportreq.date_time ,supportreq.request_type,supportreq.request_closed)
			html_content=" <h4>Support Request  </h4> <br> <ul><li> %s </li> <li> Appointment Date and Time : %s  </li> <li> Request Type: %s  </li> <li> Request Status: %s  </li> </ul>"  % (user.first_name,supportreq.date_time ,supportreq.request_type,supportreq.request_closed)
			#to = ['keeganpatrao@gmail.com',]
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")	
			msg.send()
			return HttpResponseRedirect(reverse('accountingbuddy:thanks_support'))
	else:
		form = SupportReqForm()
	return render(request, 'datepick.html', {'form': form})

class SupportRequestView(LoginRequiredMixin,generic.ListView):
	model=Support_request
	template_name='accountingbuddy/supportreq_detail.html'
	context_object_name='supportreq'
	
	def get_queryset(self):
		if self.request.user.is_staff:
			return Support_request.objects.all().order_by('date_time')
		else :
			return get_list_or_404(Support_request, user=self.request.user )
		
 
class SupportRequestUpdateView(UserPassesTestMixin,UpdateView):
	model=Support_request
	form_class=SupportReqForm
	template_name='datepick.html'
	context_object_name='form'
	success_url=reverse_lazy('accountingbuddy:support-req-view')
	
	def test_func(self):
          if self.request.user.has_perm('accountingbuddy.change_Support_request'):
              return True
          if self.request.user.is_staff :
              return True
          else :
                 req=get_object_or_404(Support_request, pk=self.kwargs['pk'])
                 if req.user==self.request.user:
                    return True
                 else:
                    return False
	
def AdvertView(request):
	q=Advert.objects.get(id=1)
	return HttpResponse(" %s" % q.content)
	
	

      

    
    
	




  
