from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.exceptions import ObjectDoesNotExist

PROJECT_NAME = "MyApp"


# Create your views here.
def index(request):
	if 'userid' in request.session:
		print "Userid: ", request.session['userid']
		return redirect('login:index')

	# if validate_user(request):
	# 	return redirect(reverse('login:success'))

	if 'userid' in request.session:
		print "Userid, post validation: ", request.session['userid']

	if not 'first_name' in request.session:
		request.session['first_name'] = ""
	if not 'last_name' in request.session:
		request.session['last_name'] = ""
	if not 'email' in request.session:
		request.session.email = ""
	# if not 'error' in request.session:
	# 	request.session['email'] = ""
	# 	request.session['last_name'] = ""
	# 	request.session['first_name'] = ""
	messages.error(request, "Error: No user specified.")
	messages.success(request, "This page works!")
	return render(request, 'bootstrap/index.html')


def login(request):
	print PROJECT_NAME
	if request.session.get('is_authed'):
		return redirect('secrets:index')

	if request.method == "POST":
		print "Processing Login for", request.POST['email']
		results = User.objects.login(request.POST)
		if not results['error']:
			messages.success(request, "Successfully logged in!")
			user = results['user']
			# print user['id'], user['first_name']
			print user.id, user.first_name
			request.session['userid'] = user.id
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['email'] = user.email
			request.session['is_authed'] = True
		else:
			for msg in results['messages']:
				messages.error(request, msg)
			request.session['email'] = request.POST['email']
		return redirect("secrets:index")
	else:
		return render(request, "bootstrap/login.html")


def do_register(request):
	if request.method == "POST":
		print "Processing Registration!"
		action = "registered"
		results = User.objects.register(request.POST)
		if not results['error']:
			messages.success(request, "Successfully " + action + "!")
			user = results['user']
			# print user['id'], user['first_name']
			print user.id, user.first_name
			request.session['userid'] = user.id
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['email'] = user.email
			request.session['is_authed'] = True
		else:
			for msg in results['messages']:
				messages.error(request, msg)
			request.session['first_name'] = request.POST['first_name']
			request.session['last_name'] = request.POST['last_name']
			request.session['email'] = request.POST['email']
		return redirect( "secrets:index" )
	else:
		return render(request, "bootstrap/register.html")


def process(request):
	print "process function"
	if request.method == "POST":
		if request.POST['action'] == "Login":
			print "Processing Login for", request.POST['email']
			action = "logged in"
			results = User.objects.login(request.POST['email'], request.POST['password'])
		elif request.POST['action'] == "Register":
			print "Processing Registration!"
			action = "registered"
			results = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['dob'])

		print results
		if not results['error']:
			messages.success(request, "Successfully " + action + "!")
			user = results['user']
			# print user['id'], user['first_name']
			print user.id, user.first_name
			request.session['userid'] = user.id
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['email'] = user.email
		else:
			for msg in results['messages']:
				messages.error(request, msg)
			request.session['first_name'] = request.POST['first_name']
			request.session['last_name'] = request.POST['last_name']
			request.session['email'] = request.POST['email']

	return redirect("login:index")


def success(request):
	return render(request, 'success.html')


def logout(request):
	request.session.clear()
	return redirect("login:index")


def edit(request, userid = 0):
	if not userid:
		userid = request.session['userid']

	# if userid == my userid, Edit Profile (vs Edit user #id)
	try:
		user = User.objects.get(id=userid)
	except ObjectDoesNotExist:
		messages.error(request, "Invalid User")
	return render(request, 'bootstrap/edit_user.html')


def admin(request):
	return render(request, 'boostrap/view_users.html')
