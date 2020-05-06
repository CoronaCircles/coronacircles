from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget

from .models import Testimonial, CarouselItem


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


@admin.register(CarouselItem)
class CarouselItemAdmin(TranslationAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}
    fieldsets = (
        (None, {"fields": ("url", "title", "content",)}),
        (
            _("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": ("registration_required", "template_name"),
            },
        ),
    )
    list_filter = ("registration_required",)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
