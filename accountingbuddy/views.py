from django.shortcuts import render


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
from accountingbuddy.models import MyProfile, Pricing


# Create your views here.


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

class businessFormCreateView(LoginRequiredMixin,UpdateView):
	model=Business_request
	template_name='accountingbuddy/business_request_form.html'
	form_class=BusinessRequestForm
	context_obeject_name='breq'
	success_url=reverse_lazy('accountingbuddy:pricing-india')
	
	





  
