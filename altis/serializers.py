from rest_framework import serializers

from .models import ContactMessage, DevisRequest, ServiceChoices


class DevisRequestSerializer(serializers.ModelSerializer):
    # Honeypot : invisible pour l'humain, souvent rempli par les bots
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True, default=""
    )

    service = serializers.ChoiceField(
        choices=ServiceChoices.choices,
        error_messages={"invalid_choice": "Service non reconnu."},
    )

    class Meta:
        model = DevisRequest
        fields = [
            "id",
            "nom", "email", "telephone", "entreprise",
            "service", "description", "budget", "delai",
            "created_at", "website",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "nom": {"error_messages": {"blank": "Nom requis."}},
            "email": {"error_messages": {"invalid": "Email invalide."}},
            "telephone": {"error_messages": {"blank": "Téléphone requis."}},
            "entreprise": {"required": False, "allow_blank": True},
            "budget": {"required": False, "allow_blank": True},
            "delai": {"required": False, "allow_blank": True},
        }

    # --- Honeypot ---
    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Requête rejetée.")
        return value

    # --- Miroir des règles zod ---
    def validate_nom(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Nom requis.")
        return value

    def validate_email(self, value):
        return value.strip().lower()

    def validate_telephone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Téléphone requis.")
        return value

    def validate_description(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Description requise.")
        if len(value) > 2000:
            raise serializers.ValidationError("Description trop longue (2000 max).")
        return value

    def validate(self, attrs):
        # Normalisation des optionnels : None -> ""
        for field in ("entreprise", "budget", "delai"):
            if attrs.get(field) is None:
                attrs[field] = ""
            else:
                attrs[field] = attrs[field].strip()
        return attrs

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Message libre : `sujet` accepte n'importe quel texte,
    `telephone` est optionnel — contrairement au devis.
    """

    # Honeypot : invisible pour l'humain, souvent rempli par les bots
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True, default=""
    )

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "nom", "email", "telephone", "entreprise",
            "sujet", "message",
            "created_at", "website",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "nom": {"error_messages": {"blank": "Nom requis."}},
            "email": {"error_messages": {"invalid": "Email invalide."}},
            "telephone": {"required": False, "allow_blank": True},
            "entreprise": {"required": False, "allow_blank": True},
            "sujet": {"error_messages": {"blank": "Sujet requis."}},
        }

    # --- Honeypot ---
    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Requête rejetée.")
        return value

    # --- Miroir des règles zod ---
    def validate_nom(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Nom requis.")
        return value

    def validate_email(self, value):
        return value.strip().lower()

    def validate_sujet(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Sujet requis.")
        if len(value) > 200:
            raise serializers.ValidationError("Sujet trop long (200 max).")
        return value

    def validate_message(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Message requis.")
        if len(value) < 10:
            raise serializers.ValidationError(
                "Le message doit contenir au moins 10 caractères."
            )
        if len(value) > 2000:
            raise serializers.ValidationError("Message trop long (2000 max).")
        return value

    def validate(self, attrs):
        # Normalisation des optionnels : None -> ""
        for field in ("telephone", "entreprise"):
            if attrs.get(field) is None:
                attrs[field] = ""
            else:
                attrs[field] = attrs[field].strip()
        return attrs

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)
