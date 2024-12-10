import random
import string
from django.db import models
from django.contrib.auth.models import User  # Utilise le modèle User de Django

# Create your models here.
class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    birthdate = models.DateField()
    Nss = models.CharField(max_length=12)
    University = models.CharField(max_length=200)
    password = models.CharField(max_length=255)  # Ajouter un champ de mot de passe

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Hackaton(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    teamLimit = models.IntegerField()
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, editable=False)  # Code unique et non modifiable
    hackaton = models.ForeignKey(Hackaton, on_delete=models.CASCADE, related_name='teams')
    participants = models.ManyToManyField(Participant, related_name='teams', blank=True)
    full = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Générer un code aléatoire si le champ est vide
        if not self.code:
            self.code = self.generate_random_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_random_code():
        letters = random.choices(string.ascii_uppercase, k=3)  # Génère 3 lettres majuscules
        digits = random.choices(string.digits, k=3)  # Génère 3 chiffres
        combined = letters + digits
        random.shuffle(combined)  # Mélanger les lettres et chiffres
        return ''.join(combined)  # Convertir la liste en string

    def __str__(self):
        return f"{self.name} ({self.code})"

class Document(models.Model):
    title = models.CharField(max_length=100)
    pdf = models.BinaryField()  # Pour stocker le fichier PDF sous forme binaire

    def __str__(self):
        return self.title
