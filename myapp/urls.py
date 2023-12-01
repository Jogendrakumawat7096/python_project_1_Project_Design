
from django.urls import path
from . import views


urlpatterns = [

    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('logout/',views.logout,name='logout'),
    path('change-pass/',views.change_pass,name='change-pass'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    
    
    
]