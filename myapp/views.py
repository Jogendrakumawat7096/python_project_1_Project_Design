from django.shortcuts import render, redirect
from django.core.mail import send_mail
from . models import Contact, Register
from django.conf import settings
import random


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        try:
            user = Register.objects.get(email=email)
            msg = "Email is already registered"
            return render(request, 'register.html', {'msg': msg})
        except :
            if password == cpassword:
                Register.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=email,
                    mobile=request.POST['mobile'],
                    password=password,
                    image=request.POST['image'],
                )
                msg = "Registration Successful"
                return render(request, 'register.html', {'msg': msg})
            else:
                msg = "Password and Confirm Password do not match"
                return render(request, 'register.html', {'msg': msg})
    else:
        return render(request, 'register.html')

    
def login(request):
    if request.method == "POST":

        try:
            user = Register.objects.get(email=request.POST['email'])
            if request.POST['password']==user.password:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                return render(request, 'index.html')
            else:
                msg = "Incorrect Password"
                return render(request, 'login.html', {'msg': msg})
        except:
            msg = "Email Not Registered"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')
def contact(request):
    msg = ""
    contacts = Contact.objects.all().order_by("-id")[:5]
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['message']
        )
        msg = "Contact Saved Successfully"
    return render(request, 'contact.html', {'msg': msg, 'contacts': contacts})

def about(request):
    return render(request, 'about.html')

def forgot_password(request):
    if request.method == "POST":
        try:
            user = Register.objects.get(email=request.POST['email'])
            otp = random.randint(1000, 9999)
            subject = "OTP for Forgot Password"
            message = "Hello"+user.fname+" Your OTP for forgot password is" +str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'otp.html', {'otp': otp, 'email': user.email})
        except:
            msg = "Email Not Registered"
            return render(request, 'forgot-password.html', {'msg': msg})
    else:
        return render(request, 'forgot-password.html')

def verify_otp(request):
    email = request.POST['email']
    otp = int(request.POST['otp'])
    uotp = int(request.POST['uotp'])
    if otp == uotp:
        return render(request, 'new-password.html', {'email': email})
    else:
        msg = "Invalid OTP"
        return render(request, 'otp.html', {'otp': otp, 'email': email, 'msg': msg})

def new_password(request):
    email = request.POST['email']
    np=request.POST['np']
    cnp=request.POST['cnp']
    
    if np==cnp:
        user = Register.objects.get(email=email)
        user.password = np
        user.save()
        msg = "Password updated successfully"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg = "New Password and Confirm New Password do not match"
        return render(request, 'new-password.html', {'msg': msg,'email':email})

def logout(request):
    del  request.session['email']
    del  request.session['fname']

    return render(request, 'login.html')

def change_pass(request):
    if request.method == "POST":
        try:
            user = Register.objects.get(email=request.session.get('email'))
            if request.POST['opassword']==user.password:
                if request.POST['npassword'] == request.POST['cnpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    return redirect('logout')
                else:
                    msg = "New Password and Confirm New Password do not match"
            else:
                msg = "Old Password does not match"
        except Register.DoesNotExist:
            msg = "User not found"
        return render(request, 'change-pass.html', {'msg': msg})
    else:
        return render(request, 'change-pass.html')
