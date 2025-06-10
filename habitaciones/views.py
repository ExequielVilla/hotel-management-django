from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitacion, TipoHabitacion, ServicioHab, FotoHabitacion, CamaTipoHabitacion, TipoCama
from .forms import HabitacionForm, TipoHabForm, ServicioHabForm, TipoCamaForm
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from PIL import Image
import io
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages

# Para Login:
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login

# Agregar el PermissionRequiredMixin
class Test(ListView):
    model = FotoHabitacion
    template_name = 'test.html'
    context_object_name = 'fotos'


def indice(request):
    return render(request, 'habitacion_lista.html')

############################################################
####################### HABITACIONES #######################
class HabitacionListView(LoginRequiredMixin, ListView):
    model = Habitacion
    template_name = 'habitacion_lista.html'
    context_object_name = 'habitaciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['habitaciones'] = Habitacion.objects.filter(activo=True)
        return context


class HabitacionCreateView(LoginRequiredMixin, CreateView):
    model = Habitacion
    form_class = HabitacionForm  # el nombre de la variable es "form"
    template_name = 'habitacion_form_modal.html'
    success_url = reverse_lazy('habitacion_lista')  # Redirige a la lista de habitaciones después de crear

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}) # Devuelve errores en formato JSON si el formulario no es válido

class HabitacionDetailView(LoginRequiredMixin, DetailView):
    model = Habitacion
    template_name = ''

class HabitacionUpdateView(LoginRequiredMixin, UpdateView):
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

class HabitacionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        habitacion = get_object_or_404(Habitacion, pk=pk)
        habitacion.activo = False
        habitacion.save()
        return redirect("habitacion_lista")

class HabitacionLimpiezaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        habitacion = get_object_or_404(Habitacion, pk=pk)
        if habitacion and habitacion.estado == "En limpieza":
            habitacion.estado = "Habilitada"
            habitacion.save()
            return JsonResponse({
                "success": True,
                "message": f"La habitación {habitacion.numero} ({habitacion.tipo_habitacion.nombre}) fue habilitada con éxito."
            })
        return JsonResponse({
            "success": False,
            "message": "La habitación no está en estado 'En limpieza'."
        })


