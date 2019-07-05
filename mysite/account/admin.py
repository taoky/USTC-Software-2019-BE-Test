from django.contrib import admin
from .models import UserPro


class UserProAdmin(admin.ModelAdmin):
    lise_display = ('user', 'phone', 'company', 'selfpro')
    list_filter = ('company',)

admin.site.register(UserPro,UserProAdmin)