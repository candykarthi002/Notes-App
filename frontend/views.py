from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Notes
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

@login_required(login_url="/login")
def index(request):
	current_user = request.user
	notes = Notes.objects.filter(author=current_user)
	notes = list(notes.order_by('-created_at'))
	fav_notes = []
	for i in notes:
		if i.favourite:
			fav_notes.append(i)
	return render(request, 'frontend/home.html', {'user': request.user, "notes": notes, "fav_notes": fav_notes,})

@login_required(login_url="/login")
def create_page(request):
	if request.method == "POST":
		t = request.POST.get("title")
		if t:
			print(t)
			content = request.POST.get("text")
			if content:
				current_user = request.user
				n = Notes(author=current_user, name=t, text=content, favourite=False)
				n.save()
				messages.add_message(request, messages.SUCCESS, "Notes Created!")
				return HttpResponseRedirect("/")
	return render(request, 'frontend/create_page.html')

@login_required(login_url="/login")
def edit_notes(request, id):
	if request.method == "POST":
		t = request.POST.get("title")
		if t:
			print(t)
			content = request.POST.get("text")
			if content:
				notes_for_update = Notes.objects.filter(id=id).first()
				notes_for_update.name = t
				notes_for_update.text = content
				notes_for_update.created_at = datetime.datetime.now()
				notes_for_update.save()
				messages.add_message(request, messages.SUCCESS, "Changes Saved!")
				return HttpResponseRedirect("/")
	filtered_notes = Notes.objects.filter(id=id).first()
	print(filtered_notes.id)
	return render(request, 'frontend/edit_page.html', {"notes": filtered_notes})

@login_required(login_url="/login")
def add_favourite(request, id):
	n = Notes.objects.filter(id=id).first()
	if n:
		n.favourite = not n.favourite
		n.save()
		messages.add_message(request, messages.SUCCESS if n.favourite else messages.ERROR, f"\"{n.name}\" was {'added to' if n.favourite else 'removed from'} Favourites!")
	return HttpResponseRedirect('/')

@login_required(login_url="/login")
def delete_notes(request, id):
	n = Notes.objects.filter(id=id).first()
	if n:
		n.delete()
		# flash(f"{n.name} deleted successfully!")
		messages.add_message(request, messages.SUCCESS, f'{n.name} was deleted successfully!')
	return HttpResponseRedirect('/')

def sign_up(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	if request.method == "POST":
		username = request.POST.get('username')
		if User.objects.filter(username=username).exists():
			messages.add_message(request, messages.ERROR, "Username already exists!")
			return render(request, 'frontend/signup.html')
		email = request.POST.get('email')
		if User.objects.filter(email=email).exists() and not validate_email(email):
			messages.add_message(request, messages.ERROR, "Email already exists!")
			return render(request, 'frontend/signup.html')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if len(password1) < 6 and password1 != password2:
			messages.add_message(request, messages.ERROR, "Error due to password mismatching or insufficient password length!")
			return render(request, 'frontend/signup.html')
		new_user = User.objects.create_user(username, email, password1)
		new_user.save()
		messages.add_message(request, messages.SUCCESS, "User Created!")
		user = authenticate(request, username=username, password=password1)
		if user is not None:
			login(request, user)
			messages.add_message(request, messages.SUCCESS, "User Logged In!")
			return HttpResponseRedirect('/')
		return HttpResponseRedirect('/login')
	return render(request, 'frontend/signup.html')

def login_user(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		username = User.objects.filter(email=email).first()
		user = authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			messages.add_message(request, messages.SUCCESS, "User Logged In!")
			return HttpResponseRedirect('/')
		else:
			messages.add_message(request, messages.ERROR, "Login Error!")
	return render(request, 'frontend/login.html')

@login_required(login_url="/login")
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')