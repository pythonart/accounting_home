from django.contrib import admin
from .models import Pricing,  Business_request, SendMails,SupportTypes,Support_request

# Register your models here.

admin.site.register(Pricing)
admin.site.register(Business_request)
admin.site.register(SendMails)
admin.site.register(SupportTypes)
admin.site.register(Support_request)



