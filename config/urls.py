from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from school.views import approve_teacher, reject_teacher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),
    path('approve-teacher/<int:pk>/', approve_teacher, name='approve_teacher'),
    path('reject-teacher/<int:pk>/', reject_teacher, name='reject_teacher'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
