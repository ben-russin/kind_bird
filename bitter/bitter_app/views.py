from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Bite
from .forms import BiteForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User 


def home(request):
    if request.user.is_authenticated:
        form = BiteForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                bite = form.save(commit=False)
                bite.user = request.user
                bite.save()
                messages.success(request, ("Bite Posted"))
                return redirect('home')


        bites = Bite.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"bites":bites, "form":form})
    else:
        bites = Bite.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"bites":bites})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles':profiles})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page"))
        return redirect('home')

def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.remove(profile)
        # Save our profile
        request.user.profile.save()

        messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged In To View This Page"))
        return redirect('home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to follow
        profile = Profile.objects.get(user_id=pk)
        # Follow the user
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()

        messages.success(request, (f"You Have Successfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged In To View This Page"))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        bites = Bite.objects.filter(user_id=pk).order_by("-created_at")
        #Post Form Logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile, "bites":bites})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page"))
        return redirect('home')
    
def followers(request, pk):
    if request.user.is_authenticated:
    # Change the line above to allow anybody to view a followers list, but add logic to stop them from following and unfollowing
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles':profiles})
    else:
        messages.success(request, ("That's Not Your Profile Page"))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
    # Change the line above to allow anybody to view a followers list, but add logic to stop them from following and unfollowing
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profiles':profiles})
    else:
        messages.success(request, ("That's Not Your Profile Page"))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You've successfully logged In 😎"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in - Please try again 💀"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out - Until Next Time 👋"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # second_name = form.cleaned_data['second_name']
            # email = form.cleaned_data['email']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You've successfully registered 🚀"))
            return redirect('home')


    return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        # Get Forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None ,request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, ("Your Profile Has Been Updated!"))
            return redirect('home')

        return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page 😔"))
        return redirect('home')
    
def bite_like(request, pk):
    if request.user.is_authenticated:
        bite = get_object_or_404(Bite, id=pk)
        if bite.likes.filter(id=request.user.id):
            bite.likes.remove(request.user)
        else:
            bite.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    
    else:
        messages.success(request, ("You Must Be Logged In To View This Page 😔"))
        return redirect('home')
    
def bite_show(request, pk):
    bite = get_object_or_404(Bite, id=pk)
    if bite:
        return render(request, "show_bite.html", {'bite':bite})
    else:
        messages.success(request, ("That Bite Does Not Exist"))
        return redirect('home')

def delete_bite(request, pk):
    if request.user.is_authenticated:
        bite = get_object_or_404(Bite, id=pk)
        if request.user.username == bite.user.username:
            bite.delete()
            messages.success(request, "Your Bite Has Been Deleted")
            # Add delete logic here if needed, e.g. bite.delete()
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "That's Not Your Property")
            return redirect('home')
    else:
        messages.error(request, "You need to be logged in to delete a bite")
        return redirect('login')  
    
def edit_bite(request, pk):
    if request.user.is_authenticated:
        # Find the bite
        bite = get_object_or_404(Bite, id=pk)

        # Check if the logged-in user is the owner of the bite
        if request.user.username == bite.user.username:
            if request.method == "POST":
                form = BiteForm(request.POST, instance=bite)
                if form.is_valid():
                    form.save()  # Since user is already set, no need to set it again
                    messages.success(request, ("Your Bite Has Been Edited"))
                    return redirect('home')
                else:
                    # Form is not valid, render the page with form errors
                    return render(request, "edit_bite.html", {'form': form, 'bite': bite})
            else:
                # GET request, show the form for the first time
                form = BiteForm(instance=bite)
                return render(request, "edit_bite.html", {'form': form, 'bite': bite})
        else:
            # User is not the owner of the bite
            messages.error(request, "That's Not Your Property")
            return redirect('home')
    else:
        # User is not authenticated
        messages.error(request, "Please Log In To Continue")
        return redirect('login')  # Redirect to login page

def search(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = Bite.objects.filter(body__contains = search)

        return render(request, 'search.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search.html', {})

def search_user(request):
    if request.method == "POST":
        search = request.POST['search']
        # Include related Profile objects in the queryset
        searched = User.objects.filter(username__contains=search).select_related('profile')
        return render(request, 'search_user.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search_user.html', {})

