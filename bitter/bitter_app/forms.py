from typing import Any
from django import forms
from .models import Bite, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

# Profile Extras Form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
    website_link = forms.CharField(label="Website Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
    facebook_link = forms.CharField(label="Facebook Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
    instagram_link = forms.CharField(label="Instagram Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
    linkedin_link = forms.CharField(label="Linkedin Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin Link'}))
    twitter_link = forms.CharField(label="Twitter Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Twitter Link'}))

    class Meta:
        model = Profile
        fields = ('profile_image', )

class BiteForm(forms.ModelForm):
    body = forms.CharField(required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Write Your Bite",
                "class": "form-control",
            }
            ),
            label="",
        )
    class Meta:
        model = Bite
        exclude = ("user", "likes",)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    # Allow a user to update first and/or last name without changing the username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username