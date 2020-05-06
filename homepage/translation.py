from modeltranslation.translator import register, TranslationOptions
from .models import Testimonial, CarouselItem


@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(CarouselItem)
class CarouselItemOptions(TranslationOptions):
    fields = ["headline", "text"]
