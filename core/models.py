from django.db import models

class Publication(models.Model):
    titre = models.CharField(max_length=255)
    image = models.ImageField(upload_to='publications/')  # Les images seront stockées dans media/publications/
    date_publication = models.DateField()
    description = models.TextField(blank=True, null=True)  # Optionnel, pour ajouter plus de détails

    def __str__(self):
        return self.titre

