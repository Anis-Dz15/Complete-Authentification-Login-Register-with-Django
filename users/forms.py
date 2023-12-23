from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Edit User 
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

# Edit Profile         
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
# Registration Form
class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    
    class Meta:
        model= User
        fields = { 'username','email','first_name'}
        
    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password2']
    