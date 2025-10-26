from django.urls import path
from . import views

app_name = 'bulletin'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # News
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),

    # Events
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),

    # Specials
    path('specials/', views.SpecialListView.as_view(), name='special_list'),
    path('specials/<slug:slug>/', views.SpecialDetailView.as_view(), name='special_detail'),

    # Promotions
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/<slug:slug>/', views.PromotionDetailView.as_view(), name='promotion_detail'),

    # Resources
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/<slug:slug>/', views.ResourceDetailView.as_view(), name='resource_detail'),

    # About
    path('about/', views.about, name='about'),
]
