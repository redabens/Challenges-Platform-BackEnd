from django.urls import path
from .views import Hackathon, ParticipantList, ChallengeList, TeamList, SubmissionList, UserList

urlpatterns = [
    path('hackathon/', Hackathon.as_view(), name='hackathon-list'),
    path('participants/', ParticipantList.as_view(), name='participant-list'),
    path('challenges/', ChallengeList.as_view(), name='challenge-list'),
    path('teams/', TeamList.as_view(), name='team-list'),
    path('submissions/', SubmissionList.as_view(), name='submission-list'),
        path('users/', UserList.as_view(), name='user-list'),
]