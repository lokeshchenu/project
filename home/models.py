import multiselectfield
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.utils.timezone import now
from multiselectfield import MultiSelectField


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
      return self.user.username

class OnlineContest(models.Model):
    contestName=models.CharField('contestName',max_length=200)
    contestLink=models.CharField('contestLink',max_length=200)
    TYPE_CHOICES = (
        ('Hackathon', 'HACKATHON'),
        ('Competitive', 'COMPETITIVE'),
    )
    contestType=models.CharField(max_length=12,choices=TYPE_CHOICES, default='hackathon')
    startingDateTime=models.DateTimeField('startingDateTime',default=now,editable=True)
    endingDateTime=models.DateTimeField('endingDateTime',default=now,editable=True)

    def __str__(self):
        return self.contestName


class Challenge(models.Model):
    challengeName=models.CharField('challengeName',max_length=200)
    createdBy=models.CharField('createdBy',max_length=200)
    TYPE_CHOICES = (
        ('Easy', 'EASY'),
        ('Medium', 'MEDIUM'),
        ('Hard','HARD')
    )
    challengeType=models.CharField(max_length=7,choices=TYPE_CHOICES,default='Easy')
    problemStatement=models.TextField('problemStatement')
    inputFormat=models.TextField('inputFormat')
    constraints=models.TextField('constraints')
    outputFormat=models.TextField('outputFormat')
    approach=models.TextField('approach')
    problemSolution=models.TextField('problemSolution')
    LANGUAGE_CHOICES=(
        ('Python','PYTHON'),
        ('C','C'),
        ('C++','C++')
    )
    languages=MultiSelectField(max_length=30,choices=LANGUAGE_CHOICES)
    Score = models.CharField('Score',max_length=10,default='100',editable=True)


    def __str__(self):
        return self.challengeName

class CampusContest(models.Model):
    challenge = models.ManyToManyField(Challenge,related_name='challenge')
    contestName = models.CharField('contestName', max_length=200)
    organizer = models.CharField('organizer', max_length=200)
    TYPE_CHOICES = (
        ('Hackathon', 'HACKATHON'),
        ('Competitive', 'COMPETITIVE'),
    )
    contestType = models.CharField(max_length=12, choices=TYPE_CHOICES, default='Hackathon')
    startingDateTime = models.DateTimeField('startingDateTime', default=now, editable=True)
    endingDateTime = models.DateTimeField('endingDateTime', default=now, editable=True)
    description=models.TextField('description')
    prizes=models.TextField('prizes')
    rules=models.TextField('rules')
    scoring=models.TextField('scoring')
    def __str__(self):
        return self.contestName


class TestCase(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE)
    testcaseName=models.CharField('testcaseName',max_length=20)
    explanation=models.TextField('explanation')
    input=models.TextField('input')
    output=models.TextField('output')
    score=models.PositiveIntegerField('score')

    def __str__(self):
        return self.testcaseName

class ChallengeLeaderboard(models.Model):
    user=models.CharField('user',max_length=20)
    contest=models.CharField('contest',max_length=20)
    challenge = models.CharField('challenge', max_length=20)
    status=models.CharField('status',max_length=20)
    score=models.CharField('score',max_length=20)
    def __str__(self):
        return self.challenge