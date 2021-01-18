from django.contrib import admin
from .models import profileModel
# Register your models here.
class profileAdmin(admin.ModelAdmin):
    readonly_fields=('Fullname',)#it says to add readonly field created to admin
admin.site.register(profileModel,profileAdmin)

