from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def SignupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful, welcome to weather!')
            return redirect('home')

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else: 
            messages.success(request, 'There was an error logging in, try again.')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')
     
def LogoutView(request):
    logout(request)
    messages.success(request, 'Logout successfull')
    return redirect('home')

     
