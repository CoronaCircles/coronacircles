from django.views.generic import TemplateView

from circles.models import Event
from .models import Testimonial, CarouselItem


class Homepage(TemplateView):
    template_name = "homepage/homepage.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["events"] = Event.objects.upcoming()
        data["testimonials"] = Testimonial.objects.all()
        data["carousel_items"] = CarouselItem.objects.all()
        return data
