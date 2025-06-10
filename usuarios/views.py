from django.shortcuts import render, redirect, get_object_or_404
from .models import Huesped
from .forms import HuespedForm
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HuespedSerializer

# Para Login:
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login

# pdf
from weasyprint import HTML
import tempfile
#excel
from django.http import HttpResponse
from openpyxl import Workbook

class HuespedExportPdfView(View):
    def get(self, request, *args, **kwargs):
        # generar el HTML de los datos
        html_string = render_to_string('usuarios/huesped_pdf.html', {'huespedes': Huesped.objects.all()})
        html = HTML(string=html_string)

        with tempfile.TemporaryDirectory() as tmpdirname:
            pdf_file_path = f"{tmpdirname}/huespedes.pdf"
            html.write_pdf(pdf_file_path)

            with open(pdf_file_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="huespedes.pdf"'
                return response

class HuespedExportExcelView(View):
    def get(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        ws.title = "Huéspedes"

        headers = ["Nombre", "Apellido", "DNI/Pasaporte", "Email", "Teléfono", "Preferencias"]
        ws.append(headers)

        for huesped in Huesped.objects.filter(activo=True):
            ws.append([
                huesped.nombre,
                huesped.apellido,
                huesped.dni_pasaporte,
                huesped.email,
                huesped.telefono or "-",
                huesped.preferencias or "-"
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="huespedes.xlsx"'
        wb.save(response)
        return response

class HuespedListView(LoginRequiredMixin, ListView):
    model = Huesped
    template_name = 'usuarios/huesped_lista.html'
    context_object_name = 'huespedes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['huespedes'] = Huesped.objects.filter(activo=True)
        return context

class HuespedCreateView(LoginRequiredMixin, CreateView):
    model = Huesped
    form_class = HuespedForm  # el nombre de la variable es "form"
    template_name = 'usuarios/huesped_form_modal.html'
    success_url = reverse_lazy('huesped_lista')  # Redirige a la lista de huespedes después de crear

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}) # Devuelve errores en formato JSON si el formulario no es válido

class HuespedUpdateView(LoginRequiredMixin, UpdateView):
    model = Huesped
    form_class = HuespedForm
    template_name = 'usuarios/huesped_form_modal.html'
    success_url = reverse_lazy('huesped_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class HuespedDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        huesped = get_object_or_404(Huesped, pk=pk)
        huesped.activo = False
        huesped.save()
        return redirect("huesped_lista")

class ApiHuespedView(LoginRequiredMixin, APIView):
    def get(self, request, pk):
        try:
            huesped = Huesped.objects.get(pk=pk , activo=True)
            serializer = HuespedSerializer(huesped)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Huésped no encontrado o inactivo'}, status=status.HTTP_404_NOT_FOUND)