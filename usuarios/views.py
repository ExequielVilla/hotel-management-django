from django.shortcuts import render, redirect, get_object_or_404
from .models import Huesped
from .forms import HuespedForm
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from PIL import Image



class HuespedListView(ListView):
    model = Huesped
    template_name = 'huesped_lista.html'
    context_object_name = 'huespedes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['huespedes'] = Huesped.objects.filter(activo=True)
        return context

class HuespedCreateView(CreateView):
    model = Huesped
    form_class = HuespedForm  # el nombre de la variable es "form"
    template_name = 'huesped_form_modal.html'
    success_url = reverse_lazy('huesped_lista')  # Redirige a la lista de huespedes después de crear

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}) # Devuelve errores en formato JSON si el formulario no es válido

class HuespedUpdateView(UpdateView):
    model = Huesped
    form_class = HuespedForm
    template_name = 'huesped_form_modal.html'
    success_url = reverse_lazy('huesped_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save() # Guarda/actualiza la habitación
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class HuespedDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        huesped = get_object_or_404(Huesped, pk=pk)
        huesped.activo = False
        huesped.save()
        return redirect("huesped_lista")