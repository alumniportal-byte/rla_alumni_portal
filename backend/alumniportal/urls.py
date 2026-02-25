from django.urls import path
from . import views

urlpatterns = [
    path("api/slides/", views.api_slides),
    path("api/testimonials/", views.api_testimonials),
    path("api/settings/", views.api_settings),
    path("api/events/",views.api_events),
    path('api/bearers/', views.api_office_bearers, name='api_office_bearers'),
    path('api/committee/', views.api_committee, name='api_committee'),
    path('api/committee/members/', views.api_committee_members, name='api_committee_members'),
    path('api/alumni/', views.api_alumni_list, name='api_alumni_list'),
    # Sabhi categories fetch karne ke liye
    path('api/alumni-categories/', views.get_categories, name='get_categories'),
    # Specific category ke members fetch karne ke liye
    path('api/wall-of-fame/<int:category_id>/', views.get_wall_of_fame, name='get_wall_of_fame'),
    path('api/event/', views.get_events, name='get_events'),
    path('api/event/<int:event_id>/', views.get_event_photos, name='get_event_photos'),
    path('api/suggestion-link/', views.api_suggestion_link, name='api_suggestion_link'),
    path('api/grouped-events/', views.get_grouped_events, name='get_grouped_events'),
    path('api/faculty/', views.api_faculty_list, name='api_faculty_list'),
    path('api/staff/', views.api_staff_list, name='api_staff_list'),
]