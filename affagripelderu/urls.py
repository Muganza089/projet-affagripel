from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('agriculture', agriculture, name='agriculture'),
    path('peche_et_elevage', peche_et_elevage, name='peche_et_elevage'),
    path('devRural', devRural, name='devRural'),
    path('apropos', apropos, name='apropos'),
    path('contact', contact, name='contact'),
    path('demandeAudience', demandeAudience, name='demandeAudience'),
    path('aff_fonciere', aff_fonciere, name='aff_fonciere'),
    path('cpd', cpd, name='cpd'),
    path('newsletter/subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    
    # Fichiers SEO statiques au niveau de la racine
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),

    path('admin/', admin.site.urls),
    path('publication/<int:pk>/', publication_detail, name='publication_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'core.views.custom_403_view'
handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'
