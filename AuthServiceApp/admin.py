from django.contrib import admin
from django.contrib.auth.models import User
from .models import Account, Client, Expert, UserCalendar, ExpertCalendar
# Register your models here.
admin.site.register(Account)
admin.site.register(Client)
admin.site.register(Expert)
admin.site.register(UserCalendar)
admin.site.register(ExpertCalendar)

