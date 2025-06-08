from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .forms import TeacherApplicationForm
from .models import TeacherApplication
from django.contrib.auth.decorators import user_passes_test
from .models import TeacherApplication
from django.shortcuts import render
from django.shortcuts import get_object_or_404  
from .models import TeacherApplication
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from .forms import InterviewEvaluationForm
from django.core.mail import send_mail
from .utils import is_group_manager


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'teacher'  # فقط مدرس می‌تونه ثبت‌نام کنه
            user.save()
            login(request, user)
            return redirect('dashboard_teacher')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # ریدایرکت به پنل هر نقش
            if user.role == 'teacher':
                return redirect('dashboard_teacher')
            elif user.role == 'group_manager':
                return redirect('dashboard_group_manager')
            elif user.role == 'security':
                return redirect('dashboard_security')
            elif user.role == 'province_admin':
                return redirect('dashboard_province_admin')
            else:
                return redirect('home')
        else:
            return render(request, 'registration/login.html', {
                'error': 'نام کاربری یا رمز عبور اشتباه است.'
            })
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')





class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')  # مسیر موفقیت




@login_required
def apply_teacher_view(request):
    try:
        existing_app = TeacherApplication.objects.get(user=request.user)
        return redirect('dashboard_teacher')  # اگر قبلاً ثبت کرده بود، به داشبورد بره
    except TeacherApplication.DoesNotExist:
        pass

    if request.method == 'POST':
        form = TeacherApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('dashboard_teacher')
    else:
        form = TeacherApplicationForm()

    return render(request, 'application/apply_teacher.html', {'form': form})







@login_required
def dashboard_teacher_view(request):
    try:
        application = TeacherApplication.objects.get(user=request.user)
    except TeacherApplication.DoesNotExist:
        application = None
    return render(request, 'dashboard/teacher.html', {
        'application': application
    })




#مدیر گروه اموزشی 
def is_group_manager(user):
    return user.is_authenticated and user.role == 'group_manager'

@user_passes_test(is_group_manager)
def group_manager_dashboard(request):
    applications = TeacherApplication.objects.all()
    return render(request, 'dashboard/group_manager.html', {'applications': applications})





@user_passes_test(is_group_manager)
def review_applications_view(request):
    applications = TeacherApplication.objects.all()
    return render(request, 'dashboard/review_applications.html', {'applications': applications})




#پنل کارشناس حراست
def is_security(user):
    return user.is_authenticated and user.role == 'security'

@user_passes_test(is_security)
def security_dashboard(request):
    applications = TeacherApplication.objects.all()
    return render(request, 'dashboard/security.html', {'applications': applications})





def is_province_admin(user):
    return user.is_authenticated and user.role == 'province_admin'

@user_passes_test(is_province_admin)
def province_admin_dashboard(request):
    applications = TeacherApplication.objects.filter(status='در حال بررسی')
    return render(request, 'dashboard/province_admin.html', {'applications': applications})
    


#پنل معاون آموزشی استان

def is_province_admin(user):
    return user.is_authenticated and user.role == 'province_admin'

@user_passes_test(is_province_admin)
def province_admin_dashboard(request):
    applications = TeacherApplication.objects.filter(status='در حال بررسی')
    return render(request, 'dashboard/province_admin.html', {'applications': applications})





#پنل مدیر سیستم (ادمین اصلی)

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_panel_view(request):
    return render(request, 'dashboard/admin.html')



#________________________________________________________________________________________________________________


#وضعیت رد و تایید درخاست ها 
#مدیر گروه - بررسی اولیه درخواست
@user_passes_test(is_group_manager)
def group_review_application(request, pk):
    application = get_object_or_404(TeacherApplication, pk=pk)
    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision == 'approve':
            application.status = 'ارسال به حراست'
        elif decision == 'reject':
            application.status = 'رد شده توسط مدیر گروه'
        application.save()
        return HttpResponseRedirect(reverse('dashboard_group_manager'))
    return render(request, 'review/group_review.html', {'application': application})



#کارشناس حراست - بررسی امنیتی
@user_passes_test(is_security)
def security_review_application(request, pk):
    application = get_object_or_404(TeacherApplication, pk=pk)

    if request.method == 'POST':
        form = InterviewEvaluationForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            decision = request.POST.get('decision')

            if decision == 'approve':
                app.status = 'ارسال به معاون آموزشی'

                # ارسال ایمیل به مدرس
                send_mail(
                    subject='بررسی اولیه شما تأیید شد',
                    message=f'سلام {app.user.username}، درخواست شما تأیید و به مرحله بعد ارسال شد.',
                    from_email=None,  # از تنظیمات settings خوانده می‌شود
                    recipient_list=[app.user.email],
                    fail_silently=True,
                )

            elif decision == 'reject':
                app.status = 'رد شده توسط حراست'

            app.save()
            return HttpResponseRedirect(reverse('dashboard_security'))

    else:
        form = InterviewEvaluationForm(instance=application)

    return render(request, 'review/security_review.html', {
        'application': application,
        'form': form
    })




#معاون آموزشی - بررسی نهایی + صدور کد مدرسی


@user_passes_test(is_province_admin)
def province_final_review(request, pk):
    application = get_object_or_404(TeacherApplication, pk=pk)

    if request.method == 'POST':
        form = InterviewEvaluationForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            decision = request.POST.get('decision')
            if decision == 'approve':
                app.status = 'تایید نهایی'
                if not app.teacher_code:
                    app.teacher_code = f"TCHR{random.randint(1000, 9999)}"
            elif decision == 'reject':
                app.status = 'رد شده توسط معاون آموزشی'
            app.save()
            return redirect('dashboard_province_admin')
    else:
        form = InterviewEvaluationForm(instance=application)

    return render(request, 'review/province_review.html', {
        'form': form,
        'application': application
    })






