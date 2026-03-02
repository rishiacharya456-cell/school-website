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

# school/views.py

from django.shortcuts import render
from .models import GameControl

def home(request):
    game = GameControl.objects.first()

    context = {
        "game_active": game.is_active if game else False
    }

    return render(request, "school/index.html", context)

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import random
import string
import os

from .models import Ticket, GameSession, SpinResult


# ==========================================================
# GENERATE AND PRINT TICKETS (UNCHANGED)
# ==========================================================
def generate_and_print_tickets(request, count):

    count = int(count)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="holi_{count}_tickets.pdf"'

    width, height = A4
    c = canvas.Canvas(response, pagesize=A4)

    template_path = os.path.join(
        settings.BASE_DIR,
        "static/images/ticket.png"
    )

    characters = string.ascii_uppercase + string.digits

    tickets_per_page = 3
    total_pages = count // tickets_per_page

    if count % tickets_per_page != 0:
        total_pages += 1

    ticket_index = 0

    for page in range(total_pages):

        c.drawImage(template_path, 0, 0, width=width, height=height)

        positions = [
            (410, 700),
            (410, 420),
            (410, 140),
        ]

        for pos in positions:

            if ticket_index >= count:
                break

            while True:
                ticket_code = ''.join(random.sample(characters, 6))
                if not Ticket.objects.filter(ticket_id=ticket_code).exists():
                    Ticket.objects.create(ticket_id=ticket_code)
                    break

            c.setFont("Helvetica-Bold", 22)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(pos[0], pos[1], ticket_code)

            ticket_index += 1

        c.showPage()

    c.save()
    return response




# ==========================================================
# CONTROLLED SPIN ENGINE (FULL AUTO + MANUAL + SAFE)
# ==========================================================
from django.utils import timezone
from django.db import transaction
import random
import string


def controlled_spin(request):

    session = GameSession.objects.filter(is_active=True).last()

    if not session:
        return JsonResponse({"status": "error", "message": "Game not active"})

    characters = string.ascii_uppercase + string.digits

    # -----------------------------------------
    # Collect Previous Spins
    # -----------------------------------------
    previous_spins = list(
        SpinResult.objects.filter(session=session)
        .values_list("value", flat=True)
    )

    shown_chars = []
    for spin in previous_spins:
        for ch in spin:
            shown_chars.append(ch)

    # -----------------------------------------
    # Active Eligible Tickets
    # -----------------------------------------
    tickets = Ticket.objects.filter(
        is_paid=True,
        is_validated=True,
        is_winner=False
    )

    # ==========================================================
    # 🔴 MANUAL FORCED WINNER MODE
    # ==========================================================
    if session.forced_winner and session.forced_winner in tickets:

        forced_ticket = session.forced_winner
        missing_chars = []

        for ch in forced_ticket.ticket_id:
            if ch not in shown_chars:
                missing_chars.append(ch)

        # Generate required character
        if missing_chars:
            value = missing_chars[0]
        else:
            value = random.choice(characters)

    # ==========================================================
    # 🔵 NORMAL SAFE CONTROL MODE
    # ==========================================================
    else:

        # STEP 1: Detect completion risk
        completion_risk = {}

        for ticket in tickets:

            missing_chars = []

            for ch in ticket.ticket_id:
                if ch not in shown_chars:
                    missing_chars.append(ch)

            # If only 1 character missing → risk
            if len(missing_chars) == 1:
                last_char = missing_chars[0]

                if last_char not in completion_risk:
                    completion_risk[last_char] = 0

                completion_risk[last_char] += 1

        # STEP 2: Build SAFE pool
        safe_characters = []

        for c in characters:
            if completion_risk.get(c, 0) <= 1:
                safe_characters.append(c)

        if not safe_characters:
            safe_characters = list(characters)

        # STEP 3: Helpful detection
        helpful_chars = set()

        for ticket in tickets:
            for ch in ticket.ticket_id:
                if ch not in shown_chars:
                    helpful_chars.add(ch)

        # STEP 4: 20–30% helpful probability
        chance = random.random()

        if chance < 0.3:
            possible = [c for c in safe_characters if c in helpful_chars]
            value = random.choice(possible) if possible else random.choice(safe_characters)
        else:
            possible = [c for c in safe_characters if c not in helpful_chars]
            value = random.choice(possible) if possible else random.choice(safe_characters)

    # STEP 5: Optional double character (still safe)
    if random.random() > 0.5:
        value += random.choice(characters)

    # -----------------------------------------
    # SAVE SPIN
    # -----------------------------------------
    SpinResult.objects.create(session=session, value=value)

    session.spin_count += 1
    session.save()

    # ==========================================================
    # 🔥 AUTO WINNER DETECTION
    # ==========================================================
    spins = SpinResult.objects.filter(session=session).values_list("value", flat=True)

    displayed_chars = []
    for spin in spins:
        for ch in spin:
            displayed_chars.append(ch)

    for ticket in tickets:

        full_match = True

        for ch in ticket.ticket_id:
            if ch not in displayed_chars:
                full_match = False
                break

        if full_match:

            assign_prize(ticket, session)
            break

    return JsonResponse({
        "status": "ok",
        "value": value
    })
    
    
    
    
    
    # your imports
