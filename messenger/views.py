from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm #import django form
from django.contrib.auth.models import User#help to create user object quickly
#this is user model we would be working with
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate#to make user login after signup
from .forms import messageForm
from .models import messageModel
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
@login_required
def chooseuser(request):


        alluser=User.objects.all().order_by('username')

        return render(request,"messenger/choseusertosendmessage.html",{"alluser":alluser,"messageany":"Select user to whom you want to send message"})

@login_required
def sendmessage(request,usern):
    return render(request,"posts/signupuser.html",{'form':messageForm(),"usern":usern})


@login_required
def sendmessageto(request,usern):
    if request.method =="GET": #when user first visit form show the form


        u1 = request.user
        user2=User.objects.filter(username=usern)
        oneuser=user2[0]

        mylist=messageModel.objects.filter(receiver=u1,sender=oneuser).order_by("-date1")|messageModel.objects.filter(receiver=usern,sender=u1).order_by("-date1")

        return render(request,"messenger/sendmessage.html",{"mylist":mylist,'form':messageForm(),"usern":usern})

    else:
        #try:
               #if length is not large we send save it
               #when he click submit
               #fetch information from post request
                if User.objects.filter(username=usern).exists():
                    form=messageForm(request.POST)
                    #whatever user sent in post method we cnvert it to TodoForm form ie form
                    newmessage=form.save(commit=False) #commit =False means donot unnecessarily save it into database
                    #in newtodo user field is missing
                    newmessage.sender=request.user#sende is sender
                    newmessage.receiver=usern
                    newmessage.date1=timezone.now()
                    newmessage.save()#now it put it in database
                    #after saving  this we want to send them to current page so that they can see current to do
                    #redirecting to same page
                    u1 = request.user
                    user2=User.objects.filter(username=usern)
                    oneuser=user2[0]

                    mylist=messageModel.objects.filter(receiver=u1,sender=oneuser).order_by("-date1")|messageModel.objects.filter(receiver=usern,sender=u1).order_by("-date1")
                    messages.success(request, 'your message sent!')
                    return render(request,"messenger/sendmessage.html",{"mylist":mylist,'form':messageForm(),"usern":usern})



                    #return redirect('viewmessage')
                else:
                    return render(request,"messenger/sendmessage.html",{'form':messageForm(),"usern":usern,"error":"Receiver donot exist currently.  Message sending failed! Try again with receiver name that exist."})

        #except ValueError:
               #return redirect('sendmessage')
                #if length of title is long we send back to same page otherwise we will get error


        #if length of title is long we send back to same page otherwise we will get error
"""
@login_required
def receivedmessage(request):
    messages=messageModel.objects.filter(receiver=User.username).order_by("-date1")
    #messages=messageModel.objects.all().order_by("-date1")#if we apply .all then for person everyon to do list will be shown
    return render(request,'messenger/messageview.html',{'messages':messages,"r1":User.username})
    #request.user.username is way to acess this person logged in logged in
@login_required
def sentmessage(request):
    #messages=messageModel.objects.all().order_by("-date1")
    messages=messageModel.objects.filter(sender=request.user).order_by("-date1")#if we apply .all then for person everyon to do list will be shown
    return render(request,'messenger/messageview.html',{'messages':messages})
"""
@login_required
def viewmessage(request):
    #messages=messageModel.objects.all().order_by("-date1")
    #u1=takeuser(r1)
    u1 = request.user
    mylist=messageModel.objects.filter(receiver=u1).order_by("-date1")|messageModel.objects.filter(sender=request.user).order_by("-date1")
    return render(request,'messenger/messageview.html',{"mylist":mylist,"messageany":"you can reply to person/send anothermessage to person by clicking on message"})
"""
@login_required
def viewmessage(request):
    #messages=messageModel.objects.all().order_by("-date1")
    #u1=takeuser(r1)
    u1 = request.user
    messagesrec=messageModel.objects.filter(receiver=u1).order_by("-date1")

    messagessent=messageModel.objects.filter(sender=request.user).order_by("-date1")#if we apply .all then for person everyon to do list will be shown
    l=[]
    l1=messagesrec.count()
    l2=messagessent.count()

    l3=min(l1,l2)
    i=0
    while i<l3:
      l.append(messagesrec[i])
      l.append(messagessent[i])
      #pass
      i+=1
    if l1>l2:
      while i<l1:
        l.append(messagesrec[i])
        i+=1
    else:
      while i<l2:
        l.append(messagessent[i])
        i+=1
    mylist= l
    return render(request,'messenger/messageview.html',{"mylist":mylist})
    #{'messagessent':messagessent,'messagesrec':messagesrec,}
"""
