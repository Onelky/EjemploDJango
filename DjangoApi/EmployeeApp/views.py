from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # Esto es para acceder al API
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import  Cliente1, EstudianteCreate, EstudianteReturn

from types import SimpleNamespace as Namespace 
import pyodbc
import json

from .conexion import Conexion


class EstudianteApi:
    @csrf_exempt
    def getListaEstudiantes(request):

        response = ""
        estado_conexion = False 
        conn = Conexion.get_string_conection()
                
        cursor = conn.cursor() 
        cursor.execute("SELECT id_estudiante, Persona.id_persona, Persona.Nombre, Apellido, est.id_carrera, Persona.id_estado, Fecha_nacimiento,\
                        Cedula, CorreoPersonal, CorreoInstitucional, Telefono \
                        FROM Estudiante est\
                            INNER JOIN Persona \
                                ON est.id_persona = Persona.id_persona\
                            INNER JOIN Tipo_Estado estado\
                                ON Persona.id_estado = estado.id_estado\
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

                connection = Conexion.get_string_conection()

                print('\n\n\n  DATAA ', estudiante)
               
                cursor = connection.cursor()
                query = """INSERT INTO Persona(
                        id_estado,
                        Nombre,
                        Apellido,
                        Cedula,
                        CorreoPersonal,
                        Telefono,
                        Fecha_nacimiento
                        ) VALUES (?,?,?,?,?,?,?)"""

                # Primero se crea la persona
                            
                cursor.execute(query, [estudiante.id_estado, estudiante.Nombre, estudiante.Apellido, estudiante.Cedula, estudiante.CorreoPersonal, estudiante.Telefono, estudiante.Fecha_nacimiento])
                connection.commit()

                
                # Se crea el estudiante 

                query = """INSERT INTO Estudiante(id_carrera, id_persona)
                SELECT ?, MAX(id_persona)
                FROM Persona"""

                cursor.execute(query, estudiante.id_carrera)
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
        try: 
            
 
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
            response = {"estado": "Exito"}

        except: 
            response = {"estado": "fail"}
        

        return JsonResponse(response, safe=True)
        

#class MaestroApi:
    #@csrf_exempt
    #def getListaMaestros(request):
       