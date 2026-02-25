import email
from django.contrib import admin
from .models import *
from alumniportal.models import CollegeOfficeBearer, CommitteeMember, CommitteeYear, DistinguishedAlumni, DistinguishedCategory, EventFolder, EventImage, HomeSlider, RegisterLink, SuggestionLink, Testimonial, Alumni,SystemSetting
# HOME SLIDER
# =============================
@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "created_at", "position")
    search_fields = ("image",)
    list_editable = ("image","position")


# =============================
# TESTIMONIAL
# =============================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course","position","message","linkedin","image","batch", "created_at")
    search_fields = ("name", "course", "batch")
    list_filter = ("course", "batch","name")
    list_editable = ("name", "course", "batch", "position",'message','linkedin','image')


# =============================
# OFFICE BEARERS
# =============================
@admin.register(AssociationBearer)
class AssociationBearerAdmin(admin.ModelAdmin):
    list_display = ("position", "name", "designation", "qualification", "message", "image")
    search_fields = ("name", "designation", "qualification", "message", "image")
    list_editable = ("position","name", "designation", "qualification", "message", "image")
    list_display_links = None
    ordering = ('position',)
@admin.register(CollegeOfficeBearer)
class CollegeOfficeBearerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "designation","image","position")
    search_fields = ("name", "designation")
    list_editable = ("designation","name","position",'image')
# =============================
# COMMITTEE YEAR
# =============================
@admin.register(CommitteeYear)
class CommitteeYearAdmin(admin.ModelAdmin):
    list_display = ("id", "year_range", "position")
    search_fields = ("year_range",)
    list_editable = ("year_range","position")


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "committee", "role", "name", "department", "position")
    list_filter = ("committee", "role", "department")
    search_fields = ("name", "role", "department", "committee")
    list_editable = ("committee", "role", "name", "department", "position")


# =============================
# REGISTERED ALUMNI
# =============================
@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course", "batch", "email","phone", "current_designation","is_registered", "position")
    list_filter = ("course", "batch", "is_registered")
    search_fields = ("name","course", "batch", "email", "phone", "current_designation", "is_registered")
    list_editable = ("position", "name", "course", "batch", "email","phone","current_designation","is_registered")


# =============================
# DISTINGUISHED CATEGORY
# =============================
@admin.register(DistinguishedCategory)
class DistinguishedCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "position")
    list_editable = ("title", "position")


@admin.register(DistinguishedAlumni)
class DistinguishedAlumniAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "course", "batch", "current_position", "position", "image")
    list_filter = ("category", "course", "batch","name")
    search_fields = ("name", "course", "batch", "current_position", "category")
    list_editable = ("name", "category", "course", "batch", "current_position", "position", "image")


# =============================
# EVENT FOLDER
# =============================
@admin.register(EventFolder)
class EventFolderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "position")
    list_editable = ("title", "position")

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ("id", "folder", "image", "position")
    list_filter = ("folder",)
    search_fields = ("folder__title",)
    list_editable = ("folder", "image", "position")


# =============================
# LINKS
# =============================
admin.site.register(RegisterLink)
admin.site.register(SuggestionLink)

from django.contrib import admin
from .models import (
    AcademicDepartment, 
    AdminDepartment, 
    Faculty, 
    NonTeachingStaff, 
    EventCategory, 
    AlumniEvent
)

# --- 1. DEPARTMENTS SETUP ---
@admin.register(AcademicDepartment)
class AcademicDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('name',) # Aap admin list se hi department name change kar sakte ho

@admin.register(AdminDepartment)
class AdminDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('name',) # Aap admin list se hi department name change kar sakte ho


# --- 2. FACULTY SETUP ---
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'designation', 'order')
    list_filter = ('department','designation') # Right side mein filter aa jayega department wise
    search_fields = ('name', 'department','designation')
    list_editable = ('name', 'department', 'designation','order',) # Aap admin list se hi order change kar sakte ho


# --- 3. NON-TEACHING STAFF SETUP ---
@admin.register(NonTeachingStaff)
class NonTeachingStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'designation', 'order')
    list_filter = ('department','designation') # Right side mein filter aa jayega department wise
    search_fields = ('name', 'department','designation')
    list_editable = ('name', 'department', 'designation','order') # Aap admin list se hi order change kar sakte ho


# --- 4. EVENTS SETUP ---
@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('name',) # Aap admin list se hi category name change kar sakte ho

@admin.register(AlumniEvent)
class AlumniEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'year_session', 'organized_by', 'date','resource_person', 'batch')
    list_filter = ('category', 'year_session', 'organized_by', 'date', 'batch')
    search_fields = ('title', 'category', 'year_session', 'organized_by', 'date')
    list_display_links = None # Isse koi bhi field clickable nahi rahegi, sirf edit karne ke liye hi editable fields pe click karna padega
    date_hierarchy = 'date' # Top par calendar navigation aa jayega
    list_editable = ('title', 'category', 'year_session', 'organized_by', 'date','resource_person', 'batch')