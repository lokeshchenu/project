from django import forms
import multiselectfield
from multiselectfield import MultiSelectField
from home.models import OnlineContest, CampusContest, Challenge, TestCase,ChallengeLeaderboard
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class OnlineContest(forms.ModelForm):
    contestName=forms.CharField(widget=forms.CharField)
    class Meta():
        model=OnlineContest
        fields=('contestLink','contestType','startingDateTime','endingDateTime')

class CampusContest(forms.ModelForm):
    contestName=forms.CharField(widget=forms.CharField)
    class Meta():
        model=CampusContest
        fields=('organizer','contestType','startingDateTime','endingDateTime','description','prizes','rules','scoring')

class Challenge(forms.ModelForm):
    challengeName=forms.CharField(widget=forms.CharField)
    class Meta():
        model=Challenge
        fields=('createdBy','challengeType','problemStatement','inputFormat','constraints','outputFormat','approach','problemSolution','languages','Score')

class TestCase(forms.ModelForm):
    name=forms.CharField(widget=forms.CharField)
    class Meta():
        model=TestCase
        fields=('testcaseName','explanation','input','output','score')

class ChallengeLeaderboard(forms.ModelForm):
    user=forms.CharField(widget=forms.CharField)
    class Meta():
        model=ChallengeLeaderboard
        fields=('contest','challenge','status','score')
