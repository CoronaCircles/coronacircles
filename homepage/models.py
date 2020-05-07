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


class SimplePage(models.Model):
    url = models.CharField(_("URL Path"), max_length=255, unique=True)
    title = models.CharField(_("Title"), max_length=255)
    text = models.TextField(_("Text"))
    template_name = models.CharField(_("Template Name"), max_length=255, blank=True)

    def __str__(self) -> str:
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def get_template_names(self):
        templates = ["homepage/simple_page.html"]
        if self.template_name:
            templates = [
                self.template_name,
                f"homepage/{self.template_name}",
            ] + templates
        return templates

    class Meta:
        verbose_name = _("Simple Page")
        verbose_name_plural = _("Simple Pages")
        ordering = ("url",)
