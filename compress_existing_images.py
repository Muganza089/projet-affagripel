import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affagripelderu.settings')
django.setup()

from core.models import Publication, Audience

def compress_all():
    print("Compressing Publication images...")
    publications = Publication.objects.all()
    count_pub = 0
    for pub in publications:
        if pub.image and getattr(pub.image, 'name', None) and not pub.image.name.lower().endswith('.webp'):
            print(f"Compressing: {pub.image.name}")
            try:
                pub.save()
                count_pub += 1
            except Exception as e:
                print(f"Failed to compress {pub.image.name}: {e}")

    print(f"Successfully compressed {count_pub} publication images.")

    print("\nCompressing Audience images...")
    audiences = Audience.objects.all()
    count_aud = 0
    for aud in audiences:
        if aud.photo_identite and getattr(aud.photo_identite, 'name', None) and not aud.photo_identite.name.lower().endswith('.webp'):
            print(f"Compressing: {aud.photo_identite.name}")
            try:
                aud.save()
                count_aud += 1
            except Exception as e:
                print(f"Failed to compress {aud.photo_identite.name}: {e}")

    print(f"Successfully compressed {count_aud} audience images.")

if __name__ == '__main__':
    compress_all()
