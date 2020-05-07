from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404

from circles.models import Event
from .models import Testimonial, CarouselItem, SimplePage


class Homepage(TemplateView):
    template_name = "homepage/homepage.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["events"] = Event.objects.upcoming()
        data["testimonials"] = Testimonial.objects.all()
        data["carousel_items"] = CarouselItem.objects.all()
        return data


class SimplePageView(DetailView):
    model = SimplePage
    context_object_name = "page"

    def get_template_names(self):
        page = self.get_object()
        return page.get_template_names()

    def get_object(self):
        return get_object_or_404(SimplePage, url=self.kwargs["url"])
