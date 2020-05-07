from django.contrib import admin
from django.db import models

from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget

from .models import Testimonial, CarouselItem, SimplePage


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


@admin.register(CarouselItem)
class CarouselItemAdmin(TranslationAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


@admin.register(SimplePage)
class SimplePageAdmin(TranslationAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}
