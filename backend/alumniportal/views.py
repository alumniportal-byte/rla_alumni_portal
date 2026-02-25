from django.shortcuts import render

from django.http import JsonResponse
from .models import HomeSlider, SuggestionLink, Testimonial,RegisterLink,EventFolder,EventImage,CollegeOfficeBearer


# ===============================
# 🔹 API: SLIDES
# ===============================
def api_slides(request):
    data = [
        {
            "image": s.image.url if s.image else ""
        }
        for s in HomeSlider.objects.all()
    ]
    return JsonResponse(data, safe=False)


# ===============================
# 🔹 API: TESTIMONIALS
# ===============================
def api_testimonials(request):
    data = [
        {
            "name": t.name,
            "course": t.course,
            "batch": t.batch,
            "text": t.message,
            "linkedin_url": t.linkedin,
            "image": t.image.url if t.image else ""
        }
        for t in Testimonial.objects.all()
    ]
    return JsonResponse(data, safe=False)


# ===============================
# 🔹 API: SETTINGS
# ===============================
def api_settings(request):

    setting = RegisterLink.objects.first()

    if not setting:
        return JsonResponse({"register_link": "#"})

    return JsonResponse({
        "register_link": setting.register_url
    })

from django.http import JsonResponse
from .models import EventFolder, EventImage

def api_events(request):
    data = []
    folders = EventFolder.objects.all()
    
    for folder in folders:
        # Get the first image associated with this folder
        first_image = EventImage.objects.filter(folder=folder).first()
        
        cover_url = ""
        if first_image and first_image.image:
            try:
                cover_url = request.build_absolute_uri(first_image.image.url)
            except Exception:
                cover_url = "https://via.placeholder.com/300" # Fallback if URL fails
        else:
            # If no image exists, provide a placeholder so the card isn't empty
            cover_url = "https://via.placeholder.com/300"
            
        data.append({
            "title": folder.title,
            "cover": cover_url
        })
        
    return JsonResponse(data, safe=False)

from django.http import JsonResponse
from .models import AssociationBearer

def api_office_bearers(request):
    data = []
    # Model ke Meta class mein ordering=['position'] hai, to ye apne aap sorted aayega
    bearers = AssociationBearer.objects.all().order_by('position')
    
    for b in bearers:
        # --- Image URL Logic (Same as your api_events) ---
        image_url = ""
        if b.image:
            try:
                # Ye image ka complete link banata hai (http://localhost:8000/media/...)
                image_url = request.build_absolute_uri(b.image.url)
            except Exception:
                image_url = "https://via.placeholder.com/150" # Fallback
        else:
            image_url = "https://via.placeholder.com/150" # Placeholder agar image na ho

        # --- Data Append ---
        data.append({
            "id": b.id,
            "name": b.name,
            "position": b.designation, 
            "qualification": b.qualification,
            "message": b.message,
            "image": image_url
        })
        
    return JsonResponse(data, safe=False)
from django.http import JsonResponse
from .models import CommitteeYear, CommitteeMember

def api_committee(request):
    data = []
    # Years ko fetch karte hain (Meta ordering='position' hai to sorted aayenge)
    committee_years = CommitteeYear.objects.all()

    for year_obj in committee_years:
        members_data = []
        
        # Is specific year ke members nikalte hain
        members = CommitteeMember.objects.filter(committee=year_obj)
        
        for m in members:
            members_data.append({
                "id": m.id,
                "role": m.role,            # e.g. "Convener"
                "name": m.name,            # e.g. "Dr. Amit"
                "department": m.department, # e.g. "Computer Science"
                      
            })

        data.append({
            "id": year_obj.id,
            "session": year_obj.year_range, # React 'session' dhund raha hai, Model 'year_range' de raha hai
            "members": members_data
        })

    return JsonResponse(data, safe=False)

def api_committee_members(request):
    # Sirf teachers ka data fetch ho raha hai
    members = CollegeOfficeBearer.objects.all().order_by('position')
    
    data = []
    for m in members:
        data.append({
            "id": m.id,
            "name": m.name,
            "designation": m.designation,
            # Image URL handle kar rahe hain (Cloudinary ya Local)
            "image": m.image.url if m.image else "/placeholder.jpg"
        })
    
    return JsonResponse(data, safe=False)

from django.http import JsonResponse
from .models import Alumni

def api_alumni_list(request):
    # Search aur Filters hum frontend pe handle kar rahe hain, 
    # isliye yahan se saara data bhej rahe hain.
    alumni_queryset = Alumni.objects.all().order_by('name')
    
    data = []
    for person in alumni_queryset:
        data.append({
            "id": person.id,
            "name": person.name,
            "course": person.course,
            "batch": person.batch,
            "is_registered": person.is_registered,
        })
    
    return JsonResponse(data, safe=False)

