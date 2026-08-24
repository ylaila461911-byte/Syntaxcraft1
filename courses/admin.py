from django.contrib import admin
from .models import Lecture, Course, Enrollment

admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(Enrollment)