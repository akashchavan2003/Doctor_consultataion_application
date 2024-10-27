"""login_signup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
   path('', views.default_login,name='login1'),
   path('login/',views.regular_login,name='login'),
   path('register_patient/',views.register_patient,name='register_patient'),
   path('register_doctor/',views.register_doctor,name='register_doctor'),
   path('doctor_details/<int:id>/', views.doctor_details, name='doctor_details'),
   path('logout/',views.logout,name='logout'),
   path('doctors_list/',views.display_doctors,name='doctors_list'),
   path('toggle-status/', views.toggle_status, name='toggle_status'),
   path('chat/<int:id>/',views.chat_dashboard,name='chat'),
   path('update_profile/',views.profile_update,name='update_profile'),
   path('patient_profile',views.patient_profile,name='patient_profile'),
   path('patient_dashboard_view',views.dashboard_view,name='patient_dashboard_view'),
   path('add_booking_slots',views.add_booking_slots,name='add_booking_slots'),
   path('book_appointment/<int:id>/',views.showing_appointment_booking,name='book_appointment'),
   path('doctor_dashboard_view/',views.doctor_dashboard,name='doctor_dashboard_view'),
   path('doctor_profile/',views.doctor_profile_view,name='doctor_profile'),
   path('doc_slots_show/',views.doc_add_slots_show,name='doc_slots_show'),



]
