from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from altis.emails import send_devis_notification
from altis.models import DevisRequest


class Command(BaseCommand):
    help = "Envoie une notification de devis de test (sans écrire en base)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--id", type=int,
            help="ID d'un devis existant. Sinon, objet factice non sauvegardé.",
        )

    def handle(self, *args, **options):
        self.stdout.write("─" * 55)
        self.stdout.write(f"Backend       : {settings.EMAIL_BACKEND}")
        self.stdout.write(f"Hôte SMTP     : {getattr(settings, 'EMAIL_HOST', '—')}")
        self.stdout.write(f"Port          : {getattr(settings, 'EMAIL_PORT', '—')}")
        self.stdout.write(f"Compte        : {getattr(settings, 'EMAIL_HOST_USER', '—')}")
        self.stdout.write(f"From          : {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"Destinataires : {settings.ALTIS_NOTIFY_EMAILS}")
        self.stdout.write("─" * 55)

        if options["id"]:
            devis = DevisRequest.objects.get(pk=options["id"])
        else:
            devis = DevisRequest(
                id=0,
                nom="Client de test",
                email="client-test@example.com",
                telephone="+243 99 365 33 32",
                entreprise="ACME SARL",
                service="Cybersécurité",
                description="Audit de sécurité du réseau interne — test d'envoi.",
                budget="3 000 - 6 000 $",
                delai="Sous 3 semaines",
                source_origin="https://altisphere-group.com",
                ip_address="127.0.0.1",
            )
            devis.created_at = timezone.now()

        sent = send_devis_notification(devis)
        if sent:
            self.stdout.write(self.style.SUCCESS(f"✅ {sent} message(s) accepté(s) par le serveur"))
        else:
            self.stdout.write(self.style.ERROR("❌ Aucun message envoyé — voir les logs ci-dessus"))