from django.utils import timezone
from django.http import JsonResponse
from .models import Ticket, GameSession, SpinResult
import random
import string

# ==========================================================
# CONTROLLED SPIN ENGINE (FINAL STABLE VERSION)
# ==========================================================
from django.utils import timezone
from django.http import JsonResponse
import random
import string


def controlled_spin(request):

    session = GameSession.objects.filter(is_active=True).last()

    if not session:
        return JsonResponse({"status": "error", "message": "Game not active"})

    characters = string.ascii_uppercase + string.digits
    value = None  # prevent undefined error

    # -----------------------------------------
    # Collect Previous Spins
    # -----------------------------------------
    previous_spins = list(
        SpinResult.objects.filter(session=session)
        .values_list("value", flat=True)
    )

    shown_chars = []
    for spin in previous_spins:
        for ch in spin:
            shown_chars.append(ch)

    # -----------------------------------------
    # Eligible Tickets
    # -----------------------------------------
    tickets = Ticket.objects.filter(
        is_paid=True,
        is_validated=True,
        is_winner=False
    )

    # ==========================================================
    # 🔴 MANUAL FORCED WINNER MODE
    # ==========================================================
    if session.forced_winner and session.forced_winner in tickets:

        forced_ticket = session.forced_winner
        missing = []

        for ch in forced_ticket.ticket_id:
            if ch not in shown_chars:
                missing.append(ch)

        if missing:
            value = missing[0]
        else:
            value = random.choice(characters)

    # ==========================================================
    # 🔵 NORMAL SAFE MODE
    # ==========================================================
    else:

        # STEP 1: Conflict detection
        completion_risk = {}

        for ticket in tickets:

            missing = []

            for ch in ticket.ticket_id:
                if ch not in shown_chars:
                    missing.append(ch)

            if len(missing) == 1:
                last_char = missing[0]
                completion_risk[last_char] = completion_risk.get(last_char, 0) + 1

        # STEP 2: Safe character pool
        safe_characters = []

        for c in characters:
            if completion_risk.get(c, 0) <= 1:
                safe_characters.append(c)

        if not safe_characters:
            safe_characters = list(characters)

        # STEP 3: Helpful characters
        helpful_chars = set()

        for ticket in tickets:
            for ch in ticket.ticket_id:
                if ch not in shown_chars:
                    helpful_chars.add(ch)

        # STEP 4: Controlled probability
        chance = random.random()

        if chance < 0.3:
            possible = [c for c in safe_characters if c in helpful_chars]
            if possible:
                value = random.choice(possible)
            else:
                value = random.choice(safe_characters)
        else:
            possible = [c for c in safe_characters if c not in helpful_chars]
            if possible:
                value = random.choice(possible)
            else:
                value = random.choice(safe_characters)

    # STEP 5: Optional Double Character
    if value is None:
        value = random.choice(characters)

    if random.random() > 0.5:
        value += random.choice(characters)

    # -----------------------------------------
    # SAVE SPIN
    # -----------------------------------------
    SpinResult.objects.create(session=session, value=value)

    session.spin_count += 1
    session.save()

    # ==========================================================
    # 🔥 AUTO WINNER DETECTION
    # ==========================================================
    spins = SpinResult.objects.filter(session=session).values_list("value", flat=True)

    displayed_chars = []
    for spin in spins:
        for ch in spin:
            displayed_chars.append(ch)

    for ticket in tickets:

        full_match = True

        for ch in ticket.ticket_id:
            if ch not in displayed_chars:
                full_match = False
                break

        if full_match:
            assign_prize(ticket, session)
            break

    return JsonResponse({
        "status": "ok",
        "value": value
    })

