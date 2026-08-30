import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape

logger = logging.getLogger("altis")


def _plain_body(devis):
    return (
        "Nouvelle demande de devis — ALTIS SPHERE GROUP\n"
        f"{'=' * 50}\n\n"
        "CLIENT\n"
        f"  Nom        : {devis.nom}\n"
        f"  Email      : {devis.email}\n"
        f"  Téléphone  : {devis.telephone}\n"
        f"  Entreprise : {devis.entreprise or '—'}\n\n"
        "DEMANDE\n"
        f"  Service    : {devis.service}\n"
        f"  Budget     : {devis.budget or '—'}\n"
        f"  Délai      : {devis.delai or '—'}\n\n"
        "DESCRIPTION\n"
        f"{devis.description}\n\n"
        f"{'=' * 50}\n"
        f"Reçu le      : {devis.created_at:%d/%m/%Y à %H:%M}\n"
        f"Référence    : #{devis.id}\n"
        f"Origine      : {devis.source_origin or '—'}\n"
        f"IP           : {devis.ip_address or '—'}\n"
    )


def _html_body(devis):
    rows = [
        ("Nom", devis.nom),
        ("Email", devis.email),
        ("Téléphone", devis.telephone),
        ("Entreprise", devis.entreprise or "—"),
        ("Service", devis.service),
        ("Budget", devis.budget or "—"),
        ("Délai", devis.delai or "—"),
    ]
    trs = "".join(
        f'<tr><td style="padding:6px 12px;background:#f5f5f5;'
        f'font-weight:600;width:130px">{escape(label)}</td>'
        f'<td style="padding:6px 12px">{escape(str(value))}</td></tr>'
        for label, value in rows
    )
    return f"""<!DOCTYPE html>
<html lang="fr"><body style="font-family:system-ui,sans-serif;color:#222">
  <h2 style="color:#0b5">Nouvelle demande de devis</h2>
  <p style="color:#666;font-size:13px">
    Référence #{devis.id} — reçue le {devis.created_at:%d/%m/%Y à %H:%M}
  </p>
  <table style="border-collapse:collapse;border:1px solid #ddd">{trs}</table>
  <h3>Description</h3>
  <p style="white-space:pre-wrap;background:#fafafa;padding:12px;
            border-left:3px solid #0b5">{escape(devis.description)}</p>
  <hr style="border:none;border-top:1px solid #eee;margin:24px 0">
  <p style="color:#999;font-size:12px">
    Origine : {escape(devis.source_origin or '—')} — IP : {devis.ip_address or '—'}
  </p>
</body></html>"""


def send_devis_notification(devis):
    """
    Notifie l'équipe d'une nouvelle demande de devis.
    Retourne le nombre de messages envoyés (0 si désactivé ou en échec).
    Ne lève jamais : l'échec d'un mail ne doit pas perdre un devis enregistré.
    """
    recipients = getattr(settings, "ALTIS_NOTIFY_EMAILS", [])
    if not recipients:
        logger.warning("ALTIS_NOTIFY_EMAILS vide — notification ignorée")
        return 0

    try:
        msg = EmailMultiAlternatives(
            subject=f"[ALTIS] Devis #{devis.id} — {devis.service} — {devis.nom}",
            body=_plain_body(devis),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
            reply_to=[devis.email],        # « Répondre » écrit au client
            headers={"X-Altis-Devis-Id": str(devis.id)},
        )
        msg.attach_alternative(_html_body(devis), "text/html")
        sent = msg.send(fail_silently=False)
        logger.info("Notification devis #%s envoyée à %s", devis.id, recipients)
        return sent
    except Exception:
        logger.exception("Échec notification devis #%s", devis.id)
        return 0


# ═══════════════════════════════════════════════════════════════
# CONTACT — page /contact, message libre
# ═══════════════════════════════════════════════════════════════

def _plain_body_contact(contact):
    return (
        "Nouveau message de contact — ALTIS SPHERE GROUP\n"
        f"{'=' * 50}\n\n"
        "EXPÉDITEUR\n"
        f"  Nom        : {contact.nom}\n"
        f"  Email      : {contact.email}\n"
        f"  Téléphone  : {contact.telephone or '—'}\n"
        f"  Entreprise : {contact.entreprise or '—'}\n\n"
        "SUJET\n"
        f"  {contact.sujet}\n\n"
        "MESSAGE\n"
        f"{contact.message}\n\n"
        f"{'=' * 50}\n"
        f"Reçu le      : {contact.created_at:%d/%m/%Y à %H:%M}\n"
        f"Référence    : CONTACT-{contact.id:05d}\n"
        f"Origine      : {contact.source_origin or '—'}\n"
        f"IP           : {contact.ip_address or '—'}\n"
    )


def _html_body_contact(contact):
    rows = [
        ("Nom", contact.nom),
        ("Email", contact.email),
        ("Téléphone", contact.telephone or "—"),
        ("Entreprise", contact.entreprise or "—"),
        ("Sujet", contact.sujet),
    ]
    trs = "".join(
        f'<tr><td style="padding:6px 12px;background:#f5f5f5;'
        f'font-weight:600;width:130px">{escape(label)}</td>'
        f'<td style="padding:6px 12px">{escape(str(value))}</td></tr>'
        for label, value in rows
    )
    return f"""<!DOCTYPE html>
<html lang="fr"><body style="font-family:system-ui,sans-serif;color:#222">
  <h2 style="color:#0b5">Nouveau message de contact</h2>
  <p style="color:#666;font-size:13px">
    Référence CONTACT-{contact.id:05d} — reçue le {contact.created_at:%d/%m/%Y à %H:%M}
  </p>
  <table style="border-collapse:collapse;border:1px solid #ddd">{trs}</table>
  <h3>Message</h3>
  <p style="white-space:pre-wrap;background:#fafafa;padding:12px;
            border-left:3px solid #0b5">{escape(contact.message)}</p>
  <hr style="border:none;border-top:1px solid #eee;margin:24px 0">
  <p style="color:#999;font-size:12px">
    Origine : {escape(contact.source_origin or '—')} — IP : {contact.ip_address or '—'}
  </p>
</body></html>"""


def send_contact_notification(contact):
    """
    Notifie l'équipe d'un nouveau message de contact.
    Retourne le nombre de messages envoyés (0 si désactivé ou en échec).
    Ne lève jamais : l'échec d'un mail ne doit pas perdre un message enregistré.
    """
    recipients = getattr(settings, "ALTIS_NOTIFY_EMAILS", [])
    if not recipients:
        logger.warning("ALTIS_NOTIFY_EMAILS vide — notification contact ignorée")
        return 0

    try:
        msg = EmailMultiAlternatives(
            subject=f"[ALTIS] Contact #{contact.id} — {contact.sujet} — {contact.nom}",
            body=_plain_body_contact(contact),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
            reply_to=[contact.email],       # « Répondre » écrit à l'expéditeur
            headers={"X-Altis-Contact-Id": str(contact.id)},
        )
        msg.attach_alternative(_html_body_contact(contact), "text/html")
        sent = msg.send(fail_silently=False)
        logger.info("Notification contact #%s envoyée à %s", contact.id, recipients)
        return sent
    except Exception:
        logger.exception("Échec notification contact #%s", contact.id)
        return 0
