from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password  # Import pour hacher le mot de passe et le checker
from django.core.exceptions import ObjectDoesNotExist
from . import models

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ['first_name', 'last_name', 'email', 'phone', 'birthdate', 'Nss', 'University', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Empêche le retour du mot de passe dans les réponses
        }

    def validate_password(self, value):
        """
        Cette méthode est appelée pour valider et hacher le mot de passe.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return make_password(value)  # Retourne le mot de passe haché

    def create(self, validated_data):
        # Si vous voulez hasher le mot de passe pour plus de sécurité
        participant = models.Participant(**validated_data)
        participant.password = validated_data['password']  # Utiliser un hash comme bcrypt si nécessaire
        participant.save()
        return participant

class ParticipantAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            # Récupérer le participant par email
            participant = models.Participant.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Participant introuvable avec cet email.")
        
        # Vérifier le mot de passe avec `check_password`
        if not check_password(password, participant.password):
            raise serializers.ValidationError("Mot de passe incorrect.")

        # Créer ou récupérer un utilisateur associé au participant
        # Si le participant n'a pas d'utilisateur lié, on crée un utilisateur
        user, created = User.objects.get_or_create(username=participant.email)

        # Enregistrer ou lier l'utilisateur au participant
        # Si un utilisateur est créé, on peut éventuellement l'associer au participant
        if created:
            user.set_password(password)  # Si l'utilisateur est nouveau, on définit son mot de passe.
            user.save()

        participant.user = user  # Lier l'utilisateur au participant
        participant.save()
        # Ajouter l'instance de participant aux données validées
        data['participant'] = participant
        return data

class HackatonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hackaton
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'teamLimit', 'is_available']

        def validate(self, data):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("La date de début ne peut pas être après la date de fin.")
            return data

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['id', 'name', 'code', 'hackaton', 'participants', 'full']
        read_only_fields = ['id', 'code']

    def create(self, validated_data):
        # Récupérer l'utilisateur authentifié
        user = self.context['request'].user  # `request.user` contient l'utilisateur authentifié
        participant = models.Participant.objects.get(user=user)  # Récupère le participant lié à cet utilisateur

        # Créer la team avec les données validées
        team = models.Team.objects.create(**validated_data)

        # Ajouter le participant à la team
        team.participants.add(participant)  # Ajouter l'utilisateur actuel à la team
        
        # Vérifier si la team est pleine
        if team.participants.count() >= team.hackaton.teamLimit:
            team.full = True
            team.save()
        return team
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['id', 'name', 'code', 'hackaton', 'participants', 'full']
        read_only_fields = ['id', 'code']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = ['id', 'title', 'pdf']