############################################################
####################### TIPOS DE HABITACIONES #######################
class TipoHabitacionListView(LoginRequiredMixin, ListView):
    model = TipoHabitacion
    template_name = 'tipo_habitacion_lista.html'
    context_object_name = 'tipos_habitacion'

    def get_queryset(self):
        return TipoHabitacion.objects.all().prefetch_related('fotos', 'camatipohabitacion_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for tipo in context['tipos_habitacion']:
            camas = tipo.camatipohabitacion_set.all()
            tipo.camas_str = ", ".join([
                f"{cama.get_tipo_cama_display()} ({cama.cantidad})" for cama in camas
            ])

        return context


def procesarImagen(imagen):
    try:
        img = Image.open(imagen)
        # img = ImageOps.exif_transpose(img)  # Corrige la rotación según los metadatos

        # Convertir a RGB si tiene canal alfa (PNG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Define tamaño máximo sin distorsionar
        target_size = (600, 600)
        img.thumbnail(target_size, Image.LANCZOS)

        # Nuevo fondo negro
        new_img = Image.new("RGB", target_size, (0, 0, 0))  # Fondo negro
        x_offset = (target_size[0] - img.size[0]) // 2
        y_offset = (target_size[1] - img.size[1]) // 2
        new_img.paste(img, (x_offset, y_offset))

        # Guarda con compresión óptima
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

class TipoHabitacionCreateView(LoginRequiredMixin, CreateView):
    model = TipoHabitacion
    form_class = TipoHabForm # nombre de la variable es "form"
    template_name = "tipo_habitacion_form_modal.html"
    success_url = reverse_lazy('tipo_habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotos_disponibles'] = FotoHabitacion.objects.all()  # Todas las fotos ya registradas
        context['form_camas'] = kwargs.get('form_camas', TipoCamaForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form_camas = TipoCamaForm(request.POST)

        if not form.is_valid() or not form_camas.is_valid():
            return self.form_invalid(form, form_camas)
        return self.form_valid(form, form_camas)

    def form_valid(self, form, form_camas):
        tipo_hab = form.save()
        # Guardar camas con cantidad > 0
        for tipo, _ in TipoCama.choices:
            cantidad = form_camas.cleaned_data.get(tipo.lower())
            if cantidad and cantidad > 0:
                CamaTipoHabitacion.objects.create(
                    tipo_habitacion=tipo_hab,
                    tipo_cama=tipo,
                    cantidad=cantidad
                )
        # Guardar fotos
        fotos_seleccionadas = self.request.POST.get("fotos-seleccionadas", "")
        if fotos_seleccionadas:
            foto_ids = fotos_seleccionadas.split(",")
            fotos = FotoHabitacion.objects.filter(id__in=foto_ids)
            tipo_hab.fotos.set(fotos)
        return redirect(self.success_url)

    def form_invalid(self, form, form_camas):
        return JsonResponse({'success': False, 'errors': form.errors, 'errors_camas': form_camas.errors})

class TipoHabitacionUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoHabitacion
    form_class = TipoHabForm
    template_name = "tipo_habitacion_form_modal.html"
    success_url = reverse_lazy('tipo_habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_habitacion = self.get_object()
        context['fotos_disponibles'] = FotoHabitacion.objects.all()
        context['fotos_seleccionadas'] = tipo_habitacion.fotos.all().values_list('id',flat=True)
        # Formulario de camas con los valores actuales
        camas_existentes = CamaTipoHabitacion.objects.filter(tipo_habitacion=tipo_habitacion)
        data_inicial = {cama.tipo_cama.lower(): cama.cantidad for cama in camas_existentes}
        context['form_camas'] = kwargs.get('form_camas', TipoCamaForm(initial=data_inicial))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form_camas = TipoCamaForm(request.POST)

        if not form.is_valid() or not form_camas.is_valid():
            return self.form_invalid(form, form_camas)
        return self.form_valid(form, form_camas)

    def form_valid(self, form, form_camas):
        tipo_hab = form.save()
        CamaTipoHabitacion.objects.filter(tipo_habitacion=tipo_hab).delete() # Eliminar camas anteriores
        # Guardar nuevas camas si cantidad > 0
        for tipo, _ in TipoCama.choices:
            cantidad = form_camas.cleaned_data.get(tipo.lower())
            if cantidad and cantidad > 0:
                CamaTipoHabitacion.objects.create(
                    tipo_habitacion=tipo_hab,
                    tipo_cama=tipo,
                    cantidad=cantidad
                )
        # Fotos
        fotos_seleccionadas = self.request.POST.get("fotos-seleccionadas", "")
        if fotos_seleccionadas:
            foto_ids = fotos_seleccionadas.split(",")
            fotos = FotoHabitacion.objects.filter(id__in=foto_ids)
            tipo_hab.fotos.set(fotos)
        else:
            tipo_hab.fotos.clear()

        return redirect(self.success_url)

    def form_invalid(self, form, form_camas):
        return JsonResponse({
            'success': False,
            'errors': form.errors,
            'errors_camas': form_camas.errors
        })

class TipoHabitacionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        tipo_habitacion = get_object_or_404(TipoHabitacion, pk=pk)
        tipo_habitacion.activo = False
        tipo_habitacion.save()
        return redirect("tipo_habitacion_lista")



##############################################################################################
####################### SERVICIOS DE HABITACIONES ##########################
class ServicioHabitacionListView(LoginRequiredMixin, ListView):
    model = ServicioHab
    template_name = 'servicio_habitacion_lista.html'
    context_object_name = 'servicios_habitacion'
    paginate_by = 9

    def get_queryset(self):
        return ServicioHab.objects.filter(activo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

class ServicioHabitacionCreateView(LoginRequiredMixin, CreateView):
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
        # if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
        #     html_form = render_to_string(self.template_name, {"form": form}, request=self.request)
        #     return JsonResponse({"success": False, "form_html": html_form}, status=400)
        return super().form_invalid(form)

class ServicioHabitacionUpdateView(LoginRequiredMixin, UpdateView):
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
        if not form.cleaned_data.get('icono'):
            form.instance.icono = 'fa-check'
        return super().form_valid(form)  # Guarda si hay cambios

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            html_form = render_to_string(self.template_name, {"form": form}, request=self.request)
            return JsonResponse({"success": False, "form_html": html_form}, status=400)
        return super().form_invalid(form)

class ServicioHabitacionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        servicio_habitacion = get_object_or_404(ServicioHab, pk=pk)
        servicio_habitacion.activo = False
        servicio_habitacion.save()
        return redirect("servicio_habitacion_lista")
