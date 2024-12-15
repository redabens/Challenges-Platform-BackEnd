from django.urls import path
from . import views

urlpatterns = [
    #participant
    path('register/', views.RegisterView.as_view(), name='participant-register'),
    path('auth/', views.ParticipantAuthView.as_view(), name='auth-participant'),
    path('delete-participant/<int:id>/', views.ParticipantDeleteView.as_view(), name='delete_participant'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    #team
    path('create-team/', views.TeamCreateView.as_view(), name='create_team'),
    path('join-team/<int:id>/', views.ParticipantJoinTeamView.as_view(), name='join_team'),
    path('hackatonteams/<int:id>/', views.TeamHackatonListView.as_view(), name='list_hacktonteams'),
    path('team/<int:id>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('remove-participant-team/<int:id>/', views.RemoveParticipantTeamView.as_view(), name='remove_participant_team'),
    #hackaton
    path('hackaton/', views.HackatonListCreateView.as_view(), name='create_hackaton'),
    # URL pour lister les challenges et en créer un (GET et POST)
    path('challenges/', views.ChallengeListCreateView.as_view(), name='challenge-list-create'),
    # URL pour récupérer un challenge spécifique par son 'id'
    path('challenges/<int:id>/', views.ChallengeDetailView.as_view(), name='challenge-detail'),
]