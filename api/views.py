from rest_framework import generics
from .models import Hackathon, Participant, Challenge, Team, Submission
from .serializers import HackathonSerializer, ParticipantSerializer, ChallengeSerializer, TeamSerializer, SubmissionSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer

class HackathonList(generics.ListCreateAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer

class ParticipantList(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class ChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class SubmissionList(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Home Page")

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
