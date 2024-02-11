from django.urls import path
from .import views
from django.contrib import admin

urlpatterns = [

    path('',views.home,name='home'),

    path('aboutus', views.aboutus),
    path('contactus', views.contactus),

    path('accounts/login/',views.loginview,name="login"),
    path('logout',views.logout_view,name='logout'),
    path('accounts/sign_up/',views.sign_up,name='signup'),

    path('adminclick', admin.site.urls,name='admindashboard'),
    path('doctorclick', views.doctorclick),
    path('patientclick', views.patientclick),
    
    
   #...........................doctor urls.............................
   #................................................................... 
    
    path('doctor-dashboard', views.doctor_dashboard,name='doctor-dashboard'),
    path('doctor-view-patient', views.doctor_view_patient,name='doctor-view-patient'),
    path('doctor-appointment', views.doctor_appointment,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment,name='doctor-delete-appointment'),
    path('delete-appointment', views.delete_appointment,name='delete-appointment'),

    #.........................patient urls...................................
    #........................................................................

    path('patient-dashboard', views.patient_dashboard,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment,name='patient-book-appointment'),
    path('book-appointment', views.book_appointment,name='book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor,name='patient-view-doctor'),
    path('patient-update-appointment', views.patient_update_appointment,name='patient-update-appointment'),
    path('update-appointment', views.update_appointment,name='update-appointment'),
   
    
]
