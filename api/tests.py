from django.test import TestCase
from django.contrib.auth.models import User
from .models import Hackathon, Participant, Challenge, Team, Submission

class HackathonModelTest(TestCase):
    def setUp(self):
        self.hackathon = Hackathon.objects.create(
            title="Test Hackathon",
            description="This is a test hackathon.",
            start_date="2023-01-01T00:00:00Z",
            end_date="2023-01-02T00:00:00Z"
        )

    def test_hackathon_creation(self):
        self.assertEqual(self.hackathon.title, "Test Hackathon")
        self.assertEqual(self.hackathon.description, "This is a test hackathon.")
        self.assertEqual(str(self.hackathon), "Test Hackathon")

class ParticipantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.participant = Participant.objects.create(
            user=self.user,
            team_name="Test Team"
        )

    def test_participant_creation(self):
        self.assertEqual(self.participant.user.username, "testuser")
        self.assertEqual(self.participant.team_name, "Test Team")
        self.assertEqual(str(self.participant), "testuser")

class ChallengeModelTest(TestCase):
    def setUp(self):
        self.challenge = Challenge.objects.create(
            title="Test Challenge",
            description="This is a test challenge.",
            pdf="challenges/test.pdf"
        )

    def test_challenge_creation(self):
        self.assertEqual(self.challenge.title, "Test Challenge")
        self.assertEqual(self.challenge.description, "This is a test challenge.")
        self.assertEqual(str(self.challenge), "Test Challenge")

class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")

    def test_team_creation(self):
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(str(self.team), "Test Team")

class SubmissionModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.challenge = Challenge.objects.create(
            title="Test Challenge",
            description="This is a test challenge.",
            pdf="challenges/test.pdf"
        )
        self.submission = Submission.objects.create(
            team=self.team,
            challenge=self.challenge,
            description="This is a test submission.",
            demo_video="http://example.com/demo",
            resource_links="http://example.com/resource1,http://example.com/resource2"
        )

    def test_submission_creation(self):
        self.assertEqual(self.submission.team.name, "Test Team")
        self.assertEqual(self.submission.challenge.title, "Test Challenge")
        self.assertEqual(self.submission.description, "This is a test submission.")
        self.assertEqual(str(self.submission), "Submission by Test Team for Test Challenge")