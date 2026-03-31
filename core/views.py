from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Publication, Contact, Audience, Personne, Delocalisation, Newsletter
from django.core.paginator import Paginator

def home(request):
    publications_list = Publication.objects.order_by('-date_publication')
    paginator = Paginator(publications_list, 10)
    page_number = request.GET.get('page')
    publications = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'publications': publications, 
        'content': 'home',
        'page_title': 'Accueil',
        'page_description': 'Bienvenue sur le site officiel d\'AFFAGRIPEL Lualaba, le Ministère Provincial des Affaires Foncières, Agriculture, Pêche, Élevage et Développement Rural.'
    })

def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'index.html', {
        'publication': publication, 
        'content': 'publication',
        'page_title': publication.titre,
        'page_description': publication.description[:150] + '...' if publication.description else 'Détails de la publication AFFAGRIPEL Lualaba.'
    })

def peche_et_elevage(request):
    return render(request, 'index.html', {
        'content': 'pecheElevage',
        'page_title': 'Pêche & Élevage',
        'page_description': 'Découvrez les actions d\'AFFAGRIPEL Lualaba pour la promotion et le développement de la pêche et de l\'élevage dans la province.'
    })

def agriculture(request):
    return render(request, 'index.html', {
        'content': 'agriculture',
        'page_title': 'Agriculture',
        'page_description': 'Informez-vous sur les initiatives agricoles et le soutien aux agriculteurs par le Ministère Provincial AFFAGRIPEL Lualaba.'
    })

def devRural(request):
    return render(request, 'index.html', {
        'content': 'devRural',
        'page_title': 'Développement Rural',
        'page_description': 'Les projets et stratégies pour le développement rural du Lualaba avec le soutien d\'AFFAGRIPEL.'
    })

def apropos(request):
    return render(request, 'index.html', {
        'content': 'apropos',
        'page_title': 'À Propos de Nous',
        'page_description': 'Apprenez-en plus sur la mission, la vision et les valeurs du Ministère Provincial AFFAGRIPEL Lualaba.'
    })

def aff_fonciere(request):
    context = {
        'content': 'aff_fonciere',
        'page_title': 'Affaires Foncières & Délocalisation',
        'page_description': 'Consultez les procédures de délocalisation et d\'indemnisation foncière via la Fondation JMK pour la Province du Lualaba.'
    }

    if request.method == 'POST':
        numero = request.POST.get('numero_identite', '').strip()
        context['numero_recherche'] = numero
        context['recherche_effectuee'] = True

        if numero:
            try:
                personne = Personne.objects.get(numero_identite=numero)
                delocalisations = personne.proprietes.all()
                context['personne'] = personne
                context['delocalisations'] = delocalisations

                if not delocalisations.exists():
                    messages.info(request, f"Aucune délocalisation enregistrée pour {personne.nom} {personne.postnom} {personne.prenom}.")
            except Personne.DoesNotExist:
                messages.error(request, f"Aucune personne trouvée avec le numéro d'identité : {numero}")
        else:
            messages.error(request, "Veuillez entrer un numéro d'identité valide.")

    return render(request, 'index.html', context)


# ================= CONTACT =================
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom_complet', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if nom and email and message_text:
            Contact.objects.create(
                nom_complet=nom,
                email=email,
                message=message_text,
            )
            messages.success(request, "Votre message a été envoyé avec succès !")
        else:
            messages.error(request, "Veuillez remplir tous les champs du formulaire de contact.")

        return redirect('contact')

    return render(request, 'index.html', {
        'content': 'contact',
        'page_title': 'Contactez-nous',
        'page_description': 'Entrez en contact avec AFFAGRIPEL Lualaba pour toute question, suggestion ou requête officielle.'
    })


# ================= DEMANDE D'AUDIENCE =================
def demandeAudience(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        poste = request.POST.get('poste', '').strip()
        photo_id = request.FILES.get('photo_id')
        lettre = request.FILES.get('lettre')

        if nom and poste and photo_id and lettre:
            Audience.objects.create(
                nom_complet=nom,
                poste=poste,
                photo_identite=photo_id,
                lettre_demande=lettre,
            )
            messages.success(request, "Votre demande d'audience a été envoyée avec succès !")
        else:
            messages.error(request, "Veuillez remplir tous les champs et joindre les fichiers requis.")

        return redirect('contact')

    return render(request, 'index.html', {
        'content': 'contact',
        'page_title': 'Demande d\'Audience',
        'page_description': 'Faites une demande formelle d\'audience auprès du Ministère Provincial des Affaires Foncières (AFFAGRIPEL Lualaba).'
    })


# ================= NEWSLETTER =================
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(email=email)
                messages.success(request, "Merci ! Vous êtes maintenant inscrit à notre newsletter.")
            else:
                messages.info(request, "Vous êtes déjà inscrit à notre newsletter.")
        else:
            messages.error(request, "Veuillez fournir une adresse email valide.")
            
    # Rediriger l'utilisateur vers la page d'où il vient (ou home par défaut)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
