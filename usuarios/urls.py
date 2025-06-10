from django.urls import path, include
from usuarios import views

urlpatterns = [
    path('huespedes/', views.HuespedListView.as_view(), name='huesped_lista'),
    path('huespedes/crear/', views.HuespedCreateView.as_view(), name='huesped_crear'),
    path('huespedes/editar/<int:pk>/', views.HuespedUpdateView.as_view(), name='huesped_editar'),
    path('huespedes/eliminar/<int:pk>/', views.HuespedDeleteView.as_view(), name='huesped_eliminar'),
    path('huesped/json/<int:pk>/', views.ApiHuespedView.as_view(), name='api_huesped'),

    path('huespedes/exportar/excel/', views.HuespedExportExcelView.as_view(), name='huesped_exportar_excel'),
    path('huespedes/exportar/pdf/', views.HuespedExportPdfView.as_view(), name='huesped_exportar_pdf'),
]
