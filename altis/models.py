from django.db import models


class ServiceChoices(models.TextChoices):
    """⚠ Doit rester strictement synchronisé avec serviceOptions côté React."""
    INTERNET = "Internet & Connectivité", "Internet & Connectivité"
    SOLUTIONS_IT = "Solutions IT pour entreprises", "Solutions IT pour entreprises"
    CYBERSECURITE = "Cybersécurité", "Cybersécurité"
    DEVELOPPEMENT = "Développement Web & Applications", "Développement Web & Applications"
    SUPPORT = "Support & Maintenance", "Support & Maintenance"
    EQUIPEMENTS = "Équipements informatiques", "Équipements informatiques"
    DOMOTIQUE = "Domotique / Maison intelligente", "Domotique / Maison intelligente"


class DevisRequest(models.Model):
    """Demande de devis soumise depuis le frontend ALTIS SPHERE (GitHub Pages)."""

    STATUT_NOUVEAU = "nouveau"
    STATUT_EN_COURS = "en_cours"
    STATUT_TRAITE = "traite"
    STATUT_REJETE = "rejete"
    STATUT_CHOICES = [
        (STATUT_NOUVEAU, "Nouveau"),
        (STATUT_EN_COURS, "En cours"),
        (STATUT_TRAITE, "Traité"),
        (STATUT_REJETE, "Rejeté / spam"),
    ]

    # --- Informations client ---
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    telephone = models.CharField(max_length=30)
    entreprise = models.CharField(max_length=120, blank=True, default="")

    # --- Informations sur la demande ---
    service = models.CharField(max_length=64, choices=ServiceChoices.choices)
    description = models.TextField()
    budget = models.CharField(max_length=120, blank=True, default="")
    delai = models.CharField(max_length=120, blank=True, default="")

    # --- Suivi interne ---
    statut = models.CharField(
        max_length=16, choices=STATUT_CHOICES, default=STATUT_NOUVEAU, db_index=True
    )
    notes_internes = models.TextField(blank=True, default="")

    # --- Traçabilité (jamais exposée à l'API) ---
    source_origin = models.CharField(max_length=200, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "altis_devis_request"     # préfixe : base partagée avec AFFAGRIPEL
        ordering = ["-created_at"]
        verbose_name = "Demande de devis ALTIS"
        verbose_name_plural = "Demandes de devis ALTIS"
        indexes = [
            models.Index(fields=["email", "-created_at"], name="altis_email_date_idx"),
        ]

    def __str__(self):
        return f"[ALTIS] {self.nom} — {self.service} ({self.created_at:%Y-%m-%d})"


class ContactMessage(models.Model):
    """
    Message libre envoyé depuis la page /contact du frontend ALTIS SPHERE.

    Différences volontaires avec DevisRequest :
      - `sujet` est du TEXTE LIBRE (pas une liste fermée)
      - `telephone` est OPTIONNEL
      - pas de budget ni de délai
    Modèle distinct pour que les deux formulaires évoluent
    séparément sans se contraindre l'un l'autre.
    """

    STATUT_NOUVEAU = "nouveau"
    STATUT_EN_COURS = "en_cours"
    STATUT_TRAITE = "traite"
    STATUT_REJETE = "rejete"
    STATUT_CHOICES = [
        (STATUT_NOUVEAU, "Nouveau"),
        (STATUT_EN_COURS, "En cours"),
        (STATUT_TRAITE, "Traité"),
        (STATUT_REJETE, "Rejeté / spam"),
    ]

    # --- Expéditeur ---
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    telephone = models.CharField(max_length=30, blank=True, default="")
    entreprise = models.CharField(max_length=200, blank=True, default="")

    # --- Contenu ---
    sujet = models.CharField(max_length=200)
    message = models.TextField()

    # --- Suivi interne ---
    statut = models.CharField(
        max_length=16, choices=STATUT_CHOICES, default=STATUT_NOUVEAU, db_index=True
    )
    notes_internes = models.TextField(blank=True, default="")

    # --- Traçabilité (jamais exposée à l'API) ---
    source_origin = models.CharField(max_length=200, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "altis_contact_message"   # préfixe : base partagée avec AFFAGRIPEL
        ordering = ["-created_at"]
        verbose_name = "Message de contact ALTIS"
        verbose_name_plural = "Messages de contact ALTIS"
        indexes = [
            models.Index(fields=["email", "-created_at"], name="altis_contact_email_idx"),
        ]

    def __str__(self):
        return f"[CONTACT] {self.nom} — {self.sujet} ({self.created_at:%Y-%m-%d})"
