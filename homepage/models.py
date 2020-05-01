from django.db import models
from django.utils.translation import gettext_lazy as _


class Testimonial(models.Model):
    image = models.ImageField(_("Image"))
    text = models.TextField(_("Text"))
    author = models.CharField(_("Author"), max_length=255)
    order = models.IntegerField(_("Order"))

    def __str__(self) -> str:
        return _("Testimonial by %(author)s") % {"author": self.author}

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ("order",)


class CarouselItem(models.Model):
    headline = models.CharField(_("Headline"), max_length=255)
    text = models.TextField(_("Text"))
    order = models.IntegerField(_("Order"))

    def __str__(self) -> str:
        return self.headline

    class Meta:
        verbose_name = _("Carousel Item")
        verbose_name_plural = _("Carousel Items")
        ordering = ("order",)
