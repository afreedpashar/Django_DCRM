from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *

# Create your views here.
def home(request):
    records = Records.objects.all()

    #checking if user is login in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #to authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have logged in successfully!")
            return redirect('home')
        else:
            messages.success(request,"There was some error loggin in...")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out successfully!!!")
    return redirect('home')


def register_user(request):
    # import pdb; pdb. set_trace()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have successfully registered.")
            return redirect('home')
    else:
        form=SignUpForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Records.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must be logged in to view the records")
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record deleted successfully")
        return redirect('home')
    else:
        messages.success(request,"You must login to delete an account")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record Added")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"You must be logged in to add record")
        return redirect('home')


def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record updated successfully")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"Must be logged in to update a record")
        return redirect('home')