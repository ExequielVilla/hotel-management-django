from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def enviar_mail_confirmacion_reserva(reserva):
    sujeto = f"Confirmación de Reserva #{reserva.id}"
    context = {
        'reserva': reserva,
    }
    mensaje_html = render_to_string('emails/confirmacion_reserva.html', context)
    mensaje_plano = strip_tags(mensaje_html)

    send_mail(
        subject=sujeto,
        message=mensaje_plano,
        from_email=None,  # Usa DEFAULT_FROM_EMAIL
        recipient_list=[reserva.huesped.email],
        html_message=mensaje_html,
    )