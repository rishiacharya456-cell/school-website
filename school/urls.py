from django.urls import path
from . import views

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
    


 
]
 