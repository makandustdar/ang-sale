from django.contrib import admin
from .models import Profile, Private, Legal, Expert, Exhibition, City, State


class PrivateAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'profile']


admin.site.register(Profile)
admin.site.register(Private, PrivateAdmin)
admin.site.register(Legal)
admin.site.register(Expert)
admin.site.register(Exhibition)
admin.site.register(State)
admin.site.register(City)
