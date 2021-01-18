from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from profileinfo.models import profileModel

class profileinfoSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(Sitemap):
		    return profileModel.objects.all()



from posts.models import feedsModel

class feedSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(Sitemap):
		    return feedsModel.objects.all()




from todo.models import Todo

class TodoSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(Sitemap):
		    return Todo.objects.all()




from messenger.models import messageModel

class messengerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(Sitemap):
	    	return messageModel.objects.all()
class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(self):
	    	return['home','newsfeedsenterbolly','newsfeedsenter','newsfeedstoi','newsfeedsworldcnn','corona','computer','hacker-news','nationalgeographic','thehindu','newscategory','newsfeedstechno','newsfeedsworld','newsfeedsgoogle','newsfeedsindia','newsfeedssports','newsfeedsci','newsfeedsscience','loginuser','signupuser','chooseuser','viewmessage','updateprofile','seeprofile','feeds','createtodo','currenttodos','completedtodos','yourfeeds','newfeeds','addpost','createtodo','currenttodos','completedtodos']

    def location(self,item):
	    	return reverse(item)


