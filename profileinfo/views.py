from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm #import django form
from django.contrib.auth.models import User#help to create user object quickly
#this is user model we would be working with
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate#to make user login after signup
from .forms import profileForm
from .forms import messagemeForm
from .forms import seeprofileForm
from .models import profileModel
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def updateprofile(request):

    if request.method =="GET": #when user first visit form show the form
                return render(request,"profileinfo/updateProfile.html",{'form':profileForm(),"us":request.user})


    else:
        try:
               #if length is not large we send save it
               #when he click submit
               #fetch information from post request

                    #form=profileForm(request.POST,request.FILES)



                    form=profileForm(request.POST,request.FILES)

                    #newprofile=form.save(commit=False)
                    #form=profileForm(request.POST)
                    #whatever user sent in post method we cnvert it to TodoForm form ie form
                    newprofile=form.save(commit=False) #commit =False means donot unnecessarily save it into database
                    if request.user.is_authenticated:
                           #newtodo.user_new=request.user
                           #in newtodo user field is missing
                           newprofile.name=request.user
                    person, created = profileModel.objects.get_or_create(name=request.user)
                    #person2, created2 = User.objects.get_or_create(username=request.user)
                    if created:
                        # means you have created a new person
                        #newprofile.save()
                        #newprofile.save()
                        if newprofile.name:
                             person.name=newprofile.name
                        if newprofile.Fullname:
                            person.Fullname=newprofile.Fullname
                        if newprofile.email:
                             person.email=newprofile.email
                             #person2.email=newprofile.email
                        if newprofile.address:
                             person.address=newprofile.address
                        if newprofile.image:
                             person.image=newprofile.image
                        if newprofile.about:
                             person.about=newprofile.about
                        if newprofile.mobile:
                             person.mobile=newprofile.mobile
                        if newprofile.resume:
                             person.resume=newprofile.resume
                        if newprofile.dob:
                             person.dob=newprofile.dob
                        #person=newprofile
                        person.save()
                        #person2.save()
                        messages.success(request,"your profile is upto date")
                        return redirect('newfeeds')
                        #person.save()
                    else:
                      # person just refers to the existing one
                      if newprofile.name:
                          person.name=newprofile.name
                      if newprofile.Fullname:
                          person.Fullname=newprofile.Fullname
                      if newprofile.email:
                          person.email=newprofile.email
                      if newprofile.address:
                          person.address=newprofile.address
                      if newprofile.image:
                          person.image=newprofile.image
                      if newprofile.about:
                          person.about=newprofile.about
                      if newprofile.mobile:
                          person.mobile=newprofile.mobile
                      if newprofile.resume:
                          person.resume=newprofile.resume
                      if newprofile.dob:
                          person.dob=newprofile.dob
                       #person=newprofile
                      person.save()
                      messages.success(request,"your profile is upto date")
                      return redirect('newfeeds')

        except ValueError:
                #if length of title is long we send back to same page otherwise we will get error
                        return render(request,"profileinfo/updateProfile.html",{'form':profileForm(),"error":"bad data"})

@login_required
def viewprofile(request,id1): #it takes back request and also primary key
    #newprofile=get_object_or_404(profileModel,title=profile_pk)
    try:
        #newprofile=profileModel.objects.filter(name=name1)
        user1=User.objects.get(pk=id1)
        newprofile=profileModel.objects.filter(name=user1)
        if newprofile.count()==0:
            return render(request,"profileinfo/updateProfile.html",{'form':profileForm(),"error":"you have not filled your profile . Please update your profile from update profile"})

        return render(request,"profileinfo/seeProfile.html",{"profile":newprofile,"user1":user1,"id1":id1})

    except :
         return render(request,"profileinfo/seeProfile.html",{"error":"you have not filled your profile . Please update your profile by providing your details"})




