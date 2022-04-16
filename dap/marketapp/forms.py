from django.core.exceptions import ValidationError
from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name','username','email','password']
            
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password)<=5:
            print('Password too short.')
            raise ValidationError('Password must be greater than 5 characters.')
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username)<=4:
            print('Username too short.')
            raise ValidationError('Username must be greater than 4 characters.')
        return username

class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=40)

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image','caption']

class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']

class TransferForm(forms.Form):
    class Meta:
        model = PostModel
        fields = ['id', 'user']
    
    user = forms.ModelChoiceField(
        queryset=UserModel.objects.all(),
        widget=forms.CheckboxInput
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text','post']

class UpvoteForm(forms.ModelForm):
    class Meta:
        model = UpvoteModel
        fields = ['comment']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionModel
        fields = ['post']