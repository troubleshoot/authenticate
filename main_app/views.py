from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
  return render(request, "login.html")

def login(request, methods=["POST"]):
  if request.POST['form'] == "register":
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else:
      password = request.POST['password']
      pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
      logged_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
      request.session['uuid'] = logged_user.id
      return redirect('/dashboard')
  elif request.POST['form'] == "login":
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else: 
      user = User.objects.filter(email=request.POST['email'])
      if user: 
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
          request.session['uuid'] = logged_user.id
          return redirect('/dashboard')
        else:
          errors['password_validate'] = "Password is invalid"
          for key, value in errors.items():
            messages.error(request, value)
      else: 
        errors['user_validate'] = "User does not exist"
        for key, value in errors.items():
          messages.error(request, value)
      return redirect('/')

def register(request):
  print(request.POST)
  errors = User.objects.register_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect("/")
  else:
    hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
      first_name = request.POST["first_name"],
      last_name = request.POST["last_name"],
      email = request.POST["email"],
      password = hash_browns
    )
    request.session['uuid'] = user.id
    return redirect('/dashboard')

def logout(request):
  del request.session['uuid']
  return redirect('/')

def dashboard(request):
  user = User.objects.get(id=request.session['uuid'])
  context = {
    'first_name' : user.first_name,
    'created_passwords' : user.created_passwords.all(),
  }
  return render(request, "dashboard.html", context)

def new(request):
  context = {
    'first_name': User.objects.get(id=request.session['uuid']).first_name,
  }
  return render(request, "create_password.html", context)

def show_password(request, id):
  context = {
    'first_name': User.objects.get(id=request.session['uuid']).first_name,
    'password' : Password.objects.get(id=id),
  }
  return render (request, "show_password.html", context)

def create_password(request):
  errors = Password.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/password/new')
  else: 
    Password.objects.create(name=request.POST['name'], url=request.POST['url'], username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], creator=User.objects.get(id=request.session['uuid']))
    return redirect('/dashboard')

def edit_password(request, id):
  context = {
    'first_name': User.objects.get(id=request.session['uuid']).first_name,
    'password' : Password.objects.get(id=id),
    'id' : id,
  }
  return render(request, 'edit_password.html', context)

def update_password(request, id):
  errors = Password.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect(f'/password/edit/{id}')
  else:
    password = Password.objects.get(id=id)
    password.name = request.POST['name']
    password.url = request.POST['url']
    password.email = request.POST['email']
    password.username = request.POST['username']
    password.password = request.POST['password']
    password.save()
  return redirect('/dashboard')

def remove_password(request, id):
  Password.objects.get(id=id).delete()
  return redirect('/dashboard')
