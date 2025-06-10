from django.urls import path, include
from reservas import views

urlpatterns = [
    path('reservas/', views.ReservaListView.as_view(), name='reserva_lista'),
    path('reservas/calendario-api/', views.ReservaCalendarioAPIView.as_view(), name='reservas_calendario'),
    path('reservas/crear/', views.ReservaCreateView.as_view(), name='reserva_crear'),
    path('reservas/editar/<int:pk>/', views.ReservaUpdateView.as_view(), name='reserva_editar'),
    path('reservas/tipo-habitacion-disponibilidad/', views.TipoHabitacionDisponibilidadView.as_view(), name='tipo_habitacion_disponibilidad'),
    path('reservas/resumen-reserva/', views.ResumenReservaView.as_view(), name='resumen_reserva'),
    path('reservas/registrar-pago/', views.RegistrarPagoView.as_view(), name='registrar_pago'),
    path('reservas/cancelar/<int:pk>/', views.ReservaCancelarView.as_view(), name='reserva_cancelar'),

    path('checkin/', views.CheckInListView.as_view(), name='checkin_lista'),
    path('checkin/registrar/<int:pk>/', views.CheckinRegistrarView.as_view(), name='checkin_registrar'),

    path('checkout/', views.CheckOutListView.as_view(), name='checkout_lista'),
    path('checkout/registrar/<int:pk>/', views.CheckOutRegistrarView.as_view(), name='checkout_registrar'),

]
