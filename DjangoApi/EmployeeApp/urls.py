from django.conf.urls import url
#from views import departmentApi
from .views import  Cliente, EstudianteApi
# Este archivo se crea para ligar un determinado metodo con una url

# Luego se debe asociar este archivo al archivo urls principal
urlpatterns = [

    url(r'^cliente/$', Cliente.getClientes),
    url(r'^cliente/([0-9]+)$', Cliente.getClientes),
    url(r'^registrarcliente/$', Cliente.registrarCliente),
    url(r'^registrarcliente/([0-9]+)$', Cliente.registrarCliente),

    # ESTUDIANTE

    url(r'^estudiantes/$', EstudianteApi.getListaEstudiantes),
    url(r'^estudiantes/([0-9]+)$', EstudianteApi.getListaEstudiantes), 
    url(r'^estudiante/$', EstudianteApi.crearEstudiante),
    url(r'^estudiante/([0-9]+)$', EstudianteApi.crearEstudiante),
    url(r'^getestudiante/$', EstudianteApi.getEstudiante),
    url(r'^getestudiante/([0-9]+)$', EstudianteApi.getEstudiante), 
    url(r'^editarestudiante/$', EstudianteApi.editarEstudiante),
    url(r'^editarestudiante/([0-9]+)$', EstudianteApi.editarEstudiante), 

    url(r'^borrarestudiante/$', EstudianteApi.borrarEstudiante),
    url(r'^borrarestudiante/([0-9]+)$', EstudianteApi.borrarEstudiante),
]