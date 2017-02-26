from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		print "Processing registration via UserManager"
		error = False
		msgs = []
		user = False
		first_name = data['first_name']
		last_name = data['last_name']
		email = data['email']
		password = data['password']
		password2 = data['confirm_password']

		if self.filter(email=email).exists():
			msgs.append("Email already exists. Please login or choose a different email.")
			error = True

		if len(email) < 5 or not EMAIL_REGEX.match(email):
			msgs.append("Invalid Email Address")
			error = True

		if not first_name.isalpha():
			error = True
			msgs.append("Invalid First Name")

		if not last_name.isalpha():
			error = True
			msgs.append("Invalid Last Name")

		if len(password) <= 8:
			error = True
			msgs.append("Password must be greater than 8 characters")
		elif password != password2:
			error = True
			msgs.append("Passwords do not match")

		# 1986-05-15
		# print "DOB:", dob
		# if len(dob) > 0:
		# 	dob = time.strptime(dob, '%Y-%m-%d')
		# 	tNow = time.strptime(time.asctime())
		# 	print dob[0]
		#
		# 	print "Dob:", dob
		# 	print "tNow:", tNow
		# 	if tNow[0] - dob[0] < 18 or (tNow[0] - dob[0] == 18 and dob[1] > tNow[1]):
		# 		error = True
		# 		msgs.append( 'Must be 18 years or older')
		# 		# time.struct_time(tm_year=1986, tm_mon=5, tm_mday=15, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=135, tm_isdst=-1)
		# else:
		# 	error = True
		# 	msgs.append( 'Please provide your Date of Birth')

		if not error:
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user = self.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
			if user.id == 1:
				user.level = User.ADMIN
				user.save()

		return {"error": error, "messages": msgs, "user": user}

	def login(self, data):
		email = data['email']
		password = data['password']
		error = True
		user = False
		msgs = []
		users = self.filter(email=email)
		if len(users) > 0:
			print users[0].email, users[0].first_name, users[0].id
			# hashed = bcrypt.hashpw( password, bcrypt.gensalt( ) )
			# Check that a unhashed password matches one that has previously been
			# hashed
			if bcrypt.hashpw(password.encode(), users[0].password.encode()) == users[0].password:
				user = users[0]
				error = False

		if error:
			msgs.append("Invalid Email or Password")

		return { "error": error, "messages": msgs, "user": user }


# Create your models here.
class User(models.Model):
	ADMIN = 9
	MODERATOR = 8
	NORMAL = 1
	LEVEL_CHOICES = (
		(ADMIN, 'Admin'),
		(NORMAL, 'Normal'),
		(MODERATOR, 'Moderator'),
	)
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	level = models.IntegerField(choices=LEVEL_CHOICES, default=NORMAL,)
	description = models.TextField()

	objects = UserManager()
