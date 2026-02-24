from django.shortcuts import render

from .models import AdmissionSettings
from .models import Notice, AdmissionSettings

def home(request):

    settings_obj = AdmissionSettings.objects.first()

    notices = Notice.objects.all()
    popup_notice = Notice.objects.filter(is_popup=True).first()

    return render(request, 'school/index.html', {
        'admission_settings': settings_obj,
        'notices': notices,
        'popup_notice': popup_notice,
    })



def about(request):
    return render(request, 'school/about.html')

def academics(request):
    return render(request, 'school/academics.html')


from .models import GalleryImage

def gallery(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'school/gallery.html', {
        'images': images
    })



from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}

Message:
{message}
"""

        send_mail(
            subject=f"New Message from {name}",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['sebschool50@gmail.com'],
            fail_silently=False,
        )

        return render(request, 'school/contact.html', {'success': True})

    return render(request, 'school/contact.html')



def admission(request):
    return render(request, 'school/admission.html')


def career(request):
    return render(request, 'school/career.html')


import requests
from django.http import JsonResponse

def google_reviews(request):
    api_key = "AIzaSyClpEjjRE_TTAG5417hroFUeGGPVp8pc9s"
    place_id = "ChIJCV9zU83B7jkRgdTUs51qZ0g"

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,reviews&key={api_key}"

    response = requests.get(url)
    data = response.json()

    return JsonResponse(data)



from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMessage

def apply(request):
    if request.method == "POST":

        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        position = request.POST.get('position')
        subject = request.POST.get('subject')
        qualification = request.POST.get('qualification')
        university = request.POST.get('university')
        experience = request.POST.get('experience')
        salary = request.POST.get('salary')
        available_from = request.POST.get('available_from')
        message = request.POST.get('message')

        resume = request.FILES.get('resume')

        email_body = f"""
New Job Application Submission

Full Name: {full_name}
Gender: {gender}
DOB: {dob}
Phone: {phone}
Email: {email}
Address: {address}

Position: {position}
Subject: {subject}
Qualification: {qualification}
University: {university}
Experience: {experience}
Expected Salary: {salary}
Available From: {available_from}

