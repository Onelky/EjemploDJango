from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # Esto es para acceder al API
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import Department, Employee, Student, Cliente

from types import SimpleNamespace as Namespace 
import pyodbc
import json


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
class Cliente:

    def getClientes(request):
        if request.method ==  'GET':
                
            conn = pyodbc.connect('Driver={sql server};'
                                    'Server=ONELKY\SQLEXPRESS;' # Se sustituye con otros datos
                                    'Database=Administracion;'
                                    'Trusted_Connection=yes;')
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente FOR JSON AUTO")
            rows = cursor.fetchall()

            response = json.loads(''.join([row[0] for row in rows]))

        return JsonResponse(response, safe=False)

    @csrf_exempt
    def registrarCliente(request):

        response = ""
        if not request.body:
            response = {"message": "empty"}
            return JsonResponse(response, safe = True)

        else:     
            try:

                data =  json.loads(request.body, object_hook = lambda d : Namespace(**d))

                connection = pyodbc.connect('Driver={sql server};'
                                        'Server=ONELKY\SQLEXPRESS;'
                                        'Database=Administracion;'
                                        'Trusted_Connection=yes;')
                
                cursor = connection.cursor()
                query = "INSERT INTO Cliente (Nom_cli, Ape_cli) VALUES (?,?)" # Esta tabla se tiene que cambiar
                cursor.execute(query, [data.nombre, data.apellido])

                connection.commit()
                response = {"estado": "exito"}
                return JsonResponse(response, safe = True)
            
            except:
                response = {"estado": "fail"}
                return JsonResponse(response, safe = True)

