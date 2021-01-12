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


]