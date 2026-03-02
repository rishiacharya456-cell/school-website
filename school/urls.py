from django.urls import path
from . import views
from .views import login_options
from .views import teacher_login, teacher_logout,teacher_signup, teacher_dashboard, change_password, create_lesson_plan

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('admission/', views.admission, name='admission'),
    path('career/', views.career, name='career'),  
    path('google-reviews/', views.google_reviews, name='google_reviews'),
     path('apply/', views.apply, name='apply'),
     path('academics/', views.explore_academics, name='academics'),
     path('admission/', views.admission, name='admission'),
     path('preschool/', views.preschool, name='preschool'),
     path('events/', views.events, name='events'),
     path('events/<int:pk>/', views.event_detail, name='event_detail'),
     path('primary/', views.primary, name='primary'),
      path('secondary/', views.secondary, name='secondary'),
      path('learning-approach/', views.learning_approach, name='learning_approach'),
      path("student-clubs/", views.student_clubs, name="student_clubs"),
    path("house-activities/", views.house_activities, name="house_activities"),
    path("generate-print/<int:count>/", views.generate_and_print_tickets, name="generate_print"),
    path('login/', login_options, name='login_options'),
    path('teacher/login/', teacher_login, name='teacher_login'),
    path('teacher/logout/', teacher_logout, name='teacher_logout'),
    path('teacher/login/', teacher_login, name='teacher_login'),
    path('teacher/signup/', teacher_signup, name='teacher_signup'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/change-password/', change_password, name='change_password'),
    path('teacher/signup/', teacher_signup, name='teacher_signup'),
     path('teacher/lesson-plan/', create_lesson_plan, name='lesson_plan'),
     path("verify-claim/", views.verify_ticket_claim, name="verify_claim"),
    path("start-game/", views.start_game_session, name="start_game"),
    path("spin/", views.controlled_spin, name="controlled_spin"),
    path("spin-history/", views.spin_history, name="spin_history"),

 
]
 