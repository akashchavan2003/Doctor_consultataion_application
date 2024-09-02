
from django.contrib.auth.models import User

from django.db import models

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use a longer length for hashed passwords
    address = models.CharField(max_length=255, null=True, blank=True)  # Increased length for more comprehensive addresses
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    height = models.IntegerField(  null=True, blank=True)  # cm
    weight = models.IntegerField(  null=True, blank=True)  # kg
    conditions = models.TextField(null=True, blank=True)  # Store conditions as a comma-separated string or JSON
    medical_reports = models.FileField(upload_to='medical_reports/', null=True, blank=True)
    age = models.IntegerField( null=True, blank=True)  # kg
    additional_notes = models.TextField(null=True, blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=30)
    online = models.BooleanField(default=False)
    hospital_name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    specialization = models.CharField(max_length=20, default=None)
    degrees = models.CharField(max_length=30, default=None)
    profile_picture = models.ImageField(upload_to='product_images/')
    phone_number = models.CharField(max_length=15, default=None)
    

    
    
    def __str__(self):
        return self.user.username


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.SET_NULL, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20,default=None, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ])

    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time} to {self.end_time}"

class Consultation(models.Model):
    appointment = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='consultations')
    consultation_notes = models.TextField()
    prescription = models.OneToOneField('Prescription', on_delete=models.CASCADE, related_name='consultation_prescription')
    consultation_date = models.DateTimeField(auto_now_add=True)

class Prescription(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='prescription_details')
    prescription_details = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    appointment = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatMessage {self.id} - {self.sender.username}"
