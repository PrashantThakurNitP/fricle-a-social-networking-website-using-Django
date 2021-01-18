from django.forms import ModelForm
from .models import profileModel
from django.contrib.auth.models import User

#this class is created so that to provide form for adding todo
#from phonenumber_field.formfields import PhoneNumberField
#class ClientForm(forms.Form):
from django import forms
class profileForm(ModelForm):
    #specify what class and what model it would be working with
    class Meta:#specify what class we are working with
        model=profileModel
        #mobile = PhoneNumberField()
        fields=['Fullname','about','email','address','image','dob']#these are feature from model that we will set
        widgets = {
            'about': forms.TextInput(attrs={'placeholder': 'Tell something about yourself'}),
            'address': forms.TextInput(attrs={'placeholder': 'Your address'}),

        }



class seeprofileForm(ModelForm):
    #specify what class and what model it would be working with
    class Meta:#specify what class we are working with
        model=User
        fields=['username']#these are feature from model that we will set
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),

        }



from messenger.models import messageModel


#this class is created so that to provide form for adding todo
class messagemeForm(ModelForm):
    #specify what class and what model it would be working with
    class Meta:#specify what class we are working with
        model=messageModel
        fields=['title']#these are feature from model that we will set
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Your message here'}),

        }

