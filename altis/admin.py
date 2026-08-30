from django.contrib import admin

from .models import ContactMessage, DevisRequest

TRACABILITE = ("source_origin", "ip_address", "user_agent", "created_at", "updated_at")


@admin.register(DevisRequest)
class DevisRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "nom", "entreprise", "service", "email", "statut")
    list_filter = ("statut", "service", "created_at")
    list_editable = ("statut",)
    search_fields = ("nom", "email", "telephone", "entreprise", "description")
    date_hierarchy = "created_at"
    list_per_page = 50

    readonly_fields = (
        "nom", "email", "telephone", "entreprise",
        "service", "description", "budget", "delai",
    ) + TRACABILITE

    fieldsets = (
        ("Client", {"fields": ("nom", "email", "telephone", "entreprise")}),
        ("Demande", {"fields": ("service", "description", "budget", "delai")}),
        ("Suivi", {"fields": ("statut", "notes_internes")}),
        ("Traçabilité", {"classes": ("collapse",), "fields": TRACABILITE}),
    )

    def has_add_permission(self, request):
        return False        # les devis ne se créent que par l'API


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "nom", "sujet", "email", "statut")
    list_filter = ("statut", "created_at")
    list_editable = ("statut",)
    search_fields = ("nom", "email", "telephone", "entreprise", "sujet", "message")
    date_hierarchy = "created_at"
    list_per_page = 50

    readonly_fields = (
        "nom", "email", "telephone", "entreprise", "sujet", "message",
    ) + TRACABILITE

    fieldsets = (
        ("Expéditeur", {"fields": ("nom", "email", "telephone", "entreprise")}),
        ("Message", {"fields": ("sujet", "message")}),
        ("Suivi", {"fields": ("statut", "notes_internes")}),
        ("Traçabilité", {"classes": ("collapse",), "fields": TRACABILITE}),
    )

    def has_add_permission(self, request):
        return False        # les messages ne se créent que par l'API
