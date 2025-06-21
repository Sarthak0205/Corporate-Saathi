"""
URL configuration for csr_volunteer project.
"""

from django.contrib import admin
from django.urls import path
from events import views  # Importing views module
from events.views import create_employee_credential, event_participants


urlpatterns = [
    path('admin/', admin.site.urls),  # Django default admin
    path('', views.dashboard, name='dashboard'),
    
    # Authentication & Dashboard
    path('admin-login/', views.admin_login, name='admin_login'),
    path('employee-login/', views.employee_login, name='employee_login'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('logout_user/', views.logout_user, name='logout_user'),

    # Event Management
    path('create-event/', views.create_event, name='create_event'),
    path('list-events/', views.list_events, name='list_events'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

    # Employee Management
    path('list-employees/', views.list_employees, name='list_employees'),
    # path('create-employee/', views.create_employee, name='create_employee'),  # Disabled

    # Admin Management
    path('manage-admins/', views.manage_admins, name='manage_admins'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin_status, name='toggle_admin_status'),

    # Employee Profile
    path('employee/profile/', views.employee_profile, name='employee_profile'),
    path('profile/edit/', views.edit_employee_profile, name='edit_employee_profile'),

    # Event Registration
    path('register-event/<int:event_id>/', views.register_for_event, name='register_event'),
    path('withdraw-event/<int:event_id>/', views.withdraw_event, name='withdraw_event'),
    path('event-participants/<int:event_id>/', event_participants, name='event_participants'),
    # path('register-employee/', views.register_employee, name='register_employee'),'
        # path('create-employee-credential/', views.create_employee_credential, name='create_employee_credential'),
    path('create-employee/', create_employee_credential, name='create_employee_credential'),
    path('event-participants/export/<int:event_id>/', views.export_event_participants_csv, name='export_event_participants_csv'),


    



]
