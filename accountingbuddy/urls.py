from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView


app_name='accountingbuddy'
urlpatterns=[  
url(r'^pricing/india/$',views.pricing_india,name='pricing-india'),
url(r'^businessrequest/submit/$',views.businessRequestFormView,name='business-req'),
url(r'^thankyou/$',TemplateView.as_view(template_name='thanks.html'),name='thanks'),
url(r'^supportrequest/create/$',views.SupportRequestView.as_view(),name='suppport-req'),
]
