from rest_framework import serializers
from .models import TeacherApplication, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'national_id', 'role']

class TeacherApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherApplication
        fields = '__all__'