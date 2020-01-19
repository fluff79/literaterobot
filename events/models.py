from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

from datetime import date


class EventIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        context['today'] = date.today()
        events = self.get_children().live().order_by('-first_published_at')
        context['events'] = events
        return context

class Event(Page):

    date = models.DateField("Event date")
    place = models.CharField(max_length=250)
    agenda = RichTextField(blank=True)
    notes = RichTextField(blank=True)
    resources = RichTextField(blank=True)
    attended = models.IntegerField(blank=True, null=True)


    search_fields = Page.search_fields + [
        index.SearchField('agenda', partial_match=True),
        index.SearchField('notes', partial_match=True),
        index.SearchField('resources', partial_match=True),
        index.FilterField('date')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('place'),
        FieldPanel('agenda', classname="full"),
        FieldPanel('notes', classname="full"),
        FieldPanel('resources', classname="full"),
        FieldPanel('attended'),
    ]

    def get_context(self, request):
        context = super(Event, self).get_context(request)
        context['today'] = date.today()
        return context

    # event_items = EventPage.objects.live().order_by('-date')

