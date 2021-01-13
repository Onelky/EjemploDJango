from django.conf.urls import url
#from views import departmentApi
from .views import EstudianteApi
from .viewCarrera import CarreraApi

urlpatterns = [

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

    # CARRERA

    url(r'^carreras/$', CarreraApi.getListaCarreras),
    url(r'^carreras/([0-9]+)$', CarreraApi.getListaCarreras),


]