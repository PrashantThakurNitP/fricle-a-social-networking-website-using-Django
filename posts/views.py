
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User#help to create user object quickly
#this is user model we would be working with
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login,logout ,authenticate#to make user login after signup
from .forms import feedsForm,CreateUserForm
from .models import feedsModel,VoteModel,CommentModel
from profileinfo.forms import seeprofileForm
from profileinfo.models import profileModel
from django.shortcuts import render,redirect, get_object_or_404
#import django form

from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import commentForm
from django.contrib import messages

from newsapi import NewsApiClient

import datetime as dt

# Create your views here.
def index(request):
    return render(request, "posts/index.html")

def home(request):

    if request.user.is_authenticated:
        #newprofile=profileModel.objects.filter(name=name1)
        user1=request.user
        newprofile=profileModel.objects.filter(name=user1)
        #newprofile=newprofile[0]
        return render(request,"posts/home.html",{"profile":newprofile,"form":seeprofileForm()})
    else:
        #return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
        return redirect("newfeeds")

    #except :
         #return render(request,"posts/home.html",{"error":"user has not fileed his form"})




        #return render(request,"posts/home.html",{"form":seeprofileForm()})
#changes new


def newfeeds(request):
    orderbylist=['-upvote','-created']
    feeds1=feedsModel.objects.filter(visibility=True).order_by('-created')

    #if we apply .all then for person everyon to do list will be shown

    if request.user.is_authenticated:
            return render(request,"posts/feeds.html",{"feeds":feeds1,"form3":commentForm()})
    else:
            return render(request,"posts/feed_not_logged_in.html",{"feeds":feeds1})

def yourfeeds(request):
    #orderbylist=['-upvote','-created']
    #if we apply .all then for person everyon to do list will be shown

    if request.user.is_authenticated:
            feeds1=feedsModel.objects.filter(user_new=request.user).order_by('-created')
            return render(request,"posts/feeds.html",{"feeds":feeds1,"form3":commentForm()})

    else:
            return redirect('loginuser')

def feeds(request):
    #orderbylist=['-upvote','-created']
    feeds1=feedsModel.objects.filter(visibility=True).order_by('-upvote','-created')
    vote=VoteModel.objects.all()
    if request.user.is_authenticated:
            return render(request,"posts/feeds.html",{"feeds":feeds1,"form3":commentForm()})
    else:
            return render(request,"posts/feed_not_logged_in.html",{"feeds":feeds1})
def one_post(request,postid):
    if request.user.is_authenticated:
         post_obj=feedsModel.objects.get(pk=postid)
         votes_all_obj=VoteModel.objects.filter(post=post_obj)
         comments_all_obj=CommentModel.objects.filter(post=post_obj)
         return render(request,"posts/one_post.html",{"many_users":votes_all_obj,"many_comments":comments_all_obj,"feed":post_obj,"form3":commentForm()})
    else:
        return render(request,"posts/one_post.html",{"many_users":votes_all_obj,"many_comments":comments_all_obj,"feed":post_obj})
@login_required
def nolikesfeed(request):
    #orderbylist=['-upvote','-created']
    feeds1=feedsModel.objects.order_by('-created')#if we apply .all then for person everyon to do list will be shown

    if request.user.is_authenticated  and request.user.id==1:
            return render(request,"posts/invisible_feeds.html",{"feeds":feeds1,"form3":commentForm()})
    else:
            return render(request,"posts/feed_not_logged_in.html",{"feeds":feeds1})
@login_required
def make_visible(request,postid):
    

    if request.method=="POST" and request.user.id==1 :
            feeds1=feedsModel.objects.order_by('-created')
            post_obj=feedsModel.objects.get(pk=postid)
            post_obj.visibility=True
            post_obj.save()
            messages.success(request, 'Post made visible')
            return render(request,"posts/invisible_feeds.html",{"feeds":feeds1,"form3":commentForm()})
    else:
        return redirect('newfeeds')
@login_required
def make_invisible(request,postid):
    

    if request.method=="POST" and request.user.id==1 :
            feeds1=feedsModel.objects.order_by('-created')
            post_obj=feedsModel.objects.get(pk=postid)
            post_obj.visibility=False
            post_obj.save()
            messages.success(request, 'Post made invisible')
            return render(request,"posts/invisible_feeds.html",{"feeds":feeds1,"form3":commentForm()})
    else:
        return redirect('newfeeds')


