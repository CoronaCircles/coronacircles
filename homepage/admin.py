from django.contrib import admin
from .models import Testimonial, CarouselItem


class TestimonialAdmin(admin.ModelAdmin):
    pass


admin.site.register(Testimonial, TestimonialAdmin)


class CarouselItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(CarouselItem, CarouselItemAdmin)
