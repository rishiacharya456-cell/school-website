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


# school/models.py

import random
import string
from django.db import models
from django.utils import timezone


# =============================
# GAME CONTROL (Enable / Disable Game)
# =============================
class GameControl(models.Model):
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "Holi Event Control"
    
from django.db import models
from django.utils import timezone


class GameSession(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    spin_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=False)

    # ===============================
    # PRIZE STATUS TRACKING
    # ===============================

    first_prize_given = models.BooleanField(default=False)
    second_prize_given = models.BooleanField(default=False)
    third_prize_given = models.BooleanField(default=False)
    fourth_prize_given = models.BooleanField(default=False)

    # ===============================
    # MANUAL PRIZE RELEASE CONTROL
    # ===============================

    allow_first_prize = models.BooleanField(default=False)
    allow_second_prize = models.BooleanField(default=False)
    allow_third_prize = models.BooleanField(default=False)
    allow_fourth_prize = models.BooleanField(default=False)

    # ===============================
    # FORCED WINNER (ADMIN CONTROL)
    # ===============================

    forced_winner = models.ForeignKey(
        "Ticket",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="forced_for_session"
    )

    forced_prize_position = models.IntegerField(
        null=True,
        blank=True
    )

    # ===============================
    # TIME RULE HELPERS
    # ===============================

    def first_prize_time_allowed(self):
        return timezone.now() >= self.started_at + timezone.timedelta(hours=1)

    def second_prize_time_allowed(self):
        return self.first_prize_given

    def third_prize_time_allowed(self):
        return self.second_prize_given

    def fourth_prize_time_allowed(self):
        return self.third_prize_given

    # ===============================
    # NEXT AVAILABLE PRIZE
    # ===============================

    def get_next_available_prize(self):
        if not self.first_prize_given:
            return 1
        elif not self.second_prize_given:
            return 2
        elif not self.third_prize_given:
            return 3
        elif not self.fourth_prize_given:
            return 4
        return None

    def __str__(self):
        return f"Game Session {self.id}"
# =============================
# GROUP LEADER
# =============================
class GroupLeader(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name






# =============================
# TICKET MODEL
# =============================
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=6, unique=True)

    group_leader = models.ForeignKey(
        GroupLeader,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_validated = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    # ===== NEW EVENT CONTROL FIELDS =====
    is_winner = models.BooleanField(default=False)
    prize_position = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="1=First, 2=Second, 3=Third, 4=Fourth"
    )

    matched_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_id

    @staticmethod
    def generate_unique_ticket():
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.sample(characters, 6))
            if not Ticket.objects.filter(ticket_id=code).exists():
                return code

    def is_eligible(self):
        """
        Ticket is eligible only if:
        - Paid
        - Validated
        - Not already winner
        """
        return self.is_paid and self.is_validated and not self.is_winner


# =============================
# BULK TICKET GENERATOR
# =============================
class TicketGenerator(models.Model):
    number_of_tickets = models.PositiveIntegerField()

    def __str__(self):
        return f"Generate {self.number_of_tickets} Tickets"


# =============================
# BULK ASSIGNMENT MODEL
# =============================
class TicketAssignment(models.Model):
    group_leader = models.ForeignKey(GroupLeader, on_delete=models.CASCADE)
    ticket_list = models.TextField(
        help_text="Paste ticket numbers separated by comma"
    )

    def __str__(self):
        return f"Assignment for {self.group_leader.name}"


# =============================
# BULK VALIDATION MODEL
# =============================
class TicketBulkValidate(models.Model):
    group_leader = models.ForeignKey(GroupLeader, on_delete=models.CASCADE)
    ticket_list = models.TextField(
        help_text="Paste tickets separated by comma"
    )

    def __str__(self):
        return f"Validation for {self.group_leader.name}"
    
    
    
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic Info
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)
    relation = models.CharField(max_length=100, null=True, blank=True)
    married = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # Qualification
    qualification_level = models.CharField(max_length=100, null=True, blank=True)
    qualification_status = models.CharField(max_length=50, null=True, blank=True)
    qualification_docs = models.FileField(upload_to='qualification_docs/', null=True, blank=True)

    # Document Info
    document_type = models.CharField(max_length=100, null=True, blank=True)
    document_number = models.CharField(max_length=100, null=True, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=200, null=True, blank=True)

    # Profile Image
    profile_image = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, default="Pending")
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    






class SpinResult(models.Model):
    value = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey("GameSession", on_delete=models.CASCADE)

    def __str__(self):
        return self.value
    
    
    
    