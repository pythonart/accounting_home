from django.contrib import admin
from .models import Pricing,  Business_request, SendMails,SupportTypes,Support_request,Advert

# Register your models here.

admin.site.register(Pricing)
admin.site.register(Business_request)
admin.site.register(SendMails)
admin.site.register(SupportTypes)
admin.site.register(Advert)


class SupportRequestAdmin(admin.ModelAdmin):
  list_display=('user','request_type','date_created','date_time','request_closed')



admin.site.register(Support_request,SupportRequestAdmin)
