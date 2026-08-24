from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from courses.views import admin_page, student_page, student_login, user_logout, register, dashboard
from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', admin_page, name='admin_page'),
    path('login/', student_login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout'),
    path('', register, name='home'),
    path('course/<int:course_id>/lectures/', views.course_lectures, name='course_lectures'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