@login_required
def like(request,postid):
    
    if request.method=="POST" :
            post_obj=feedsModel.objects.get(pk=postid)
        
            if VoteModel.objects.filter(voter=request.user,post=post_obj).exists():
                 newvote=VoteModel.objects.get(voter=request.user,post=post_obj)
                 post_obj.upvote-=1
                 post_obj.save()
                 newvote.delete()

                 messages.success(request, 'you unliked the post!')

            else:
                newvote=VoteModel(post=post_obj,voter=request.user)
                post_obj.upvote+=1
                post_obj.save()
                newvote.save(force_insert=True)
                
                messages.success(request, 'You liked the post!')
            #except:
            #messages.success(request, 'operation cannot be performed')

    return redirect("newfeeds")
@login_required
def comment_post(request,postid):
    #feedsModel.objects.filter(pk=request.pk).update(upvote = upvote+1)
    #obj=get_object_or_404(feedsModel,id=id1,user=request.user_new)

        
        if request.method=="POST" :
            post_obj=feedsModel.objects.get(pk=postid)
        
            
            newcomment=CommentModel(post=post_obj,commentator=request.user,comment=request.POST['comment'])
            newcomment.save(force_insert=True)
            #commentator
                
            messages.success(request, 'You commented on the post!')
        return redirect("newfeeds")
        

@login_required
def upvote(request,id1,up):
    #feedsModel.objects.filter(pk=request.pk).update(upvote = upvote+1)
    #obj=get_object_or_404(feedsModel,id=id1,user=request.user_new)
    if request.method=="POST" and str(request.user.username)==str(up):
        try:
                obj=feedsModel.objects.get(pk=id1)
                sall=str(obj.upvoter)
                s1=str(up)
                if obj.upvoter==None or obj.upvoter==" " or sall=="" or sall==" ":
                    obj.upvote+=1
                    #sall=sall+' '
                    #sall=sall+s1
                    obj.upvoter=s1
                    obj.save()
                    return redirect("feeds")


                else:

                    #sall=str(obj.upvoter)
                    #sall=sall+"?"
                    ulist=sall.split()
                    if s1 in ulist:
                            obj.upvote-=1
                            s2=str(obj.upvoter)

                            s3=s2.replace(s1,'')

                            #sall=sall+s1
                            obj.upvoter=s3
                            messages.success(request, 'you haved unliked the post')

                        #pass
                    else:
                    #upvoterlist=txt.split("{")

                        obj.upvote+=1
                        sall=sall+' '
                        sall=sall+s1
                        obj.upvoter=sall
                        messages.success(request, 'you haved liked the post')

                    obj.save()
                    #s = get_object_or_404(feedsModel,  pk=question_id)
                    #s.upvote+=1
                    #s.save(update_fields=["upvote"])
                    #messages.success(request, 'you haved liked the post')
                    return redirect("feeds")
        except:
                return redirect("feeds")
    else:
        return redirect("feeds")


                    #return render(request,"posts/error.html",{"upvoter":request.user.username,"ulist":ulist})
        #return redirect('feeds')

@login_required
def delete(request,id1):
    #feedsModel.objects.filter(pk=request.pk).update(upvote = upvote+1)
    #obj=get_object_or_404(feedsModel,id=id1,user=request.user_new)
    try:
        obj=feedsModel.objects.get(pk=id1,user_new__id=request.user.id)
        if request.method== 'POST':

            obj.delete()
            #after that we will send user back to current list of items


            messages.success(request, 'Your post deleted succesfully!')
    except:
            messages.success(request, 'Others post cannot be deleted!')


    return redirect('yourfeeds')


# Create your views here.

def logoutuser(request):
    try:
        if request.method=='POST' and request.user.is_authenticated:

                logout(request)
                return redirect('loginuser')
                #return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
                #return render(request,'posts/loginuser.html')#redirect to homepage after logout
        else:
                return redirect('loginuser')
            #return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
            #return render(request,'posts/loginuser.html')

    except:

        #return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
        #return render(request,'posts/loginuser.html')
        return redirect('loginuser')
#new import for signup

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
#end

