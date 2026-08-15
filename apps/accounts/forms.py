from django import forms
from django.contrib.auth.models import User
from .models import Profile

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Create a secure password (min 6 characters)'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Confirm your password'
    }))
    primary_goal = forms.ChoiceField(
        choices=Profile.GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    experience_level = forms.ChoiceField(
        choices=Profile.EXPERIENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your.email@college.edu'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'primary_goal', 'experience_level', 'daily_goal_minutes', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name'}),
            'primary_goal': forms.Select(attrs={'class': 'form-select'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'daily_goal_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 15, 'max': 240}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Share what you are learning and building...'}),
        }
