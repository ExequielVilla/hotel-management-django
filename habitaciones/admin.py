from django.contrib import admin
from .models import ServicioHab, FotoHabitacion, TipoHabitacion, Habitacion

# Configuración para ServicioHab
@admin.register(ServicioHab)
class ServicioHabAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono')  # Campos a mostrar en la lista
    search_fields = ('nombre',)  # Permitir búsqueda por nombre
    list_per_page = 20  # Número de elementos por página


# Configuración para FotoHabitacion
@admin.register(FotoHabitacion)
class FotoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'imagen_preview')  # Campos a mostrar en la lista
    readonly_fields = ('imagen_preview',)  # Mostrar vista previa de la imagen en el detalle

    def imagen_preview(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" style="max-height: 100px; max-width: 100px;" />'
        return "No hay imagen"

    imagen_preview.short_description = "Vista previa"
    imagen_preview.allow_tags = True  # Permite renderizar HTML


# Configuración para TipoHabitacion
@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'capacidad_maxima', 'servicios_list')  # Campos a mostrar en la lista
    search_fields = ('nombre',)  # Permitir búsqueda por nombre
    filter_horizontal = ('servicios', 'fotos')  # Mejorar la selección de servicios y fotos
    list_per_page = 20  # Número de elementos por página

    def servicios_list(self, obj):
        return ", ".join([servicio.nombre for servicio in obj.servicios.all()])
    
    servicios_list.short_description = "Servicios"  # Nombre de la columna en la lista


# Configuración para Habitacion
@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo_habitacion', 'estado')  # Campos a mostrar en la lista
    list_filter = ('estado', 'tipo_habitacion')  # Filtros laterales
    search_fields = ('numero', 'tipo_habitacion__nombre')  # Permitir búsqueda por número y tipo de habitación
    list_editable = ('estado',)  # Permitir editar el estado directamente desde la lista
    list_per_page = 20  # Número de elementos por página

    # Mostrar el nombre del tipo de habitación en lugar del ID
    def tipo_habitacion_nombre(self, obj):
        return obj.tipo_habitacion.nombre
    
    tipo_habitacion_nombre.short_description = "Tipo de Habitación"