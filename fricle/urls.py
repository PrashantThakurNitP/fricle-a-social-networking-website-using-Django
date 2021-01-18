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
from posts import views


from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse

from django.contrib.sitemaps.views import sitemap
from .sitemaps import feedSitemap,StaticViewSitemap,messengerSitemap,profileinfoSitemap,TodoSitemap
from django.contrib.auth import views as auth_views
sitemaps={
    'static':StaticViewSitemap,

}
""" 'feeds':feedSitemap,
    'messenger':messengerSitemap,
    'profile':profileinfoSitemap,
    'todo':TodoSitemap,
"""




urlpatterns = [
    path('www.fricle.tech/sitemap.xml',sitemap,{'sitemaps':sitemaps}),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps}),
    path('admin/', admin.site.urls),
    path(r'', include('webmaster_verification.urls')),
    path("feeds/",views.feeds,name="feeds"),
    path("newfeeds/",views.newfeeds,name="newfeeds"),
    path("yourfeeds/",views.yourfeeds,name="yourfeeds"),


   
    path('',views.home,name="home"),

    #path('', views.index , name="index" ),

    path("signupuser",views.signupuser,name="signupuser"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('logoutuser/',views.logoutuser,name="logoutuser"),
    path('loginuser/',views.loginuser,name="loginuser"),
    path('addpost/',views.addpost,name="addpost"),
    #path("addpost/",views.feeds,name="addpost"),
    path('upvote/<int:id1>/<str:up>/',views.upvote,name="upvote"),  #changed in upvote fn in views.py and feeds.html in upvote link
    path('like/<int:postid>',views.like,name="like"),
    path('see_one_post/<int:postid>',views.one_post,name="see_one_post"),
    path('canyoudoso_make_visible/<int:postid>',views.make_visible,name="make_visible_this_post"),
    path('canyoudoso_make_invisible/<int:postid>',views.make_invisible,name="make_invisible_this_post"),
    path('add_comment/<int:id1>/<str:up>/',views.add_comment,name="add_comment"),
    path('comment_post/<int:postid>',views.comment_post,name="comment_post"),
    path('delete/<int:id1>/',views.delete,name="delete"),
    path('todo/', include('todo.urls')),
    path('messenger/', include('messenger.urls')),
    path('profileinfo/', include('profileinfo.urls')),
    path('news/', include('posts.urls')),



    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_complete"),


    #path('addpost/',views.addpost,name="addpost"),

   #2nd attempt social login
    path('oauth/', include('social_django.urls', namespace='social')),


]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

