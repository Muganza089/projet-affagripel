from django.shortcuts import render,get_object_or_404
from .models import Publication

def home(request):
    publications = Publication.objects.order_by('-date_publication')  # Les plus récentes en premier
    return render(request, 'index.html', {'publications': publications,'content': 'home'})

def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'index.html', {'publication': publication, 'content': 'publication' })

def peche_et_elevage(request):
    return render(request, 'index.html', {
        'content': 'pecheElevage',
    })
def agriculture(request):
    return render(request, 'index.html', {
        'content': 'agriculture',
    })
def devRural(request):
    return render(request, 'index.html', {
        'content': 'devRural',
    })
def apropos(request):
    return render(request, 'index.html', {
        'content': 'apropos',
    })
def demandeAudience(request):
    return render(request, 'index.html', {
        'content': 'demandeAudience',
    })
def aff_fonciere(request):
    return render(request, 'index.html', {
        'content': 'aff_fonciere',
    })