@login_required
def seeprofile(request): #it takes back request and also primary key
    #newprofile=get_object_or_404(profileModel,title=profile_pk)
    if request.method =="GET": #when user first visit form show the form
                return render(request,"profileinfo/findprofile.html",{'form':seeprofileForm()})
    else:
          if User.objects.filter(username=request.POST['username']).exists():

                  #try:
                        user1=User.objects.filter(username=request.POST['username'])
                        oneuser=user1[0]
                        newprofile=profileModel.objects.filter(name=oneuser)


                        #message option start
                        """
                        form=messagemeForm(request.POST)

                        #whatever user sent in post method we cnvert it to TodoForm form ie form
                        newmessage=form.save(commit=False) #commit =False means donot unnecessarily save it into database

                        #user1=User.objects.get(pk=id1)
                        newmessage.receiver=oneuser.username
                        newmessage.sender=request.user#sende is sender
                        newmessage.date1=timezone.now()
                        newmessage.save()#now it put it in database

                        #return redirect('viewmessage')
                        #els

                        #message option end
                        """
                        return render(request,"profileinfo/seeProfile.html",{"profile":newprofile,'form2':messagemeForm(),"user1":oneuser})
                  #except :
                        #return render(request,"profileinfo/findprofile.html",{'form':seeprofileForm(),"error":"user has not fileed his form"})
          else:

                  messages.success(request,"user has not created his account with this name")

                  return render(request,"profileinfo/findprofile.html",{'form':seeprofileForm()})



@login_required
def sendmessage(request):
               return redirect('chooseuser')


@login_required
def sendmemessage(request,id1):
    #if request.method =="GET": #when user first visit form show the form
        #return render(request,"messenger/sendmessage.html",{'form':messagemeForm()})


        try:
               #if length is not large we send save it
               #when he click submit
               #fetch information from post request
                #if User.objects.filter(username=request.POST['receiver']).exists():
                    form=messagemeForm(request.POST)

                    #whatever user sent in post method we cnvert it to TodoForm form ie form
                    newmessage=form.save(commit=False) #commit =False means donot unnecessarily save it into database
                    #in newtodo user field is missing
                    user1=User.objects.get(pk=id1)
                    newmessage.receiver=user1.username
                    newmessage.sender=request.user#sende is sender
                    newmessage.date1=timezone.now()
                    newmessage.save()#now it put it in database
                    #after saving  this we want to send them to current page so that they can see current to do
                    return redirect('viewmessage')
                #else:
                    #return render(request,"messenger/sendmessage.html",{'form':messageForm(),"error":"Receiver donot exist currently.  Message sending failed! Try again with receiver name that exist."})

        except ValueError:
               return redirect('chooseuser')


"""
@login_required
def messageme(request,todo_pk): #it takes back request and also primary key
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
     #grab a todo from datbase as we know primary key and classs
     #user is passec as someone else couldnot modify only creator can modify it
    if request.method =='GET':
        form=TodoForm(instance=todo)  # we need to pass in todo object inside TodoForm
        #rather than passing empty form we pass todo object inside form
        return render(request,'todo/viewtodo.html',{'todo':todo,"form":form}) #pass in form
        #we need to display todo form filled in with information
    else:
        #take form data and save it in database
        #if someone save informatio it sending post back to save page
        try:
            form=TodoForm(request.POST,instance=todo)# we pass todo help to determine it is existing object we are updating
            # rather than empty form we pass to do object
            form.save()#if someone save data redirect to currenttodod
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,"form":form,"error":"BAD Info"})
"""










        #return render(request,"profileinfo/updateProfile.html",{'form':profileForm(),"error":"Enter your details first","id1":id1})

     #grab a todo from datbase as we know primary key and classs
     #user is passec as someone else couldnot modify only creator can modify it
"""
    if request.method =='GET':
        form=TodoForm(instance=todo)  # we need to pass in todo object inside TodoForm
        #rather than passing empty form we pass todo object inside form
        return render(request,'todo/viewtodo.html',{'todo':todo,"form":form}) #pass in form
        #we need to display todo form filled in with information
    else:
        #take form data and save it in database
        #if someone save informatio it sending post back to save page
        try:
            form=TodoForm(request.POST,instance=todo)# we pass todo help to determine it is existing object we are updating
            # rather than empty form we pass to do object
            form.save()#if someone save data redirect to currenttodod
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,"form":form,"error":"BAD Info"})
   """