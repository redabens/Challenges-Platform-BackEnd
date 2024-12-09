from django.db import models
from django.contrib.auth.models import User

# Hackathon Model
class Hackathon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Participant Profile
class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Challenge Model
class Challenge(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=200)
    description = models.TextField()
    pdf = models.FileField(upload_to='challenges/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Participant, related_name='teams')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name

# Solution Submission Model
class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='submissions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='submissions')
    description = models.TextField()
    demo_video = models.URLField(max_length=200, blank=True)
    resource_links = models.TextField(help_text="Add links separated by commas", blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.team.name} for {self.challenge.title}"

# Admin Management (Optional for extended control)
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_super_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username