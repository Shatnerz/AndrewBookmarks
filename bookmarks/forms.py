import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
    """Registration Form Class"""
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
                                label='Password',
                                widget=forms.PasswordInput()
                                )
    password2 = forms.CharField(
                                label='Password (again)',
                                widget=forms.PasswordInput()
                                )
    
    def clean_password2(self):
        """Make sure passwords pass validation and match"""
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords do not match.')
        
    def clean_username(self):
        """Make sure username is valid and not already taken"""
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and underscores.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')
    
class BookmarkSaveForm(forms.Form):
    """Form to enter and save bookmarks"""
    url = forms.URLField(
        label='URL',
        widget=forms.TextInput(attrs={'size': 64})
    )
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'size': 64})
    )
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.TextInput(attrs={'size': 64})
    )
    
class SearchForm(forms.Form):
    """Form to search bookmarks"""
    query = forms.CharField(
        label='Enter a keyword to search for',
        widget=forms.TextInput(attrs={'size': 32})
    )