# ==========================================================
# PRIZE ASSIGN FUNCTION (ADD HERE)
# ==========================================================
def assign_prize(ticket, session):

    now = timezone.now()

    if not session.first_prize_given:

        if not session.allow_first_prize:
            return

        if not session.first_prize_time_allowed():
            return

        ticket.prize_position = 1
        session.first_prize_given = True

    elif not session.second_prize_given:

        if not session.allow_second_prize:
            return

        ticket.prize_position = 2
        session.second_prize_given = True

    elif not session.third_prize_given:

        if not session.allow_third_prize:
            return

        ticket.prize_position = 3
        session.third_prize_given = True

    elif not session.fourth_prize_given:

        if not session.allow_fourth_prize:
            return

        ticket.prize_position = 4
        session.fourth_prize_given = True

    else:
        return

    ticket.is_winner = True
    ticket.save()

    session.forced_winner = None
    session.forced_prize_position = None
    session.save()
    
# ==========================================================
# VERIFY TICKET CLAIM (SEQUENCE-AWARE VERSION)
# ==========================================================
def verify_ticket_claim(request):

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"})

    ticket_code = request.POST.get("ticket_id", "").strip().upper()

    if not ticket_code:
        return JsonResponse({"status": "error", "message": "No ticket provided"})

    # -------------------------------
    # Get Ticket
    # -------------------------------
    try:
        ticket = Ticket.objects.get(ticket_id=ticket_code)
    except Ticket.DoesNotExist:
        return JsonResponse({
            "status": "invalid",
            "message": "Ticket not found"
        })

    # -------------------------------
    # Basic Validations
    # -------------------------------
    if not ticket.is_paid:
        return JsonResponse({
            "status": "invalid",
            "message": "Ticket not paid"
        })

    if not ticket.is_validated:
        return JsonResponse({
            "status": "invalid",
            "message": "Ticket not validated"
        })

    if ticket.is_winner:
        return JsonResponse({
            "status": "invalid",
            "message": "Ticket already won"
        })

    # -------------------------------
    # Get Active Session
    # -------------------------------
    session = GameSession.objects.filter(is_active=True).last()

    if not session:
        return JsonResponse({
            "status": "error",
            "message": "Game not active"
        })

    # -------------------------------
    # Collect All Spin Results
    # -------------------------------
    spins = SpinResult.objects.filter(session=session).values_list("value", flat=True)

    ticket_code = ticket.ticket_id
    matched_positions = [False] * len(ticket_code)

    # -------------------------------
    # Apply Matching Logic
    # -------------------------------
    for spin in spins:

        spin = spin.strip().upper()

        # -------- SINGLE LETTER --------
        if len(spin) == 1:
            for i, ch in enumerate(ticket_code):
                if ch == spin:
                    matched_positions[i] = True

        # -------- DOUBLE LETTER (STRICT SEQUENCE) --------
        elif len(spin) == 2:
            if spin in ticket_code:
                start_index = ticket_code.find(spin)
                matched_positions[start_index] = True
                matched_positions[start_index + 1] = True

    # -------------------------------
    # Check Missing Characters
    # -------------------------------
    missing_chars = []

    for i, matched in enumerate(matched_positions):
        if not matched:
            missing_chars.append(ticket_code[i])

    if missing_chars:
        return JsonResponse({
            "status": "invalid",
            "message": f"Still missing: {', '.join(missing_chars)}"
        })

    # -------------------------------
    # Prize Allocation
    # -------------------------------
    if not session.first_prize_given:
        prize_position = 1
        session.first_prize_given = True

    elif not session.second_prize_given:
        prize_position = 2
        session.second_prize_given = True

    elif not session.third_prize_given:
        prize_position = 3
        session.third_prize_given = True

    elif not session.fourth_prize_given:
        prize_position = 4
        session.fourth_prize_given = True

    else:
        return JsonResponse({
            "status": "closed",
            "message": "All prizes already distributed"
        })

    # -------------------------------
    # Mark Winner
    # -------------------------------
    ticket.is_winner = True
    ticket.prize_position = prize_position
    ticket.save()

    session.save()

    return JsonResponse({
        "status": "winner",
        "prize": prize_position,
        "ticket": ticket.ticket_id
    })

