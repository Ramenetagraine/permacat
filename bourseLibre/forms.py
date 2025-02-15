from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Produit, Produit_aliment, Produit_objet, Produit_service, Produit_vegetal, Adresse, Profil, Message, MessageGeneral, Choix, MessageGeneralPermacat, MessageGeneralRTG
from bourseLibre.captcha_local.fields import CaptchaField
#from tinymce.widgets import TinyMCE
from django_summernote.widgets import SummernoteWidget

fieldsCommunsProduits = ['souscategorie', 'nom_produit',  'description', 'estUneOffre', 'estPublique',
                'unite_prix', 'prix',  'type_prix', 'date_debut', 'date_expiration', ]




class ProduitCreationForm(forms.ModelForm):
    #description = TinyMCE(attrs={'cols': 80, 'rows': 20})
    estUneOffre = forms.ChoiceField(choices=((1, "Offre"), (0, "Demande")), label='', required=True)
    estPublique = forms.ChoiceField(choices=((1, "Annonce publique"), (0, "Annonce réservée aux adhérents")), label='', required=True)

    class Meta:
        model = Produit
        exclude=('user', )

        fields = ['nom_produit', 'description', 'date_debut', 'date_expiration',
                  'stock_initial', 'unite_prix','prix',]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}, ),
            'date_expiration': forms.DateInput(attrs={'type':"date"}),
            'description': SummernoteWidget(),
        }


    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_expiration = cleaned_data.get("date_expiration")
        if date_debut and date_expiration:
            # Only do something if both fields are valid so far.
            if date_debut > date_expiration:
                raise forms.ValidationError(
                    "La date de fin doit etre après la date de début"
                )
        return self.cleaned_data

class Produit_aliment_CreationForm(ProduitCreationForm):

    class Meta:
        model = Produit_aliment
        fields = fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}, ),
            'date_expiration': forms.DateInput(attrs={'type':"date"}),
            'description': SummernoteWidget(),
        }

class Produit_aliment_modifier_form(Produit_aliment_CreationForm):

    def __init__(self, *args, **kwargs):
        super(Produit_aliment_modifier_form, self).__init__(*args, **kwargs)
        self.fields["estPublique"].choices = ((1, "Annonce publique"), (0, "Annonce réservée aux adhérents")) if kwargs[
            'instance'].estPublique else ((0, "Annonce réservée aux adhérents"),(1, "Annonce publique"),)
        self.fields["estUneOffre"].choices = ((1, "Offre"), (0, "Demande")) if kwargs[
            'instance'].estUneOffre else ((0, "Demande"), (1, "Offre"), )


class Produit_vegetal_CreationForm(ProduitCreationForm):

    class Meta:
        model = Produit_vegetal
        fields = fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}, ),
            'date_expiration': forms.DateInput(attrs={'type':"date"}),
            'description': SummernoteWidget(),
        }

class Produit_vegetal_modifier_form(Produit_vegetal_CreationForm):

    def __init__(self, *args, **kwargs):
        super(Produit_vegetal_modifier_form, self).__init__(*args, **kwargs)
        self.fields["estPublique"].choices = ((1, "Annonce publique"), (0, "Annonce réservée aux adhérents")) if kwargs[
            'instance'].estPublique else ((0, "Annonce réservée aux adhérents"),(1, "Annonce publique"),)
        self.fields["estUneOffre"].choices = ((1, "Offre"), (0, "Demande")) if kwargs[
            'instance'].estUneOffre else ((0, "Demande"), (1, "Offre"), )

class Produit_service_CreationForm(ProduitCreationForm):
    class Meta:
        model = Produit_service
        fields = fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}, ),
            'date_expiration': forms.DateInput(attrs={'type':"date"}),
            'description': SummernoteWidget(),
        }

