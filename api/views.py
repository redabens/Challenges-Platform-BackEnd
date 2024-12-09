# views.py
from rest_framework import generics
from .models import Challenge, Submission, Team
from .serializers import ChallengeSerializer, SubmissionSerializer, TeamSerializer

class ChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class SubmissionList(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer