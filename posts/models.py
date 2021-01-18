


"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django_resized import ResizedImageField

# Create your models here.
class feedsModel(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)#it means having blank memeo is totally fine
    #created=models.DateTimeField(auto_now_add=True,blank=True,Default=False)#it means that it fixes time of its creation and it couldnot be changed
    #once it is set it cannot be changed
    user_new=models.ForeignKey(User,on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE,blank)
    image=models.ImageField(upload_to='media/images/',blank=True)
    upvote = models.IntegerField(default=0,blank=True)
    upvoter= models.TextField(blank=True)
    #foreig key stores the relationship between this todo and user
    #any object that is saved in database has id ie unique value for that object
    #now what foreignKey does is it takes id of user and saves here
    def __str__(self):
        return self.title
        #this function show name of title in admin page
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self
        if img.height>img.width:
                 self.image = ResizedImageField(size=[600, 400], upload_to='self.image.path')
        else:
                 self.image = ResizedImageField(size=[400, 600], upload_to='self.image.path')



"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse

# Create your models here.
class feedsModel(models.Model):
    title=models.CharField(max_length=200)
    link=models.URLField(max_length=5000,blank=True,null=True)
    description=models.TextField(blank=True,null=True)#it means having blank memeo is totally fine
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True)#it means that it fixes time of its creation and it couldnot be changed
    #once it is set it cannot be changed
    user_new=models.ForeignKey(User,on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE,blank)
    image=models.ImageField(upload_to='media/images/',blank=True,null=True)
    videofile= models.FileField(upload_to='media/videos/', blank=True,null=True)
    upvote = models.IntegerField(default=0,null=True)
    #upvoter= models.TextField(blank=True)
    #comment= models.TextField(blank=True,null=True)
    visibility=models.BooleanField(default=False,null=True)
    #foreig key stores the relationship between this todo and user
    #any object that is saved in database has id ie unique value for that object
    #now what foreignKey does is it takes id of user and saves here
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)

            import Image, ExifTags


            for orientation in ExifTags.TAGS.keys() :
                 if ExifTags.TAGS[orientation]=='Orientation' : break
            exif=dict(img._getexif().items())

            if   exif[orientation] == 3 :
                img=img.rotate(180, expand=True)
            elif exif[orientation] == 6 :
                img=img.rotate(270, expand=True)
            elif exif[orientation] == 8 :
                img=img.rotate(90, expand=True)
            output_size = (600, 600)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(self.image.path)
        except:
                pass
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('feeds')

class VoteModel(models.Model):
    voter = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(feedsModel,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.voter.username)+" liked "+str(self.post.title)
class CommentModel(models.Model):
    commentator = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(feedsModel,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    def __str__(self):
        return str(self.commentator.username)+" commented on  "+str(self.post.title)
        


        #this function show name of title in admin page

""" def save(self, *args, **kwargs):
        super().save( *args, **kwargs)  # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path
"""




"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

# Create your models here.
class feedsModel(models.Model):
	title=models.CharField(max_length=200)
	description=models.TextField(blank=True)#it means having blank memeo is totally fine
	#created=models.DateTimeField(auto_now_add=True,blank=True,Default=False)#it means that it fixes time of its creation and it couldnot be changed
	#once it is set it cannot be changed
	user_new=models.ForeignKey(User,on_delete=models.CASCADE)
	#user = models.OneToOneField(User, on_delete=models.CASCADE,blank)
	image=models.ImageField(upload_to='media/images/',blank=True)
	upvote = models.IntegerField(default=0,blank=True)
	upvoter= models.TextField(blank=True)
	#foreig key stores the relationship between this todo and user
	#any object that is saved in database has id ie unique value for that object
	#now what foreignKey does is it takes id of user and saves here
	def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)
	    img = Image.open(self.image.path)
	    output_size = (600, 600)
	    img.thumbnail(output_size)
	    img.save(self.image.path)
	def __str__(self):
	    return self.title
"""
		#this function show name of title in admin page
"""	def save(self, *args, **kwargs):
        super().save( *args, **kwargs)  # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path

"""