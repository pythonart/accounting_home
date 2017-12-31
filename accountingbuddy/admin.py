from django.contrib import admin
from .models import Pricing,  Business_request, SendMails,SupportTypes,Support_request,Advert
from .models import DesktopActivationReq,BusinessTypes,BusinessTypeFile

# Register your models here.

admin.site.register(Pricing)
admin.site.register(Business_request)
admin.site.register(SendMails)
admin.site.register(SupportTypes)
admin.site.register(Advert)
admin.site.register(DesktopActivationReq)
#admin.site.register(BusinessTypes)
#admin.site.register(BusinessTypeFile)


class SupportRequestAdmin(admin.ModelAdmin):
  list_display=('user','request_type','date_created','date_time','request_closed')
  
admin.site.register(Support_request,SupportRequestAdmin)  

class BusinessTypeFileAdmin(admin.ModelAdmin):
  list_display=('businesstype','businessFile')

admin.site register(BusinessTypeFile,BusinessTypeFileAdmin)
