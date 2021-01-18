"""fricle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .import views


from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse





urlpatterns = [

    path("newsfeedsindia/",views.newsfeedsindia,name="newsfeedsindia"),
    path("newsfeedsci/",views.newsfeedsci,name="newsfeedsci"),
    path("newsfeedsscience/",views.newsfeedsscience,name="newsfeedsscience"),
    path("newsfeedsenter/",views.newsfeedsenter,name="newsfeedsenter"),
    path("newsfeedsenterbolly/",views.newsfeedsenterbolly,name="newsfeedsenterbolly"),
    path("newsfeedssports/",views.newsfeedssports,name="newsfeedssports"),
    path("newsfeedstechno/",views.newsfeedstechno,name="newsfeedstechno"),
    path("newsfeedstoi/",views.newsfeedstoi,name="newsfeedstoi"),
    path("newsfeedsworld/",views.newsfeedsworld,name="newsfeedsworld"),
    path("hacker_news/",views.hacker_news,name="hacker-news"),
    path("newsfeedsworldcnn/",views.newsfeedsworldcnn,name="newsfeedsworldcnn"),
    path("newsfeedsgoogle/",views.newsfeedsgoogle,name="newsfeedsgoogle"),
    path("nationalgeographic/",views.nationalgeographic,name="nationalgeographic"),
    path("thehindu/",views.thehindu,name="thehindu"),
    path("ndtv/",views.ndtv,name="ndtv"),
    path("books/",views.books,name="books"),
    path("foods/",views.foods,name="foods"),
    path("religion/",views.religion,name="religion"),

    path("corona/",views.corona,name="corona"),
    path("computer/",views.computer,name="computer"),
    path("",views.newscategory,name="newscategory"),









    #path('addpost/',views.addpost,name="addpost"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

