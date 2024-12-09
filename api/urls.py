# urls.py
from django.urls import path
from .views import ChallengeList, SubmissionList, TeamList

urlpatterns = [
    path('challenges/', ChallengeList.as_view(), name='challenge-list'),
    path('submissions/', SubmissionList.as_view(), name='submission-list'),
    path('teams/', TeamList.as_view(), name='team-list'),
]