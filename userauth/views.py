from django.shortcuts import render
from userauth.forms import userregistrationform
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
UserModel = get_user_model()
# Create your views here.
def register(request):

    if request.method=="POST":
        form=userregistrationform(request.POST)
        if form.is_valid():
            newuser=form.save()
            username=form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            newuser=authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, newuser)
            return redirect("index") 
    else:
        form=userregistrationform()

    context={
        "form":form,
    }
    return render(request, "userauths/sign-up.html",context)
def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        # Accept either 'username' (preferred) or 'email' from the form
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UserModel.objects.get(email=email)
        except:
            messages.warning(request,f"user with {email} dont exist")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back!')
            return redirect('index')
        else:
            messages.warning(request, 'Invalid email or password.')
    context={}
    return render(request, "userauths/login.html",context)
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("userauth:login")
