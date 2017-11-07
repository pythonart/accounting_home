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
url(r'^thankyou/support$',TemplateView.as_view(template_name='thanks_support.html'),name='thanks_support'),
url(r'^supportrequest/create/$',views.supportRequestCreate,name='suppport-req'),
url(r'^supportrequest/view/$',views.SupportRequestView.as_view(),name='support-req-view'),
url(r'^supportrequest/update/(?P<pk>[0-9]+)/$',views.SupportRequestUpdateView.as_view(),name='support-req-update'),
url(r'^advert/$',views.AdvertView, name='advert'),  
]
