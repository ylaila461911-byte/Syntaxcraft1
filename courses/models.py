from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)

    def __str__(self):
        return self.title

class Lecture(models.Model):
    # ربط المحاضرة بكورس معين (بحيث تظهر فقط للـ كورس ده)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', null=True, blank=True)
    title = models.CharField(max_length=200)
    # Existing local uploads stay in place. New lessons use the link field.
    file = models.FileField(upload_to='lectures/', blank=True, null=True)
    link = models.URLField('رابط المحاضرة أو اللايف', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# موديل تسجيل وحجز الطلاب للكورسات
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False) # بتفعليها من الأدمن بعد الدفع والحجز
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
