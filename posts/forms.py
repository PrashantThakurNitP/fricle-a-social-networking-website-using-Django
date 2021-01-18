from django.forms import ModelForm
from .models import feedsModel,CommentModel
from django import forms

#this class is created so that to provide form for adding todo











class feedsForm(ModelForm):
	#specify what class and what model it would be working with
	class Meta:#specify what class we are working with
		model=feedsModel
		fields=['title','description','image','link','videofile']#these are feature from model that we will set
		widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Give title to your post'}),
            'description': forms.TextInput(attrs={'placeholder': 'Say something about your post'}),
            'link': forms.TextInput(attrs={'placeholder': 'Any url  or link'}),


        }


class commentForm(ModelForm):
    #specify what class and what model it would be working with
    class Meta:#specify what class we are working with
        model=CommentModel
        fields=['comment']#these are feature from model that we will set
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Click here and add your comment here'}),

        }

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUserForm(UserCreationForm):

    class Meta:#specify what class we are working with
        model=User
        fields=['username','password1','password2','email']


