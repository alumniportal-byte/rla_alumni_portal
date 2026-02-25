from collections import defaultdict
from django.utils import timezone
from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import csv
import json
from django.http import HttpResponse
from urllib3 import request
from alumniportal.models import Alumni,  DistinguishedAlumni, EventFolder, EventImage, SystemSetting, Testimonial ,AdminProfile
from alumniportal.models import HomeSlider,CollegeOfficeBearer,CommitteeYear,CommitteeMember,TableColumnSetting
from alumniportal.models import AcademicDepartment, AdminDepartment, Faculty, NonTeachingStaff, EventCategory, AlumniEvent
def is_superadmin(user):
    try:
        return user.adminprofile.role == "superadmin"
    except:
        return False
@login_required
def dashboard_home(request):

    context = {
        "alumni_count": Alumni.objects.count(),
        "event_count": EventImage.objects.count(),
        "testimonial_count": Testimonial.objects.count(),
        "latest_alumni": Alumni.objects.all().order_by("-id")[:50],
        "registered_count": Alumni.objects.filter(is_registered=True).count(),
        "pending_count": Alumni.objects.filter(is_registered=False).count(),
        "wall_count": DistinguishedAlumni.objects.count(),
        "teachers_count": Faculty.objects.count(),
        "non_teachers_count": NonTeachingStaff.objects.count(),
        "departments_count": AcademicDepartment.objects.count(),
        "admin_departments_count": AdminDepartment.objects.count(),
        "events_count": AlumniEvent.objects.count(),

    }

    return render(request, "dashboard/home.html", context)


from .forms import AlumniForm, CollegeCommitteeForm, SliderForm , TestimonialForm
from django.shortcuts import redirect, get_object_or_404

def slider(request):

    sliders = HomeSlider.objects.all().order_by('-id')
    form = SliderForm()

    # UPLOAD
    if request.method == "POST" and 'upload' in request.POST:
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("slider")

    # DELETE
    if request.method == "POST" and 'delete' in request.POST:
        slider_id = request.POST.get("slider_id")
        slider_obj = get_object_or_404(HomeSlider, id=slider_id)
        slider_obj.delete()
        return redirect("slider")

    return render(request, "dashboard/slider.html", {
        "sliders": sliders,
        "form": form
    })

def testimonials(request):

    testimonials = Testimonial.objects.all().order_by('-id').filter(is_deleted=False)
    edit_id = request.GET.get("edit")
    instance = None

    if edit_id:
        instance = get_object_or_404(Testimonial,id=edit_id)
    form = TestimonialForm(instance=instance)

      # ADD / UPDATE
    if request.method == "POST" and 'upload' in request.POST:

        if request.POST.get("tid"):
            instance = get_object_or_404(
                Testimonial,
                id=request.POST.get("tid")
            )

        form = TestimonialForm(
            request.POST,
            request.FILES,
            instance=instance
        )

        if form.is_valid():
            form.save()
            return redirect("testimonials")

    # DELETE
    if request.method == "POST" and 'delete' in request.POST:
        tid = request.POST.get("tid")
        obj = get_object_or_404(Testimonial,id=tid)
        obj.delete()
        return redirect("testimonials")

    return render(request,"dashboard/testimonials.html",{
        "form":form,
        "testimonials":testimonials,
        "edit_id":edit_id
    })

def office_bearers(request):
    return render(request, "dashboard/office_bearers.html")

from alumniportal.models import AssociationBearer
from .forms import AssociationBearerForm
from django.shortcuts import render,redirect,get_object_or_404


def association_bearers(request):
    bearers = AssociationBearer.objects.all().order_by('position')
    
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(AssociationBearer, id=edit_id) if edit_id else None
    
    # Faculty code jaisa logic: Pehle default form define karo
    form = AssociationBearerForm(instance=instance)

    if request.method == "POST":
        if 'upload' in request.POST:
            bid = request.POST.get("bid")
            instance = get_object_or_404(AssociationBearer, id=bid) if bid else None
            
            # Yahan request.FILES zaroori hai
            form = AssociationBearerForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("association_bearers")
        
        elif 'delete' in request.POST:
            bid = request.POST.get("bid")
            get_object_or_404(AssociationBearer, id=bid).delete()
            return redirect("association_bearers")

    return render(request, "dashboard/association_bearers.html", {
        "form": form, 
        "bearers": bearers, 
        "edit_id": edit_id
    })
