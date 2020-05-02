from django.contrib import admin
from .models import Event, MailTemplate


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)


class MailTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(MailTemplate, MailTemplateAdmin)