def signupuser(request):
    if request.user.is_authenticated:
        return redirect('newfeeds')
    if request.method== 'GET' :
        #we need to distinguish betwen when someone do get and post
        #if request method is get we need to return signup page and form like this
        return render(request,"posts/signupuser.html",{'form':CreateUserForm()})
        #anytime someone put url in web and hit eneter then he is guest
        #in that time we get request
        #we need to present webpage only in this case
    else:
        #create new user
        #POST method is always from form
        #when someone fill form and click submit in that case we need to save the
        #user in data base
        # we don't need to create user model
        #there is already the auth app , ie is present in setting
        #hence there is user app already been saved in database
        #********************************************************************
        #when someone has done post to us we need to create that user object

        str1=str(request.POST['username'])
        lst=str1.split()
        flag=False
        for i in str1:
            if i==" ":
                flag=True


        if "noone" in str1.lower() or "chitrang" in str1.lower() or "prashant" in str1.lower():
            return render(request,"posts/signupuser.html",{'form':CreateUserForm(),'error':"username not allowed"})

        elif request.POST['password1']==request.POST['password2'] and len(lst)==1 and flag==False: #
            #first we need to verify first and second password
            #if password match then go and create user object
            try:
                user=User.objects.create_user( username=request.POST['username'], password=request.POST['password1'],email= request.POST['email'] )
                #this is function that django has made which make it easy to create new
                #user object.  Inside this we pass username and password
                #request.POST is like dictionary
                #in user ,name that is going to submit is username , password1  and password2
                #user.save()  #user is object and we need to save it in database
                #new code
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('posts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
                #form1 = CreateUserForm(request.POST)
                #to_email = form1.cleaned_data.get('email')
                to_email=request.POST['email']
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Please confirm your email address to complete the registration')
                return redirect('loginuser')
                #return HttpResponse('Please confirm your email address to complete the registration')

                #end
                """
                login(request,user) #make them login after they sign in
                messages.success(request, str(user)+' your account has been created suceesfully!. Welcome to fricle. Share your detail and upload your nice image!')
                return redirect('updateprofile')

                """
                #return render(request,"posts/home.html",{"form":seeprofileForm()})
                #after sigin we take them them to current page which show current to do page
                #return redirect('home')
            except IntegrityError:

                return render(request,"posts/signupuser.html",{'form':CreateUserForm(),"error":"username already taken"})
        elif len(lst)>1 or flag==True:
            return render(request,"posts/signupuser.html",{'form':CreateUserForm(),'error':"space not allowed in username"})


        else:
            #print("Password didnot match .Go back and try again")
            return render(request,"posts/signupuser.html",{'form':CreateUserForm(),'error':"password not matching"})
            #tell  the user password donot match
            #create new user
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        #return HttpResponse('<h2>Thank you for your email confirmation. Now you can login your account.</h2>')
        messages.success(request, 'Your account created succesfully')
        return redirect('loginuser')
    else:
        return HttpResponse('<h1>Activation link is invalid!</h1>')


def loginuser(request):
    
                if request.user.is_authenticated:
                        print("AUTHENTICATED")
                        return redirect('newfeeds')




                elif request.method== 'GET' :
                        print("GET METHOD")

                        return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
                        """elif request.method== 'GET' and request.user!=None:
                        try:
                              logout(request)
                              return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
                        except:
                                  return render(request,"posts/loginuser.html",{'form':AuthenticationForm()})
                       """

                else:
                    try:
                         user =authenticate(request,username=request.POST['username'], password=request.POST['password'])
                         if user is None:
                                   return render(request,"posts/loginuser.html",{'form':AuthenticationForm(),'error':"username or password didnot match"})
                                      #if user is none send them to same page with error
                         else:
                                      #login
                                    login(request,user)
                                    #messages.success(request, 'welcome back '+str(user))
                                    #return redirect('newfeeds')
                                    next = ""

                                    if request.GET:

                                            next = request.GET['next']
                                    if next == "":
                                             return redirect('newfeeds')

                                    else:
                                            return redirect(next)
                                            #return HttpResponseRedirect(request.GET['next'])
                                            #return render(request,"posts/home.html",{"form":seeprofileForm()})
                    except:
                            return redirect("newfeeds")
                                    #return render(request,"posts/home.html")
    

                                    #return redirect('home')
@login_required
def addpost(request):
    #return HttpResponse("Add post feature is disabled temporarily")

    if request.method =="GET": #when user first visit form show the form
        return render(request,"posts/addpost.html",{'form':feedsForm(),'message':"Your post will be verified before it  will be made visible to other people. You can always acess and delete your post in your feeds. Click ok to proceed. Excited for your new post!"})

    else:
        try:
               #if length is not large we send save it
               #when he click submit
               #fetch information from post request
               form=feedsForm(request.POST or None,request.FILES or None)

               newtodo=form.save(commit=False)




               #whatever user sent in post method we cnvert it to TodoForm form ie form
               #newtodo=form.save(commit=False) #commit =False means donot unnecessarily save it into database
               #in newtodo user field is missing
               if request.user.is_authenticated:
                        newtodo.user_new=request.user
               newtodo.save()#now it put it in database
               #return render(request,"posts/error.html",{"form2":form})
               #after saving  this we want to send them to current page so that they can see current to do
               messages.success(request, 'Your post submitted succesfully. Your post will be approved by admin before  making it public')
               return redirect('yourfeeds')
        except ValueError:
                return redirect('feeds')
                #if length of title is long we send back to same page otherwise we will get error
                return render(request,"posts/feeds.html",{'form':feedsForm()})
                #               ,"error1":"bad data","user1":request.user,"form1":newtodo




@login_required
def add_comment(request,id1,up):
    #feedsModel.objects.filter(pk=request.pk).update(upvote = upvote+1)
    #obj=get_object_or_404(feedsModel,id=id1,user=request.user_new)
    obj=feedsModel.objects.get(pk=id1)
    s1=str(up)
    sall=str(obj.comment)
    cmt1=str(request.POST['comment'])
    try:

            if sall==" ":

              obj.comment=s1+" : "+cmt1
              obj.save()
            else:

              obj.comment=s1+" : "+cmt1+"   |    "+sall
              obj.save()

            #sall=sall+"?"
            #s.save(update_fields=["upvote"])
            messages.success(request, 'Your comment on post was added ')
            return redirect("feeds")
    except:
            return redirect("feeds")

#news
def newscategory(request):
    return render(request,"posts/news.html")
def computer(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(q='computer science',


                                      language='en',
                                      sort_by='relevancy',
                                      page=4)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            #import time
            #from datetime import datetime,timezone
            #import pytz
            #tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def books(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(q='books',


                                      language='en',
                                      sort_by='relevancy',
                                      page=4)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            #import time
            #from datetime import datetime,timezone
            #import pytz
            #tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def religion(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(q='religion',


                                      language='en',
                                      sort_by='relevancy',
                                      page=4)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            #import time
            #from datetime import datetime,timezone
            #import pytz
            #tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def foods(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(q='foods',


                                      language='en',
                                      sort_by='relevancy',
                                      page=4)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            #import time
            #from datetime import datetime,timezone
            #import pytz
            #tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})


