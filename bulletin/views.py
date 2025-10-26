from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import News, Event, Special, Promotion, Resource, Organization
from django.db.models import Q


def home(request):
    """Homepage with widgets showing recent/upcoming items from each category."""
    today = timezone.now().date()

    context = {
        'recent_news': News.objects.filter(is_published=True)[:5],
        'upcoming_events': Event.objects.filter(
            is_published=True,
            end_date__gte=today
        ).order_by('start_date')[:5],
        'active_specials': Special.objects.filter(
            is_published=True,
            start_date__lte=today,
            end_date__gte=today
        )[:5],
        'active_promotions': get_active_promotions(today)[:5],
        'recent_resources': Resource.objects.filter(is_published=True)[:5],
    }
    return render(request, 'bulletin/home.html', context)


def get_active_promotions(check_date=None):
    """Helper function to get promotions active on a given date."""
    if check_date is None:
        check_date = timezone.now().date()

    promotions = Promotion.objects.filter(
        is_published=True,
        valid_from__lte=check_date
    ).filter(
        Q(valid_until__isnull=True) | Q(valid_until__gte=check_date)
    )

    # Filter by recurrence pattern
    active_promotions = []
    for promotion in promotions:
        if promotion.is_active_on_date(check_date):
            active_promotions.append(promotion)

    return active_promotions


# News Views
class NewsListView(ListView):
    model = News
    template_name = 'bulletin/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 20

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = News
    template_name = 'bulletin/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True)


# Event Views
class EventListView(ListView):
    model = Event
    template_name = 'bulletin/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        show_past = self.request.GET.get('show_past', False)
        queryset = Event.objects.filter(is_published=True)

        if not show_past:
            queryset = queryset.filter(end_date__gte=timezone.now().date())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_past'] = self.request.GET.get('show_past', False)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'bulletin/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        return Event.objects.filter(is_published=True)


# Special Views
class SpecialListView(ListView):
    model = Special
    template_name = 'bulletin/special_list.html'
    context_object_name = 'specials'
    paginate_by = 20

    def get_queryset(self):
        today = timezone.now().date()
        return Special.objects.filter(
            is_published=True,
            start_date__lte=today,
            end_date__gte=today
        )


class SpecialDetailView(DetailView):
    model = Special
    template_name = 'bulletin/special_detail.html'
    context_object_name = 'special'

    def get_queryset(self):
        return Special.objects.filter(is_published=True)


# Promotion Views
def promotion_list(request):
    """List view for promotions active today."""
    today = timezone.now().date()
    promotions = get_active_promotions(today)

    return render(request, 'bulletin/promotion_list.html', {
        'promotions': promotions,
        'today': today,
    })


class PromotionDetailView(DetailView):
    model = Promotion
    template_name = 'bulletin/promotion_detail.html'
    context_object_name = 'promotion'

    def get_queryset(self):
        return Promotion.objects.filter(is_published=True)


# Resource Views
class ResourceListView(ListView):
    model = Resource
    template_name = 'bulletin/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 20

    def get_queryset(self):
        return Resource.objects.filter(is_published=True)


class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'bulletin/resource_detail.html'
    context_object_name = 'resource'

    def get_queryset(self):
        return Resource.objects.filter(is_published=True)


# About Us
def about(request):
    """About us page."""
    return render(request, 'bulletin/about.html')
