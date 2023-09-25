from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def authenticated(request):
    # Your custom authentication logic here
    # Return True if the user is authenticated; otherwise, return False
    if 'id' in request.session and request.session['id']:
        return True
    else:
        return False


def index(request):
    return render(request, 'forms.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    users = User.objects.all()
    for user in users:
        if user.email == request.POST['email']:
            errors["email"] = "This email already exists"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(firstname=firstname, lastname=lastname, email=email, password=pw_hash)
        user = User.objects.last()
        request.session['firstname'] = user.firstname
        request.session['id'] = user.id
        return redirect('/price')


def dashboard(request):
    if authenticated(request):
        user = User.objects.get(id=request.session['id'])
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)
    return redirect('/')


def login(request):
    user = User.objects.filter(email=request.POST['email']).first()
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['firstname'] = user.firstname
            request.session['lastname'] = user.lastname
            request.session['id'] = user.id
            messages.success = "login successful"
            return redirect('/price')
        messages.error(request, "invalid credential")
        return redirect('/')
    messages.error(request, "invalid credential")
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


def price_form(request):
    if authenticated(request):
        return render(request, 'predict.html')
    return redirect('/')


def predict(request):
    if authenticated(request):
        return render(request, 'predict.html')
    return redirect('/')
