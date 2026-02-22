import uuid
from django.db import models

import uuid
from django.db import models


class AdmissionApplication(models.Model):

    # ================= BASIC APPLICATION =================
    application_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    student_name = models.CharField(max_length=200)
    dob = models.DateField()
    class_applying = models.CharField(max_length=100)

    parent_name = models.CharField(max_length=200)
    parent_email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    previous_school = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='admission_photos/')

    # ================= ENTRANCE EXAM DETAILS =================
    entrance_date = models.DateField(null=True, blank=True)
    entrance_time = models.CharField(max_length=50, null=True, blank=True)
    entrance_venue = models.CharField(max_length=200, null=True, blank=True)

    # ================= RESULT SECTION =================
    RESULT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Selected', 'Selected'),
        ('Not Selected', 'Not Selected'),
        ('Waiting List', 'Waiting List'),
    ]

    result_status = models.CharField(
        max_length=20,
        choices=RESULT_STATUS_CHOICES,
        default='Pending'
    )

    marks_obtained = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    # Admin controls whether result is visible to public
    result_published = models.BooleanField(default=False)

    # Optional future ranking system
    merit_position = models.PositiveIntegerField(null=True, blank=True)

    # ================= META =================
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Admission Application"
        verbose_name_plural = "Admission Applications"

    def __str__(self):
        return f"{self.student_name} - {self.class_applying}"



from django.db import models
from django.contrib.auth.models import User


class EntrancePreparation(models.Model):

    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
        ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'),
        ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'),
        ('Grade 10', 'Grade 10'),
    ]

    class_name = models.CharField(max_length=50, choices=CLASS_CHOICES)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='entrance_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.class_name} - {self.subject} - {self.title}"



from django.db import models


class AdmissionSettings(models.Model):

    # ================= ADMISSION CONTROL =================
    admission_open = models.BooleanField(
        default=False,
        help_text="Tick to activate admission system and show popup on homepage."
    )

    # ================= POPUP SETTINGS =================
    popup_image = models.ImageField(
        upload_to='admission_popup/',
        blank=True,
        null=True,
        help_text="Upload admission poster image (Bharna Khulyo banner)."
    )

    popup_message = models.TextField(
        blank=True,
        help_text="Optional message to display below the popup image."
    )

    # ================= OTHER CONTROLS =================
    result_published = models.BooleanField(
        default=False,
        help_text="Allow students to check entrance results."
    )

    preparation_visible = models.BooleanField(
        default=False,
        help_text="Show entrance preparation materials to students."
    )

    # ================= META =================
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Admission System Setting"
        verbose_name_plural = "Admission System Settings"

    def __str__(self):
        return "Admission System Control Panel"


from django.db import models

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Gallery Image {self.id}"




from django.db import models


class Notice(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    notice_image = models.ImageField(upload_to='notices/', blank=True, null=True)

    is_popup = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # If this notice is popup, disable others
        if self.is_popup:
            Notice.objects.filter(is_popup=True).update(is_popup=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    image1 = models.ImageField(upload_to='events/')
    image2 = models.ImageField(upload_to='events/', blank=True, null=True)
    image3 = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Gallery Image"



from django.db import models


class PrimaryEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='primary/events/')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title




