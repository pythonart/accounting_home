from django.contrib import admin
from .models import  Business, Server

# Register your models here.


class BusinessAdmin(admin.ModelAdmin):
  list_display=('id','name','code','user','created','url')
  list_filter=('id','name','code','user','created','url')
  search_fields=('name','code','user','created')
  ordering=('name',)
  
  

admin.site.register(Business,BusinessAdmin)
admin.site.register(Server)