Message:
{message}
"""

        email_message = EmailMessage(
            subject=f"New Job Application from {full_name}",
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=['sebschool50@gmail.com'],
            reply_to=[email],
        )

        if resume:
            email_message.attach(resume.name, resume.read(), resume.content_type)

        email_message.send()

        return render(request, 'school/apply.html', {'success': True})

    return render(request, 'school/apply.html')


def explore_academics(request):
    return render(request, 'school/exploreacademics.html')





import io
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from .models import (
    AdmissionApplication,
    EntrancePreparation,
    AdmissionSettings
)


def admission(request):

    # ================= CLASS LIST =================
    class_list = [
        "Nursery", "LKG", "UKG",
        "Grade 1", "Grade 2", "Grade 3",
        "Grade 4", "Grade 5", "Grade 6",
        "Grade 7", "Grade 8", "Grade 9",
        "Grade 10"
    ]

    # ================= SYSTEM CONTROL =================
    settings_obj = AdmissionSettings.objects.first()

    if not settings_obj or not settings_obj.admission_open:
        return render(request, 'school/admission_closed.html')

    selected_class = request.GET.get('class')
    application_id = request.GET.get('application_id')

    materials = None
    result = None

    # ================= PREPARATION MATERIALS =================
    if selected_class and settings_obj.preparation_visible:
        selected_class = selected_class.strip()
        materials = EntrancePreparation.objects.filter(
            class_name__iexact=selected_class
        )

    # ================= RESULT CHECK =================
    if application_id and settings_obj.result_published:
        try:
            result = AdmissionApplication.objects.get(
                application_id=application_id.strip()
            )
        except AdmissionApplication.DoesNotExist:
            result = None

    # ================= FORM SUBMISSION =================
    if request.method == "POST":

        student = AdmissionApplication.objects.create(
            student_name=request.POST.get('student_name'),
            dob=request.POST.get('dob'),
            class_applying=request.POST.get('class_applying'),
            parent_name=request.POST.get('parent_name'),
            parent_email=request.POST.get('parent_email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            previous_school=request.POST.get('previous_school'),
            photo=request.FILES.get('photo'),
        )

        # ================= CREATE PDF =================
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # HEADER
        logo_path = settings.BASE_DIR / "static/images/logo.png"
        logo = Image(str(logo_path), width=1.1 * inch, height=1.1 * inch)

        school_info = Paragraph(
            "<font size=16 color='white'><b>SARASWOTI ENGLISH BOARDING SCHOOL</b></font><br/>"
            "<font size=9 color='white'>Sadaiv Samudaya Sanga, Sabai Samudaya Sanga</font><br/>"
            "<font size=8 color='white'>Kathmandu, Nepal | Phone: 01-XXXXXXX | Mobile: 98XXXXXXXX</font>",
            styles["Normal"]
        )

        header_table = Table([[logo, school_info]], colWidths=[90, 400])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        elements.append(header_table)
        elements.append(Spacer(1, 20))

        elements.append(Paragraph(
            "<font size=18 color='#1e3a8a'><b>ENTRANCE EXAMINATION HALL TICKET</b></font>",
            styles["Title"]
        ))
        elements.append(Spacer(1, 25))

        # STUDENT DETAILS
        info_data = [
            ["Application ID", str(student.application_id)],
            ["Student Name", student.student_name],
            ["Date of Birth", str(student.dob)],
            ["Class Applied For", student.class_applying],
            ["Parent Name", student.parent_name],
            ["Contact Number", student.phone],
        ]

        info_table = Table(info_data, colWidths=[170, 250])
        info_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#e0f2fe")),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))

        if student.photo:
            photo = Image(student.photo.path, width=1.5 * inch, height=1.5 * inch)
            combined = Table([[info_table, photo]], colWidths=[420, 120])
            combined.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(combined)
        else:
            elements.append(info_table)

        elements.append(Spacer(1, 30))

        # EXAM DETAILS
        exam_data = [
            ["Entrance Date", student.entrance_date if student.entrance_date else "To Be Announced"],
            ["Entrance Time", student.entrance_time if student.entrance_time else "To Be Announced"],
            ["Venue", student.entrance_venue if student.entrance_venue else "School Campus"],
        ]

        exam_table = Table(exam_data, colWidths=[170, 300])
        exam_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ]))

        elements.append(exam_table)
        elements.append(Spacer(1, 40))

        # FOOTER
        footer_table = Table([[
            Paragraph(
                "<font size=9 color='white'>"
                "Website: www.saraswatienglishschool.edu.np | Facebook | TikTok<br/>"
                "Powered by Saraswoti English Boarding School"
                "</font>",
                styles["Normal"]
            )
        ]])

        footer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        elements.append(footer_table)

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # EMAIL TO PARENT
        email = EmailMessage(
            subject="Entrance Examination Hall Ticket",
            body="Dear Parent,\n\nPlease find attached the official Entrance Examination Hall Ticket.",
            from_email=settings.EMAIL_HOST_USER,
            to=[student.parent_email],
        )
        email.attach("Entrance_Hall_Ticket.pdf", pdf, "application/pdf")
        email.send()

        # EMAIL TO SCHOOL
        school_email = EmailMessage(
            subject=f"New Admission Application - {student.student_name}",
            body=f"Application ID: {student.application_id}",
            from_email=settings.EMAIL_HOST_USER,
            to=['sebschool50@gmail.com'],
        )
        school_email.send()

        return render(request, 'school/admission.html', {
            'success': True,
            'materials': materials,
            'result': result,
            'class_list': class_list
        })

    return render(request, 'school/admission.html', {
        'materials': materials,
        'result': result,
        'class_list': class_list
    })


from .models import Event   # make sure this is at top



from .models import Event, Gallery

def preschool(request):
    latest_events = Event.objects.order_by('-date')
    gallery_images = Gallery.objects.order_by('-uploaded_at')[:6]

    return render(request, 'school/preschool.html', {
        'latest_events': latest_events,
        'gallery_images': gallery_images
    })



from django.shortcuts import render, get_object_or_404
from .models import Event

def events(request):
    events = Event.objects.order_by('-date')
    return render(request, 'school/events.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'school/event_detail.html', {'event': event})




from django.shortcuts import render
from .models import Gallery



from .models import PrimaryEvent, Gallery


def primary(request):
    latest_events = PrimaryEvent.objects.all()
    gallery_images = Gallery.objects.all()[:8]

    return render(request, 'school/primary.html', {
        'latest_events': latest_events,
        'gallery_images': gallery_images
    })


from .models import PrimaryEvent, Gallery


def secondary(request):
    latest_events = PrimaryEvent.objects.order_by('-date')
    gallery_images = Gallery.objects.order_by('-uploaded_at')

    return render(request, 'school/secondary.html', {
        'latest_events': latest_events,
        'gallery_images': gallery_images
    })



from django.shortcuts import render

def learning_approach(request):
    return render(request, 'school/learning.html')



from django.shortcuts import render

def student_clubs(request):
    return render(request, "school/student-clubs.html")

def house_activities(request):
    return render(request, "school/house-activities.html")

def sports(request):
    return render(request, "school/sports.html")

def arts_culture(request):
    return render(request, "school/arts_culture.html")


from django.shortcuts import render, redirect
from .models import Ticket, GameControl
import random

from django.shortcuts import render, redirect
from .models import Ticket, GameControl
import random

def home(request):
    game = GameControl.objects.first()
    winning_number = ""
    prize_round = ""

    if game and game.is_active:

        prize_round = game.current_round

        # Check if winner already selected in session
        if not request.session.get("current_winner"):

            # 1️⃣ Check manual winner for this round
            manual = Ticket.objects.filter(
                prize_type=prize_round,
                has_won=False
            ).first()

            if manual:
                winner = manual
            else:
                # 2️⃣ System auto select from unused tickets
                available = Ticket.objects.filter(has_won=False)

                if available.exists():
                    winner = random.choice(list(available))
                else:
                    winner = None

            if winner:
                winner.has_won = True
                winner.save()
                request.session["current_winner"] = winner.ticket_number
                winning_number = winner.ticket_number

        else:
            winning_number = request.session.get("current_winner")

    context = {
        "game_active": game.is_active if game else False,
        "winning_number": winning_number,
        "prize_round": prize_round
    }

    return render(request, "school/index.html", context)

def toggle_game(request):
    game, created = GameControl.objects.get_or_create(id=1)

    if game.is_active:
        # 🔴 Closing the game
        game.is_active = False

        # Clear session winner
        request.session.pop("current_winner", None)

        # Reset all tickets winner flag
        Ticket.objects.update(is_winner=False)

    else:
        # 🟢 Starting the game
        game.is_active = True

    game.save()

    return redirect("home")


from django.shortcuts import redirect
from .models import GameControl

def toggle_game(request):
    game, created = GameControl.objects.get_or_create(id=1)

    if game.is_active:
        # Closing the game
        game.is_active = False
        game.winner_selected = False
        request.session.flush()
    else:
        # Activating the game
        game.is_active = True

    game.save()
    return redirect("home")




# 🔥 ADD THIS FUNCTION HERE
def set_round(request, round_name):
    game, created = GameControl.objects.get_or_create(id=1)

    game.current_round = round_name

    # Reset winner for new round
    request.session.pop("current_winner", None)

    game.save()

    return redirect("home")