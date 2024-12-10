from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
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

# class Hackaton
class HackatonListView(generics.ListAPIView):
    queryset = models.Hackaton.objects.all()
    serializer_class = serializers.HackatonSerializer

class HackatonCreateView(generics.CreateAPIView):
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
    serializer_class = serializers.TeamSerializer

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

class TeamHackatonListView(generics.RetrieveAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    lookup_field = 'id'
# class Document