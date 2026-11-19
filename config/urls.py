from django.urls import path

from estudiantes import views

urlpatterns = [
    
    path('estudiante', views.estudiante_lista, name='estudiante_lista'),
    path('estudiante/<int:pk>', views.estudiante_detalle, name='estudiante_detalle'),
]