def college_committee(request):
    data = CommitteeMember.objects.all().order_by('committee','position')
    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item.committee].append(item)
    edit_id = request.GET.get("edit")
    instance = None

    if edit_id:
        instance = get_object_or_404(CommitteeMember,id=edit_id)
    form = CollegeCommitteeForm(instance=instance)

    # ADD / UPDATE
    if request.method == "POST" and 'upload' in request.POST:

        if request.POST.get("cid"):
            instance = get_object_or_404(
                CommitteeMember,
                id=request.POST.get("cid")
            )

        form = CollegeCommitteeForm(
            request.POST,
            request.FILES,
            instance=instance
        )

        if form.is_valid():
            form.save()
            return redirect("college_committee")

    # DELETE    
    if request.method == "POST" and 'delete' in request.POST:
        cid = request.POST.get("cid")
        obj = get_object_or_404(CommitteeMember,id=cid)
        obj.delete()
        return redirect("college_committee")
    return render(request, "dashboard/college_committee.html", {
        "data": data, "form": form ,"edit_id":edit_id,"grouped_data":dict(grouped_data)})


from .forms import CommitteeMemberForm
from alumniportal.models import CollegeOfficeBearer
def committee_members(request):
    members = CollegeOfficeBearer.objects.all().order_by('position')
    form = CommitteeMemberForm()
    edit_id = request.GET.get("edit")
    instance = None

    if edit_id:
        instance = get_object_or_404(CollegeOfficeBearer,id=edit_id)
        form = CommitteeMemberForm(instance=instance)

    # ADD / UPDATE
    if request.method == "POST" and 'upload' in request.POST:

        if request.POST.get("cmid"):
            instance = get_object_or_404(
                CollegeOfficeBearer,
                id=request.POST.get("cmid")
            )

        form = CommitteeMemberForm(
            request.POST,
            request.FILES,
            instance=instance
        )

        if form.is_valid():
            form.save()
            return redirect("committee_members")

    # DELETE    
    if request.method == "POST" and 'delete' in request.POST:
        cmid = request.POST.get("cmid")
        obj = get_object_or_404(CollegeOfficeBearer,id=cmid)
        obj.delete()
        return redirect("committee_members")
    return render(request, "dashboard/committee_members.html", {
        "members": members,
        "form": form,
        "edit_id":edit_id
    })

from alumniportal.models import Alumni
from django.db.models import Q
import pandas as pd
from django.db.models import Q

