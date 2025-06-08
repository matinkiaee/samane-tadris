
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .forms import TeacherApplicationForm
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile





class UserAuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='1234abcd',
            email='test@example.com',
            role='teacher'
        )

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '1234abcd'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, reverse('dashboard_teacher'))

    def test_wrong_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'wrong',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نام کاربری یا رمز عبور اشتباه است.')








class TeacherApplicationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='formuser',
            password='pass1234',
            role='teacher',
            national_id='1122334455',
            phone='09123456780',
            email='form@test.com'
        )

    def test_valid_form(self):
        form_data = {
            'national_id': '1234567890',
            'phone': '09123456789',
            'birth_date': '2000-01-01',
            'address': 'تهران، میدان ولیعصر، پلاک ۱۲',
            'gender': 'male',
            'religion': 'اسلام',
            'degree': 'کارشناسی',
            'field_of_study': 'کامپیوتر',
            'university': 'تهران'
        }

        file_data = {
            'resume': SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf"),
            'national_card': SimpleUploadedFile("card.pdf", b"file_content", content_type="application/pdf"),
            'degree_certificate': SimpleUploadedFile("degree.pdf", b"file_content", content_type="application/pdf"),
            'birth_certificate': SimpleUploadedFile("birth.pdf", b"file_content", content_type="application/pdf")
        }

        form = TeacherApplicationForm(data=form_data, files=file_data)
        form.instance.user = self.user

        # 👇 چاپ خطاهای فرم برای بررسی
        print("Form Errors:", form.errors)

        self.assertTrue(form.is_valid())