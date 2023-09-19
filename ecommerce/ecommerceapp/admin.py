from django.contrib import admin
from ecommerceapp.models import Package,Contact,Order,Profile
# Register your models here.
@admin.register(Package)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("package_name", "package_category")
    list_filter = ("package_category",)
# admin.site.register(Contact)
@admin.register(Contact)
class Personcontact(admin.ModelAdmin):
    list_display = ("name", "email","message")
@admin.register(Order)
class Personorder(admin.ModelAdmin):
    list_display = ("name", "package","admission")
    list_filter = ("admission",)


admin.site.register(Profile)
class Personprofile(admin.ModelAdmin):
    list_display = ("name","profile_pic")