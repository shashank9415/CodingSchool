from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea

from .models import Tutorial

class TutorialForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Tutorial
        fields = ('topicId', 'title','content','rating','slug','tags')
        widgets = {
          #  'content': input['text'](attrs={'id':'id_content','name':'content'}),
        }


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if(commit):
            user.save()

        return  user
