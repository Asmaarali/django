from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from ecommerceapp.models import Profile
from django.views.generic import View
# for creating message
from django.contrib import messages
# for login
from django.contrib.auth import authenticate,login,logout

# for sending email
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password not match")
            return render(request, "authentication/signup.html")

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email Already Exist")
                # return HttpResponse("Email already exists")
                return render(request, "authentication/signup.html")

        except Exception as identifier:
            pass

        user = User.objects.create_user(email, email, password)
        user.first_name=name
        user.is_active = False
        user.save()

        # email work
        email_subject="Activate Your Account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.send()
        messages.info(request,"Verification Link has been sent to your Email Address")

        profile=Profile(user=user,contact_number=contact)
        profile.save()
        # messages.success(request, "Account Created Successfully")
        # return render(request, "authentication/login.html")
    return render(request, "authentication/signup.html")

# ---------------------------signup work end----------------------------
# Activating  Account 
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Activated Successfully")
            return redirect('/auth/login')
        return render(request,'activatefail.html')


def handlelogin(request):
        if request.method=="POST":

            username=request.POST['email']
            userpassword=request.POST['pass1']
            myuser=authenticate(username=username,password=userpassword)

            if myuser is not None:
                login(request,myuser)
                if myuser.is_superuser or myuser.is_staff:
                    return redirect('/admin')
                messages.success(request,"Login Success")
                return redirect('/')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('/auth/login')
            
        return render(request, "authentication/login.html")


def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('/auth/login')
    # return redirect('/auth/login')
