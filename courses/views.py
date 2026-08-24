from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Lecture, Course, Enrollment

# الصفحة الرئيسية (تعرض الكورسات والمحاضرات)
def home(request):
    courses = Course.objects.all()
    lectures = Lecture.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'courses': courses,
        'lectures': lectures
    })

# صفحة لوحة تحكم رفع المحاضرات
@user_passes_test(lambda user: user.is_staff, login_url='login')
def admin_page(request):
    courses = Course.objects.all().order_by('title')

    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        course_id = request.POST.get('course')

        if title and link and course_id:
            course = get_object_or_404(Course, id=course_id)
            lecture = Lecture(title=title, link=link, course=course)
            try:
                lecture.full_clean()
                lecture.save()
            except ValidationError:
                messages.error(request, 'الرابط غير صحيح. ابدئيه بـ https://')
            else:
                messages.success(request, 'تمت إضافة رابط المحاضرة للكورس بنجاح.')
                return redirect('admin_page')

        messages.error(request, 'اكتبي العنوان، اختاري الكورس، وضعي الرابط الصحيح.')

    return render(request, 'admin.html', {'courses': courses})

# صفحة الطلاب (الرئيسية سابقة)
def student_page(request):
    lectures = Lecture.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'lectures': lectures})

# تسجيل دخول الطلاب
def student_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'login.html')

# لوحة الطالب (Dashboard)
@login_required(login_url='login')
def dashboard(request):
    courses = Course.objects.all()
    
    # نجيب فقط أسامي الكورسات اللي الطالب حجزها وتم الموافقة عليها من الأدمن
    user_enrolled_courses = Enrollment.objects.filter(user=request.user, is_approved=True).values_list('course_id', flat=True)
    
    # المحاضرات تظهر فقط للكورسات المحجوزة
    lectures = Lecture.objects.filter(course_id__in=user_enrolled_courses).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'courses': courses,
        'lectures': lectures,
        'user_enrolled_courses': user_enrolled_courses,
    })

# تسجيل الخروج
def user_logout(request):
    logout(request)
    return redirect('login')

# إنشاء حساب طالب جديد
def register(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل، اختر اسماً آخر')
        else:
            # إنشاء المستخدم وتشفير كلمة المرور تلقائياً
            user = User.objects.create_user(username=u, email=email, password=p)
            login(request, user) # تسجيل دخوله مباشرة بعد إنشاء الحساب
            return redirect('dashboard')
            
    return render(request, 'register.html')
@login_required(login_url='login')
def course_lectures(request, course_id):
    # التأكد أن الطالب حجز الكورس ده وتم الموافقة عليه
    is_enrolled = Enrollment.objects.filter(user=request.user, course_id=course_id, is_approved=True).exists()
    
    if not is_enrolled:
        messages.error(request, 'عفواً، هذا الكورس غير مفعل لحسابك.')
        return redirect('dashboard')
        
    course = Course.objects.get(id=course_id)
    lectures = Lecture.objects.filter(course=course).order_by('-created_at')
    
    return render(request, 'course_lectures.html', {
        'course': course,
        'lectures': lectures
    })