# dashboard/views.py
import pandas as pd # Pandas import karna na bhulein
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AlumniForm, AlumniUploadForm
from django.contrib import messages # Error dikhane ke liye

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from alumniportal.models import Alumni  # Model import check karein
from .forms import AlumniForm, AlumniUploadForm
import pandas as pd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def alumni_register(request):
    
    # ==========================================
    # 1. FILTER & SEARCH LOGIC
    # ==========================================
    search = request.GET.get("search", "")
    batch = request.GET.get("batch", "")
    course = request.GET.get("course", "")
    Status = request.GET.get("Status", "")

    # Default: Show latest added first
    alumni = Alumni.objects.all().order_by("-id").filter(is_deleted=False)  # Deleted records ko filter karein

    if search:
        alumni = alumni.filter(name__icontains=search)
    if batch:
        alumni = alumni.filter(batch=batch)
    if course:
        alumni = alumni.filter(course=course)
    if Status:
        if Status == "True":
            alumni = alumni.filter(is_registered=True)
        elif Status == "False":
            alumni = alumni.filter(is_registered=False)

    paginator = Paginator(alumni, 200)  # Show 200 alumni per page
    
    page_number = request.GET.get('page')
    try:
        alumni = paginator.page(page_number)
    except PageNotAnInteger:
        # Agar page number nahi hai to first page dikhayein
        alumni = paginator.page(1)
    except EmptyPage:
        # Agar page number range se bahar hai to last page dikhayein
        alumni = paginator.page(paginator.num_pages)

    # Dropdowns ke liye unique values
    batches = Alumni.objects.values_list("batch", flat=True).distinct().order_by("batch")
    courses = Alumni.objects.values_list("course", flat=True).distinct().order_by("course")
    
    # ==========================================
    # 2. FORMS INITIALIZATION
    # ==========================================
    form = AlumniForm()           # Manual Entry ke liye
    upload_form = AlumniUploadForm() # Excel Upload ke liye
    
    # Agar Edit button click kiya ho
    edit_id = request.GET.get("edit")
    if edit_id:
        instance = get_object_or_404(Alumni, id=edit_id)
        form = AlumniForm(instance=instance)

    # ==========================================
    # 3. POST REQUEST HANDLING
    # ==========================================
    if request.method == "POST":
        # ---------------------------------------
        # CASE A: BULK UPLOAD (Excel/CSV)
        # ---------------------------------------
        if 'bulk_upload' in request.POST:
            upload_form = AlumniUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                file = request.FILES["file"]
                try:
                    # File read karein
                    if file.name.endswith(".csv"):
                        df = pd.read_csv(file)
                    elif file.name.endswith((".xlsx", ".xls")):
                        df = pd.read_excel(file)
                    else:
                        messages.error(request, "Invalid file format. Please use .csv or .xlsx")
                        return redirect("alumni_register")

                    # --- KEY FIX: DATA CLEANING ---
                    
                    # 1. Khali values (NaN) ko empty string banayein
                    df = df.fillna('')

                    # 2. Headers ko lowercase aur underscore me badle
                    # Example: "Current Designation" -> "current_designation"
                    # Example: "Student Name" -> "student_name"
                    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

                    count = 0
                    for _, row in df.iterrows():
                        # Name check (Empty name skip karein)
                        name_val = str(row.get("name", "")).strip()
                        if not name_val:
                            continue

                        # Designation Fix: Check both keys
                        # Pehle 'current_designation' dhunde, na mile to 'designation'
                        desig_val = row.get("current_designation", row.get("designation", ""))

                        # Registration Fix: Handle Yes/No/True/1
                        reg_raw = str(row.get("is_registered", row.get("registered", ""))).lower().strip()
                        is_reg_bool = True if reg_raw in ["true", "yes", "1", "registered", "y"] else False

                        # Database me save karein
                        Alumni.objects.create(
                            name=name_val,
                            course=str(row.get("course", "")).strip(),
                            batch=str(row.get("batch", "")).strip(),
                            current_designation=str(desig_val).strip(),
                            email=str(row.get("email", "")).strip(),
                            phone=str(row.get("phone", "")).strip(),
                            is_registered=is_reg_bool
                        )
                        count += 1
                    
                    messages.success(request, f"Successfully uploaded {count} alumni records!")
                
                except Exception as e:
                    messages.error(request, f"Error processing file: {str(e)}")
                
                return redirect("alumni_register")

        # ---------------------------------------
        # CASE B: MANUAL ADD / UPDATE
        # ---------------------------------------
        elif 'add_single' in request.POST:
            # Check if updating existing
            instance = None
            aid = request.POST.get("aid")
            if aid:
                instance = get_object_or_404(Alumni, id=aid)

            form = AlumniForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                msg = "Alumni updated!" if instance else "Alumni added!"
                messages.success(request, msg)
                return redirect("alumni_register")
            else:
                messages.error(request, "Error in form. Please check fields.")

        # ---------------------------------------
        # CASE C: DELETE
        # ---------------------------------------
        elif 'delete' in request.POST:
            aid = request.POST.get("aid")
            if aid:
                obj = get_object_or_404(Alumni, id=aid)
                obj.delete()
                messages.success(request, "Record deleted successfully.")
            return redirect("alumni_register")
    visible_columns = TableColumnSetting.objects.filter(
    user=request.user,
    table_name="alumni",
    is_visible=True
    ).values_list("column_name",flat=True)

    try:
        settings = SystemSetting.objects.first()
        visible_columns = json.loads(settings.alumni_columns) if settings and settings.alumni_columns else ["sno","name","course","batch","phone","status"]
    except:
        visible_columns = ["sno","name","course","batch","phone","status"]


    # ==========================================
    # 4. RENDER TEMPLATE
    # ==========================================
    context = {
        "alumni": alumni,
        "batches": batches,
        "courses": courses,
        "form": form,
        "upload_form": upload_form,
        "edit_id": edit_id,
        "current_search": search,
        "current_batch": batch,
        "current_status": Status,
        "current_course": course,
        "visible_columns": visible_columns,
    }
    return render(request, "dashboard/alumni_register.html", context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from alumniportal.models import DistinguishedAlumni, DistinguishedCategory
from .forms import WallUploadForm # WallForm agar use nahi ho raha to hata dein
import pandas as pd


from django.core.files.base import ContentFile
import requests  # Image download ke liye
from .forms import  WallForm

# ...existing code...
# ...existing code...
def wall_of_fame(request):
    import re, os, zipfile, tempfile, traceback
    from django.db import IntegrityError
    from django.utils.text import slugify
    from django.shortcuts import render, get_object_or_404, redirect
    from django.contrib import messages

    categories = DistinguishedCategory.objects.all().order_by("position").filter(is_deleted=False)
    category_id = request.GET.get("category")

    alumni = DistinguishedAlumni.objects.all().order_by("category__position", "position").filter(is_deleted=False)
    if category_id:
        try:
            alumni = alumni.filter(category__id=category_id)
        except Exception:
            pass

    # Edit logic: GET request se instance load karna
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(DistinguishedAlumni, id=edit_id) if edit_id else None
    
    upload_form = WallUploadForm()
    form = WallForm(instance=instance)

    # POST handling
    if request.method == "POST":
        try:
            # ---------- BULK UPLOAD ----------
            if "bulk_upload" in request.POST:
                upload_form = WallUploadForm(request.POST, request.FILES or None)
                if not upload_form.is_valid():
                    messages.error(request, "Upload form invalid.")
                    return redirect("wall_of_fame")

                file = request.FILES.get("file")
                if not file:
                    messages.error(request, "No file uploaded.")
                    return redirect("wall_of_fame")

                # read file
                if file.name.lower().endswith(".csv"):
                    df = pd.read_csv(file, dtype=str, keep_default_na=False)
                else:
                    df = pd.read_excel(file, dtype=str)

                # normalize headers and rows
                df = df.fillna("")
                df.columns = (
                    df.columns.astype(str)
                    .str.strip()
                    .str.lower()
                    .str.replace(r"[^\w\s]", "", regex=True)
                    .str.replace(r"\s+", "_", regex=True)
                )

                if "name" not in df.columns:
                    messages.error(request, "File must contain a 'name' column.")
                    return redirect("wall_of_fame")

                # optional images ZIP
                images_map = {}
                zip_file = request.FILES.get("images_zip")
                if zip_file:
                    tmpdir = tempfile.mkdtemp()
                    try:
                        with zipfile.ZipFile(zip_file) as z:
                            z.extractall(tmpdir)
                        for root, _, files in os.walk(tmpdir):
                            for fname in files:
                                images_map[fname.lower()] = os.path.join(root, fname)
                    except Exception as ze:
                        print("ZIP extract error:", ze)

                default_category, _ = DistinguishedCategory.objects.get_or_create(title="Uncategorized")
                created = updated = 0
                errors = []

                for idx, row in df.iterrows():
                    row_no = idx + 2
                    try:
                        name_val = str(row.get("name", "") or "").strip()
                        if not name_val:
                            errors.append(f"Row {row_no}: name empty")
                            continue

                        cat_name = str(row.get("category", "") or "").strip()
                        if cat_name:
                            cat_name_clean = cat_name.title()
                            category_obj = DistinguishedCategory.objects.filter(title__iexact=cat_name_clean).first()
                            if not category_obj:
                                category_obj = DistinguishedCategory.objects.create(title=cat_name_clean)
                        else:
                            category_obj = default_category

                        pos_raw = str(row.get("position", "") or "").strip()
                        position_val = int(pos_raw) if pos_raw.isdigit() else 0
                        current_pos = str(row.get("current_position", "") or "").strip()
                        course_val = str(row.get("course", "") or "").strip()
                        batch_val = str(row.get("batch", "") or "").strip()

                        qs = DistinguishedAlumni.objects.filter(name__iexact=name_val, category=category_obj)
                        obj = qs.first()
                        if obj:
                            obj.course = course_val or obj.course
                            obj.batch = batch_val or obj.batch
                            obj.current_position = current_pos or obj.current_position
                            obj.position = position_val or obj.position
                            obj.save()
                            target_obj = obj
                            updated += 1
                        else:
                            try:
                                target_obj = DistinguishedAlumni.objects.create(
                                    name=name_val,
                                    course=course_val,
                                    batch=batch_val,
                                    current_position=current_pos,
                                    category=category_obj,
                                    position=position_val
                                )
                                created += 1
                            except IntegrityError:
                                target_obj = DistinguishedAlumni.objects.create(
                                    name=name_val,
                                    course=course_val,
                                    batch=batch_val,
                                    current_position=current_pos,
                                    category=default_category,
                                    position=position_val
                                )
                                created += 1

                        # image handling: URL or filename from ZIP
                        image_raw = str(row.get("image_url", "") or "").strip()
                        if image_raw and image_raw.lower() != "null":
                            if image_raw.lower().startswith("http"):
                                try:
                                    img_url = image_raw
                                    if "drive.google.com" in img_url:
                                        m = re.search(r"/d/([a-zA-Z0-9_-]+)", img_url) or re.search(r"id=([a-zA-Z0-9_-]+)", img_url)
                                        if m:
                                            img_url = f"https://drive.google.com/uc?export=download&id={m.group(1)}"
                                    resp = requests.get(img_url, timeout=15)
                                    if resp.status_code == 200 and resp.content:
                                        ctype = resp.headers.get("content-type", "")
                                        ext = ".jpg"
                                        if "png" in ctype:
                                            ext = ".png"
                                        elif "gif" in ctype:
                                            ext = ".gif"
                                        filename = f"{slugify(name_val)[:50]}_{target_obj.id}{ext}"
                                        target_obj.image.save(filename, ContentFile(resp.content), save=True)
                                    else:
                                        errors.append(f"Row {row_no}: image download returned {resp.status_code}")
                                except Exception as ie:
                                    errors.append(f"Row {row_no}: image download failed ({str(ie)[:100]})")
                            else:
                                # try match filename in uploaded ZIP
                                key = os.path.basename(image_raw).lower()
                                local_path = images_map.get(key)
                                if local_path and os.path.exists(local_path):
                                    with open(local_path, "rb") as f:
                                        ext = os.path.splitext(key)[1] or ".jpg"
                                        filename = f"{slugify(name_val)[:50]}_{target_obj.id}{ext}"
                                        target_obj.image.save(filename, ContentFile(f.read()), save=True)
                                else:
                                    errors.append(f"Row {row_no}: image file '{image_raw}' not found")

                    except Exception as row_e:
                        errors.append(f"Row {row_no}: {str(row_e)[:120]}")
                        continue

                msg = f"✅ Uploaded: {created}, Updated: {updated}."
                if errors:
                    msg += f" ⚠️ {len(errors)} rows had issues (see server log)."
                    for e in errors[:10]:
                        print("WOF UPLOAD ERROR:", e)
                messages.success(request, msg)
                return redirect("wall_of_fame")

            elif "save_single" in request.POST:
                did = request.POST.get("did") or request.GET.get("edit") # Dono jagah check karo
                    
                if did:
                    instance = get_object_or_404(DistinguishedAlumni, id=did)
                    form = WallForm(request.POST, request.FILES, instance=instance)
                else:
                    form = WallForm(request.POST, request.FILES)

                if form.is_valid():
                    form.save()
                    messages.success(request, "Data Saved!")
                    return redirect(request.path)
                else:
                    messages.error(request, "Form error. Please check the fields.")
                    return redirect(request.path)
            # ---------- DELETE ----------
            elif "delete" in request.POST:
                did = request.POST.get("did")
                obj = get_object_or_404(DistinguishedAlumni, id=did)
                obj.delete()
                messages.success(request, "Deleted successfully.")
                return redirect(request.path)


        except Exception as e:
            traceback.print_exc()
            messages.error(request, f"Error: {str(e)}")
            return redirect(request.path)
        
    return render(request, "dashboard/wall_of_fame.html", {
        "alumni": alumni,
        "categories": categories,
        "upload_form": upload_form,
        "form": form,
        "selected_category": int(category_id) if category_id else None,
        "edit_id": edit_id
    })
# ...existing code...
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EventImageForm

# ==========================================
# 1. GALLERY VIEW (Upload Logic)
# ==========================================
def gallery_view(request):
    folders = EventFolder.objects.all().order_by('-id')
    form = EventImageForm()

    if request.method == "POST":
        
        # --- UPLOAD LOGIC ---
        if 'upload' in request.POST:
            # 1. Form me Data aur Files dono pass karein
            form = EventImageForm(request.POST, request.FILES)
            
            # 2. Images ki list alag se nikalein
            images_list = request.FILES.getlist('images')

            if form.is_valid() or images_list:
                folder_obj = form.cleaned_data.get('folder')
                new_folder_name = form.cleaned_data.get('new_folder')

            target_folder = None

            if new_folder_name:
                target_folder = EventFolder.objects.create(title=new_folder_name)
            elif folder_obj:
                target_folder = folder_obj
            else:
                messages.error(request, "Select or create a folder.")
                return redirect('gallery_view')

            if not images_list:
                messages.error(request, "No images selected!")
                return redirect('gallery_view')

            count = 0
            for img in images_list:
                EventImage.objects.create(folder=target_folder, image=img)
                count += 1

            messages.success(request, f"{count} images uploaded.")
            return redirect('gallery_view')

    return render(request, 'dashboard/gallery.html', {
        'folders': folders, 
        'form': form
    })

# ==========================================
# 2. FOLDER DETAIL (Edit/Delete Logic)
# ==========================================
def folder_detail(request, id):
    # Folder fetch karein ya 404 error de
    folder = get_object_or_404(EventFolder, id=id)
    
    # Images fetch karein position ke hisab se sort karke
    images = folder.images.all().order_by('position') 

    if request.method == "POST":
        
        # A. Delete Single Image
        if 'delete_image' in request.POST:
            img_id = request.POST.get('img_id')
            try:
                img_obj = EventImage.objects.get(id=img_id)
                img_obj.delete()
                messages.success(request, "Image deleted.")
            except EventImage.DoesNotExist:
                messages.error(request, "Image not found.")
            return redirect('folder_detail', id=id)

        # B. Update Positions (Drag & Drop sorting ke liye future proofing)
        elif 'update_positions' in request.POST:
            for key, value in request.POST.items():
                if key.startswith('pos_'):
                    # key format: pos_15 (where 15 is image ID)
                    img_id = key.split('_')[1]
                    try:
                        img_obj = EventImage.objects.get(id=img_id)
                        img_obj.position = int(value)
                        img_obj.save()
                    except:
                        continue
            messages.success(request, "Positions updated!")
            return redirect('folder_detail', id=id)

    return render(request, 'dashboard/folder_detail.html', {
        'folder': folder,
        'images': images
    })

@login_required
def admin_control(request):

    if not request.user.is_superuser:
        messages.error(request,"Permission Denied")
        return redirect("dashboard")

    admins = AdminProfile.objects.select_related("user")

    return render(request,"dashboard/admin_control.html",{
        "admins":admins
    })



# ====================================================
# ✅ EXPORT TESTIMONIALS (WITHOUT IMAGES)
# ====================================================
# ====================================================
# 1. MAIN EXPORT DASHBOARD VIEW (Jo Page Dikhaega)
# ====================================================
@login_required
def export_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request,"Permission Denied")
        return redirect("dashboard")
    print("\n" + "="*80)
    print("🔴 EXPORT_DASHBOARD VIEW CALLED")
    print("="*80)
    
    # Get all data
    recent_alumni = Alumni.objects.all().order_by('-id')[:5]
    recent_testimonials = Testimonial.objects.all().order_by('-id')[:5]
    recent_wof = DistinguishedAlumni.objects.all().order_by('-id')[:5]
    categories = DistinguishedCategory.objects.all()
    
    # Get filter options
    courses = list(Alumni.objects.values_list('course', flat=True).distinct().exclude(course__isnull=True).exclude(course=''))
    batches = list(Alumni.objects.values_list('batch', flat=True).distinct().exclude(batch__isnull=True).exclude(batch=''))
    
    print(f"Recent Alumni: {recent_alumni.count()}")
    print(f"Recent Testimonials: {recent_testimonials.count()}")
    print(f"Recent WOF: {recent_wof.count()}")
    print(f"Courses: {courses}")
    print(f"Batches: {batches}")
    print(f"Categories: {categories.count()}")
    print("="*80)

    context = {
        'recent_alumni': recent_alumni,
        'recent_testimonials': recent_testimonials,
        'recent_wof': recent_wof,
        'categories': categories,
        'courses': courses,
        'batches': batches,
    }
    
    return render(request, 'dashboard/export_data.html', context)
# ====================================================
# 2. EXPORT TESTIMONIALS (CSV)
# ====================================================
def export_testimonials(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="testimonials.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(["Name", "Course", "Batch", "Message"])

    testimonials = Testimonial.objects.all().order_by("name")

    for t in testimonials:
        writer.writerow([
            t.name or "",
            t.course or "",
            t.batch or "",
            t.message or ""
        ])

    return response


# ====================================================
# 3. EXPORT ALUMNI REGISTER (CSV with Filters)
# ====================================================
# ...existing code...
def export_alumni_register(request):
    alumni = Alumni.objects.all().order_by("name")

    # Get Filters
    course = request.GET.get("course")
    batch = request.GET.get("batch")
    status = request.GET.get("status")

    # Apply Filters
    if course:
        alumni = alumni.filter(course__iexact=course.strip())
    
    if batch:
        alumni = alumni.filter(batch__iexact=batch.strip())

    if status:
        if status == "registered":
            alumni = alumni.filter(is_registered=True)
        elif status == "pending":
            alumni = alumni.filter(is_registered=False)

    # Generate CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="alumni_filtered.csv"'
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(["Name", "Course", "Batch", "Email", "Phone", "Status", "Designation"])

    for a in alumni:
        phone_raw = str(a.phone or "").strip()
        # Force Excel to treat phone as text by prefixing an apostrophe
        phone_text = f"'{phone_raw}" if phone_raw else ""
        writer.writerow([
            a.name or "", 
            a.course or "", 
            a.batch or "", 
            a.email or "", 
            phone_text, 
            "Registered" if a.is_registered else "Pending",
            a.current_designation or ""
        ])

    return response
# ...existing code...


# ====================================================
# 4. EXPORT WALL OF FAME (CSV)
# ====================================================
def export_wall_of_fame(request):
    alumni = DistinguishedAlumni.objects.select_related("category").order_by(
        "category__position", "position"
    )

    category = request.GET.get("category")

    if category:
        alumni = alumni.filter(category__id=category)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="wall_of_fame.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(["Name", "Category", "Course", "Batch", "Current Position"])

    for a in alumni:
        writer.writerow([
            a.name or "",
            a.category.title if a.category else "",
            a.course or "",
            a.batch or "",
            a.current_position or ""
        ])

    return response

@login_required
def table_column_control(request):
    if not is_superadmin(request.user):
        messages.error(request,"Permission Denied")
        return redirect("dashboard")
    TABLE_COLUMNS = {
        "alumni":[
            "name","course","batch","current_designation",
            "email","phone","is_registered"
        ],
        "testimonial":[
            "name","course","batch","message"
        ],
        "wof":[
            "name","course","batch","current_position"
        ]
    }

    if request.method == "POST":
        table = request.POST.get("table")

        # remove old settings
        TableColumnSetting.objects.filter(
            user=request.user,
            table_name=table
        ).delete()

        for col in TABLE_COLUMNS.get(table,[]):
            visible = request.POST.get(col) == "on"

            TableColumnSetting.objects.create(
                user=request.user,
                table_name=table,
                column_name=col,
                is_visible=visible
            )

        return redirect("table_column_control")

    user_settings = TableColumnSetting.objects.filter(user=request.user)

    return render(request,"dashboard/table_columns.html",{
        "TABLE_COLUMNS":TABLE_COLUMNS,
        "user_settings":user_settings
    })

@login_required
def system_settings(request):

    if not is_superadmin(request.user):
        return redirect("dashboard")

    setting,created = SystemSetting.objects.get_or_create(id=1)

    if request.method=="POST":
        setting.site_title = request.POST.get("site_title")
        setting.maintenance_mode = request.POST.get("maintenance")=="on"
        setting.allow_registration = request.POST.get("register")=="on"
        setting.save()
        return redirect("system_settings")

    return render(request,"dashboard/system_settings.html",{"setting":setting})

# dashboard/views.py
from django.http import HttpResponse

def backup_download(request):
    # Yahan baad me backup ka code likhenge
    return HttpResponse("Backup download functionality coming soon!")

from .forms import FacultyForm, NonTeachingStaffForm, AlumniEventForm

# --- Faculty Management ---
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Category model bhi import karein
from .forms import FacultyForm, NonTeachingStaffForm, AlumniEventForm


# --- Teaching Faculty Management ---
def manage_faculty(request):
    # Dhyan dein: related_name='teachers' hai isliye prefetch_related('teachers') likha hai
    departments = AcademicDepartment.objects.prefetch_related('teachers').all()
    
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Faculty, id=edit_id) if edit_id else None
    form = FacultyForm(instance=instance)

    if request.method == "POST":
        if 'upload' in request.POST:
            fid = request.POST.get("fid")
            instance = get_object_or_404(Faculty, id=fid) if fid else None
            form = FacultyForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Faculty member saved!")
                return redirect("manage_faculty")
        
        elif 'delete' in request.POST:
            fid = request.POST.get("fid")
            get_object_or_404(Faculty, id=fid).delete()
            messages.success(request, "Faculty deleted!")
            return redirect("manage_faculty")

    return render(request, "dashboard/manage_faculty.html", {
        "form": form, 
        "departments": departments, 
        "edit_id": edit_id
    })

