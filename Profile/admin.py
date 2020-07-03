from django.contrib import admin
from .models import Profile, Callback

admin.site.register(Profile)


class CallbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')
    readonly_fields = ['name', 'email', 'text']


admin.site.register(Callback, CallbackAdmin)
