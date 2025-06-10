from django.contrib import admin
from .models import Pago, Reserva
# from .models import CustomUser, Huesped

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ("username", "email", "es_admin", "es_recepcionista", "es_huesped")

# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Pago)
admin.site.register(Reserva)