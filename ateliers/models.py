from django.db import models
from bourseLibre.models import Profil, Suivis
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from bourseLibre import settings
from django.contrib.auth.models import Group, User
import uuid

class Choix():
    type_atelier = ('0','Permaculture'), ('1',"Bricolage"), ('2','Cuisine'), ('3','Bien-être'),('4',"Musique"), ('5', 'Autre...')
    couleurs_ateliers = {
        '2':'#4DC490', '1':'#C0EDA0', '3':'#00AA8B', '0':'#FCE79C',
        # '0':"#e0f7de", '1':"#dcc0de",
        # '5':"#d1ecdc",'3':"#fcf6bd", '4':"#d0f4de", '7':"#fff2a0",
        # '9':"#ffc4c8", '2':"#bccacf", '10':"#87bfae", '11':"#bcb4b4"
    }
    statut_atelier = ('0', 'proposition'), ('1', "accepté, en cours d'organisation"),
    type_difficulte = ('0', 'facile'), ('1', "moyen"), ("2", "difficile")
    type_jauge = ('1', "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")
    type_budget = ('0', "0"), ('1', "1"), ("2", "2"), ("3", "3")
    type_temps = ('1', "1h"), ("2", "2h"), ("3", "3h"), ("4", "4h"), ("5", "6h"), ("6", "1 journée"),  ("7", "plusieurs jours"),  ("8", "plusieurs mois"),
    type_age = ('0', '3-6 ans'), ('1', "7-11 ans"), ("2", "12 ans et plus"), ("3", "3-11ans"), ("4", "Tout public")
    #type_atelier = ('0', 'Observation'), ('1', "Experience"), ("2", "Jardinage")

    def get_categorie(num):
        return Choix.type_atelier[int(num)][1]

    def get_difficulte(num):
        return Choix.type_difficulte[int(num)][1]

    def get_age(num):
        return Choix.type_atelier[int(num)][1]

    def get_typeAtelier(num):
        return Choix.type_atelier[int(num)][1]

    def get_couleur_cat(cat):
            return Choix.couleurs_ateliers[cat]

class Atelier(models.Model):
    categorie = models.CharField(max_length=30,
        choices=(Choix.type_atelier),
        default='0', verbose_name="categorie")
    statut = models.CharField(max_length=30,
        choices=(Choix.statut_atelier),
        default='proposition', verbose_name="statut de la atelier")
    titre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=100, default=uuid.uuid4)
    description = models.TextField(null=True, blank=True)
    materiel = models.TextField(null=True, blank=True, verbose_name="Matériel nécessaire")
    référent = models.CharField(max_length=120, null=True, blank=True,  verbose_name="Référent(e.s)")

    date_atelier = models.DateTimeField(verbose_name="Date prévue", default=timezone.now, blank=True, null=True)

    date_creation = models.DateTimeField(verbose_name="Date de parution", default=timezone.now)
    date_modification = models.DateTimeField(verbose_name="Date de modification", default=timezone.now)

    date_dernierMessage = models.DateTimeField(verbose_name="Date du dernier message", auto_now=True)
    dernierMessage = models.CharField(max_length=100, default=None, blank=True, null=True)

    tags = TaggableManager(verbose_name=("Mots-clés"), help_text=("Une liste de mots clés, séparés par des virgules."), blank=True,)

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)


    class Meta:
        ordering = ('-date_creation', )
        
    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('ateliers:lireAtelier', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_creation = timezone.now()
        return super(Atelier, self).save(*args, **kwargs)

    @property
    def get_couleur(self):
            return Choix.couleurs_ateliers[self.categorie]

    @property
    def get_couleur_cat(self,cat):
            return Choix.couleurs_ateliers[cat]




class CommentaireAtelier(models.Model):
    auteur_comm = models.ForeignKey(Profil, on_delete=models.CASCADE)
    commentaire = models.TextField()
    atelier = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "(" + str(self.id) + ") "+ str(self.auteur_comm) + ": " + str(self.atelier)

