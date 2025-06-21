from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import  EmployeeProfileForm 
from django.utils import timezone
 # Ensure this is already imported at the top

# Import your models and forms
from .models import CSRProject
from .forms import CSRProjectForm
from .models import EmployeeProfile

# Check if the user is an admin (staff)
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Main dashboard (public)
def dashboard(request):
    return render(request, 'dashboard.html')

# Admin Login View
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # make sure only admins can login here
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
            return redirect('admin_login')

    return render(request, 'admin_login.html')


# Admin Registration View
def admin_register(request):
    # ✅ Step 1: Check if max admin limit reached
    max_admins = 3
    current_admins = User.objects.filter(is_staff=True).count()

    if current_admins >= max_admins:
        messages.error(request, "Admin registration limit reached.")
        return render(request, 'admin_register.html')  # 👈 Stay on the register page

    # ✅ Step 2: Handle POST data
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('admin_register')

        # ✅ Step 3: Create Admin Account
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_staff = True
        user.save()

        messages.success(request, "Admin registered successfully.")
        return redirect('admin_login')

    return render(request, 'admin_register.html')


from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser)
def manage_admins(request):
    admins = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'manage_admins.html', {'admins': admins})

@user_passes_test(is_superuser)
def toggle_admin_status(request, user_id):
    admin_user = get_object_or_404(User, id=user_id, is_staff=True, is_superuser=False)
    admin_user.is_active = not admin_user.is_active
    admin_user.save()
    messages.success(request, f"Admin '{admin_user.username}' status updated.")
    return redirect('manage_admins')

# Admin Dashboard (protected)
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Employee Login (static for now, we’ll add logic later)
from django.contrib.auth import authenticate, login
from django.contrib import messages

def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an employee.")
            return redirect('employee_login')

    return render(request, 'employee_login.html')



# Logout
@login_required
def logout_user(request):
    is_admin = request.user.is_staff
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('admin_login' if is_admin else 'employee_login')

    

from django.db.models import Q

@login_required
@user_passes_test(is_admin)
def list_employees(request):
    query = request.GET.get('q')
    department_filter = request.GET.get('department')

    employees = EmployeeProfile.objects.select_related('user')

    if query:
        employees = employees.filter(
            Q(user__username__icontains=query) | Q(department__icontains=query)
        )

    if department_filter and department_filter != 'all':
        employees = employees.filter(department=department_filter)

    departments = EmployeeProfile.objects.values_list('department', flat=True).distinct()

    return render(request, 'list_employees.html', {
        'employees': employees,
        'query': query,
        'departments': departments,
        'selected_department': department_filter
    })

# views.py

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CSRProjectForm

def create_event(request):
    if request.method == 'POST':
        form = CSRProjectForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)  # Don't save to DB yet
            event.created_by = request.user  # Set the current user
            event.save()  # Now save to DB
            messages.success(request, "Event created successfully!")
            return redirect('list_events')  # Adjust the redirect as needed
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CSRProjectForm()
    
    return render(request, 'create_event.html', {'form': form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(CSRProject, id=event_id)

    if request.method == 'POST':
        form = CSRProjectForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('list_events')
    else:
        form = CSRProjectForm(instance=event)

    return render(request, 'edit_event.html', {'form': form})





@login_required
def list_events(request):
    events = CSRProject.objects.all()  # Show all events to any logged-in admin
    return render(request, 'list_events.html', {'events': events})


from .models import CSRProject, EventParticipation

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(CSRProject, pk=event_id)

    # Only allow employees to register
    if request.user.is_staff:
        messages.error(request, "Admins cannot register for events.")
        return redirect('employee_dashboard')

    # Check if already registered
    already_registered = EventParticipation.objects.filter(event=event, employee=request.user).exists()

    if already_registered:
        messages.info(request, "You are already registered for this event.")
    else:
        EventParticipation.objects.create(event=event, employee=request.user)
        messages.success(request, "Successfully registered for the event.")

        

    return redirect('employee_dashboard')

from django.views.decorators.http import require_POST
@login_required
def withdraw_event(request, event_id):
    event = get_object_or_404(CSRProject, id=event_id)

    # ✅ Corrected field name: use `employee`, not `user`
    registration = EventParticipation.objects.filter(employee=request.user, event=event).first()
    if registration:
        registration.delete()
        messages.success(request, "You have withdrawn from the event.")
    else:
        messages.warning(request, "You are not registered for this event.")

    return redirect('employee_dashboard')


@login_required
def employee_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    now = timezone.now()
    upcoming_events = CSRProject.objects.filter(date__gte=now).order_by('date')
    past_events = CSRProject.objects.filter(date__lt=now).order_by('-date')

    # Get IDs of events the user has registered for
    registered_event_ids = EventParticipation.objects.filter(
        employee=request.user
    ).values_list('event_id', flat=True)

    return render(request, 'employee_dashboard.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'registered_event_ids': registered_event_ids,  # 👈 Add this
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import EmployeeProfile

def employee_profile(request):
    profile = EmployeeProfile.objects.filter(user=request.user).first()
    now = timezone.now()

    # Get all past events the employee has participated in
    past_events = CSRProject.objects.filter(
        eventparticipation__employee=request.user,
        date__lt=now
    ).order_by('-date')

    return render(request, 'employee_profile.html', {
        'profile': profile,
        'past_events': past_events,
    })

@login_required
def edit_employee_profile(request):
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)


    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('employee_profile')
    else:
        form = EmployeeProfileForm(instance=profile)

    return render(request, 'edit_employee_profile.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_event(request, event_id):
    event = get_object_or_404(CSRProject, id=event_id)
    
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('list_events')

from django.shortcuts import get_object_or_404
from .models import CSRProject

@login_required
@user_passes_test(is_admin)
def event_participants(request, event_id):
    event = get_object_or_404(CSRProject, id=event_id)

    # Get all participation records for this event
    participations = EventParticipation.objects.filter(event=event).select_related('employee')

    # Get employee profiles from participating users
    employee_profiles = EmployeeProfile.objects.filter(user__in=[p.employee for p in participations])

    context = {
        'event': event,
        'participants': employee_profiles,
        'total_participants': employee_profiles.count(),
    }

    return render(request, 'event_participants.html', context)

from .forms import EmployeeRegistrationForm
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Replace with your actual dashboard URL name
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'register_employee.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import EmployeeProfile

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def create_employee_credential(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department = request.POST.get('department')
        phone = request.POST.get('phone')
        supervisor_id = request.POST.get('supervisor')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('create_employee_credential')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        supervisor = User.objects.get(id=supervisor_id) if supervisor_id else None

        EmployeeProfile.objects.create(
            user=user,
            department=department,
            phone=phone,
            supervisor=supervisor
        )

        messages.success(request, "Employee credential created successfully.")
        return redirect('admin_dashboard')

    supervisors = User.objects.filter(is_staff=True)
    return render(request, 'create_employee_credential.html', {'supervisors': supervisors})

from django.http import HttpResponse
import csv
from .models import EventParticipation, CSRProject, EmployeeProfile

def export_event_participants_csv(request, event_id):
    event = CSRProject.objects.get(id=event_id)
    participations = EventParticipation.objects.filter(event=event).select_related('employee')

    # Prepare CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.title}_participants.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Department', 'Registered On'])

    for p in participations:
        profile = EmployeeProfile.objects.filter(user=p.employee).first()
        department = profile.department if profile else 'N/A'

        writer.writerow([
            p.employee.username,
            p.employee.email,
            department,
            p.registered_on.strftime("%Y-%m-%d %H:%M"),
        ])

    return response
