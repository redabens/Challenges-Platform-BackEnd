# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Hackathon, Participant, Challenge, Team, Submission
from django.contrib.auth.models import User

class HackathonTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hackathon_data = {
            'title': 'Test Hackathon',
            'description': 'This is a test hackathon',
            'start_date': '2023-01-01T00:00:00Z',
            'end_date': '2023-12-31T23:59:59Z'
        }
        self.hackathon = Hackathon.objects.create(**self.hackathon_data)

    def test_get_hackathons(self):
        response = self.client.get(reverse('hackathon-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.hackathon_data['title'])

class ParticipantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.participant_data = {
            'user': self.user,
            'team_name': 'Test Team'
        }
        self.participant = Participant.objects.create(**self.participant_data)

    def test_get_participants(self):
        response = self.client.get(reverse('participant-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['team_name'], self.participant_data['team_name'])

class ChallengeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hackathon = Hackathon.objects.create(
            title='Test Hackathon',
            description='This is a test hackathon',
            start_date='2023-01-01T00:00:00Z',
            end_date='2023-12-31T23:59:59Z'
        )
        self.challenge_data = {
            'hackathon': self.hackathon,
            'title': 'Test Challenge',
            'description': 'This is a test challenge',
            'pdf': 'path/to/pdf'
        }
        self.challenge = Challenge.objects.create(**self.challenge_data)

    def test_get_challenges(self):
        response = self.client.get(reverse('challenge-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.challenge_data['title'])

class TeamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hackathon = Hackathon.objects.create(
            title='Test Hackathon',
            description='This is a test hackathon',
            start_date='2023-01-01T00:00:00Z',
            end_date='2023-12-31T23:59:59Z'
        )
        self.team_data = {
            'name': 'Test Team',
            'hackathon': self.hackathon
        }
        self.team = Team.objects.create(**self.team_data)

    def test_get_teams(self):
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.team_data['name'])

class SubmissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hackathon = Hackathon.objects.create(
            title='Test Hackathon',
            description='This is a test hackathon',
            start_date='2023-01-01T00:00:00Z',
            end_date='2023-12-31T23:59:59Z'
        )
        self.team = Team.objects.create(name='Test Team', hackathon=self.hackathon)
        self.challenge = Challenge.objects.create(
            hackathon=self.hackathon,
            title='Test Challenge',
            description='This is a test challenge',
            pdf='path/to/pdf'
        )
        self.submission_data = {
            'team': self.team,
            'challenge': self.challenge,
            'description': 'This is a test submission',
            'demo_video': 'http://example.com/demo',
            'resource_links': 'http://example.com/resource1,http://example.com/resource2'
        }
        self.submission = Submission.objects.create(**self.submission_data)

    def test_get_submissions(self):
        response = self.client.get(reverse('submission-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], self.submission_data['description'])