def corona(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(q='coronavirus',
                                          language='en',
                                          country='in')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
            #import time
            #from datetime import datetime,timezone
            #import pytz
            #tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def ndtv(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(sources='NDTV News')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime((myarticle["publishedAt"]).astimezone(tz),"%Y-%m-%dT%H:%M:%SZ"))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def thehindu(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(sources='the-hindu')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])

        try:
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
            #import time
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime((myarticle["publishedAt"]),"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def nationalgeographic(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(sources='national-geographic')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        #time.append(myarticle["publishedAt"])
        try:
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
        except:
            time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def newsfeedsgoogle(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(sources='google-news-in')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def newsfeedsworld(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(



                                      language='en',
                                      sources="bbc-news",
                                      sort_by='relevancy',
                                      page=4)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def hacker_news(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(



                                      language='en',
                                      sources="hacker-news",
                                      sort_by='relevancy',
                                      page=2)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def newsfeedsworldcnn(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_everything(



                                      language='en',
                                      sources="cnn",
                                      sort_by='relevancy',
                                      page=2)
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def newsfeedsenter(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(category="entertainment",language='en',country='us')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def newsfeedsenterbolly(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(category="entertainment",language='en',country='in')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def newsfeedstechno(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(category="technology",language='en',country='us')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def newsfeedsscience(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(category="science",language='en',country='us')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})
def newsfeedssports(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(category="sports",language='en',country="in")
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        author.append(myarticle['author'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def newsfeedsci(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(sources="espn-cric-info",language='en')
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        #time.append(myarticle["publishedAt"])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        author.append(myarticle['source']['name'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def newsfeedstoi(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(sources="the-times-of-india")
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])

        author.append(myarticle['source']['name'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})

def newsfeedsindia(request):
    newsapi=NewsApiClient(api_key="be9a230794c94431a9c387de985efa46")
    topheadlines=newsapi.get_top_headlines(country="in")
    articles=topheadlines['articles']
    des=[]
    news=[]
    img=[]
    url=[]
    time=[]
    author=[]
    for i in range(len(articles)):
        myarticle=articles[i]
        news.append(myarticle['title'])
        des.append(myarticle['description'])
        img.append(myarticle['urlToImage'])
        url.append(myarticle['url'])
        try:
            from datetime import timezone
            import pytz
            tz=pytz.timezone('Asia/Kolkata')
            #time_now=datetime.now(timezone.utc).astimezone(tz)
            time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").astimezone(tz))
            #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        except:
            time.append(myarticle["publishedAt"])
        #time.append(dt.datetime.strptime(myarticle["publishedAt"],"%Y-%m-%dT%H:%M:%SZ"))
        author.append(myarticle['source']['name'])
    mylist=zip(news,des,img,url,time,author)
    return render(request,"posts/newspage.html",{"mylist":mylist})







        #authenticate return user object
       #we need to check whether they have given cotrrect username or not
        #authenticate return user object
       #we need to check whether they have given cotrrect username or not

