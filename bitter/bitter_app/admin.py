from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Bite

# Register your models here.

#Unregister Groups
admin.site.unregister(Group)

# Profile info joined with User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #Only display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister initial User
admin.site.unregister(User)
# Reregister User and Profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

#Register Bites
admin.site.register(Bite)