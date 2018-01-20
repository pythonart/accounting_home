from django.contrib import admin
from .models import Invoice,Agent,SubscriptionType,Subscription,

# Register your models here.

admin.site.register(Invoice)
admin.site.register(Agent)
admin.site.register(SubscriptionType)
admin.site.register(Subscription)
