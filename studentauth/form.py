from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, StudentProfile
from django.forms import FileInput
from django.contrib.auth.forms import PasswordChangeForm



class RegistrationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    SCHOOL = (
        ('nile', 'Nile University'),
        ('baze', 'Baze University'),

    )
    fullname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}))


    school = forms.ChoiceField(choices=SCHOOL, widget=forms.Select())
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'phone', 'school','gender', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email address already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone','fullname']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = [
            'image',
            'fullname',
            'phone',
            'department',
            'country',
            'city',
            'state',
            'postal_code',
            'address',
            'hostel',
            'identity_type',
            'identity_image',



        ]

        widgets = {
            'image': FileInput(attrs={'onchange': 'loadFile(event)', 'class': 'upload'}),

        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].required = False
        self.fields['phone'].required = False
        self.fields['image'].required = False

