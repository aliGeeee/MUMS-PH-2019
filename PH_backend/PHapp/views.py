from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.models import User
from django.forms import formset_factory, ValidationError
from .models import Puzzles, Teams, SubmittedGuesses, Individuals
from .forms import SolveForm, TeamRegForm, IndivRegForm, IndivRegFormSet, LoginForm
from django.conf import settings
import json
import datetime
import pytz
import random
import os
from .helperFunctions import *

aest = pytz.timezone("Australia/Melbourne")

#releaseTimes = [aest.localize(datetime.datetime(2019, 4, 24, 12)) + datetime.timedelta(days=i) for i in range(10)]
releaseTimes = [aest.localize(datetime.datetime(2019, 3, 1, 12)) + datetime.timedelta(days=i) for i in range(10)]

def index(request):
	huntOver = False if releaseStage(releaseTimes) < len(releaseTimes) else True
	return render(request, 'PHapp/home.html', {'huntOver':huntOver})

@login_required
def puzzles(request):
	puzzleList = []
	for puzzle in Puzzles.objects.filter(releaseStatus__lte = releaseStage(releaseTimes)):
		allGuesses = [i.correct for i in SubmittedGuesses.objects.filter(puzzle=puzzle)]
		if len(SubmittedGuesses.objects.filter(puzzle=puzzle, team=request.user, correct=True)) == 0:
			puzzleList.append([puzzle, False, sum(allGuesses), len(allGuesses)-sum(allGuesses), calcWorth(puzzle, releaseTimes)])
		else:
			puzzleList.append([puzzle, True, sum(allGuesses), len(allGuesses)-sum(allGuesses), calcWorth(puzzle, releaseTimes)])
	puzzleList = sorted(puzzleList, key=lambda x:x[0].id)
	return render(request, 'PHapp/puzzles.html', {'puzzleList':puzzleList})

@login_required
def puzzleInfo(request, title):
	try:
		puzzle = Puzzles.objects.get(pdfPath=title)
	except:
		raise Http404()
	if releaseStage(releaseTimes) < puzzle.releaseStatus:
		raise Http404()

	allGuesses = SubmittedGuesses.objects.filter(puzzle=puzzle)
	allSolves = sorted([[i, calcSingleTime(i, i.submitTime, releaseTimes)[0]] for i in allGuesses if i.correct], key=lambda x:x[0].submitTime)
	
	totalRight = len(allSolves)
	totalWrong = len(allGuesses) - totalRight

	return render(request, 'PHapp/puzzleStats.html', 
		{'puzzle':puzzle, 'allSolves':allSolves, 'totalWrong':totalWrong, 'totalRight':totalRight, 'avTime':calcPuzzleTime(puzzle, releaseTimes)[0]})

@login_required
def showPuzzle(request, puzzleURL):
	try:
		puzzle = Puzzles.objects.get(pdfPath=puzzleURL.replace('.pdf', ''))
	except:
		raise Http404()
	if releaseStage(releaseTimes) < puzzle.releaseStatus:
		raise Http404()
	try:
		return FileResponse(open(os.path.join(settings.BASE_DIR, 'PHapp/puzzleFiles/', puzzleURL), 'rb'), content_type='application/pdf')
	except FileNotFoundError:
		raise Http404("PDF file not found at "+os.path.join(settings.BASE_DIR, 'PHapp/puzzleFiles/', puzzleURL))

@login_required
def solve(request, title):
	try:
		puzzle = Puzzles.objects.get(pdfPath=title)
	except:
		raise Http404()
	if releaseStage(releaseTimes) < puzzle.releaseStatus:
		raise Http404()
	
	team = Teams.objects.get(authClone = request.user)

	if True in [i.correct for i in SubmittedGuesses.objects.filter(team = request.user, puzzle = puzzle)]:
		points = SubmittedGuesses.objects.filter(team=request.user, correct=True, puzzle=puzzle)[0].pointsAwarded
		return render(request, 'PHapp/solveCorrect.html', {'puzzle':puzzle, 'points':points, 'team':team})

	if team.guesses <= 0:
		return render(request, 'PHapp/noGuesses.html')

	if request.method == 'POST':
		solveform = SolveForm(request.POST)
		if solveform.is_valid():
			guess = stripToLetters(solveform.cleaned_data['guess'])
			
			if guess == puzzle.answer:
				newSubmit = SubmittedGuesses()
				newSubmit.team = request.user
				newSubmit.puzzle = puzzle
				newSubmit.guess = guess
				newSubmit.submitTime = datetime.datetime.now()
				newSubmit.correct = True
				newSubmit.pointsAwarded = calcWorth(puzzle, releaseTimes)
				newSubmit.save()

				solveTime = calcSolveTime(team, releaseTimes)
				team.avHr = solveTime[1]
				team.avMin = solveTime[2]
				team.avSec = solveTime[3]
				team.teamPoints += calcWorth(puzzle, releaseTimes)
				team.teamPuzzles += 1
				team.save()

				return redirect('/solve/{}/'.format(title))

			else:
				if len(SubmittedGuesses.objects.filter(guess=guess, puzzle=puzzle, team=team.authClone)) == 0:
					newSubmit = SubmittedGuesses()
					newSubmit.team = request.user
					newSubmit.puzzle = puzzle
					newSubmit.guess = guess
					newSubmit.submitTime = datetime.datetime.now()
					newSubmit.correct = False
					newSubmit.save()
					team.guesses -= 1
					team.save()
					displayWrong = True
					displayDouble = False
					displayGuess = None
				else:
					displayWrong = False
					displayDouble = True
					displayGuess = guess

	else:
		solveform = SolveForm()
		displayWrong = False
		displayDouble = False
		displayGuess = None

	previousGuesses = [i.guess for i in SubmittedGuesses.objects.filter(puzzle=puzzle, team=team.authClone, correct=False)]
	previousGuesses = sorted(previousGuesses)

	return render(request, 'PHapp/solve.html', 
		{'solveform':solveform, 'displayWrong':displayWrong, 'displayDouble':displayDouble, 'displayGuess':displayGuess, 'puzzle':puzzle, 'team':team, 'previousGuesses':previousGuesses})

