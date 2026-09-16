from django.urls import path
from . import views, api_views

app_name = 'restaurants'

urlpatterns = [
    path('search/', views.restaurant_search_view, name='search'),
    path('compare/', views.restaurant_compare_view, name='compare'),
    path('<slug:slug>/claim/', views.claim_restaurant_view, name='claim'),
    path('<slug:slug>/', views.restaurant_detail_view, name='detail'),
    path('<slug:slug>/review/', views.add_review_view, name='add_review'),
    
    # REST API endpoints
    path('api/list/', api_views.RestaurantListAPIView.as_view(), name='api_list'),
    path('api/<int:restaurant_id>/live-tables/', api_views.LiveTableStatusAPIView.as_view(), name='api_live_tables'),
    path('api/<int:restaurant_id>/compare/', api_views.RestaurantCompareAPIView.as_view(), name='api_compare'),
]
