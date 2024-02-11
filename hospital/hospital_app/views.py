from django.shortcuts import render,redirect
from .models import Doctor,Patient,Appointment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from .import forms
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta


# Create your views here.


@login_required
def home(request):
    try:
        if request.user.is_authenticated:
            userGroup = Group.objects.get(user=request.user).name
            print(userGroup)
            if userGroup =='PATIENT':
                return render(request,'patient_dashboard.html')
            elif  userGroup =='DOCTOR':
                return render(request,'doctor_dashboard.html')
            elif userGroup=='ADMIN':
                return render(request,'index.html')
    except Exception as e:
        print(e)
        return redirect('login')


def loginview(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=uname, password=pwd)
    if user is not None:
            login(request,user)
            return redirect('home')
              
    else:
        return render(request,"login.html",{"msg":"Invalid login"})



def logout_view(request):
    logout(request)
    return redirect('login')


def sign_up(request):
    try:
        form = UserCreationForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
               form.save()
               return redirect('login')
        else:
            return render(request,'sign_up.html',{'form': userform,'msg':'Invalid login'})
    except Exception as e:
        print(e)
        userform = UserCreationForm()
        return render(request, 'sign_up.html',{'form':userform})  



def doctorclick(request):
    if request.user.is_authenticated:
        return render(request,'doctorclick.html')
    else:
        return HttpResponseRedirect('accounts/login/')


def patientclick(request):
    if request.user.is_authenticated:
        return render(request,'patientclick.html')
    else:
        return HttpResponseRedirect('accounts/login/')

# ....................Doctor views..................................
#..................................................................


@login_required
def doctor_dashboard(request):
    #for three cards
    patientcount=Patient.objects.filter(status=True,assignedDoctorId=request.user.id).count()

    # Calculate the date range for the last 2 days
    end_date = datetime.now().date()  # Today's date
    start_date = end_date - timedelta(days=2)  # Date 2 days ago

    # Filter appointments based on status, doctorId, and appointmentDate within the date range
    appointmentcount=Appointment.objects.filter(status=True,doctorId=request.user.id,appointmentDate__range=(start_date, end_date)).count()
    
    #for  table in doctor dashboard
    patients=Patient.objects.filter(status=True,assignedDoctorId=request.user.id)
    appointments=Appointment.objects.filter(status=True,doctorId=request.user.id,appointmentDate__range=(start_date, end_date))
    
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patients':patients,
    'appointments':appointments,
    'doctor':Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor_dashboard.html',context=mydict)


def doctor_view_patient(request):
    patients=Patient.objects.filter(status=True,assignedDoctorId=request.user.id)
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_view_patient.html',{'patients':patients,'doctor':doctor})


def doctor_appointment(request):
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_appointment.html',{'doctor':doctor})


def doctor_view_appointment(request):
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar

    # Calculate the date range for the last 2 days
    end_date = datetime.now().date()  # Today's date
    start_date = end_date - timedelta(days=2)  # Date 2 days ago


    # Filter appointments based on status, doctorId, and appointmentDate within the date range
    appointments=Appointment.objects.filter(status=True,doctorId=request.user.id,appointmentDate__range=(start_date, end_date))
    return render(request,'doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



def doctor_delete_appointment(request):
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.filter(status=True,doctorId=request.user.id)
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



def delete_appointment(request):
    patientId=request.POST['patientId']
    appointment=Appointment.objects.get(patientId=patientId)
    appointment.delete()

    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.filter(status=True,doctorId=request.user.id)
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor,'message':"Deleted"})


#.................................Patient views.............................
#...........................................................................


@login_required
def patient_dashboard(request):
    patient=Patient.objects.get(user_id=request.user.id)
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)

    mydict={
    'patient':patient,
    'doctorName':doctor.user,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    
    }
    return render(request,'patient_dashboard.html',context=mydict)


def patient_appointment(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient_appointment.html',{'patient':patient})

def patient_book_appointment(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient_book_appointment.html',{'patient':patient})


def book_appointment(request):
    PatientId=request.POST['patientId']
    PatientName=request.POST['patientName']
    Profile_pic=request.POST['profile_pic']
    DoctorId=request.POST['doctorId']
    DoctorName=request.POST['doctorName']
    Des=request.POST['des']
    appointmentobj=Appointment(patientId=PatientId,patientName=PatientName,profile_pic=Profile_pic,doctorId=DoctorId,doctorName=DoctorName,description=Des)
    appointmentobj.save()

    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.filter(patientId=request.user.id)
    return render(request,'patient_book_appointment.html',{'appointments':appointments,'patient':patient,'message':"Booked"})


def patient_view_appointment(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.filter(patientId=request.user.id)
    return render(request,'patient_view_appointment.html',{'appointments':appointments,'patient':patient})

def patient_update_appointment(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.filter(patientId=request.user.id)
    return render(request,'patient_update_appointment.html',{'appointments':appointments,'patient':patient})


def update_appointment(request):

    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.filter(patientId=request.user.id)

    update_patientId=request.POST['patientId']
    doctorIdNew=request.POST['doctorIdNew']
    doctorNameNew=request.POST['doctorNameNew']
    desNew=request.POST['desNew']
    appointments=Appointment.objects.filter(patientId=update_patientId)
    if appointments.exists():
        appointments.update(patientId=update_patientId,doctorId=doctorIdNew,doctorName=doctorNameNew,description=desNew)    
        return render(request,'patient_update_appointment.html',{'appointments':appointments,'patient':patient,'message':"Updated"})
 
    else:
        return render(request,'patient_update_appointment.html',{'appointments':appointments,'patient':patient,'message':"No records found"})
 

def patient_view_doctor(request):
    doctors=Doctor.objects.filter(status=True)
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient_view_doctor.html',{'patient':patient,'doctors':doctors})



#............................About us and Contact us.......................
#..........................................................................

def aboutus(request):
    return render(request,'aboutus.html')

def contactus(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})
