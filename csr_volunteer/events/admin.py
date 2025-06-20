from django.contrib import admin
from .models import EmployeeProfile, CSRProject, EventParticipation

class EventParticipationInline(admin.TabularInline):
    model = EventParticipation
    extra = 0
    readonly_fields = ('employee', 'registered_on')
    can_delete = False
    verbose_name = "Registered Employee"
    verbose_name_plural = "Registered Employees"

class CSRProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'view_registered_count')
    inlines = [EventParticipationInline]

    def view_registered_count(self, obj):
        return EventParticipation.objects.filter(event=obj).count()
    view_registered_count.short_description = 'Registered Employees'

admin.site.register(EmployeeProfile)
admin.site.register(CSRProject, CSRProjectAdmin)
admin.site.register(EventParticipation)
