from django.contrib import admin
from .models import Testimonial, CarouselItem
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.widgets import CKEditorWidget


class TestimonialAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}
    pass


admin.site.register(Testimonial, TestimonialAdmin)


class CarouselItemAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}
    pass


admin.site.register(CarouselItem, CarouselItemAdmin)


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
