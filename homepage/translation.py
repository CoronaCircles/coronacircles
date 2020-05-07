from modeltranslation.translator import register, TranslationOptions
from .models import Testimonial, CarouselItem, SimplePage


@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(CarouselItem)
class CarouselItemOptions(TranslationOptions):
    fields = ["headline", "text"]


@register(SimplePage)
class SimplePageOptions(TranslationOptions):
    fields = ["title", "text"]