class Produit_service_modifier_form(Produit_service_CreationForm):

    def __init__(self, *args, **kwargs):
        super(Produit_service_modifier_form, self).__init__(*args, **kwargs)
        self.fields["estPublique"].choices = ((1, "Annonce publique"), (0, "Annonce réservée aux adhérents")) if \
        kwargs[
            'instance'].estPublique else ((0, "Annonce réservée aux adhérents"), (1, "Annonce publique"),)
        self.fields["estUneOffre"].choices = ((1, "Offre"), (0, "Demande")) if kwargs[
            'instance'].estUneOffre else ((0, "Demande"), (1, "Offre"),)

class Produit_objet_CreationForm(ProduitCreationForm):
    class Meta:
        model = Produit_objet
        fields = fieldsCommunsProduits
        widgets = {
            'date_debut': forms.DateInput(attrs={'type':"date"}, ),
            'date_expiration': forms.DateInput(attrs={'type':"date"}),
            'description': SummernoteWidget(),
        }

class Produit_objet_modifier_form(Produit_objet_CreationForm):

    def __init__(self, *args, **kwargs):
        super(Produit_objet_modifier_form, self).__init__(*args, **kwargs)
        self.fields["estPublique"].choices = ((1, "Annonce publique"), (0, "Annonce réservée aux adhérents")) if kwargs[
            'instance'].estPublique else ((0, "Annonce réservée aux adhérents"),(1, "Annonce publique"),)
        self.fields["estUneOffre"].choices = ((1, "Offre"), (0, "Demande")) if kwargs[
            'instance'].estUneOffre else ((0, "Demande"), (1, "Offre"), )

class AdresseForm(forms.ModelForm):
    rue = forms.CharField(label="Rue", required=False)
    code_postal = forms.CharField(label="Code postal*", initial="66000")
    telephone = forms.CharField(label="Téléphone", required=False)
    pays = forms.CharField(label="Pays*", initial="France",required=True)
    latitude = forms.FloatField(label="Latitude", initial="42", required=False,widget = forms.HiddenInput())
    longitude = forms.FloatField(label="Longitude", initial="2", required=False,widget = forms.HiddenInput())

    class Meta:
        model = Adresse
        exclude = ('latitude', 'longitude')

    def save(self, *args, **kwargs):
        adresse = super(AdresseForm, self).save(commit=False)
        adresse.set_latlon_from_adresse()
        adresse.save()
        return adresse

class ProfilCreationForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme*", help_text="Attention les majuscules sont importantes...")
    description = forms.CharField(label=None, help_text="Une description de vous même", required=False, widget=forms.Textarea)
    competences = forms.CharField(label=None, help_text="Par exemple: electricien, bouturage, aromatherapie, pépinieriste, etc...", required=False, widget=forms.Textarea, )
    site_web = forms.CharField(label="Site web", help_text="n'oubliez pas le https://", required=False)
    captcha = CaptchaField()
    email = forms.EmailField(label="Email*",)

    statut_adhesion = forms.ChoiceField(choices=Choix.statut_adhesion, label='', required=True)
    statut_adhesion_rtg = forms.ChoiceField(choices=Choix.statut_adhesion_rtg, label='', required=True)
    accepter_annuaire = forms.BooleanField(required=False, label="J'accepte d'apparaitre dans l'annuaire du site et la carte et rend mon profil visible par tous les inscrits")
    accepter_conditions = forms.BooleanField(required=True, label="J'ai lu et j'accepte les Conditions Générales d'Utilisation du site",  )
    pseudo_june = forms.CharField(label="Pseudonyme dans la monnaie libre (Duniter)",  help_text="Si vous avez un compte en June",required=False)


    def __init__(self, request, *args, **kargs):
        super(ProfilCreationForm, self).__init__(request, *args, **kargs)
        self.fields['description'].strip = False
        self.fields['competences'].strip = False

    class Meta(UserCreationForm):
        model = Profil
        fields = ['username', 'password1',  'password2', 'first_name', 'last_name', 'email', 'site_web', 'description', 'competences', 'pseudo_june', 'inscrit_newsletter', 'accepter_annuaire', 'statut_adhesion', 'statut_adhesion_rtg', 'accepter_conditions']
        exclude = ['slug', ]


    def save(self, commit = True, is_active=False):
        return super(ProfilCreationForm, self).save(commit)
        self.is_active=is_active



class ProducteurChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme")
    description = forms.CharField(label="Description", help_text="Une description de vous même",widget=SummernoteWidget)
    competences = forms.CharField(label="Savoir-faire", help_text="Par exemple: electricien, bouturage, aromatherapie, etc...",widget=SummernoteWidget)
    inscrit_newsletter = forms.BooleanField(required=False)
    accepter_annuaire = forms.BooleanField(required=False, label="J'accepte d'apparaitre dans l'annuaire du site et la carte et rend mon profil visible par tous")
    password=None

    def __init__(self, *args, **kargs):
        super(ProducteurChangeForm, self).__init__(*args, **kargs)
        self.fields['description'].strip = False
        self.fields['competences'].strip = False

    class Meta:
        model = Profil
        fields = ['username', 'first_name', 'last_name', 'email', 'site_web', 'description', 'competences', 'pseudo_june', 'accepter_annuaire', 'inscrit_newsletter']


class ProducteurChangeForm_admin(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme")
    description = forms.CharField(label="Description", initial="Une description de vous même", widget=forms.Textarea)
    competences = forms.CharField(label="Savoir-faire",
                                  initial="Par exemple: electricien, bouturage, aromatherapie, etc...", required=False,
                                  widget=forms.Textarea)
    avatar = forms.ImageField(required=False)
    inscrit_newsletter = forms.BooleanField(required=False)
    accepter_annuaire = forms.BooleanField(required=False)
    cotisation_a_jour = forms.BooleanField(required=False)
    pseudo_june = forms.CharField(label="pseudo_june",required=False)

    statut_adhesion = forms.ChoiceField(choices=Choix.statut_adhesion)
    statut_adhesion_rtg = forms.ChoiceField(choices=Choix.statut_adhesion_rtg)
    password = None

    class Meta:
        model = Profil
        fields = ['username', 'email', 'description', 'competences', 'inscrit_newsletter', 'statut_adhesion', 'statut_adhesion_rtg', 'pseudo_june', 'accepter_annuaire', 'cotisation_a_jour']

    def __init__(self, *args, **kwargs):
        super(ProducteurChangeForm_admin, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False
        self.fields['competences'].strip = False

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100, label="Sujet",)
    msg = forms.CharField(label="Message", widget=SummernoteWidget)
    renvoi = forms.BooleanField(label="recevoir une copie",
                                     help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False
                                 )



class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ['conversation','auteur']

        widgets = {
                'message': forms.Textarea(attrs={'rows': 2}),
            }

    def __init__(self, request, message=None, *args, **kwargs):
        super(MessageForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['message'].initial = message

class ChercherConversationForm(forms.Form):
    destinataire = forms.ChoiceField(label='destinataire')

    def __init__(self, user, *args, **kwargs):
        super(ChercherConversationForm, self).__init__(*args, **kwargs)
        self.fields['destinataire'].choices = [(i,u) for i, u in enumerate(Profil.objects.all().order_by('username')) if u != user]

class MessageGeneralForm(forms.ModelForm):
    class Meta:
        model = MessageGeneral
        exclude = ['auteur']

        widgets = {
            'message': forms.Textarea(attrs={'rows': 1}),
        }

    #def __init__(self, request, message=None, *args, **kwargs):
    #    super(MessageGeneralForm, self).__init__(request, *args, **kwargs)


class MessageGeneralPermacatForm(forms.ModelForm):

    class Meta:
        model = MessageGeneralPermacat
        exclude = ['auteur']

        widgets = {
                'message': forms.Textarea(attrs={'rows': 1}),
            }

class MessageGeneralRTGForm(forms.ModelForm):

    class Meta:
        model = MessageGeneralRTG
        exclude = ['auteur']

        widgets = {
                'message': forms.Textarea(attrs={'rows': 1}),
            }