def teams(request):
	allTeams = []
	totRank = 1
	ausRank = 1

	teamsWithSolves = Teams.objects.filter(teamPoints__gt=0)
	for team in teamsWithSolves:
		allTeams.append([team, "{:02d}h {:02d}m {:02d}s".format(team.avHr, team.avMin, team.avSec), team.avHr, team.avMin, team.avSec])

	allTeams = sorted(allTeams, key=lambda x:x[0].id) #sort by ID
	allTeams = sorted(allTeams, key=lambda x:3600*x[2]+60*x[3]+x[4]) #sort by average solve time
	allTeams = sorted(allTeams, key=lambda x:-x[0].teamPuzzles) #sort by team puzzles
	allTeams = sorted(allTeams, key=lambda x:-x[0].teamPoints) #sort by team points

	for i in range(len(allTeams)):
		allTeams[i].append(totRank)
		totRank += 1
		if allTeams[i][0].aussie:
			allTeams[i].append(ausRank)
			ausRank += 1
		else:
			allTeams[i].append('-')

	teamsWithoutSolves = Teams.objects.filter(teamPoints=0)
	allTeams += sorted([[team, '-', None, None, None, '-', '-'] for team in teamsWithoutSolves], key=lambda x:x[0].id)

	teamName = None
	if request.user.is_authenticated:
		teamName = Teams.objects.get(authClone = request.user).teamName
	
	return render(request, 'PHapp/teams.html', {'allTeams':allTeams, 'teamName':teamName})

def teamReg(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		userForm = UserCreationForm(request.POST)
		regForm = TeamRegForm(request.POST)
		indivFormSet = IndivRegFormSet(request.POST)

		if userForm.is_valid() and indivFormSet.is_valid() and regForm.is_valid():
			userForm.save()

			username = userForm.cleaned_data.get('username')
			raw_password = userForm.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)

			newTeam = regForm.save()
			newTeam.authClone = user
			newTeam.save()
			newTeam.aussie = False
			
			for indivForm in indivFormSet:
				if indivForm.cleaned_data.get('name') == None:
					continue
				newIndiv = Individuals()
				newIndiv.name = indivForm.cleaned_data.get('name')
				newIndiv.email = indivForm.cleaned_data.get('email')
				newIndiv.aussie = indivForm.cleaned_data.get('aussie')
				newIndiv.melb = indivForm.cleaned_data.get('melb')
				newIndiv.team = newTeam
				newIndiv.save()
				if newIndiv.aussie:
					newTeam.aussie = True

			newTeam.save()
			return redirect('/')
	
	else:
		userForm = UserCreationForm()
		regForm = TeamRegForm()
		indivFormSet = IndivRegFormSet()
	return render(request, 'PHapp/teamReg.html', {'userForm':userForm, 'regForm':regForm, 'indivFormSet':indivFormSet})

def teamInfo(request, teamId):
	team = Teams.objects.get(id=teamId)
	membersList = Individuals.objects.filter(team=team)
	correctList = [[i, calcSingleTime(i, i.submitTime, releaseTimes)[0], len(SubmittedGuesses.objects.filter(team=team.authClone, correct=False))] for i in SubmittedGuesses.objects.filter(team=team.authClone, correct=True)]
	correctList = sorted(correctList, key=lambda x:x[0].submitTime)
	anySolves = True if len(correctList) > 0 else False
	avSolveTime = "{:02d}h {:02d}m {:02d}s".format(team.avHr, team.avMin, team.avSec) if anySolves else '-'
	return render(request, 'PHapp/teamInfo.html', {'team':team, 'members':membersList, 'correctList':correctList, 'anySolves':anySolves, 'avSolveTime':avSolveTime})

@login_required
def hints(request, title):
	try:
		puzzle = Puzzles.objects.get(pdfPath=title)
	except:
		raise Http404()
	if releaseStage(releaseTimes) < puzzle.releaseStatus:
		raise Http404()

	toRender = []
	anyHints = False
	nextHint = releaseTimes[puzzle.releaseStatus]
	if releaseStage(releaseTimes) - puzzle.releaseStatus >= 1:
		toRender.append([1, puzzle.hint1])
		anyHints = True
		nextHint = releaseTimes[puzzle.releaseStatus + 1]
	if releaseStage(releaseTimes) - puzzle.releaseStatus >= 2:
		toRender.append([2, puzzle.hint2])
		nextHint = releaseTimes[puzzle.releaseStatus + 2]
	if releaseStage(releaseTimes) - puzzle.releaseStatus >= 3:
		toRender.append([3, puzzle.hint3])
		nextHint = None
	return render(request, 'PHapp/hints.html', {'toRender':toRender, 'anyHints':anyHints, 'nextHint':nextHint, 'puzzle':puzzle})

def faq(request):
	return render(request, 'PHapp/faq.html')

def rules(request):
	return render(request, 'PHapp/rules.html')

def loginCustom(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data.get('username')
			password = loginForm.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			
			if user == None:
				loginForm = LoginForm()
				return render(request, 'PHapp/login.html', {'loginForm':loginForm, 'wrong':True})
			else:
				login(request, user)
				return redirect('/')
	else:
		loginForm = LoginForm()

	return render(request, 'PHapp/login.html', {'loginForm':loginForm, 'wrong':False})

def logoutCustom(request):
	logout(request)
	return redirect('/')