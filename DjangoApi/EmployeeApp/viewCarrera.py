from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # Esto es para acceder al API
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import  Cliente1, EstudianteCreate, EstudianteReturn

from types import SimpleNamespace as Namespace 
import pyodbc
import json

from .conexion import Conexion

class CarreraApi:
    @csrf_exempt
    def getListaCarreras(request):

        try:
            response = ""
            estado_conexion = False 
            conn = Conexion.get_string_conection()
                    
            cursor = conn.cursor() 
            cursor.execute("""SELECT *  
                            FROM Carrera FOR JSON AUTO""")
        
            rows = cursor.fetchall()
            #print('\n\n\nRE S PONSEEE   ', rows)

            if len(rows)>0:
                response = json.loads(''.join([row[0] for row in rows]))


            else:
                response = {"message": "No hay datos almacenados"} 

            return JsonResponse(response, safe=False)

        except:
            response = {"estado": "fail"}
            return JsonResponse(estudiante, safe = True)
                

            