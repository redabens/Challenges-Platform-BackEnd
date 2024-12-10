from django.urls import path
from . import views

urlpatterns = [
    #participant
    path('register/', views.RegisterView.as_view(), name='participant-register'),
    path('auth/', views.ParticipantAuthView.as_view(), name='auth-participant'),
    path('delete_participant/<int:id>/', views.ParticipantDeleteView.as_view(), name='delete_participant'),
    #team
    path('create_team/', views.TeamCreateView.as_view(), name='create_team'),
    path('hackatonteams/<int:id>/', views.TeamHackatonListView.as_view(), name='list_hacktonteams'),
    #hackaton
    path('create_hackaton/', views.HackatonCreateView.as_view(), name='create_hackaton'),
    path('hackatons/', views.HackatonListView.as_view(), name='list_hackatons'),
]