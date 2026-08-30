# altis/throttles.py
from rest_framework.throttling import AnonRateThrottle


class DevisSubmitThrottle(AnonRateThrottle):
    """Quota dédié au formulaire de devis, indépendant de ceux d'AFFAGRIPEL."""
    scope = "altis_devis"


class ContactSubmitThrottle(AnonRateThrottle):
    """
    Quota dédié au formulaire de contact.
    Séparé du devis : un visiteur peut légitimement poser plusieurs
    questions sans être bloqué par le quota des demandes de devis.
    """
    scope = "altis_contact"
