from django.urls import path
from django.contrib.auth import views as auth_views
from .views import group_manager_dashboard,security_dashboard,province_admin_dashboard, admin_panel_view
from .views import group_review_application,security_review_application,province_final_review

from .views import (
    register_view,
    login_view,
    logout_view,
    CustomPasswordChangeView,
    apply_teacher_view,
    dashboard_teacher_view,
    review_applications_view,
)



urlpatterns = [
    # احراز هویت
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),

    # پنل مدرس
    path('apply/', apply_teacher_view, name='apply_teacher'),
    path('dashboard/', dashboard_teacher_view, name='dashboard_teacher'),

    # پنل مدیر گروه برای بررسی درخواست‌ها
    path('applications/review/', review_applications_view, name='review_applications'),

    # تغییر رمز موفق
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('dashboard/group/', group_manager_dashboard, name='dashboard_group_manager'),
    path('dashboard/security/', security_dashboard, name='dashboard_security'),
    path('dashboard/province/', province_admin_dashboard, name='dashboard_province_admin'),
    path('dashboard/admin/', admin_panel_view, name='dashboard_admin'),
    path('application/<int:pk>/review/group/', group_review_application, name='group_review_application'),
    path('application/<int:pk>/review/security/', security_review_application, name='security_review_application'),
    path('application/<int:pk>/review/final/', province_final_review, name='province_final_review'),
    
]

