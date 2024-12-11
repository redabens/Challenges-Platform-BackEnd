from django.urls import path
from . import views

urlpatterns = [
    #participant
    path('register/', views.RegisterView.as_view(), name='participant-register'),
    path('auth/', views.ParticipantAuthView.as_view(), name='auth-participant'),
    path('delete_participant/<int:id>/', views.ParticipantDeleteView.as_view(), name='delete_participant'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    #team
    path('create_team/', views.TeamCreateView.as_view(), name='create_team'),
    path('join_team/<int:id>/', views.ParticipantJoinTeamView.as_view(), name='join_team'),
    path('hackatonteams/<int:id>/', views.TeamHackatonListView.as_view(), name='list_hacktonteams'),
    path('team/<int:id>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('remove_participant_team/<int:id>/', views.RemoveParticipantTeamView.as_view(), name='remove_participant_team'),
    #hackaton
    path('create_hackaton/', views.HackatonCreateView.as_view(), name='create_hackaton'),
    path('hackatons/', views.HackatonListView.as_view(), name='list_hackatons'),
]