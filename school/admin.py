from django.contrib import admin
from .models import AdmissionApplication, EntrancePreparation, AdmissionSettings


# ================= ADMISSION APPLICATION ADMIN =================
@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'student_name',
        'class_applying',
        'result_status',
        'marks_obtained',
        'result_published',
        'submitted_at'
    )

    list_filter = (
        'class_applying',
        'result_status',
        'result_published'
    )

    search_fields = (
        'student_name',
        'parent_name',
        'application_id'
    )

    readonly_fields = (
        'application_id',
        'submitted_at'
    )

    fieldsets = (

        ("Student Information", {
            'fields': (
                'application_id',
                'student_name',
                'dob',
                'class_applying',
                'photo'
            )
        }),

        ("Parent Information", {
            'fields': (
                'parent_name',
                'parent_email',
                'phone',
                'address',
                'previous_school'
            )
        }),

        ("Entrance Exam Details", {
            'fields': (
                'entrance_date',
                'entrance_time',
                'entrance_venue'
            )
        }),

        ("Result Section (Admin Control)", {
            'fields': (
                'result_status',
                'marks_obtained',
                'remarks',
                'merit_position',
                'result_published'
            )
        }),
    )






# ================= OTHER MODELS =================
admin.site.register(EntrancePreparation)
admin.site.register(AdmissionSettings)



from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django import forms
from .models import GalleryImage


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

    change_list_template = "admin/gallery_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-multiple/', self.admin_site.admin_view(self.upload_multiple))
        ]
        return custom_urls + urls

    def upload_multiple(self, request):
        if request.method == "POST":
            files = request.FILES.getlist('images')
            title = request.POST.get('title')

            for file in files:
                GalleryImage.objects.create(
                    title=title,
                    image=file
                )

            self.message_user(request, "Images uploaded successfully!")
            return redirect("../")

        return redirect("../")


admin.site.register(GalleryImage, GalleryImageAdmin)





from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_popup', 'created_at')
    list_filter = ('is_popup',)
    search_fields = ('title',)


from django.contrib import admin
from .models import Event

admin.site.register(Event)



from .models import Gallery

admin.site.register(Gallery)




from .models import PrimaryEvent


@admin.register(PrimaryEvent)
class PrimaryEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)

# school/admin.py



from django.contrib import admin, messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import openpyxl
import os

from .models import (
    GameControl,
    Ticket,
    TicketGenerator,
    GroupLeader,
    TicketBulkValidate,
    GameSession
)

admin.site.register(GameControl)


