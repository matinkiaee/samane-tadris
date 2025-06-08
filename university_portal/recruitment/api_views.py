from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import TeacherApplication
from .serializers import TeacherApplicationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
import random



class TeacherApplicationListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'teacher':
            apps = TeacherApplication.objects.filter(user=user)

        elif user.role == 'group_manager':
            apps = TeacherApplication.objects.all()

        elif user.role == 'security':
            apps = TeacherApplication.objects.filter(status='ارسال به حراست')

        elif user.role == 'province_admin':
            apps = TeacherApplication.objects.filter(status='ارسال به معاون آموزشی')

        elif user.is_superuser:
            apps = TeacherApplication.objects.all()

        else:
            return Response({'detail': 'دسترسی ندارید.'}, status=403)

        serializer = TeacherApplicationSerializer(apps, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'teacher':
            return Response({'detail': 'فقط مدرس می‌تواند درخواست ثبت کند.'}, status=403)

        serializer = TeacherApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherApplicationDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        application = get_object_or_404(TeacherApplication, pk=pk)
        serializer = TeacherApplicationSerializer(application)
        return Response(serializer.data)

    def put(self, request, pk):
        application = get_object_or_404(TeacherApplication, pk=pk)
        serializer = TeacherApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    








class IsGroupManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'group_manager'

class IsSecurity(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'security'

class IsProvinceAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'province_admin'


# ویوی بررسی توسط نقش خاص
class ApplicationReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        application = get_object_or_404(TeacherApplication, pk=pk)

        role = request.user.role
        data = {}

        decision = request.data.get('decision')

        if role == 'group_manager':
            if decision == 'approve':
                application.status = 'ارسال به حراست'
            elif decision == 'reject':
                application.status = 'رد شده توسط مدیر گروه'

        elif role == 'security':
            if decision == 'approve':
                application.status = 'ارسال به معاون آموزشی'
            elif decision == 'reject':
                application.status = 'رد شده توسط حراست'

        elif role == 'province_admin':
            if decision == 'approve':
                application.status = 'تایید نهایی'
                if not application.teacher_code:
                    application.teacher_code = f"TCHR{random.randint(1000, 9999)}"
            elif decision == 'reject':
                application.status = 'رد شده توسط معاون آموزشی'

        else:
            return Response({'detail': 'شما دسترسی ندارید.'}, status=403)

        application.save()
        serializer = TeacherApplicationSerializer(application)
        return Response(serializer.data)
