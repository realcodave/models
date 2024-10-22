from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ModelProfile, Gallery

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']  # Removed 'username'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        if commit:
            user.save()
        return user
            
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ModelProfileForm(forms.ModelForm):
    class Meta:
        model = ModelProfile
        fields = [
            'fullname', 'height', 'hobby', 'language', 'gender',
            'nationality', 'location', 'address', 'bio',
            'dob', 'image', 'phone_number', 'x', 'facebook',
            'instagram', 'linkedin', 'occuption', 
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']
