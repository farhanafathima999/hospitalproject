from django.contrib import admin
from .models import Doctor,Patient,Appointment


# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display=['id','user','profile_pic','address','mobile','department','status']
    ordering=['id']
    search_fields=('id','user','mobile')
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display=['id','user','age','profile_pic','address','mobile','symptoms','assignedDoctorId','status']
    ordering=['id']
    search_fields=('id','user','mobile')
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display=['patientId','patientName','profile_pic','doctorId','doctorName','appointmentDate','description','status']
    ordering=['appointmentDate']
    search_fields=('patientId','patientName')
admin.site.register(Appointment, AppointmentAdmin)