# ===============================
# GROUP LEADER ADMIN
# ===============================
class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = (
        "ticket_id",
        "is_validated",
        "is_paid",
        "is_winner",
        "prize_position",
        "created_at"
    )
    readonly_fields = ("ticket_id", "created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(GroupLeader)
class GroupLeaderAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [TicketInline]


# ===============================
# TICKET ADMIN
# ===============================
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        "ticket_id",
        "group_leader",
        "is_validated",
        "is_paid",
        "is_winner",
        "prize_position",
        "created_at"
    )

    list_filter = (
        "group_leader",
        "is_validated",
        "is_paid",
        "is_winner",
        "prize_position"
    )

    search_fields = ("ticket_id",)

    actions = [
        "print_selected_tickets",
        "mark_as_paid",
        "mark_as_winner_first",
        "mark_as_winner_second",
        "mark_as_winner_third",
        "mark_as_winner_fourth",
        "reset_winner_status",
        "export_leader_summary"
    ]

    # ----------------------------
    # PRINT TICKETS (3 PER PAGE)
    # ----------------------------
    def print_selected_tickets(self, request, queryset):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="holi_tickets.pdf"'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        template_path = os.path.join(
            settings.BASE_DIR,
            "static/images/ticket.png"
        )

        tickets = list(queryset)

        positions = [
            (410, 700),
            (410, 420),
            (410, 140),
        ]

        index = 0

        while index < len(tickets):

            c.drawImage(template_path, 0, 0, width=width, height=height)

            for pos in positions:
                if index >= len(tickets):
                    break

                c.setFont("Helvetica-Bold", 22)
                c.drawString(pos[0], pos[1], tickets[index].ticket_id)
                index += 1

            c.showPage()

        c.save()
        return response

    print_selected_tickets.short_description = "🖨 Print Selected Tickets (3 per page)"

    # ----------------------------
    # MARK SELECTED AS PAID
    # ----------------------------
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(is_paid=True)
        self.message_user(
            request,
            f"{updated} tickets marked as PAID.",
            messages.SUCCESS
        )

    mark_as_paid.short_description = "💰 Mark Selected Tickets as Paid"

    # ----------------------------
    # MARK WINNERS (PRIZE CONTROL)
    # ----------------------------
    def _mark_winner(self, request, queryset, prize_number):

        updated = 0

        for ticket in queryset:
            if not ticket.is_winner:
                ticket.is_winner = True
                ticket.prize_position = prize_number
                ticket.save()
                updated += 1

        self.message_user(
            request,
            f"{updated} ticket(s) marked as Prize {prize_number} winner.",
            messages.SUCCESS
        )

    def mark_as_winner_first(self, request, queryset):
        self._mark_winner(request, queryset, 1)

    def mark_as_winner_second(self, request, queryset):
        self._mark_winner(request, queryset, 2)

    def mark_as_winner_third(self, request, queryset):
        self._mark_winner(request, queryset, 3)

    def mark_as_winner_fourth(self, request, queryset):
        self._mark_winner(request, queryset, 4)

    mark_as_winner_first.short_description = "🏆 Mark as FIRST Prize"
    mark_as_winner_second.short_description = "🥈 Mark as SECOND Prize"
    mark_as_winner_third.short_description = "🥉 Mark as THIRD Prize"
    mark_as_winner_fourth.short_description = "🎁 Mark as FOURTH Prize"

    # ----------------------------
    # RESET WINNER STATUS
    # ----------------------------
    def reset_winner_status(self, request, queryset):
        updated = queryset.update(
            is_winner=False,
            prize_position=None
        )

        self.message_user(
            request,
            f"{updated} ticket(s) winner status reset.",
            messages.WARNING
        )

    reset_winner_status.short_description = "🔄 Reset Winner Status"

    # ----------------------------
    # EXPORT LEADER SUMMARY
    # ----------------------------
    def export_leader_summary(self, request, queryset):

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Leader Summary"

        ws.append([
            "Leader Name",
            "Total Tickets",
            "Validated",
            "Paid",
            "Unpaid",
            "Winners",
            "Total Amount (Rs.50 each)"
        ])

        leaders = GroupLeader.objects.all()

        for leader in leaders:
            tickets = Ticket.objects.filter(group_leader=leader)

            total = tickets.count()
            validated = tickets.filter(is_validated=True).count()
            paid = tickets.filter(is_paid=True).count()
            unpaid = tickets.filter(is_paid=False).count()
            winners = tickets.filter(is_winner=True).count()

            total_amount = paid * 50

            ws.append([
                leader.name,
                total,
                validated,
                paid,
                unpaid,
                winners,
                total_amount
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=leader_summary.xlsx"

        wb.save(response)
        return response

    export_leader_summary.short_description = "📊 Export Leader Wise Summary (Excel)"


# ===============================
# TICKET GENERATOR ADMIN
# ===============================
@admin.register(TicketGenerator)
class TicketGeneratorAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        for _ in range(obj.number_of_tickets):
            code = Ticket.generate_unique_ticket()
            Ticket.objects.create(ticket_id=code)

        messages.success(
            request,
            f"{obj.number_of_tickets} tickets generated successfully."
        )

        return
from .models import GameSession, SpinResult
# ===============================
# BULK VALIDATION ADMIN
# ===============================
@admin.register(TicketBulkValidate)
class TicketBulkValidateAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        ticket_codes = obj.ticket_list.replace("\n", ",").split(",")

        not_found = []
        already_validated = []
        validated_count = 0

        for code in ticket_codes:
            code = code.strip().upper()

            if not code:
                continue

            try:
                ticket = Ticket.objects.get(ticket_id=code)

                if ticket.is_validated:
                    already_validated.append(code)
                else:
                    ticket.group_leader = obj.group_leader
                    ticket.is_validated = True
                    ticket.save()
                    validated_count += 1

            except Ticket.DoesNotExist:
                not_found.append(code)

        if validated_count:
            messages.success(
                request,
                f"{validated_count} tickets validated successfully."
            )

        if already_validated:
            messages.warning(
                request,
                f"Already validated: {', '.join(already_validated)}"
            )

        if not_found:
            messages.error(
                request,
                f"Not found in system: {', '.join(not_found)}"
            )

        return redirect("/admin/school/ticket/")




# ==================================
# SPIN RESULT ADMIN
# ==================================
@admin.register(SpinResult)
class SpinResultAdmin(admin.ModelAdmin):
    list_display = ("value", "session", "created_at")
    list_filter = ("session",)
    ordering = ("-created_at",)
    search_fields = ("value",)
    
from .models import GameSession


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "started_at",
        "is_active",
        "first_prize_given",
        "second_prize_given",
        "third_prize_given",
        "fourth_prize_given",
    )

    actions = ["activate_session", "deactivate_session"]

    def activate_session(self, request, queryset):
        # deactivate all others
        GameSession.objects.update(is_active=False)

        for session in queryset:
            session.is_active = True
            session.save()

        self.message_user(request, "Selected session activated.")

    activate_session.short_description = "▶ Activate Game Session"

    def deactivate_session(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected session deactivated.")

    deactivate_session.short_description = "⛔ Deactivate Game Session"
    
from django.contrib import admin
from .models import Teacher
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import admin
from django.utils.html import format_html
from .models import Teacher



from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'email',
        'subject',
        'status',
        'view_profile_image',
        'view_document',
        'approve_button',
        'reject_button',
    )

    list_filter = ('status', 'subject', 'qualification_level')
    search_fields = ('full_name', 'email', 'contact_no')

    readonly_fields = (
        'view_profile_image',
        'view_document',
    )

    fieldsets = (
        ("Basic Information", {
            'fields': (
                'full_name',
                'email',
                'dob',
                'contact_no',
                'emergency_contact',
                'relation',
                'married',
                'subject',
                'experience',
                'address',
            )
        }),

        ("Qualification Details", {
            'fields': (
                'qualification_level',
                'qualification_status',
                'qualification_docs',
                'view_document',
            )
        }),

        ("Document Details", {
            'fields': (
                'document_type',
                'document_number',
                'issued_date',
                'expiry_date',
                'issuing_authority',
            )
        }),

        ("Profile", {
            'fields': (
                'profile_image',
                'view_profile_image',
                'status',
            )
        }),
    )

    # 🔥 Profile Image Preview
    def view_profile_image(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="80" style="border-radius:8px;" />',
                obj.profile_image.url
            )
        return "No Image"

    view_profile_image.short_description = "Profile Preview"

    # 🔥 Qualification Document Preview
    def view_document(self, obj):
        if obj.qualification_docs:
            return format_html(
                '<a href="{}" target="_blank" style="color:green;">View Document</a>',
                obj.qualification_docs.url
            )
        return "No Document"

    view_document.short_description = "Qualification Document"

    # 🔥 Approve Button
    def approve_button(self, obj):
        if obj.status != "Approved":
            url = reverse('approve_teacher', args=[obj.id])
            return format_html(
                '<a class="button" style="background:green;color:white;padding:5px 10px;border-radius:5px;text-decoration:none;" href="{}">Approve</a>',
                url
            )
        return format_html('<span style="color:green;font-weight:bold;">Approved</span>')

    approve_button.short_description = "Approve"

    # 🔥 Reject Button
    def reject_button(self, obj):
        if obj.status != "Rejected":
            url = reverse('reject_teacher', args=[obj.id])
            return format_html(
                '<a class="button" style="background:red;color:white;padding:5px 10px;border-radius:5px;text-decoration:none;" href="{}">Reject</a>',
                url
            )
        return format_html('<span style="color:red;font-weight:bold;">Rejected</span>')

    reject_button.short_description = "Reject"