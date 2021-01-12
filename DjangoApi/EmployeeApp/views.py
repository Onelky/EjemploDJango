from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # Esto es para acceder al API
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import  Cliente1, EstudianteCreate, EstudianteReturn

from types import SimpleNamespace as Namespace 
import pyodbc
import json

from .conexion import Conexion


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
            response = {"message": "fail"}
            return JsonResponse(response, safe = True)

        else:     
            try:
                data =  json.loads(request.body)
                cliente = Cliente1(**data)

                            
                connection = Conexion.get_string_conection()

                print('\n\n\n CLIENTEEE  ', cliente)

                
                cursor = connection.cursor()
                query = "INSERT INTO Cliente (Nom_cli, Ape_cli) VALUES (?,?)" # Esta tabla se tiene que cambiar
                cursor.execute(query, [cliente.nombre, cliente.apellido])

                connection.commit()
                response = {"estado": "exito"}
                connection.close()
                return JsonResponse(response, safe = True)
            
            except:
                response = {"estado": "fail"}
                return JsonResponse(cliente, safe = True)

        """"
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
"""

class EstudianteApi:
    @csrf_exempt
    def getListaEstudiantes(request):

        response = ""
        estado_conexion = False 
        conn = Conexion.get_string_conection()
                
        cursor = conn.cursor() 
        cursor.execute("SELECT id_estudiante, p.Nombre, Apellido, car.Nombre, estado, Fecha_nacimiento,\
                        Cedula, CorreoPersonal, CorreoInstitucional, Telefono \
                        FROM Estudiante est\
                            INNER JOIN Persona p\
                                ON est.id_persona = p.id_persona\
                            INNER JOIN Tipo_Estado estado\
                                ON p.id_estado = estado.id_estado\
                            INNER JOIN Carrera car\
                                ON est.id_carrera = car.id_carrera \
                            FOR JSON AUTO")
       
        rows = cursor.fetchall()
        #print('\n\n\nRE S PONSEEE   ', rows)

        if len(rows)>0:
            response = json.loads(''.join([row[0] for row in rows]))


        else:
            response = {"message": "No hay datos almacenados"} 

        return JsonResponse(response, safe=False)

    @csrf_exempt
    def crearEstudiante(request):
        response = ""
        
        if not request.body:
            response = {"message": "No se pudo crear el usuario"}
            return JsonResponse(response, safe = True)

        else:     
            try:
                data =  json.loads(request.body)
                estudiante = EstudianteCreate(**data)
                print(estudiante)

                connection = Conexion.get_string_conection()

                print('\n\n\n  DATAA ', estudiante)
               
                cursor = connection.cursor()
                query = "INSERT INTO Persona(\
                        id_estado,\
                        Nombre,\
                        Apellido,\
                        Cedula,\
                        CorreoPersonal,\
                        Telefono,\
                        Fecha_nacimiento\
                        ) VALUES (?,?,?,?,?,?,?)" 

                # Primero se crea la persona
                            
                cursor.execute(query, [estudiante.id_estado, estudiante.Nombre, estudiante.Apellido, estudiante.Cedula, estudiante.CorreoPersonal, estudiante.Telefono, estudiante.Fecha_nacimiento])
                connection.commit()

                
                # Se crea el estudiante 

                query = f"INSERT INTO Estudiante(id_carrera, id_persona)\
                SELECT {estudiante.id_carrera}, MAX(id_persona)\
                FROM Persona"

                cursor.execute(query)
                connection.commit()


                response = {"estado": "exito"}
                connection.close()
                return JsonResponse(response, safe = True)
            
            except:
                response = {"estado": "fail"}
                return JsonResponse(estudiante, safe = True)
    
    @csrf_exempt
    def getEstudiante(request):
        response = ""
        conn = Conexion.get_string_conection()
        idP = json.loads(request.body)
        id_persona = idP["id"]

                
        cursor = conn.cursor() 
        cursor.execute("""SELECT id_estudiante, p.id_persona, p.Nombre, Apellido, 
                        car.Nombre, estado, Fecha_nacimiento,
                        Cedula, CorreoPersonal, CorreoInstitucional, Telefono 
                        FROM Estudiante est
                            INNER JOIN Persona p
                                ON est.id_persona = p.id_persona
                            INNER JOIN Tipo_Estado estado
                                ON p.id_estado = estado.id_estado
                            INNER JOIN Carrera car
                                ON est.id_carrera = car.id_carrera 
                        WHERE id_estudiante = ?
                            FOR JSON AUTO""", id_persona)
       
        rows = cursor.fetchall()
        #print('\n\n\nRE S PONSEEE   ', rows)

        if len(rows)>0:
            response = json.loads(''.join([row[0] for row in rows]))


        else:
            response = {"message": "No hay datos almacenados"} 

        return JsonResponse(response, safe=False)
    
    @csrf_exempt
    def editarEstudiante(request):
        response = ""
        
        if not request.body:
            response = {"message": "No se pudo actualizar el usuario"}
            return JsonResponse(response, safe = True)

        else:     
            try:
                data =  json.loads(request.body)
                estudiante = EstudianteCreate(**data)
                print(estudiante, '\n\n\n')

                connection = Conexion.get_string_conection()

               
                cursor = connection.cursor()
                query = """UPDATE Persona
                        SET id_estado = ?,
                        Nombre = ?,
                        Apellido = ?,
                        Cedula = ?,
                        CorreoPersonal = ?,
                        Telefono = ?,
                        Fecha_nacimiento = ?
                        
                        WHERE id_persona = ?""" 

                # Primero se crea la persona
                            
                cursor.execute(query, estudiante.id_estado, estudiante.Nombre, estudiante.Apellido, estudiante.Cedula, estudiante.CorreoPersonal, estudiante.Telefono, estudiante.Fecha_nacimiento, estudiante.id_persona)

                connection.commit()

                
                # Se edita el estudiante

                query = """UPDATE Estudiante
                        SET id_carrera = ?
                        WHERE id_persona = ?""" 
                 
                cursor.execute(query, estudiante.id_carrera, estudiante.id_persona)
                connection.commit()


                response = {"estado": "El estudiante se ha actualizado exitosamente."}
                connection.close()
                return JsonResponse(response, safe = True)
            
            except:
                response = {"estado": "fail"}
                return JsonResponse(estudiante, safe = True)
    
    @csrf_exempt
    def borrarEstudiante(request):
        response = ""
        conn = Conexion.get_string_conection()
        idP = json.loads(request.body)
        id_persona = idP["id"]
        cursor = conn.cursor() 

        cursor.execute("""DELETE FROM Estudiante
                        WHERE id_persona = ?""", id_persona)
        
        conn.commit()

       
        cursor.execute("""DELETE FROM Persona
                        WHERE id_persona = ?""", id_persona)
        
        conn.commit()


        return JsonResponse(response, safe=False)
        





class MaestroApi:
    @csrf_exempt
    def getListaMaestros(request):
        response = ""
        estado_conexion = False 
        conn = Conexion.get_string_conection()
                
        cursor = conn.cursor() 
        cursor.execute("SELECT id_estudiante, p.Nombre, Apellido, car.Nombre, estado, Fecha_nacimiento,\
                        Cedula, CorreoPersonal, CorreoInstitucional, Telefono \
                        FROM Estudiante est\
                            INNER JOIN Persona p\
                                ON est.id_persona = p.id_persona\
                            INNER JOIN Tipo_Estado estado\
                                ON p.id_estado = estado.id_estado\
                            INNER JOIN Carrera car\
                                ON est.id_carrera = car.id_carrera \
                            FOR JSON AUTO")
       
        rows = cursor.fetchall()
        #print('\n\n\nRE S PONSEEE   ', rows)

        if len(rows)>0:
            response = json.loads(''.join([row[0] for row in rows]))


        else:
            response = {"message": "No hay datos almacenados"} 

        return JsonResponse(response, safe=False)

        
    

