from django.urls import path
from habitaciones import views

urlpatterns = [
    path('', views.HabitacionListView.as_view(), name='indice'),
    path('habitaciones/', views.HabitacionListView.as_view(), name='habitacion_lista'),
    path('habitaciones/crear/', views.HabitacionCreateView.as_view(), name='habitacion_crear'),
    path('habitaciones/editar/<int:pk>/', views.HabitacionUpdateView.as_view(), name='habitacion_editar'),
    path('habitaciones/eliminar/<int:pk>/', views.HabitacionDeleteView.as_view(), name='habitacion_eliminar'),
    path('habitaciones/registrar-limpieza/<int:pk>/', views.HabitacionLimpiezaView.as_view(), name='habitacion_limpieza'),

    path('tipos-habitacion/', views.TipoHabitacionListView.as_view(), name= 'tipo_habitacion_lista'),
    path("subir-foto/", views.subirFoto, name="subir_foto"),
    path('tipos-habitacion/crear/', views.TipoHabitacionCreateView.as_view (), name='tipo_habitacion_crear'),
    path('tipos-habitacion/editar/<int:pk>/', views.TipoHabitacionUpdateView.as_view (), name='tipo_habitacion_editar'),
    path('tipos-habitacion/eliminar/<int:pk>/', views.TipoHabitacionDeleteView.as_view (), name='tipo_habitacion_eliminar'),

    path('servicios-habitacion/', views.ServicioHabitacionListView.as_view(), name='servicio_habitacion_lista'),
    path('servicios-habitacion/crear/', views.ServicioHabitacionCreateView.as_view(), name='servicio_habitacion_crear'),
    path('servicios-habitacion/editar/<int:pk>/', views.ServicioHabitacionUpdateView.as_view (), name='servicio_habitacion_editar'),
    path('servicios-habitacion/eliminar/<int:pk>/', views.ServicioHabitacionDeleteView.as_view (), name='servicio_habitacion_eliminar'),

    path('test/', views.indice, name='test'),
]