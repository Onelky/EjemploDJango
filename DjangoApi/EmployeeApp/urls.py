from django.conf.urls import url
#from views import departmentApi
from EmployeeApp import views
# Este archivo se crea para ligar un determinado metodo con una url

# Luego se debe asociar este archivo al archivo urls principal
urlpatterns = [
    url(r'^department/$',views.departmentApi),
    url(r'^department/([0-9]+)$',views.departmentApi),

    url(r'^employee/$',views.EmployeeApi),
    url(r'^employee/([0-9]+)$',views.EmployeeApi),

    url(r'^student/$',views.StudentApi),
    url(r'^student/([0-9]+)$',views.StudentApi),
]