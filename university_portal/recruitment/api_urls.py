from django.urls import path
from .api_views import TeacherApplicationListCreate, TeacherApplicationDetail
from .api_views import ApplicationReviewAPIView



urlpatterns = [
    path('applications/', TeacherApplicationListCreate.as_view(), name='api_applications'),
    path('applications/<int:pk>/', TeacherApplicationDetail.as_view(), name='api_application_detail'),
    path('applications/<int:pk>/review/', ApplicationReviewAPIView.as_view(), name='api_application_review'),
    
]