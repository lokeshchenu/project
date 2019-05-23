from django.contrib import admin
from home.models import UserProfileInfo, User, OnlineContest, CampusContest ,Challenge,TestCase,ChallengeLeaderboard

# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(OnlineContest)
admin.site.register(CampusContest)
admin.site.register(Challenge)
admin.site.register(TestCase)
admin.site.register(ChallengeLeaderboard)