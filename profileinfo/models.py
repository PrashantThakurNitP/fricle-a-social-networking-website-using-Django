
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django_resized import ResizedImageField
#from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.modelfields import PhoneNumberField
#<<<<<<< HEAD
# Create your models here.
class profileModel(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE) #username

    #title=models.ForeignKey(User,on_delete=models.CASCADE) #username
    Fullname=models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=254,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    about=models.TextField(blank=True,null=True)#it means having blank memeo is totally fine
    #created=models.DateTimeField(auto_now_add=True,blank=True,Default=False)#it means that it fixes time of its creation and it couldnot be changed
    #once it is set it cannot be changed

    image=models.ImageField(upload_to='media/images/',blank=True,null=True)
    resume= models.FileField(upload_to='media/pdf/', max_length=254, blank=True,null=True)

    mobile = PhoneNumberField(blank=True,null=True)
    address= models.TextField(blank=True,null=True)

    def __str__(self):
        return self.Fullname
        #this function show name of title in admin page
    """def save(self):
        super().save()  # saving image first
        img = Image.open(self.image.path) # Open image using self
        if img.height>img.width:
             self.image = ResizedImageField(size=[600, 400], upload_to='self.image.path')
        else:
            self.image = ResizedImageField(size=[400, 600], upload_to='self.image.path')
"""