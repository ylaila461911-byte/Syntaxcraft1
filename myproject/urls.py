from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from courses.views import admin_page, student_page

urlpatterns = [
    path('admin-panel/', admin_page, name='admin_page'),
    path('', student_page, name='student_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)