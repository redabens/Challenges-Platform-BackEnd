from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from . import serializers

# Create your views here.

# class Participant
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permet l'accès sans authentification

    def post(self, request, *args, **kwargs):
        serializer = serializers.ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipantAuthView(APIView):
    permission_classes = [AllowAny]  # Permet à tout le monde de tenter l'authentification

    def post(self, request, *args, **kwargs):
        serializer = serializers.ParticipantAuthSerializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.validated_data['participant']
            user = participant.user

            # Créer un token JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "message": "Connexion réussie.",
                    "token": access_token,
                    "participant": {
                        "first_name": participant.first_name,
                        "last_name": participant.last_name,
                        "email": participant.email,
                    }
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipantDeleteView(generics.DestroyAPIView):
    queryset = models.Participant.objects.all()
    serializer_class = serializers.ParticipantSerializer
    lookup_field = 'id'
    def destroy(self, request, *args, **kwargs):
        # Récupérer l'instance avant de la supprimer
        participant = self.get_object()
        
        # Supprimer l'instance
        participant.delete()
        
        # Retourner une réponse personnalisée
        return Response(
            {'message': f"Participant {participant.first_name} {participant.last_name} deleted successfully."},
            status=status.HTTP_200_OK
        )
class ParticipantJoinTeamView(generics.UpdateAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # L'équipe est déjà récupérée grâce à 'get_object()'
        team = self.get_object()

        # Ajouter le participant (le reste de la logique est identique)
        user = request.user
        try:
            participant = models.Participant.objects.get(user=user)
        except models.Participant.DoesNotExist:
            return Response({'detail': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)

        if participant in team.participants.all():
            return Response({'detail': 'You are already in this team.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ajouter le participant
        team.participants.add(participant)

        # Vérifier si l'équipe est pleine
        if team.participants.count() >= team.hackaton.teamLimit:
            team.full = True
            team.save()

        # Sauvegarder l'équipe après modification
        team.save()

        return Response(
            {'message': f"Team {team.name} {team.code} updated successfully. Participant {user.first_name} joined."},
            status=status.HTTP_200_OK
        )

class ParticipantLeaveTeamView(generics.UpdateAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # L'équipe est déjà récupérée grâce à 'get_object()'
        team = self.get_object()

        # Ajouter le participant (le reste de la logique est identique)
        user = request.user
        try:
            participant = models.Participant.objects.get(user=user)
        except models.Participant.DoesNotExist:
            return Response({'detail': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)

        if participant not in team.participants.all():
            return Response({'detail': 'You are not in this team.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ajouter le participant
        team.participants.remove(participant)

        # Vérifier si l'équipe est pleine
        if team.participants.count() < team.hackaton.teamLimit:
            team.full = False
            team.save()

        # Sauvegarder l'équipe après modification
        team.save()

        return Response(
            {'message': f"Team {team.name} {team.code} updated successfully. Participant {user.first_name} left."},
            status=status.HTTP_200_OK
        )

# class Hackaton
class HackatonListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Permet d'assurer que l'utilisateur est authentifié
    queryset = models.Hackaton.objects.all()
    serializer_class = serializers.HackatonSerializer

class HackatonCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # Permet d'assurer que l'utilisateur est authentifié
    queryset = models.Hackaton.objects.all()
    serializer_class = serializers.HackatonSerializer

    def create(self, request, *args, **kwargs):
        # Sérialisation et création de l'objet
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Sauvegarder le hackathon
            serializer.save()
            return Response(
                {'message': f'Hackathon {serializer.instance.name} created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Team
class TeamCreateView(generics.CreateAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamCreateSerializer

    def create(self, request, *args, **kwargs):
        # Sérialisation et création de l'objet
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Sauvegarder la team
            serializer.save() 
             # Retourner une réponse personnalisée
            return Response(
                {'message': f"Team {serializer.instance.name} {serializer.instance.code} created successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamDetailView(generics.RetrieveAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    lookup_field = 'id'

class TeamHackatonListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Permet d'assurer que l'utilisateur est authentifié
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    lookup_field = 'id'

class RemoveParticipantTeamView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]  # Permet d'assurer que l'utilisateur est authentifié
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # Récupérer l'équipe à partir de l'ID dans l'URL
        team = self.get_object()

        # Vérifier si l'utilisateur est un administrateur
        # if not request.user.is_staff:  # Vérifier si l'utilisateur est un admin
        #     return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Récupérer l'ID du participant à retirer depuis les données de la requête (par exemple)
        participant_id = request.data.get('participant_id')
        if not participant_id:
            return Response({'detail': 'Participant ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = models.Participant.objects.get(id=participant_id)
        except models.Participant.DoesNotExist:
            return Response({'detail': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si le participant appartient bien à cette équipe
        if participant not in team.participants.all():
            return Response({'detail': 'Participant is not in this team.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retirer le participant de l'équipe
        team.participants.remove(participant)

        # Si l'équipe devient vide, on peut définir `full` à `False` (selon la logique de ton projet)
        if team.participants.count() < team.hackaton.teamLimit:
            team.full = False
            team.save()

        # Retourner une réponse avec un message de succès
        return Response(
            {'message': f"Participant {participant.user.first_name} {participant.user.last_name} has been removed from team {team.name} {team.code}."},
            status=status.HTTP_200_OK
        )
# class Document
# logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Informer le client que la déconnexion est réussie
        return Response({"message": "Déconnexion réussie."}, status=200)