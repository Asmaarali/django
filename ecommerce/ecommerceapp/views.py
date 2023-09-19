from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
# for displaying products
from ecommerceapp.models import Package,Contact,Order,Profile
from math import ceil
# for creating message
from django.contrib import messages

# Create your views here.
def about(request):
    return render(request,"about.html")

def index(request):
    allProds = []
    catprods = Package.objects.values('package_category','id')
    print(catprods)
    cats = {item['package_category'] for item in catprods}
    print(cats)
    for cat in cats:
        prod= Package.objects.filter(package_category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}

    return render(request,"index.html",params) 


def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        msg=request.POST['txtMsg']
        myquery=Contact(name=name,email=email,phone=phone,message=msg)
        myquery.save()
        messages.success(request,"message send successfully")
        return redirect('/contact')
    return render(request,"contact.html") 

def order(request):
    # context={}
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        package=request.POST['package']
        payment=request.POST['payment']
        msg=request.POST['txtMsg']
        myquery=Order(name=name,email=email,package=package,address=msg,payment=payment)
        myquery.save()
        messages.success(request,"Your order has been booked successfully")
        return redirect('/order')
    order=Order.objects.filter(email=request.user.email)
    # print(order)
    # context['order']=order
    # order=Order.objects.get(id=request.user.id)
    return render(request,"order.html",{'order':order})

def profile(request):
    login_user=get_object_or_404(User,id=request.user.id)
    context={}
    profile=Profile.objects.get(user__username=request.user.username)
    context['profile']=profile

    # updating profile
    if "update_profile" in request.POST:
        name=request.POST['name']
        phone=request.POST['phone']
        address=request.POST['address']
        profile_pic=request.FILES.get('profile_pic')

        profile.user.first_name=name
        profile.user.save()
        profile.contact_number=phone
        profile.address=address
        profile.profile_pic=profile_pic
        profile.save()
        messages.success(request,"Profile hass been updated successfully")
        return redirect('/profile')

        # change password
    if "change_pass" in request.POST:
        current_pass=request.POST['current_pass']
        new_pass=request.POST['new_pass']
        confirm_pass=request.POST['confirm_pass']

        checkpass=login_user.check_password(current_pass)  
        if new_pass == confirm_pass:
            if checkpass:
                login_user.set_password(new_pass)
                login_user.save()
                login(request,login_user)
                messages.success(request,"Password hass been changed successfully") 
                return redirect('/profile')
            else:
                messages.warning(request,"current password incorrect") 
        else:
            messages.warning(request,"New & Confirm Password didnot match") 
        # if checkpass==True:
        #     login_user.set_password(new_pass)
        #     messages.success(request,"Password hass been changed successfully")
        # else:
        #     messages.warning(request,"current password incorrect") 
   
    return render(request,"profile.html",context)