from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Event, MailTemplate


class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ('type','language_code')
@admin.register(Event)


class EventAdmin(admin.ModelAdmin):
    list_display = ("uuid", "start", "language", "host")

@admin.register(MailTemplate)


class MailTemplateAdmin(TranslationAdmin):
    list_display = ("type",)