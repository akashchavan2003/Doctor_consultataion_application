from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from app.models import Doctor,Patient,AppointmentSlot
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def register_doctor(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        hospital_n = request.POST.get('hospital_name')
        profile_picture = request.FILES.get('profile_picture')
        phone_n = request.POST.get('phone_number')
        deg = request.POST.get('degrees')
        specialization = request.POST.get('specialization')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if all([full_name, email, address, profile_picture, hospital_n, username, password]):
            # Create the User
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = full_name
            user.is_staff = True  # Assuming doctors have staff privileges
            user.save()

            # Create the Doctor associated with this User
            doctor = Doctor.objects.create(
                user=user,
                full_name=full_name,
                phone_number=phone_n,
                specialization=specialization,
                degrees=deg,
                email=email,
                address=address,
                profile_picture=profile_picture,
                hospital_name=hospital_n
            )
            doctor.save()
            print("Doctor created successfully.....")
    return render(request, 'doctor_signup.html')
from django.contrib.auth import logout as auth_logout
def logout(request):
    auth_logout(request)
    return redirect('login')


def register_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if all([first_name, last_name, username, email, password, address, profile_picture]):
            # Create the User
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = False  # Assuming patients do not have staff privileges
            user.save()

            # Create the Patient associated with this User
            patient = Patient.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                address=address,
                profile_picture=profile_picture
            )
            patient.save()
            print("Patient created successfully.....")
    return render(request, 'patient_signup.html')

def regular_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        login_user = authenticate(request, username=username, password=password)

        if login_user is not None:
            # Check user role
            if login_user.is_staff:
                login(request, login_user)
                print("Logged in as admin")
                user = User.objects.get(username=username)
                doctor = user.doctor 
                return render(request,'doctor.html',{'doc':doctor})
            else:
                login(request, login_user)
                print("Logged in as user")
                user=Patient.objects.get(username=username)
                return render(request,'user.html',{'pat':user})
        print("Incorrect username or password")
        return render(request, 'login.html',{'error_message':"username and password is wrong"})
    return render(request, 'login.html')

def doctor_details(request,id):
    doctor = Doctor.objects.get(id=id)
    return render(request, 'online_profile.html', {'doctor': doctor})


def default_login(request):
    return render(request,'login.html')

def display_doctors(request):
    doctors = Doctor.objects.filter(online=True) 
    return render(request, 'online_doc_list.html', {'doctors': doctors})


def chat_dashboard(request,id):
    doc=Doctor.objects.get(id=id)
    return render(request,'chat.html',{'doc':doc})

@login_required
def toggle_status(request):
    if request.method == 'POST':
        doctor = Doctor.objects.get(user=request.user)
        # Toggle the status
        doctor.online = not doctor.online
        doctor.save()
        return render(request,'doctor.html',{'doc':doctor})
from decimal import Decimal, InvalidOperation  


def profile_update(request):
    user_id=request.user.id
    patient = Patient.objects.get(id=user_id)

    if request.method == 'POST':
        try:
            patient.age = int(request.POST.get('age'))
            patient.height = int(request.POST.get('height'))
            patient.weight = int(request.POST.get('weight'))
            patient.date_of_birth = request.POST.get('date_of_birth')
            patient.phone_number = request.POST.get('phone_number')
        except (ValueError, InvalidOperation):
            # Handle the error, maybe return an error message to the user
            return render(request, 'patient_update.html', {'error_message': 'Invalid input!'})

        patient.conditions = request.POST.get('conditions')
        patient.additional_notes = request.POST.get('additional_notes')

        # Handling file upload for medical_reports
        if 'medical_reports' in request.FILES:
            patient.medical_reports = request.FILES['medical_reports']

        # Save the patient data
        patient.save()

        # Redirect or return success response
        return redirect('update_profile')
        


    return render(request, 'patient_update.html', {'patient': patient})
        

def patient_profile(request):
    try:
        user_id=request.user.id
        patient=Patient.objects.get(id=user_id)
    except ObjectDoesNotExist:
        print("User does not found")
    except Exception as e:
        print("error to get information from database for the user id:",user_id)
    return render(request,'patient_profile.html',{'patient':patient})

def dashboard_view(request):
     user_id=request.user.id
     patient=Patient.objects.get(id=user_id)
     return render(request,'user.html',{'pat':patient})



def add_booking_slots(request):
    user_id=request.user.id
    doctor= Doctor.objects.get(user_id=user_id)
    try:
        if request.method == 'POST':
            date = request.POST.get('date')
            st_t = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            is_avi = request.POST.get('is_available') == 'on'  # Ensure this is treated as a boolean

            # Create the AppointmentSlot with the correct doctor
            slot = AppointmentSlot.objects.create(
                doctor=doctor,
                date=date,
                start_time=st_t,
                end_time=end_time,
                is_available=is_avi,
                status='Scheduled'
            )
            slot.save()
            return render(request, 'add_appointment.html', {
    'success_msg': f"Time Slot Added as on Date: {date}, From {st_t} TO {end_time}"
})
    except Exception as e:
        return render(request,'add_appointment',{'error_message':"Adding slots Failed....."})
    return render(request, 'add_appointment.html', {'doctor': doctor,'doc':doctor})

def showing_appointment_booking(request, id):
    return render(request,'patient_appointment_booking.html')


def doctor_dashboard(request):
    doctor=Doctor.objects.get(user=request.user)
    return render(request,'doctor.html',{'doc':doctor})

def doctor_profile_view(request):
    doctor=Doctor.objects.get(user=request.user)
    print(doctor.address)
    return render(request,'doctor_profile_dashboard.html',{'doctor':doctor,'doc':doctor})