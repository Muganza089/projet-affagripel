# altis/views.py
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import (
    api_view, permission_classes, throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .emails import send_contact_notification, send_devis_notification
from .models import ServiceChoices
from .serializers import ContactMessageSerializer, DevisRequestSerializer
from .throttles import ContactSubmitThrottle, DevisSubmitThrottle

logger = logging.getLogger("altis")


def client_ip(request):
    """IP réelle du client, en tenant compte du reverse proxy Nginx."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def tracking_fields(request):
    """Métadonnées de traçabilité communes aux deux formulaires."""
    return {
        "source_origin": request.META.get("HTTP_ORIGIN", "")[:200],
        "ip_address": client_ip(request),
        "user_agent": request.META.get("HTTP_USER_AGENT", "")[:300],
    }


# ═══════════════════════════════════════════════════════════════
# DIAGNOSTIC
# ═══════════════════════════════════════════════════════════════

@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok", "service": "altis-api"})


@api_view(["GET"])
@permission_classes([AllowAny])
def services(request):
    """Source de vérité unique pour la liste des services du formulaire devis."""
    return Response({"services": [c.value for c in ServiceChoices]})


@api_view(["GET"])
@permission_classes([AllowAny])
def mail_config(request):
    """
    Diagnostic de la configuration email — DEBUG UNIQUEMENT.
    Retourne 404 en production : ces informations ne doivent jamais être publiques.
    """
    if not settings.DEBUG:
        return Response(status=status.HTTP_404_NOT_FOUND)

    backend = settings.EMAIL_BACKEND
    payload = {
        "email_mode": getattr(settings, "EMAIL_MODE", "?"),
        "backend": backend,
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipients": getattr(settings, "ALTIS_NOTIFY_EMAILS", []),
        "recipients_count": len(getattr(settings, "ALTIS_NOTIFY_EMAILS", [])),
    }

    if "smtp" in backend:
        payload["smtp"] = {
            "host": getattr(settings, "EMAIL_HOST", None),
            "port": getattr(settings, "EMAIL_PORT", None),
            "use_tls": getattr(settings, "EMAIL_USE_TLS", None),
            "use_ssl": getattr(settings, "EMAIL_USE_SSL", None),
            "user": getattr(settings, "EMAIL_HOST_USER", "") or None,
            # ⚠ jamais le mot de passe, même en DEBUG
            "password_set": bool(getattr(settings, "EMAIL_HOST_PASSWORD", "")),
            "timeout": getattr(settings, "EMAIL_TIMEOUT", None),
        }

    if "filebased" in backend:
        payload["file_path"] = str(getattr(settings, "EMAIL_FILE_PATH", ""))

    return Response(payload)


# ═══════════════════════════════════════════════════════════════
# SOUMISSIONS
# ═══════════════════════════════════════════════════════════════

def _handle_submission(request, serializer_class, notifier, label):
    """
    Logique commune : valider -> enregistrer -> notifier.

    L'enregistrement en base et l'envoi du mail sont découplés :
    un échec SMTP ne fait jamais perdre une demande.
    """
    serializer = serializer_class(data=request.data)
    if not serializer.is_valid():
        logger.info("%s ALTIS rejeté : %s", label, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    instance = serializer.save(**tracking_fields(request))
    logger.info("%s #%s enregistré — %s", label, instance.id, instance.nom)

    # Notification : ne lève jamais, retourne 0 en cas d'échec
    sent = notifier(instance)
    if not sent:
        logger.warning(
            "%s #%s enregistré mais notification NON envoyée", label, instance.id
        )

    payload = {"id": instance.id, "created_at": instance.created_at}
    if settings.DEBUG:
        payload["mail_sent"] = bool(sent)      # aide au test local uniquement

    return Response(payload, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([DevisSubmitThrottle])
def devis_submit(request):
    """
    POST /api/altis/devis/ — modal « Demander un devis ».
    `service` doit appartenir à ServiceChoices.

    201 -> {"id": .., "created_at": ..}          (+ "mail_sent" si DEBUG)
    400 -> {"champ": ["message"]}
    429 -> quota dépassé
    """
    return _handle_submission(
        request, DevisRequestSerializer, send_devis_notification, "Devis"
    )


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([ContactSubmitThrottle])
def contact_submit(request):
    """
    POST /api/altis/contact/ — page /contact, message libre.
    `sujet` est du texte libre, `telephone` est optionnel.

    201 -> {"id": .., "created_at": ..}          (+ "mail_sent" si DEBUG)
    400 -> {"champ": ["message"]}
    429 -> quota dépassé
    """
    return _handle_submission(
        request, ContactMessageSerializer, send_contact_notification, "Contact"
    )
