from rest_framework import serializers
from Employee.models import Employee

class Employee_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['Happy','Neutral','Sad','Angry','Disgusted','Timestamp']