# ==========================================================
# START GAME SESSION
# ==========================================================
def start_game_session(request):

    GameSession.objects.update(is_active=False)

    GameSession.objects.create(is_active=True)

    return JsonResponse({
        "status": "started"
    })



from django.shortcuts import render

def login_options(request):
    return render(request, 'accounts/login_options.html')




from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Teacher   # Make sure Teacher model exists


def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Check if user belongs to Teacher group
            if not user.groups.filter(name='Teacher').exists():
                return render(request, 'teacher/login.html', {
                    'error': 'You are not authorized as a teacher.'
                })

            # Check if teacher profile exists
            try:
                teacher = Teacher.objects.get(user=user)
            except Teacher.DoesNotExist:
                return render(request, 'teacher/login.html', {
                    'error': 'Teacher profile not found.'
                })

            # Check if approved
            if teacher.status != "Approved":
                return render(request, 'teacher/login.html', {
                    'error': 'Your account is not approved yet.'
                })

            login(request, user)

            # First login password change check
            if teacher.first_login:
                return redirect('change_password')

            return redirect('teacher_dashboard')

        else:
            return render(request, 'teacher/login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'teacher/login.html')




def teacher_logout(request):
    logout(request)
    return redirect('teacher_login')




from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings
import random
import string

import random
import string
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .models import Teacher


def teacher_signup(request):

    if request.method == "POST":

        # Basic Info
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        contact_no = request.POST.get('contact_no')
        emergency_contact = request.POST.get('emergency_contact')
        relation = request.POST.get('relation')
        married = request.POST.get('married')
        subject = request.POST.get('subject')
        experience = request.POST.get('experience')
        address = request.POST.get('address')

        # Qualification
        qualification_level = request.POST.get('qualification_level')
        qualification_status = request.POST.get('qualification_status')
        qualification_docs = request.FILES.get('qualification_docs')

        # Document Info
        document_type = request.POST.get('document_type')
        document_number = request.POST.get('document_number')
        issued_date = request.POST.get('issued_date')
        expiry_date = request.POST.get('expiry_date')
        issuing_authority = request.POST.get('issuing_authority')

        # Files
        profile_image = request.FILES.get('profile_image')

        # Check if email exists
        if Teacher.objects.filter(email=email).exists():
            return render(request, 'teacher/signup.html', {
                'error': 'Email already registered'
            })

        # If qualification completed but no file uploaded
        if qualification_status == "Completed" and not qualification_docs:
            return render(request, 'teacher/signup.html', {
                'error': 'Qualification document is required if completed.'
            })

        # Generate Username & Password
        username = email.split("@")[0] + str(random.randint(100, 999))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True
        )

        # Assign Teacher Group
        teacher_group, created = Group.objects.get_or_create(name="Teacher")
        user.groups.add(teacher_group)

        # Create Teacher Profile
        Teacher.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            dob=dob,
            contact_no=contact_no,
            emergency_contact=emergency_contact,
            relation=relation,
            married=married,
            subject=subject,
            experience=experience,
            address=address,
            qualification_level=qualification_level,
            qualification_status=qualification_status,
            qualification_docs=qualification_docs,
            document_type=document_type,
            document_number=document_number,
            issued_date=issued_date,
            expiry_date=expiry_date,
            issuing_authority=issuing_authority,
            profile_image=profile_image,
            status="Pending"
        )

        return render(request, 'teacher/signup_success.html')

    return render(request, 'teacher/signup.html')



