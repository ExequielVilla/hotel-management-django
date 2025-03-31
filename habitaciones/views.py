from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitacion, TipoHabitacion, ServicioHab, FotoHabitacion
from .forms import HabitacionForm, TipoHabForm, ServicioHabForm, FotoHabForm
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from PIL import Image
# from io import BytesIO
import io
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

# Para Login:
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login


class Test(ListView):
    model = FotoHabitacion
    template_name = 'test.html'
    context_object_name = 'fotos'

@login_required
def indice(request):
    return render(request, 'habitacion_lista.html')

############################################################
####################### HABITACIONES #######################
class HabitacionListView(ListView):
    model = Habitacion
    template_name = 'habitacion_lista.html'
    context_object_name = 'habitaciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['habitaciones'] = Habitacion.objects.filter(activo=True)
        return context


class HabitacionCreateView(CreateView):
    model = Habitacion
    form_class = HabitacionForm  # el nombre de la variable es "form"
    template_name = 'habitacion_form_modal.html'
    success_url = reverse_lazy('habitacion_lista')  # Redirige a la lista de habitaciones después de crear

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}) # Devuelve errores en formato JSON si el formulario no es válido

class HabitacionDetailView(DetailView):
    model = Habitacion
    template_name = ''

class HabitacionUpdateView(UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'habitacion_form_modal.html'
    success_url = reverse_lazy('habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save() # Guarda/actualiza la habitación
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class HabitacionDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        habitacion = get_object_or_404(Habitacion, pk=pk)
        habitacion.activo = False
        habitacion.save()
        return redirect("habitacion_lista")



############################################################
####################### TIPOS DE HABITACIONES #######################
class TipoHabitacionListView(ListView):
    model = TipoHabitacion
    template_name = 'tipo_habitacion_lista.html'
    context_object_name = 'tipos_habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_habitacion'] = TipoHabitacion.objects.filter(activo=True)
        return context

    def get_queryset(self):
        return TipoHabitacion.objects.all().prefetch_related('fotos')

def procesarImagen(imagen):
    try:
        img = Image.open(imagen)
        # img = ImageOps.exif_transpose(img)  # Corrige la rotación según los metadatos

        # Convertir a RGB si tiene canal alfa (PNG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Definir tamaño máximo sin distorsionar
        target_size = (600, 600)
        img.thumbnail(target_size, Image.LANCZOS)

        # Nuevo fondo negro
        new_img = Image.new("RGB", target_size, (0, 0, 0))  # Fondo negro
        x_offset = (target_size[0] - img.size[0]) // 2
        y_offset = (target_size[1] - img.size[1]) // 2
        new_img.paste(img, (x_offset, y_offset))

        # Guardar con compresión óptima
        output = io.BytesIO()
        new_img.save(output, format="JPEG", quality=90, optimize=True)
        output.seek(0)

        return ContentFile(output.read(), name=imagen.name)

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None

def subirFoto(request):
    fotos_subidas = request.FILES.getlist("fotos")
    if request.method != "POST" or not fotos_subidas:
        return JsonResponse({"error": "No se subieron las imágenes"}, status=400)
    try:
        fotos = []
        for foto in request.FILES.getlist("fotos"):
            # imagen_procesada = procesarImagen(foto)
            if(foto):
                nueva_foto = FotoHabitacion.objects.create(imagen=foto)
                fotos.append({
                    "id": nueva_foto.id,
                    "url": nueva_foto.imagen.url
                })
        if (fotos):
            return JsonResponse({"fotos": fotos})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

class TipoHabitacionCreateView(CreateView):
    model = TipoHabitacion
    form_class = TipoHabForm # nombre de la variable es "form"
    template_name = "tipo_habitacion_form_modal.html"
    success_url = reverse_lazy('tipo_habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotos_disponibles'] = FotoHabitacion.objects.all()  # Todas las fotos ya registradas
        return context

    def form_valid(self, form):
        tipo_habitacion = form.save() # Guardar el nuevo tipo de habitación
        fotos_seleccionadas = self.request.POST.get("fotos-seleccionadas", "") # Obtener las fotos seleccionadas desde el formulario
        if fotos_seleccionadas: # Convertir la cadena de IDs en una lista y asociar las fotos
            foto_ids = fotos_seleccionadas.split(",")
            fotos = FotoHabitacion.objects.filter(id__in=foto_ids)
            tipo_habitacion.fotos.set(fotos)
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class TipoHabitacionDetailView(DetailView):
    model = TipoHabitacion
    template_name = 'tipo_habitacion_detalle.html'
    context_object_name = 'tipoHab'

class TipoHabitacionUpdateView(UpdateView):
    model = TipoHabitacion
    form_class = TipoHabForm
    template_name = "tipo_habitacion_form_modal.html"
    success_url = reverse_lazy('tipo_habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_habitacion = self.get_object()
        context['fotos_disponibles'] = FotoHabitacion.objects.all()
        context['fotos_seleccionadas'] = tipo_habitacion.fotos.all().values_list('id',flat=True)
        return context

    def form_valid(self, form):
        tipo_habitacion = form.save() # Guarda/actualiza el tipo de habitación
        fotos_seleccionadas = self.request.POST.get("fotos-seleccionadas", "") # Obtener las fotos seleccionadas desde el formulario
        if fotos_seleccionadas: # Convertir la cadena de IDs en una lista y asociar las fotos
            foto_ids = fotos_seleccionadas.split(",")
            fotos = FotoHabitacion.objects.filter(id__in=foto_ids)
            tipo_habitacion.fotos.set(fotos)
        else:
            tipo_habitacion.fotos.clear()  # Si se deseleccionaron todas, limpiar
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class TipoHabitacionDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        tipo_habitacion = get_object_or_404(TipoHabitacion, pk=pk)
        tipo_habitacion.activo = False
        tipo_habitacion.save()
        return redirect("tipo_habitacion_lista")



##############################################################################################
####################### SERVICIOS DE HABITACIONES ##########################
class ServicioHabitacionListView(ListView):
    model = ServicioHab
    template_name = 'servicio_habitacion_lista.html'
    context_object_name = 'servicios_habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios_habitacion'] = ServicioHab.objects.filter(activo=True)
        return context


ICONOS_FONT_AWESOME = [
    "fa-baby-carriage", "fa-ban-smoking", "fa-bath", "fa-bed", "fa-bell-concierge", "fa-book-atlas",
    "fa-briefcase", "fa-bus", "fa-bus-simple", "fa-cable-car", "fa-car", "fa-caravan", "fa-cart-flatbed-suitcase",
    "fa-dumbbell", "fa-earth-americas", "fa-elevator", "fa-hotel", "fa-hot-tub-person", "fa-key", "fa-kitchen-set",
    "fa-map", "fa-map-location-dot", "fa-martini-glass", "fa-martini-glass-citrus", "fa-monument", "fa-mountain-city",
    "fa-mug-saucer", "fa-person-swimming", "fa-person-walking-luggage", "fa-plane", "fa-plane-circle-check",
    "fa-plane-circle-xmark", "fa-plane-departure", "fa-snowflake", "fa-spa", "fa-stairs", "fa-suitcase",
    "fa-suitcase-rolling", "fa-taxi", "fa-toilet", "fa-toilet-paper", "fa-train-tram", "fa-tree-city", "fa-umbrella-beach",
    "fa-utensils", "fa-van-shuttle", "fa-water-ladder", "fa-wheelchair", "fa-wheelchair-move", "fa-wifi", "fa-wine-glass"
]

class ServicioHabitacionCreateView(CreateView):
    model = ServicioHab
    form_class = ServicioHabForm
    template_name = 'servicio_habitacion_form_modal.html'
    success_url = reverse_lazy('servicio_habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iconos'] = ICONOS_FONT_AWESOME
        return context

    def form_valid(self, form):
        if not form.has_changed():  # Verifica si hay cambios
            return redirect(self.success_url)  # Redirige sin guardar
        return super().form_valid(form)  # Guarda si hay cambios

    def form_invalid(self, form):
        # print("entroooo1")
        # if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
        #     html_form = render_to_string(self.template_name, {"form": form}, request=self.request)
        #     return JsonResponse({"success": False, "form_html": html_form}, status=400)
        return super().form_invalid(form)

class ServicioHabitacionUpdateView(UpdateView):
    model = ServicioHab
    form_class = ServicioHabForm
    template_name = "servicio_habitacion_form_modal.html"
    success_url = reverse_lazy('servicio_habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iconos'] = ICONOS_FONT_AWESOME
        return context

    def form_valid(self, form):
        if not form.has_changed():  # Verifica si hay cambios
            return redirect(self.success_url)  # Redirige sin guardar
        return super().form_valid(form)  # Guarda si hay cambios

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            html_form = render_to_string(self.template_name, {"form": form}, request=self.request)
            return JsonResponse({"success": False, "form_html": html_form}, status=400)
        return super().form_invalid(form)

class ServicioHabitacionDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        servicio_habitacion = get_object_or_404(ServicioHab, pk=pk)
        servicio_habitacion.activo = False
        servicio_habitacion.save()
        return redirect("servicio_habitacion_lista")
