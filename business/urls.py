from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView
from business.views import BusinessListView


app_name='business'
urlpatterns=[  
url(r'^business/create/$', views.BusinessCreateView         , name='business-create'),
url(r'^business/list/$'  , views.BusinessListView.as_view() , name='business-list'  ),
url(r'^business/gstexport/$', views.GstOffLineView          , name='business-gst-export'),  
url(r'^business/salesinvoice/$',views.SalesInvoiceCreate,name='sales-invoice'),
url(r'^business/salesinvline/$',views.SalesInvoiceLine,name='sales-inv-line'),  
url(r'^business/salesinvformset/(?P<pk>[0-9]+)/$',views.SalesInvoiceFormSetView,name='sales-inv-formset'),  
]
