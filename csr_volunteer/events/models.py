from django.db import models
from django.contrib.auth.models import User

# Employee profile model
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    joined_on = models.DateField(auto_now_add=True)
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='supervised_employees',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

# CSR Project model
class CSRProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Event participation model
class EventParticipation(models.Model):
    event = models.ForeignKey(CSRProject, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} joined {self.event.title}"
    
    
