from django.shortcuts import render, redirect, get_object_or_404
from habitaciones.models import TipoHabitacion, Habitacion
from .models import Reserva, Pago
from usuarios.models import Huesped
from .forms import ReservaForm, PagoForm
from usuarios.forms import HuespedForm
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import TipoHabitacionDisponibilidadSerializer
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
import json
from django.utils.formats import number_format
from django.db import transaction
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .utils import enviar_mail_confirmacion_reserva

# Para Login:
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login

#filtros
from django_filters.views import FilterView
from .filters import ReservaFilter

class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reserva_lista.html'
    context_object_name = 'reservas'
    paginate_by = 7
    filterset_class = ReservaFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.GET.get('o')
        if order:
            queryset = queryset.order_by(order)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pago_form'] = PagoForm()
        return context

class ReservaCalendarioAPIView(LoginRequiredMixin, View):
    def get(self, request):
        reservas = Reserva.objects.all()
        events = []
        for r in reservas:
            events.append({
                "title": f"{r.huesped.nombre} - {r.habitaciones_str()}",
                "start": r.fecha_check_in_esperada.isoformat(),
                "end": r.fecha_check_out_esperada.isoformat(),
                "allDay": True,
                "estado": r.estado
            })
        return JsonResponse(events, safe=False)


def habitacionesNoDisponibles(check_in, check_out):
    # Habitaciones que NO están reservadas en el rango de fechas (con reservas activas)
    habitaciones_no_disponibles = Habitacion.objects.filter(
        reserva__estado__in=['Pendiente', 'Confirmada', 'En curso'],  # Solo reservas activas
        reserva__fecha_check_in_esperada__lt=check_out,  # Reserva empieza antes del checkout solicitado
        reserva__fecha_check_out_esperada__gt=check_in   # Reserva termina después del checkin solicitado
    ).distinct()  # Evita duplicados si una habitación tiene múltiples reservas
    return habitaciones_no_disponibles

class TipoHabitacionDisponibilidadView(LoginRequiredMixin, View):
    def get(self, request):
        fecha_check_in = request.GET.get('check_in')
        fecha_check_out = request.GET.get('check_out')
        cantidad_huespedes = request.GET.get("cantidad_huespedes")
        # Validación 1: Campos requeridos
        if not fecha_check_in or not fecha_check_out:
            return render(request, "habitaciones_disponibles.html", {'error': 'Fechas son requeridas'}, status=200)
        check_in = parse_date(fecha_check_in)
        check_out = parse_date(fecha_check_out)
        # Validación 2: Intervalo válido entre check-in < check-out
        if not check_in or not check_out or check_in >= check_out:
            return render(request, "habitaciones_disponibles.html", {'error': 'Rango de fechas inválido (el check-in debe ser antes que check-out)'}, status=200)
        # Validación 3: Las fechas no pueden ser anteriores a hoy
        hoy = timezone.now().date()
        if check_in < hoy or check_out < hoy:
            return render(request, "habitaciones_disponibles.html", {'error': 'No se permiten reservas en fechas pasadas'}, status=200)

        reservas_ocupadas  = Reserva.objects.filter(
            fecha_check_in_esperada__lt=check_out,
            fecha_check_out_esperada__gt=check_in
            #activo=True
        )

        habitaciones_ocupadas_ids  = Habitacion.objects.filter(reserva__in=reservas_ocupadas).values_list('id', flat=True)

        tipos_hab_disponibles = TipoHabitacion.objects.filter(activo=True).annotate(
            cant_disponibles=Count(
                'habitacion',
                filter=~Q(habitacion__id__in=habitaciones_ocupadas_ids)
            )
        ).filter(cant_disponibles__gt=0)
        serializer = TipoHabitacionDisponibilidadSerializer(tipos_hab_disponibles, many=True)
        return render(request, "habitaciones_disponibles.html", {
            "data": serializer.data,
        })

class ResumenReservaView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            noches = data.get("noches")
            cantidad_huespedes = data.get("cantidad_huespedes")
            habitaciones_seleccionadas = data.get("habitaciones_seleccionadas", [])
            total = data.get("total")
            total_str = data.get("total_str")

            return render(request, "resumen_reserva.html", {
                "check_in": check_in,
                "check_out": check_out,
                "noches": noches,
                "cantidad_huespedes": cantidad_huespedes,
                "habitaciones_seleccionadas": habitaciones_seleccionadas,
                "total": total,
                "total_str": total_str,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
class ReservaCreateView( CreateView):
    model = Reserva
    form_class = ReservaForm  # el nombre de la variable es "form"
    template_name = 'reserva_form_modal.html'
    success_url = reverse_lazy('reserva_lista')  # Redirige a la lista de reservas después de crear

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['huesped_form'] = kwargs.get('huesped_form', HuespedForm())
        context['pago_form'] = kwargs.get('pago_form', PagoForm())
        context['huespedes'] = Huesped.objects.filter(activo=True)
        return context

    def form_valid(self, form):
        reserva = form.save(commit=False)
        try:
            #print(dict(self.request.POST))
            with transaction.atomic():  # Transacción atómica p/ seguridad
                print("000")
                # 1. Procesar habitaciones seleccionadas
                fecha_check_in = self.request.POST.get('fecha_check_in_esperada')
                print("a.0")
                fecha_check_out = self.request.POST.get('fecha_check_out_esperada')
                print("1.s")
                habitaciones_no_disponibles = habitacionesNoDisponibles(fecha_check_in, fecha_check_out)
                print("d.0")
                todas_habitaciones = []
                print("1.0")
                tipos_hab_seleccionadas = json.loads(self.request.POST.get('tipos_hab_seleccionadas', '[]'))
                print("1.1")
                for hab in tipos_hab_seleccionadas:
                    tipo_hab_id = hab['tipo_hab_id']
                    cantidad = hab['cantidad']
                    habitaciones = Habitacion.objects.filter(
                        tipo_habitacion__id=tipo_hab_id,
                        activo=True
                    ).exclude(
                        id__in=habitaciones_no_disponibles.values('id'),
                    ).order_by('?')[:cantidad] # order_by('?') -> aleatoriedad
                    todas_habitaciones.extend(habitaciones)
                print("111")
                # 2. Procesar huésped
                huesped_id = self.request.POST.get('huesped_seleccionado')
                if huesped_id:
                    huesped = Huesped.objects.get(pk=huesped_id)
                else:
                    huesped = Huesped.objects.create(
                        nombre=self.request.POST.get('nombre'),
                        apellido=self.request.POST.get('apellido'),
                        dni_pasaporte=self.request.POST.get('dni_pasaporte'),
                        email=self.request.POST.get('email'),
                        telefono=self.request.POST.get('telefono'),
                        preferencias=self.request.POST.get('preferencias', '')
                    )
                print("222")
                # 3. Procesar pago
                total_reserva = self.request.POST.get('total_reserva', 0)
                metodo_pago = self.request.POST.get('metodo_pago')
                pago = False
                if metodo_pago and metodo_pago in dict(Pago.METODOS):
                    pago = Pago.objects.create(
                        metodo_pago=metodo_pago,
                        monto_pagado=total_reserva
                    )
                print("333")
                # 4. Actualización y guardado de reserva
                reserva.huesped = huesped
                reserva.monto_total = total_reserva
                reserva.save()
                reserva.usuario=self.request.user if self.request.user.is_authenticated else None
                reserva.habitaciones.set(todas_habitaciones)
                print("444")
                if pago:
                    reserva.pago = pago
                    reserva.estado = 'Confirmada'
                reserva.save()
                print("qqqq")
                if reserva.estado == 'Confirmada':
                    enviar_mail_confirmacion_reserva(reserva)
                return JsonResponse({
                    'success': True,
                    'message': 'Reserva creada exitosamente',
                    'redirect_url': str(self.success_url)  # Asegúrate que es una cadena
                }, status=201)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}) # Devuelve errores en formato JSON si el formulario no es válido

class ReservaUpdateView(UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva_form_modal.html'
    success_url = reverse_lazy('reserva_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        data = self.request.POST
        return 0
        #return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


########################################
############### CHECKIN "###############
class CheckInListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'checkin_lista.html'
    context_object_name = 'checkins'

    def get_queryset(self):
        hoy = timezone.now().date()
        return Reserva.objects.filter(
            Q(estado='Confirmada'),
            fecha_check_in_esperada=hoy,
            fecha_check_in_efectuada__isnull=True
        )
class CheckinRegistrarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.fecha_check_in_efectuada is None:
            reserva.fecha_check_in_efectuada = timezone.now()
            reserva.estado = 'En curso'
            for habitacion in reserva.habitaciones.all():
                habitacion.estado = 'Ocupada'
                habitacion.save()
            reserva.save()
            return JsonResponse({'success': True, 'message': 'Check-in realizado correctamente'})
        else:
            return JsonResponse({'success': False, 'message': 'Este huésped ya hizo el check-in'})



########################################
############### CHECKOUT "###############
class CheckOutListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'checkout_lista.html'
    context_object_name = 'checkouts'

    def get_queryset(self):
        return Reserva.objects.filter(
            estado='En curso',
            fecha_check_out_efectuada__isnull=True
        )
class CheckOutRegistrarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.fecha_check_out_efectuada is None:
            reserva.fecha_check_out_efectuada = timezone.now().date()
            reserva.estado = 'Finalizada'
            for habitacion in reserva.habitaciones.all():
                habitacion.estado='En limpieza'
                habitacion.save()
            reserva.save()
        return redirect('reserva_lista')

class ReservaCancelarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.estado == 'Pendiente' or reserva.estado == 'Confirmada':
            reserva.estado = 'Cancelada'
            reserva.save()
        return redirect('reserva_lista')


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class RegistrarPagoView(View):
    def post(self, request):
        reserva_id = request.POST.get('reserva_id')
        reserva = get_object_or_404(Reserva, id=reserva_id)
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.monto_pagado = reserva.monto_total
            pago.save()

            reserva.pago = pago
            reserva.estado = 'Confirmada'
            reserva.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

