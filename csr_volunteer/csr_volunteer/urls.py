"""
URL configuration for csr_volunteer project.
"""

from django.contrib import admin
from django.urls import path
from events.views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin (keep this for superuser access)
    path('', dashboard, name='dashboard'),
    path('admin-login/', admin_login, name='admin_login'),
    path('employee-login/', employee_login, name='employee_login'),
    path('admin-register/', admin_register, name='admin_register'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout_user/', logout_user, name='logout_user'),
    path('create-employee/', create_employee, name='create_employee'),
    path('create-event/', create_event, name='create_event'),
    path('list-events/', list_events, name='list_events'),
    path('list-employees/', list_employees, name='list_employees'),
path('employee-dashboard/', employee_dashboard, name='employee_dashboard'),
path('manage-admins/', manage_admins, name='manage_admins'),
path('toggle-admin/<int:user_id>/', toggle_admin_status, name='toggle_admin_status'),
path('edit-event/<int:event_id>/', edit_event, name='edit_event'),
path('register-event/<int:event_id>/', register_for_event, name='register_event'),
     path('employee/profile/', employee_profile, name='employee_profile'),
    path('profile/edit/', edit_employee_profile, name='edit_employee_profile'),
    path('withdraw-event/<int:event_id>/', withdraw_event, name='withdraw_event'),



]