# --- Non-Teaching Staff Management ---
def manage_staff(request):
    # Dhyan dein: related_name='staff_members' hai
    departments = AdminDepartment.objects.prefetch_related('staff_members').all()
    
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(NonTeachingStaff, id=edit_id) if edit_id else None
    form = NonTeachingStaffForm(instance=instance)

    if request.method == "POST":
        if 'upload' in request.POST:  # <--- Check karein ye button ka name hai
            # Yahan dhyaan dein: HTML mein hidden input ka name 'sid' hai
            sid = request.POST.get("sid") 
            instance = get_object_or_404(NonTeachingStaff, id=sid) if sid else None
            
            form = NonTeachingStaffForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("manage_staff")
        
        elif 'delete' in request.POST:
            sid = request.POST.get("sid")
            get_object_or_404(NonTeachingStaff, id=sid).delete()
            return redirect("manage_staff")
    else:
        form = NonTeachingStaffForm(instance=instance)

    return render(request, "dashboard/manage_staff.html", {
        "form": form,
        "departments": departments,
        "edit_id": edit_id
    })
# --- Alumni Events Management ---
def manage_alumni_events(request):
    # 1. Sabse pehle saare events nikalo aur category + session ke hisaab se sort karo
    # Regroup sahi se chale iske liye sorting bahut zaroori hai
    events = AlumniEvent.objects.all().order_by('category__name', '-year_session', '-date')
    
    # 2. Form logic (Ye aapka pehle se sahi hai)
    categories = EventCategory.objects.prefetch_related('alumnievent_set').all()
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(AlumniEvent, id=edit_id) if edit_id else None
    form = AlumniEventForm(instance=instance)
    if request.method == "POST":
        if 'upload' in request.POST:
            eid = request.POST.get("eid")
            instance = get_object_or_404(AlumniEvent, id=eid) if eid else None
            form = AlumniEventForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("manage_alumni_events")
        
        elif 'delete' in request.POST:
            get_object_or_404(AlumniEvent, id=request.POST.get("eid")).delete()
            return redirect("manage_alumni_events")

    # 3. Yahan 'events' ko context mein add karna zaroori hai
    return render(request, "dashboard/manage_alumni_events.html", {
        "form": form, 
        "events": events,      # <--- Sabse zaroori: Yeh bhejiye
        "categories": categories, 
        "edit_id": edit_id
    })