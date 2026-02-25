from django import forms

from alumniportal.models import (
    Alumni,
    AlumniEvent,
    Faculty, 
    HomeSlider, 
    AssociationBearer,
    NonTeachingStaff, 
    Testimonial, 
    CommitteeMember, 
    CollegeOfficeBearer,
    CommitteeYear,
    DistinguishedAlumni,
    EventFolder,
    EventImage
    
)

# ---------------------------------------------------
# 1. Slider Form
# ---------------------------------------------------
class SliderForm(forms.ModelForm):
    class Meta:
        model = HomeSlider
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 5MB")
            if not image.name.lower().endswith(('.jpg','.jpeg','.png')):
                raise forms.ValidationError("Only JPG, JPEG, PNG allowed")
        return image

# ---------------------------------------------------
# 2. Testimonial Form
# ---------------------------------------------------
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name','course','batch','message','linkedin','image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:
                raise forms.ValidationError("Max size 5MB")
            if not image.name.lower().endswith(('.jpg','.jpeg','.png')):
                raise forms.ValidationError("Only JPG/JPEG/PNG allowed")
        return image

# ---------------------------------------------------
# 3. Association Bearer Form
# ---------------------------------------------------
class AssociationBearerForm(forms.ModelForm):
    class Meta:
        model = AssociationBearer
        fields = ['position', 'name', 'designation', 'qualification', 'message', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        # Faculty logic: Sirf tab check karo jab nayi image upload ho
        if image:
            if hasattr(image, 'size') and image.size > 5*1024*1024:
                raise forms.ValidationError("Max size 5MB allowed")
        # Agar image nahi hai, toh Django automatically purani image rakhta hai 
        # basharte hum use None return karke overwrite na karein.
        return image
# 4. College Committee Form
# ---------------------------------------------------
class CollegeCommitteeForm(forms.ModelForm):
    class Meta:
        model = CommitteeMember
        fields = ['position','committee','role','name','department']

# ---------------------------------------------------
# 5. Committee Member Form (Office Bearer)
# ---------------------------------------------------
class CommitteeMemberForm(forms.ModelForm):
    class Meta:
        model = CollegeOfficeBearer
        fields = ['position','name','designation','image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:
                raise forms.ValidationError("Max 5MB allowed")
            if not image.name.lower().endswith(('.jpg','.jpeg','.png')):
                raise forms.ValidationError("Only JPG/JPEG/PNG allowed")
        return image

# ---------------------------------------------------
# 6. Alumni Forms (New Logic)
# ---------------------------------------------------

# A. Manual Entry Form (Isme File field nahi hoga)
class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        # Ensure ye fields model me maujood hon
        fields = ['name', 'course', 'batch', 'current_designation', 'email', 'phone', 'is_registered']

# B. Bulk Upload Form (Isme sirf File field hoga)
class AlumniUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv, .xlsx'}),
        label="Upload Excel/CSV File"
    )

from django import forms
from alumniportal.models import DistinguishedAlumni

# A. Bulk Upload Form
class WallUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv, .xlsx'}),
        label="Upload Excel/CSV File"
    )

# B. Manual Add/Edit Form
class WallForm(forms.ModelForm):
    class Meta:
        model = DistinguishedAlumni
        fields = ['category', 'name', 'course', 'batch', 'current_position', 'image', 'position']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'current_position': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        # Faculty code logic: Sirf tab check karo jab image object exist kare
        if image and hasattr(image, 'size'):
            if image.size > 5*1024*1024:
                raise forms.ValidationError("Max 5MB allowed")
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                raise forms.ValidationError("Only JPG/JPEG/PNG allowed")
        return image


from django import forms

# Custom Widget for Multiple Files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class EventImageForm(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=EventFolder.objects.all(),
        required=False,
        label="Select Existing Folder",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    new_folder = forms.CharField(
        required=False,
        label="OR Create New Folder",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Folder Name'})
    )
    
    # 🔥 YAHAN DHYAN DEIN
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        label="Select Images",
        required=False  # Ye widget se bahar hai
    )

class ImageEditForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['position']
        widgets = {
            'position': forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
        }

# --- Faculty & Staff Forms ---
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['department', 'name', 'designation', 'image', 'order']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5*1024*1024:
            raise forms.ValidationError("Max size 5MB allowed")
        return image

class NonTeachingStaffForm(forms.ModelForm):
    class Meta:
        model = NonTeachingStaff
        fields = ['department', 'name', 'designation']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
        }

# --- Alumni Event Form ---
class AlumniEventForm(forms.ModelForm):
    class Meta:
        model = AlumniEvent
        fields = ['category', 'year_session', 'title', 'organized_by',  'resource_person', 'batch', 'image', 'report_pdf', 'date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'year_session': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2025-26'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'resource_person': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'organized_by': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }