from django import forms
from django.contrib.auth.models import User
from .models import CSRProject, EmployeeProfile

# CSR Event Form
class CSRProjectForm(forms.ModelForm):
    class Meta:
        model = CSRProject
        fields = ['title', 'description', 'location', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Edit Profile Form (still useful for employees)
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

class EmployeeRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = EmployeeProfile
        fields = ['department', 'phone', 'supervisor']

    def save(self, commit=True):
        # Create User object
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.is_staff = False  # Ensure they are not admin
        user.save()

        # Create and link EmployeeProfile
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile

