from django.urls import path
from .views import HackathonList, ParticipantList, ChallengeList, TeamList, SubmissionList

urlpatterns = [
    path('hackathons/', HackathonList.as_view(), name='hackathon-list'),
    path('participants/', ParticipantList.as_view(), name='participant-list'),
    path('challenges/', ChallengeList.as_view(), name='challenge-list'),
    path('teams/', TeamList.as_view(), name='team-list'),
    path('submissions/', SubmissionList.as_view(), name='submission-list'),
]