from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path("",views.index,name="index"),
    path("contact",views.contact,name="contact"),
    path("order",views.order,name="order"),
    path("profile",views.profile,name="profile"),
    path("about",views.about,name="about"),
]