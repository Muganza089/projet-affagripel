from django.contrib import admin
from .models import Publication, Personne, Delocalisation, DelocalisationPlantation, Contact, Audience, Newsletter

#================ PUBLICATIONS =================
@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication')
    search_fields = ('titre',)


# ================= PERSONNE =================
@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'postnom', 'prenom', 'numero_identite', 'telephone')
    search_fields = ('nom', 'postnom', 'numero_identite', 'telephone')


# ================= DELOCALISATION =================
@admin.register(Delocalisation)
class DelocalisationAdmin(admin.ModelAdmin):
    change_form_template = "admin/delocalisation_change_form.html"
    list_display = (
        'personne',
        'type_propriete',
        'type_delocalisation',
        'ancienne_adresse',
        'nouvelle_adresse',
        'montant_compensation',
        'date_demande'
    )

    list_filter = ('type_delocalisation', 'type_propriete', 'date_demande')

    search_fields = (
        'personne__nom',
        'personne__postnom',
        'personne__numero_identite',
        'ancienne_adresse',
        'nouvelle_adresse'
    )

    autocomplete_fields = ['personne']

    readonly_fields = ('date_demande',)
    fieldsets = (
        ("Informations générales", {
            "fields": ("personne", "type_propriete", "type_delocalisation")
        }),

        ("Ancienne adresse", {
            "fields": ("ancienne_adresse", "ancienne_latitude", "ancienne_longitude")
        }),

        ("Nouvelle adresse", {
            "fields": ("nouvelle_adresse", "nouvelle_latitude", "nouvelle_longitude")
        }),

        ("Compensation", {
            "fields": ("montant_compensation",)
        }),

        ("Meta", {
            "fields": ("date_demande",)
        }),
    )


# ================= DELOCALISATION DES PLANTATIONS =================
@admin.register(DelocalisationPlantation)
class DelocalisationPlantationAdmin(admin.ModelAdmin):
    change_form_template = "admin/cpd_plantation_change_form.html"

    list_display = (
        'nom', 'postnom', 'prenom',
        'type_piece_identite',
        'nature_culture', 'type_structure_maison',
        'date_enregistrement'
    )

    list_filter = ('type_piece_identite', 'type_structure_maison', 'date_enregistrement')

    search_fields = (
        'nom', 'postnom', 'prenom',
        'numero_carte_electeur', 'numero_passeport',
        'numero_permis_conduire', 'numero_attestation_naissance',
        'nature_culture'
    )

    readonly_fields = ('date_enregistrement',)

    fieldsets = (
        ("Identité (obligatoire)", {
            "fields": ("nom", "postnom", "prenom", "photo")
        }),
        ("Pièce d'identité (obligatoire)", {
            "description": "Choisissez le type de pièce, puis renseignez le numéro correspondant.",
            "fields": (
                "type_piece_identite",
                "numero_carte_electeur",
                "numero_passeport",
                "numero_permis_conduire",
                "numero_attestation_naissance",
            )
        }),
        ("Plantation (facultatif)", {
            "fields": ("superficie", "nature_culture"),
            "classes": ("collapse",),
        }),
        ("Structure maison (facultatif)", {
            "fields": ("superficie_maison", "type_structure_maison"),
            "classes": ("collapse",),
        }),
        ("Méta", {
            "fields": ("date_enregistrement",)
        }),
    )


# ================= CONTACT =================
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('nom_complet', 'email', 'message')
    readonly_fields = ('nom_complet', 'email', 'message', 'date_envoi')
    list_editable = ('lu',)

    def has_add_permission(self, request):
        return False


# ================= AUDIENCE =================
@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'poste', 'statut', 'date_demande')
    list_filter = ('statut', 'date_demande')
    search_fields = ('nom_complet', 'poste')
    readonly_fields = ('nom_complet', 'poste', 'photo_identite', 'lettre_demande', 'date_demande')
    list_editable = ('statut',)

    def has_add_permission(self, request):
        return False

# ================= NEWSLETTER =================
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_inscription', 'actif')
    list_filter = ('actif', 'date_inscription')
    search_fields = ('email',)
    list_editable = ('actif',)
    readonly_fields = ('date_inscription',)
