from django.urls import path
from . import views 

urlpatterns = [
    # Dashboard Home
    path('', views.dashboard_home, name='dashboard'),

    # Home Tab Features
    path("slider/", views.slider, name="slider"),
    path("testimonials/", views.testimonials, name="testimonials"),

    # About / Committee Section
    path("office-bearers/", views.office_bearers, name="office_bearers"),
    path("association-bearers/", views.association_bearers, name="association_bearers"),
    path("college-committee/", views.college_committee, name="college_committee"),
    path("committee-members/", views.committee_members, name="committee_members"),

    # Alumni Section (Jo aap abhi bana rahe the)
    path("alumni-register/", views.alumni_register, name="alumni_register"),
    path("wall-of-fame/", views.wall_of_fame, name="wall_of_fame"),
    path("gallery/", views.gallery_view, name="gallery_view"),
    path('gallery/<int:id>/', views.folder_detail, name='folder_detail'), # New Page

    # Admin & Exports
    path("export/", views.export_dashboard, name="export_dashboard"),
    path("export/testimonials/", views.export_testimonials, name="export_testimonials"),
    path("export/alumni/", views.export_alumni_register, name="export_alumni"),
    path("export/wall-of-fame/", views.export_wall_of_fame, name="export_wall"),
    path("admin-control/", views.admin_control, name="admin_control"),
    path('backup-download/', views.backup_download, name='backup_download'),
    path("dashboard/faculty/", views.manage_faculty, name="manage_faculty"),
    path("dashboard/staff/", views.manage_staff, name="manage_staff"),
    path("dashboard/alumni-events/", views.manage_alumni_events, name="manage_alumni_events"),
]
