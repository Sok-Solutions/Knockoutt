

import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .models import questions, koo, questionshot, gamesss, casuall, duelll
import random as rd
import string
import json
import pyrebase
import random
from django.http import HttpResponseRedirect



"""INITIALIZE FIREBASE"""
config={
    "apiKey": "AIzaSyDkTGod3Yh0fSlBPGPkdyLbxmYt0fZw9Rw",
    "authDomain": "knockout-2afbe.firebaseapp.com",
    "databaseURL": "https://knockout-2afbe-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "knockout-2afbe",
    "storageBucket": "knockout-2afbe.appspot.com",
    "messagingSenderId": "85603705850",
    "appId": "1:85603705850:web:88799d48ecc53bdb6b7a43",
    "measurementId": "G-VJDQDM84WW"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()



# Create your views here.
def warn(request):
    request.session['warning'] = 1
    print('warning was accepted!')
    return render(request, 'warn.html')
def firebase(request):
    channel_name = database.child('Data').child('Name').get().val()
    channel_city = database.child('Data').child('City').get().val()
    channel_age = database.child('Data').child('Age').get().val()
    return render(request, 'firebase.html', {
        "channel_name" : channel_name,
        "channel_age" : channel_age,
        "channel_city" : channel_city
    })

def postsignup(request):
    password2 = request.POST.get('password2')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if password == password2:
        if len(password) < 6:
                errormsg = "Das Passwort muss länger als 6 Zeichen sein!"
                return render(request, 'register.html', {'err' : errormsg})
        else:
            user = auth.create_user_with_email_and_password(email, password)
            return render(request, 'account/login.html')
    else:
        errormsg = "Die Passwörter stimmen nicht überein!"
        return render(request, 'register.html', {'err' : errormsg})

    
def startt(request):
    print("Logged in with google!")
    return redirect("/start/")

def postsigin(request):
    
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = auth.sign_in_with_email_and_password(email, password)
    request.session['idToken'] = user['idToken']
    return redirect("/start/")
def play(request):
    print("Started playing")
    quests = None
    if request.session['gamemode'] == "hot":
        quests = questionshot.objects.all()
        print("hot")
    if request.session['gamemode'] == "normal":
        print("normal")
        quests = questions.objects.all()
    if request.session['gamemode'] == "duell":
        print("normal")
        quests = duelll.objects.all()  
    if request.session['gamemode'] == "ko":
        print("normal")
        quests = koo.objects.all()
    if request.session['gamemode'] == "casual":
        print("normal")
        quests = casuall.objects.all()
    names = gamesss.objects.filter(gameid = request.session['gameid'])
    rand_questforweb = []
    i = 0
    while i < len(quests):
        rand_questforweb.append(i)
        i = i+1
    print("RANDOMQUESTS:")
    print(rand_questforweb)
    rand_questforweb = random.sample(list(rand_questforweb), len(rand_questforweb))
    
    print("RANDOMQUESTS:")
    print(rand_questforweb)
    print("LAENGE" + str(len(quests)))
    questforweb = []
    rq = rand_questforweb
    i = 0
    while i < (len(quests)):
        print("ASJDHLKAJSDHAKLSHD" + str(i))
        print("Withname: " + str(quests[rq[i]].withname))
        if quests[rq[i]].withname == True:
            st = random.randint(0, (len(names)-1))
            st2 = random.randint(0, (len(names)-1))
            while st2 == st:
                st2 = random.randint(0, (len(names)-1))
            print("st1:" + str(st) + " st2: " + str(st2))
            name1 = names[int(st)].name
            name2 = names[int(st2)].name
            if str(quests[rq[i]].question).count("#") == 1:
                if str(quests[rq[i]].question).count("§") == 1:
                    zwischen = quests[rq[i]].question.replace("#", name1)
                    print("ZWISCHEN1" + zwischen)
                    zwischen = zwischen.replace("§", name2)
                    print("ZWISCHEN1" + zwischen)
                    questforweb.append([zwischen, i]) 
                    print("Hallo")
                else:
                    zwischen = quests[rq[i]].question.replace("#", names[int(st)].name)
                    print(zwischen)
                    questforweb.append([zwischen, i]) 
        if quests[rq[i]].withname == False:
            print(quests[rq[i]].question)
            questforweb.append([quests[rq[i]].question, i])
        i = i+1
    print("QUESTSFORWEB:")
    print(questforweb)
    last = len(questforweb)
    print(last)
    return render(request, 'play.html', {'quests' : questforweb, 'last' : last})
def hot(request):
    request.session['gamemode'] = "hot"
    request.session.modified = True
    print("1" + request.session['gamemode'])
    print("Game started!")
    if request.method == 'POST':
        print('Received data:', request.POST['Name'])
        gameidd = ''
        if request.session['gameid'] == 'a':
            gameidd = ''.join(random.choice(string.ascii_lowercase) for i in range(100))
        else:
            gameidd = request.session['gameid']
        gamesss.objects.create(gameid = gameidd, userid = request.user, name = request.POST['Name'])
        #database.child("Data").child("Games").push({"gameid" : gameidd})
        request.session['gameid'] = gameidd
    have_names = False

    all_names = gamesss.objects.filter(gameid = request.session['gameid'])
    if len(all_names) > 0:
        have_names = True
        print("Game REady")
    return render(request, 'hot.html', {'all_names' : all_names, 'have_names' : json.dumps(have_names)})
def ko(request):
    request.session['gamemode'] = "ko"
    request.session.modified = True
    print("1" + request.session['gamemode'])
    print("Game started!")
    
    if request.method == 'POST':
        print('Received data:', request.POST['Name'])
        gameidd = request.session['gameid']
        gamesss.objects.create(gameid = gameidd, userid = request.user, name = request.POST['Name'])
        #database.child("Data").child("Games").push({"gameid" : gameidd})
        request.session['gameid'] = gameidd
    have_names = False

    all_names = gamesss.objects.filter(gameid = request.session['gameid'])
    if len(all_names) > 0:
        have_names = True
        print("Game REady")
    return render(request, 'ko.html', {'all_names' : all_names, 'have_names' : json.dumps(have_names)})
def duell(request):
    request.session['gamemode'] = "duell"
    request.session.modified = True
    print("1" + request.session['gamemode'])
    print("Game started!")
    if request.method == 'POST':
        print('Received data:', request.POST['Name'])
        gameidd = ''
        if request.session['gameid'] == 'a':
            gameidd = ''.join(random.choice(string.ascii_lowercase) for i in range(100))
        else:
            gameidd = request.session['gameid']
        gamesss.objects.create(gameid = gameidd, userid = request.user, name = request.POST['Name'])
        #database.child("Data").child("Games").push({"gameid" : gameidd})
        request.session['gameid'] = gameidd
    have_names = False

    all_names = gamesss.objects.filter(gameid = request.session['gameid'])
    if len(all_names) > 0:
        have_names = True
        print("Game REady")
    return render(request, 'duell.html', {'all_names' : all_names, 'have_names' : json.dumps(have_names)})
def casual(request):
    request.session['gamemode'] = "casual"
    request.session.modified = True
    print("1" + request.session['gamemode'])
    print("Game started!")
    if request.method == 'POST':
        print('Received data:', request.POST['Name'])
        gameidd = ''
        if request.session['gameid'] == 'a':
            gameidd = ''.join(random.choice(string.ascii_lowercase) for i in range(100))
        else:
            gameidd = request.session['gameid']
        gamesss.objects.create(gameid = gameidd, userid = request.user, name = request.POST['Name'])
        #database.child("Data").child("Games").push({"gameid" : gameidd})
        request.session['gameid'] = gameidd
    have_names = False

    all_names = gamesss.objects.filter(gameid = request.session['gameid'])
    if len(all_names) > 0:
        have_names = True
        print("Game REady")
    return render(request, 'casual.html', {'all_names' : all_names, 'have_names' : json.dumps(have_names)})
def game(request):
    request.session['gamemode'] = "normal"
    request.session.modified = True
    print("Game started!")
    if request.method == 'POST':
        print('Received data:', request.POST['Name'])
        gameidd = ''
        if request.session['gameid'] == 'a':
            gameidd = ''.join(random.choice(string.ascii_lowercase) for i in range(100))
        else:
            gameidd = request.session['gameid']
        gamesss.objects.create(gameid = gameidd, userid = request.user, name = request.POST['Name'])
        #database.child("Data").child("Games").push({"gameid" : gameidd})
        request.session['gameid'] = gameidd
    have_names = False

    all_names = gamesss.objects.filter(gameid = request.session['gameid'])
    if len(all_names) > 0:
        have_names = True
        print("Game REady")
    return render(request, 'game.html', {'all_names' : all_names, 'have_names' : json.dumps(have_names)})
def start(request):
    users = database.child("users").get()
    print(users.val())
    request.session['gameid']='a'

    if request.method == 'POST':

        numofq = request.POST.get('numofq')
        request.session['numofquest'] = numofq
        request.session['gameid'] = ''.join(random.choice(string.ascii_lowercase) for i in range(100))
        print("hallo" + str(numofq))
    #user = request.session['idToken']
    #print((auth.get_account_info(user)))
    return render(request, 'index.html')

def loginpage(request):
    context = {
        'errmsg' : ''
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('succ')
            login(request, user) 
            return redirect('/start/')
        else:
            context = {
        'errmsg' : 'Password and/or Username wrong!'
    }
            print('notsucc')
    
            


    return render(request, 'login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('/accounts/login/')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/accounts//login/')

    context = {'form' :form}
    return render(request, 'register.html', context)

def gamechoice(request):
    return render(request, 'gamechoice.html')
def addName(request):
    if request.POST['contentko'] != "":
        name = request.POST['contentko']
        gameidd = request.session['gameid']
        if name == "":
            print("NAME IS EMPTY")
        else:
            gamesss.objects.create(gameid = gameidd, userid = request.user, name = name)
        return HttpResponseRedirect('/ko/')
def addNameCasual(request):
    if request.POST['contentko'] != "":
        name = request.POST['contentko']
        gameidd = request.session['gameid']
        if name == "":
            print("NAME IS EMPTY")
        else:
            gamesss.objects.create(gameid = gameidd, userid = request.user, name = name)
        return HttpResponseRedirect('/casual/')   
def addNameDuell(request):
    if request.POST['contentko'] != "":
        name = request.POST['contentko']
        gameidd = request.session['gameid']
        if name == "":
            print("NAME IS EMPTY")
        else:
            gamesss.objects.create(gameid = gameidd, userid = request.user, name = name)
        return HttpResponseRedirect('/duell/')   
def addNameNormal(request):
    if request.POST['contentko'] != "":
        name = request.POST['contentko']
        gameidd = request.session['gameid']
        if name == "":
            print("NAME IS EMPTY")
        else:
            gamesss.objects.create(gameid = gameidd, userid = request.user, name = name)
        return HttpResponseRedirect('/game/')   
def addNameHot(request):
    if request.POST['contentko'] != "":
        name = request.POST['contentko']
        gameidd = request.session['gameid']
        if name == "":
            print("NAME IS EMPTY")
        else:
            gamesss.objects.create(gameid = gameidd, userid = request.user, name = name)
        return HttpResponseRedirect('/hot/')   

def deleteTodoView(request, i):
    y = gamesss.objects.get(id= i)
    y.delete()
    return HttpResponseRedirect('/game/') 
def deleteTodoViewCasual(request, i):
    y = gamesss.objects.get(id= i)
    y.delete()
    return HttpResponseRedirect('/casual/')
def deleteTodoViewDuell(request, i):
    y = gamesss.objects.get(id= i)
    y.delete()
    return HttpResponseRedirect('/duell/')
def deleteTodoViewHot(request, i):
    y = gamesss.objects.get(id= i)
    y.delete()
    return HttpResponseRedirect('/hot/')   
def deleteTodoViewKo(request, i):
    y = gamesss.objects.get(id= i)
    y.delete()
    return HttpResponseRedirect('/ko/') 

