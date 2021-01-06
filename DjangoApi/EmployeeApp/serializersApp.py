from rest_framework import serializers
from EmployeeApp.models import Department, Employee, Student


class DeparmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('DepartmentId',
                  'DepartmentName')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('Id',
                  'Name',
                  'Department',
                  'Date_joining',
                  'PhotoFileName')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','name','phone','address','Grade','createdDate','lastUpdatedDate','grade','gender')
        