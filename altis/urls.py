from django.urls import path

from .views import contact_submit, health, services, mail_config, devis_submit

app_name = "altis"

urlpatterns = [
    path("health/", health, name="health"),
    path("services/", services, name="services"),
    path("mail-config/", mail_config, name="mail-config"),   # 404 si DEBUG=False
    path("devis/", devis_submit, name="devis-submit"),
    path("contact/", contact_submit, name="contact-submit"),
]