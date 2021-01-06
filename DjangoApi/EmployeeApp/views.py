from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # Esto es para acceder al API
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmployeeApp.models import Department, Employee, Student
from EmployeeApp.serializersApp import EmployeeSerializer, DeparmentSerializer, StudentSerializer

# Create your views here.
@csrf_exempt
def departmentApi(request, id=0):
    if request.method == 'GET':
        departments = Department.objects.all()
        departments_serializer = DeparmentSerializer(departments, many=True)
        return JsonResponse(departments_serializer.data, safe=False)

    elif request.method == 'POST':
        department_data = JSONParser().parse(request)
        department_serializer = DeparmentSerializer(data= department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("hah", safe= False)

        return JsonResponse("hola!!", safe = False)

@csrf_exempt
def EmployeeApi(request, id=0):
    if request.method == 'GET':
        employees = Employee.objects.all()
        employee_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employee_serializer.data, safe=False)
        

    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        employee_serializer = EmployeeSerializer(data= employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse(employee_serializer.data, safe= False)

        return JsonResponse("no!!", safe = False )


@csrf_exempt
def StudentApi(request, id=0):
    if request.method == 'GET':
        students = Student.objects.all()
        student_serializer = StudentSerializer(students, many=True)
        return JsonResponse(student_serializer.data, safe=False)

    elif request.method == 'POST':
        student_saved = False
        student_data = JSONParser().parse(request)
        student_serializer = DeparmentSerializer(data= student_data)
        
        if student_serializer.is_valid():
            student_serializer.save()
            student_saved = True
        
        if student_saved:
            return JsonResponse(student_serializer.data, safe= True)
        
        else:
            return JsonResponse("Failure", safe = False )
