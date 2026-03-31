import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.core.validators import RegexValidator
#====================PUBLICATIONS==========================
class Publication(models.Model):
    titre = models.CharField(max_length=255)
    image = models.ImageField(upload_to='publications/')  # Les images seront stockées dans media/publications/
    date_publication = models.DateField()
    description = models.TextField(blank=True, null=True)  # Optionnel, pour ajouter plus de détails

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.lower().endswith('.webp'):
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            output = BytesIO()
            img.save(output, format='WEBP', quality=75)
            output.seek(0)
            
            name_without_ext = os.path.splitext(self.image.name)[0]
            new_name = f"{name_without_ext}.webp"
            self.image.save(new_name, ContentFile(output.read()), save=False)
            
        super().save(*args, **kwargs)
from django.core.validators import RegexValidator

#==============PERSONNE=============================

class Personne(models.Model):

    numero_validator = RegexValidator(
        regex=r'^[0-9]{11}$',
        message="Le numéro d'identité doit contenir exactement 11 chiffres"
    )

    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    numero_identite = models.CharField(
        max_length=11,
        unique=True,
        validators=[numero_validator]
    )

    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nom} {self.postnom}"
    
#============DELOCALISATINON==============

class Delocalisation(models.Model):

    TYPE_PROPRIETE_CHOICES = [
        ('maison', "Maison"),
        ('concession', "Concession"),
        ('parcelle_vide', "Parcelle vide"),
        ('autre', "Autre"),
    ]

    TYPE_DELOCALISATION = [
        ('deplacement', "Délocalisation vers un autre lieu"),
        ('compensation', "Compensation financière"),
    ]

    personne = models.ForeignKey(
        'Personne',
        on_delete=models.CASCADE,
        related_name="proprietes"
    )

    type_propriete = models.CharField(max_length=20, choices=TYPE_PROPRIETE_CHOICES)
    type_delocalisation = models.CharField(max_length=20, choices=TYPE_DELOCALISATION)

    # ================= ANCIENNE ADRESSE =================
    ancienne_adresse = models.CharField(max_length=255, null=True, blank=True)
    ancienne_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ancienne_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # ================= NOUVELLE ADRESSE (OPTIONNEL) =================
    nouvelle_adresse = models.CharField(max_length=255, blank=True, null=True)
    nouvelle_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    nouvelle_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # ================= COMPENSATION =================
    montant_compensation = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.personne} - {self.type_delocalisation}"
    def clean(self):
        from django.core.exceptions import ValidationError

        if self.type_delocalisation == 'deplacement':
            if not self.nouvelle_adresse:
                raise ValidationError("La nouvelle adresse est requise pour un déplacement")

        if self.type_delocalisation == 'compensation':
            if not self.montant_compensation:
                raise ValidationError("Le montant de compensation est requis")


#====================CONTACT==========================
class Contact(models.Model):
    nom_complet = models.CharField(max_length=200, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom_complet} — {self.email} ({self.date_envoi.strftime('%d/%m/%Y')})"


#====================AUDIENCE==========================
class Audience(models.Model):

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('refusee', 'Refusée'),
    ]

    nom_complet = models.CharField(max_length=200, verbose_name="Nom complet")
    poste = models.CharField(max_length=200, verbose_name="Poste / Fonction / Profession")
    photo_identite = models.ImageField(
        upload_to='audiences/identites/',
        verbose_name="Photo de la carte d'identité"
    )
    lettre_demande = models.FileField(
        upload_to='audiences/lettres/',
        verbose_name="Lettre de demande"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name="Statut"
    )
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")

    class Meta:
        verbose_name = "Demande d'audience"
        verbose_name_plural = "Demandes d'audience"
        ordering = ['-date_demande']

    def __str__(self):
        return f"{self.nom_complet} — {self.get_statut_display()} ({self.date_demande.strftime('%d/%m/%Y')})"

    def save(self, *args, **kwargs):
        if self.photo_identite and not self.photo_identite.name.lower().endswith('.webp'):
            img = Image.open(self.photo_identite)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            output = BytesIO()
            img.save(output, format='WEBP', quality=80)
            output.seek(0)
            
            name_without_ext = os.path.splitext(self.photo_identite.name)[0]
            new_name = f"{name_without_ext}.webp"
            
            self.photo_identite.save(new_name, ContentFile(output.read()), save=False)
            
        super().save(*args, **kwargs)


#====================NEWSLETTER==========================
class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Adresse Email")
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    actif = models.BooleanField(default=True, verbose_name="Abonnement Actif")

    class Meta:
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.email} ({'Actif' if self.actif else 'Désabonné'})"
