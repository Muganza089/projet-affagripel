from django.contrib import admin
from django.urls import path
from core.views import*
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
    path('',home, name='home'),
    path('agriculture',agriculture, name='agriculture'),
    path('peche_et_elevage',peche_et_elevage, name='peche_et_elevage'),
    path('devRural',devRural, name='devRural'),
    path('apropos',apropos, name='apropos'),
    path('demandeAudience',demandeAudience, name='demandeAudience'),
    path('aff_fonciere',aff_fonciere, name='aff_fonciere'),
    

    path('admin/', admin.site.urls),
    path('publication/<int:pk>/', publication_detail, name='publication_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
