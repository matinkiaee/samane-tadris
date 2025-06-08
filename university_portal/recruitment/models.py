from django.contrib.auth.models import AbstractUser
from django.db import models



# کاربر اصلی سیستم با نقش‌های مختلف
class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'مدرس'),
        ('province_admin', 'مدیر استان'),
        ('security', 'کارشناس حراست'),
        ('group_manager', 'مدیر گروه'),
    ]
    national_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return self.username




# فرم اطلاعات متقاضی تدریس
class TeacherApplication(models.Model):
    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=30)
    address = models.TextField()

    # فایل‌ها و مستندات
    national_card = models.FileField(upload_to='documents/national_card/')
    birth_certificate = models.FileField(upload_to='documents/birth_certificate/')
    resume = models.FileField(upload_to='documents/resumes/')
    degree_certificate = models.FileField(upload_to='documents/degrees/')

    # تحصیلات و تخصص
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    university = models.CharField(max_length=100)

    # وضعیت بررسی
    status = models.CharField(max_length=30, default='در حال بررسی')
    interview_result = models.TextField(blank=True, null=True)
    final_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    teacher_code = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    


    
    
class TeachingExperience(models.Model):
    application = models.ForeignKey(TeacherApplication, on_delete=models.CASCADE, related_name='teaching_experiences')
    semester = models.CharField(max_length=20)
    university = models.CharField(max_length=100)
    credit_hours = models.IntegerField()
    certificate = models.FileField(upload_to='documents/teaching_certificates/')

    def __str__(self):
        return f"{self.university} - {self.semester}"







#register/
#login/
#dashboard/teacher/