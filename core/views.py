from django.shortcuts import render

def home(request):
     return render(request, "index.html", {
        'content': 'home',
    })
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
        'content': 'devMode',
    })
def aff_fonciere(request):
    return render(request, 'index.html', {
        'content': 'devMode',
    })

