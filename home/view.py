from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context,loader
from home.forms import UserForm, OnlineContest, TestCase
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import OnlineContest, CampusContest,Challenge,TestCase,ChallengeLeaderboard
import filecmp
import datetime
from datetime import datetime
import time
import pytz
import subprocess
import os
from datetime import date
import datetime as dt

import CCMS


def challengeLeaderboard(request, challenge):
    challenges=ChallengeLeaderboard.objects.filter(challenge=challenge)
    template = loader.get_template('home/challengeLeaderboard.html')
    context = {'challenges': challenges}
    return HttpResponse(template.render(context, request))

def contestLeaderboard(request, contest):
    contests=ChallengeLeaderboard.objects.filter(contest=contest)
    template = loader.get_template('home/contestLeaderboard.html')
    context = {'contests': contests}
    return HttpResponse(template.render(context, request))

def challenge(request,Id):
    contest = CampusContest.objects.get(pk=Id)
    template = loader.get_template('home/challenge.html')
    context = {
        'contest': contest,
            }
    return HttpResponse(template.render(context,request))

def challengePage(request,contest,cid):
    challenge=Challenge.objects.get(pk=cid)
    template=loader.get_template('home/challengePage.html')
    context={'challenge':challenge,'contest':contest}
    return HttpResponse(template.render(context,request))

def index(request):
    return render(request,'home/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            return render(request, 'home/login.html',{'user_form': user_form})
        else:
            print(user_form.errors)
            return render(request, 'home/registration.html',
                          {'user_form': user_form})
    else:
        user_form = UserForm()
        return render(request,'home/registration.html',
                          {'user_form':user_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'home/login.html', {})

def online(request):
    all_contests = OnlineContest.objects.all()
    context = {
        'all_contests': all_contests
    }
    return render(request, 'home/online.html',context)

def campus(request):
    all_contests = CampusContest.objects.all()
    context = {
        'all_contests': all_contests
    }
    return render(request, 'home/campus.html', context)

def campus_contest(request,CampusContest_id):

    contest=get_object_or_404(CampusContest,pk=CampusContest_id)
    return render(request,'home/campus_contest.html',{'CampusContest_id':contest})



def storefile(request, user, contest, challenge):
    if request.method=='POST':
        language = request.POST.get("language")
        code = request.POST.get("editor")
        Path = "/home/lokeshchenu/CCMS/files/" + user + "/" + contest + "/" + challenge + "/"
        extension = ""
        if (language == "C"):
            extension = ".c"
        elif (language == "C++"):
            extension = ".cpp"
        elif language == "Python":
            extension = ".py"
        contest_name = contest.replace(" ", "_")
        actual_filename=Path + user + "_" + contest_name + extension
        try:
            os.makedirs(Path)
            f = request.FILES['file']
            with open(actual_filename, "wb") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        except:
            filename = actual_filename
            f1 = open(filename, "w")
            f1.write(code)
            f1.close()
        path = Path + user + "_" + contest
        testcases = {}
        if (language == "C"):
            command = "gcc -o "+user+"_"+contest+"_"+language+" "+user+"_"+contest+extension
            proc = subprocess.Popen("cd 'files/" +user+"/"+contest+"/"+challenge+"' && "+command, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            err = proc.stderr.read()
            if (err != ""):
                return HttpResponse(err)
            else:
                testcases = TestCase.objects.filter(challenge__challengeName=challenge)
                for testcase in testcases:
                    inp=testcase.input
                    out=testcase.output
                    Id=testcase.id
                    f1 = open(Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt", "w")
                    f1.write(inp)
                    f1.close()
                    f2 = open(Path + user + "_" + contest_name + language + "test_output" + str(Id) + ".txt", "w")
                    f2.write(out)
                    f2.close()

                    f1 = open(Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt", "r")
                    proc = subprocess.Popen("cd files/" +user+"/"+contest+"/"+challenge+" && ./" + user + "_" + contest_name + "_" + language,
                        shell=True, stdin=f1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True
                    )
                    f1.close()
                    output = str(proc.stdout.read())
                    fd1 = open(
                        Path + user + "_" + contest_name + "_" + language + "_user_output" + str(Id) + ".txt", "w")
                    fd1.write(output)
                    fd1.close()

        elif (language == "C++"):
            command = "g++ -o "+user+"_"+contest+"_"+language+" "+user+"_"+contest+extension
            proc = subprocess.Popen("cd 'files/" +user+"/"+contest+"/"+challenge+"' && "+command, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            err = proc.stderr.read()
            if (err != ""):
                return HttpResponse(err)
            else:
                testcases = TestCase.objects.filter(challenge__challengeName=challenge)
                for testcase in testcases:
                    inp=testcase.input
                    out=testcase.output
                    Id=testcase.id
                    f1 = open(Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt", "w")
                    f1.write(inp)
                    f1.close()
                    f2 = open(Path + user + "_" + contest_name + language + "test_output" + str(Id) + ".txt", "w")
                    f2.write(out)
                    f2.close()
                    f1 = open(Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt", "r")
                    proc = subprocess.Popen("cd files/" +user+"/"+contest+"/"+challenge+" && ./" + user + "_" + contest_name + "_" + language,
                        shell=True, stdin=f1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True
                    )
                    f1.close()
                    output = str(proc.stdout.read())
                    fd1 = open(
                        Path + user + "_" + contest_name + "_" + language + "_user_output" + str(Id) + ".txt", "w")
                    fd1.write(output)
                    fd1.close()
        elif (language == "Python"):
            testcases = TestCase.objects.filter(challenge__challengeName=challenge)
            err = ""
            proc = subprocess.Popen("cd 'files/" +user+"/"+contest+"/"+challenge+"'", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            for testcase in testcases:
                Id = testcase.id
                inp = testcase.input
                out=testcase.output
                f1 = open(Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt", "w")
                f1.write(inp)
                f1.close()
                f2 = open(Path + user + "_" + contest_name + language + "test_output" + str(Id) + ".txt", "w")
                f2.write(out)
                f2.close()
                f1 = open(Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt", "r")

                command ="cd 'files/" +user+"/"+contest+"/"+challenge+"' && python3 " + user + "_" + contest_name + extension + " < " + Path + user + "_" + contest_name + language + "test_input" + str(Id) + ".txt"
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
                f1.close()
                output = str(proc.stdout.read())
                err = proc.stderr.read()
                if (err != ""):
                    break
                fd1 = open(Path + user + "_" + contest_name + "_" + language + "_user_output" + str(Id) + ".txt", "w")
                fd1.write(output)
                fd1.close()
            if (err != ""):
                return HttpResponse(err)

        status = "Correct Answer"
        score = 0
        for testcase in testcases:
            Id = testcase.id
            f1 = open(Path + user + "_" + contest_name + language + "test_output" + str(Id) + ".txt", "r")
            a1 = f1.read()
            f1.close()
            f2 = open(Path + user + "_" + contest_name + "_" + language + "_user_output" + str(Id) + ".txt", "r")
            a2 = f2.read()
            f2.close()
            if(a1==a2 or a1==a2[0:-1]):
                score = score + testcase.score
            else:
                status = "Wrong Answer"
        try:
            r=ChallengeLeaderboard.objects.get(user=user)
        except:
            r=ChallengeLeaderboard()
        r.user=user
        r.contest=contest
        r.challenge=challenge
        r.status=status
        r.score=score
        r.save()
        return HttpResponse("Score:"+str(score)+"   Status:"+str(status))

