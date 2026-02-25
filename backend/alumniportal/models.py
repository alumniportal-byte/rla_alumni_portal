from django.db import models
from django.core.exceptions import ValidationError
import os

# -----------------------------
# COMMON IMAGE VALIDATION
# -----------------------------
def validate_image(image):
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError("Image size must be under 5MB.")

    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only JPG, JPEG, PNG allowed.")


# =============================
# HOME TAB
# =============================

class HomeSlider(models.Model):
    image = models.ImageField(upload_to='home_slider/', validators=[validate_image])
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    
    class Meta: 
        ordering = ['position']

    def __str__(self):
        return f"Slider Image {self.id}"


class RegisterLink(models.Model):
    register_url = models.URLField()

    def __str__(self):
        return self.register_url


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)
    linkedin = models.URLField(blank=True,null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', validators=[validate_image])
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.name


# =============================
# ABOUT TAB
# =============================
class CollegeOfficeBearer(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    image = models.ImageField(upload_to='college_office_bearers/', validators=[validate_image])
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.name

class AssociationBearer(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='office_bearers/', blank=True, null=True)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
        
    class Meta: 
        ordering = ['position']
        
    def __str__(self):
        return self.name


class CommitteeYear(models.Model):
    year_range = models.CharField(max_length=20)  # example 2022-2023
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.year_range


class CommitteeMember(models.Model):
    committee = models.ForeignKey(CommitteeYear, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.name


# =============================
# REGISTERED ALUMNI TAB
# =============================

class Alumni(models.Model):
    name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)
    current_designation = models.CharField(max_length=200, blank=True, null=True) # Blank allowed for flexibility
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_registered = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.name


# =============================
# DISTINGUISHED ALUMNI TAB
# =============================

class DistinguishedCategory(models.Model):
    title = models.CharField(max_length=200)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.title


class DistinguishedAlumni(models.Model):
    category = models.ForeignKey(DistinguishedCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)
    current_position = models.CharField(max_length=200)
    image = models.ImageField(upload_to='distinguished/', blank=True, null=True)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    class Meta: 
        ordering = ['position']
    
    def __str__(self):
        return self.name


# =============================
# ALUMNI MEET GALLERY
# =============================

from django.core.exceptions import ValidationError

# 1. VALIDATOR FUNCTION (Agar ye pehle se nahi hai to yahan add karein)
def validate_image(image):
    file_size = image.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb} MB")

# ==========================================
# 2. EVENT FOLDER MODEL
# ==========================================
class EventFolder(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    
    class Meta: 
        ordering = ['position']

    def __str__(self):
        return self.title

# ==========================================
# 3. EVENT IMAGE MODEL
# ==========================================
class EventImage(models.Model):
    # 🔥 Change: related_name='images' joda hai
    folder = models.ForeignKey(EventFolder, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='events/', validators=[validate_image])
    position = models.PositiveIntegerField(default=0, help_text="(Eg: 1, 2, 3)")
    
    class Meta: 
        ordering = ['position']

    def __str__(self):
        return f"{self.folder.title} Image"

# =============================
# SUGGESTION LINK
# =============================

class SuggestionLink(models.Model):
    form_url = models.URLField()

    def __str__(self):
        return self.form_url
    

from django.contrib.auth.models import User
from django.db import models

class AdminProfile(models.Model):

    ROLE_CHOICES = (
        ("superadmin","Super Admin"),
        ("admin","Admin"),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="admin")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
# =============================
# ADMIN TABLE COLUMN CONTROL
# =============================

class TableColumnSetting(models.Model):

    TABLE_CHOICES = (
        ("alumni","Alumni Table"),
        ("testimonial","Testimonial Table"),
        ("wof","Wall Of Fame"),
        ("committee","Committee"),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    table_name = models.CharField(max_length=50,choices=TABLE_CHOICES)
    column_name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user","table_name","column_name")

    def __str__(self):
        return f"{self.user.username} - {self.table_name} - {self.column_name}"
    
class SystemSetting(models.Model):
    site_title = models.CharField(max_length=200,default="Alumni Portal")
    maintenance_mode = models.BooleanField(default=False)
    allow_registration = models.BooleanField(default=True)

    def __str__(self):
        return self.site_title


from django.db import models

# --- 1. DEPARTMENTS (Separate for Faculty and Staff) ---

class AcademicDepartment(models.Model):
    """Departments for Faculty (e.g., Computer Science, History)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Academic: {self.name}"

class AdminDepartment(models.Model):
    """Departments for Non-Teaching (e.g., Accounts, Administration, Library)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Admin: {self.name}"

# --- 2. FACULTY & STAFF ---

class Faculty(models.Model):
    department = models.ForeignKey(AcademicDepartment, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faculty_photos/')
    order = models.IntegerField(default=0) # Display order set karne ke liye

    def __str__(self):
        return f"{self.name} - {self.department.name}"

class NonTeachingStaff(models.Model):
    department = models.ForeignKey(AdminDepartment, on_delete=models.CASCADE, related_name='staff_members')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    order = models.IntegerField(default=0) # Display order set karne ke liye
    # Aapne kaha tha isme photo nahi chahiye, sirf table format hoga

    def __str__(self):
        return f"{self.name} - {self.department.name}"

# --- 3. ALUMNI EVENTS (Lecture Series, Workshops, etc.) ---

class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True) # Lecture Series, Career Guidance

    def __str__(self):
        return self.name

class AlumniEvent(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    year_session = models.CharField(max_length=20) # e.g., 2025-2026
    title = models.CharField(max_length=200)
    organized_by = models.CharField(max_length=200) 
    image = models.ImageField(upload_to='event_photos/')
    report_pdf = models.FileField(upload_to='event_reports/')
    date = models.DateField()
    resource_person = models.CharField(max_length=200, blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True, null=True) # Optional field for batch info
    def __str__(self):
        return f"{self.title} ({self.year_session})"