from django import forms
from django.contrib.auth.models import User
from .models import CSRProject, EmployeeProfile

# Existing CSR Event Form
class CSRProjectForm(forms.ModelForm):
    class Meta:
        model = CSRProject
        fields = ['title', 'description', 'location', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile


class EmployeeCreationForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = EmployeeProfile
        fields = ['department', 'phone']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_staff = False
        if commit:
            user.save()
            profile = super().save(commit=False)
            profile.user = user
            profile.save()
            return profile
        return super().save(commit=False)

def save(self, commit=True):
    user = User.objects.create_user(
        username=self.cleaned_data['username'],
        email=self.cleaned_data['email'],
        password=self.cleaned_data['password']
    )
    user.is_staff = False  # Make it an employee
    if commit:
        user.save()
        profile = super().save(commit=False)
        profile.user = user
        profile.save()
        return profile
    return super().save(commit=False)

from django import forms
from .models import EmployeeProfile

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['department', 'phone', 'supervisor']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
        }