from django.http import JsonResponse
from .models import DistinguishedCategory, DistinguishedAlumni

def get_categories(request):
    categories = DistinguishedCategory.objects.all()
    data = [{ "id": c.id, "name": c.title} for c in categories]
    return JsonResponse(data, safe=False)

def get_wall_of_fame(request, category_id):
    members = DistinguishedAlumni.objects.filter(category_id=category_id).order_by('-batch')
    data = [{
        "name": m.name,
        "photo": m.image.url if m.image else "",
        "position": m.current_position,
        "course": m.course,
        "batch": m.batch
    } for m in members]
    return JsonResponse(data, safe=False)

def get_event_photos(request, event_id):
    images = EventImage.objects.filter(folder_id=event_id).order_by('position')
    data = [{"url": request.build_absolute_uri(img.image.url)} for img in images]
    return JsonResponse(data, safe=False)

def get_events(request):
    data = []
    folders = EventFolder.objects.all().order_by('-created_at')
    
    for folder in folders:
        first_image = EventImage.objects.filter(folder=folder).first()
        cover_url = "https://via.placeholder.com/300"
        if first_image and first_image.image:
            cover_url = request.build_absolute_uri(first_image.image.url)
            
        data.append({
            "id": folder.id,
            "title": folder.title,
            "created_at": folder.created_at.strftime("%d %b %Y") if hasattr(folder, 'created_at') else "",
            "cover": cover_url
        })
    return JsonResponse(data, safe=False)

 # Aapne pehle settings ke liye use kiya tha

def api_suggestion_link(request):
    # Hum pehla record uthayenge jisme suggestion_url ho
    # Agar model mein suggestion_url nahi hai to add kar dena ya alag model bana lena
    setting = SuggestionLink.objects.first()

    if not setting:
        return JsonResponse({"suggestion_link": "#"})

    return JsonResponse({
        "suggestion_link": setting.form_url
    })


# Dropdowns ko populate karne ke liye
from django.http import JsonResponse
from .models import AlumniEvent, EventCategory
from collections import defaultdict

def get_grouped_events(request):
    # Category -> Session -> Events ki hierarchy banayenge
    events_qs = AlumniEvent.objects.all().order_by('category__name', '-year_session', '-date')
    
    grouped_data = {}

    for e in events_qs:
        cat_name = e.category.name
        session = e.year_session
        
        if cat_name not in grouped_data:
            grouped_data[cat_name] = {}
        
        if session not in grouped_data[cat_name]:
            grouped_data[cat_name][session] = []
            
        grouped_data[cat_name][session].append({
            "id": e.id,
            "title": e.title,
            "organized_by": e.organized_by,
            "resource_person": e.resource_person or "N/A",
            "batch": e.batch or "N/A",
            "date": e.date.strftime("%d %b %Y"),
            "image": request.build_absolute_uri(e.image.url) if e.image else None,
            "report": request.build_absolute_uri(e.report_pdf.url) if e.report_pdf else None,
        })
    
    return JsonResponse(grouped_data, safe=False)

from django.http import JsonResponse
from .models import AcademicDepartment, Faculty, NonTeachingStaff # Make sure model names match

def api_faculty_list(request):
    # Saare departments uthao
    departments = AcademicDepartment.objects.all()
    data = []

    for dept in departments:
        # Har department ke teachers nikalo
        teachers_list = []
        # 'teachers' wahi related_name hai jo tumne ForeignKey mein diya hai
        teachers = dept.teachers.all().order_by('order') 
        
        for t in teachers:
            teachers_list.append({
                "name": t.name,
                "designation": t.designation,
                "image": t.image.url if t.image else None,
            })
        
        # Department ka data structure
        data.append({
            "id": dept.id,
            "name": dept.name,
            "teachers": teachers_list
        })

    return JsonResponse(data, safe=False)

from .models import AdminDepartment

def api_staff_list(request):
    # Hum AdminDepartment se data uthayenge taaki grouping automatic ho jaye
    departments = AdminDepartment.objects.prefetch_related('staff_members').all()
    
    data = []
    for dept in departments:
        data.append({
            "id": dept.id,
            "name": dept.name, # Ye banega Accordion Title (e.g., Accounts Section)
            "staff_members": list(dept.staff_members.all().values('name', 'designation', 'order'))
        })
    
    return JsonResponse(data, safe=False)