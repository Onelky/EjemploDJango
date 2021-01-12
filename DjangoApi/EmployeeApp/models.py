#import serializers as serializers
from django.db import models
from rest_framework import serializers
from django.utils.timezone import datetime
from marshmallow_dataclass import dataclass
from typing import List
#from DjangoApi.EmployeeApp.models import Employees, Department

from pydantic import BaseModel



# Create your models here.
# Aqui se agregan los modelos o clases del programa

#class DepartmentSerializer(serializers.ModelSerializer):

class Department(models.Model):
    DepartmentId = models.AutoField(primary_key = True)
    DepartmentName = models.CharField(max_length=20)


class Cliente1(BaseModel):

    nombre: str
    apellido: str   
    id: int = None  

    #id_clientes = models.AutoField(primary_key = True)
    #Nom_cli = models.CharField(max_length=50)
    #Ape_cli = models.CharField(max_length=50)

class Persona:
    id_persona: int = None  
    estado: str # hay que buscarlo en la BD 
    Nombre: str 
    Apellido: str 
    Fecha_nacimiento: str
    Cedula: str
    CorreoPersonal: str 
    CorreoInstitucional: str = None  
    Telefono: str
    Clave: str = None 

class Area(BaseModel):
    id_area: int = None
    NombreArea: str

class Materia(BaseModel):
    id_materia: int = None 
    id_area: int  #FK
    NombreMateria: str
    Codigo: str

class Trimestre(BaseModel):
    id_trimestre: int = None
    fecha_inicio: datetime
    fecha_final: datetime
    
class Carrera(BaseModel):
    id_carrera: int = None
    id_area: int #KF
    id_coordinador: int #FK
    Nombre: str
    Duracion: int 


class Calificacion(BaseModel):
    id_calif: int = None
    id_materia: int #FK
    id_estudiante: int #FK
    Calificacion: datetime
    id_trimestre: int #FK


class Estudiante(BaseModel):
    id_estudiante: int = None
    id_persona: int #FK
    id_carrera: int #FK  
    calificaciones: List[Calificacion] = []  
    
class Maestro(BaseModel):
    id_maestro: int
    id_contrato: str #FK
    id_persona: int #FK
    Salario: float


    