from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Teacher


def teacher_login(request):

    if request.method == "POST":
        input_value = request.POST.get('username')
        password = request.POST.get('password')

        # 🔥 Check if input is email
        try:
            user_obj = User.objects.get(email=input_value)
            username = user_obj.username
        except User.DoesNotExist:
            username = input_value  # Assume it's already username

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Check if user belongs to Teacher group
            if not user.groups.filter(name='Teacher').exists():
                return render(request, 'teacher/login.html', {
                    'error': 'You are not authorized as a teacher.'
                })

            # Get teacher profile safely
            try:
                teacher = Teacher.objects.get(user=user)
            except Teacher.DoesNotExist:
                return render(request, 'teacher/login.html', {
                    'error': 'Teacher profile not found.'
                })

            # Check approval status
            if teacher.status != "Approved":
                return render(request, 'teacher/login.html', {
                    'error': 'Your account is not approved yet.'
                })

            login(request, user)

            # 🔥 Force password change on first login
            if teacher.first_login:
                return redirect('change_password')

            return redirect('teacher_dashboard')

        # If authentication failed
        return render(request, 'teacher/login.html', {
            'error': 'Invalid username/email or password.'
        })

    return render(request, 'teacher/login.html')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            teacher = Teacher.objects.get(user=request.user)
            teacher.first_login = False
            teacher.save()

            return redirect('teacher_dashboard')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'teacher/change_password.html', {'form': form})




from django.contrib.auth.decorators import login_required

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')




from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings

import random
import string
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings


def approve_teacher(request, pk):

    teacher = get_object_or_404(Teacher, pk=pk)

    # Generate Joining Year
    joining_year = timezone.now().year

    # Count how many teachers already approved this year
    count = Teacher.objects.filter(status="Approved").count() + 1

    # Format number with leading zero
    teacher_number = str(count).zfill(2)

    # Generate Username
    username = f"SEBS-{joining_year}-T-{teacher_number}"

    # Generate Temporary Password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Update User
    user = teacher.user
    user.username = username
    user.set_password(temp_password)
    user.save()

    # Update Teacher
    teacher.status = "Approved"
    teacher.first_login = True
    teacher.save()

    # Send Email with Username & Password
    send_mail(
        "Welcome to Saraswoti English Boarding School",
        f"""
Dear {teacher.full_name},

Congratulations! Your registration has been approved.

Your Login Credentials:

Username: {username}
Temporary Password: {temp_password}

Please login and change your password immediately.

Regards,
Saraswoti English Boarding School
""",
        settings.EMAIL_HOST_USER,
        [teacher.email],
        fail_silently=False,
    )

    return redirect('/admin/school/teacher/')


def reject_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.status = "Rejected"
    teacher.save()
    return redirect('/admin/school/teacher/')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def create_lesson_plan(request):
    return render(request, 'teacher/lesson_plan.html')



def spin_history(request):

    session = GameSession.objects.filter(is_active=True).last()

    if not session:
        return JsonResponse({
            "status": "error"
        })

    spins = list(
        SpinResult.objects.filter(session=session)
        .values_list("value", flat=True)
    )

    return JsonResponse({
        "status": "ok",
        "history": spins
    })