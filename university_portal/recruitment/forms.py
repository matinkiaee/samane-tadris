from django import forms
from .models import TeacherApplication, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import TeacherApplication
import re
from datetime import date







class TeacherApplicationForm(forms.ModelForm):
    class Meta:
        model = TeacherApplication
        exclude = ['user', 'created_at', 'status', 'teacher_code', 'final_score', 'interview_result']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if not re.match(r'^\d{10}$', national_id):
            raise forms.ValidationError("کد ملی باید دقیقاً ۱۰ رقم باشد.")
        return national_id

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^09\d{9}$', phone):
            raise forms.ValidationError("شماره تلفن باید با ۰۹ شروع شود و ۱۱ رقم باشد.")
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            age = (date.today() - birth_date).days // 365
            if age < 22:
                raise forms.ValidationError("سن شما باید حداقل ۲۲ سال باشد.")
        return birth_date

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if not resume:
            raise forms.ValidationError("ارسال فایل رزومه الزامی است.")
        return resume

    def clean_degree_certificate(self):
        degree = self.cleaned_data.get('degree_certificate')
        if not degree:
            raise forms.ValidationError("مدرک تحصیلی الزامی است.")
        return degree

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance.user if self.instance else self.initial.get('user')
        if TeacherApplication.objects.filter(user=user).exists():
            raise forms.ValidationError("شما قبلاً یک درخواست ثبت کرده‌اید.")
        return cleaned_data





class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'national_id', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'  # نقش پیش‌فرض برای ثبت‌نام
        if commit:
            user.save()
        return user
    



#ساخت فرم برای ارزیابی نهایی
class InterviewEvaluationForm(forms.ModelForm):
    class Meta:
        model = TeacherApplication
        fields = ['final_score', 'interview_result']
        widgets = {
            'interview_result': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_final_score(self):
        score = self.cleaned_data.get('final_score')
        if score is not None and (score < 0 or score > 100):
            raise forms.ValidationError("نمره باید بین ۰ تا ۱۰۰ باشد.")
        return score
    





