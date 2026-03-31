import os

def update_models():
    filepath = 'core/models.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add imports
    imports = """import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.core.validators import RegexValidator"""
    
    content = content.replace("from django.db import models\nfrom django.core.validators import RegexValidator", imports)
    
    # Handle \r\n if needed
    content = content.replace("from django.db import models\r\nfrom django.core.validators import RegexValidator", imports)
    
    # 2. Update Publication str/save
    target_pub = """    def __str__(self):
        return self.titre"""
        
    replacement_pub = """    def __str__(self):
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
            
        super().save(*args, **kwargs)"""
        
    content = content.replace(target_pub, replacement_pub)
    content = content.replace(target_pub.replace('\n', '\r\n'), replacement_pub)
    
    target_aud = """    def __str__(self):
        return f"{self.nom_complet} — {self.get_statut_display()} ({self.date_demande.strftime('%d/%m/%Y')})\""""
        
    replacement_aud = """    def __str__(self):
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
            
        super().save(*args, **kwargs)"""
        
    content = content.replace(target_aud, replacement_aud)
    content = content.replace(target_aud.replace('\n', '\r\n'), replacement_aud)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("models.py updated successfully.")

if __name__ == '__main__':
    update_models()
