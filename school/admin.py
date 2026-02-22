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

