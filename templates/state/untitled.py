# def user_login(request):
# 	category_list = Category.objects.order_by('-likes')
# 	if request.method == "POST":

# 	# Gather the username and password provided by the user.
# 	# This information is obtained from the login form.
# 	# We use request.POST.get('<variable>') as opposed to request.POST['<variable>'\],
# 	# because the request.POST.get('<variable>') returns None, if the value does no\
# 	#t exist,
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		# Use Django's machinery to attempt to see if the username/password
# 		# combination is valid - a User object is returned if it is.
# 		user = authenticate(username=username, password=password)

# 		# If we have a User object, the details are correct.
# 		# If None (Python's way of representing the absence of a value), no user
# 		# with matching credentials was found

# 		if user:
# 			#is the account active? it could have been diabled.
# 			if user.is_active:
# 				# if the account is valid and active we can log the user in .
# 				# we'll  send the user back to hompage.
# 				login(request,user)
# 				return  HttpResponseRedirect(reverse('profile'))

# 			else:
# 				#an inactive account was used -no logging in !
# 				return HttpResponse ("Your Rango account is disabled.")
# 		else:

# 			print "invalide login details: {0},{1}".format(username,password)
# 			return render(request,"rango/login.html",{'categories':category_list})
# 	else:

# 		return render(request,'rango/login.html',{'categories':category_list})

# def register(request):
# 	# A boolean value for telling the template
# # whether the registration was successful.
# # Set to False initially. Code changes value to
# # True when registration succeeds.
# 	category_list = Category.objects.order_by('-likes')
# 	registered = False
# 	if request.method == "POST":
# 		# Attempt to grab information from the raw form information.
# # Note that we make use of both UserForm and UserProfileForm.

# 		user_form = UserForm(data=request.POST)
# 		profile_form = UserProfileForm(data = request.POST)
# 		if user_form.is_valid() and profile_form.is_valid():
# 			user = user_form.save()
# 			# Now we hash the password with the set_password method.
# 			# Once hashed, we can update the user object.
# 			user.set_password(user.password)
# 			user.save()

# 			# Now sort out the UserProfile instance.
# 			# Since we need to set the user attribute ourselves,
# 			# we set commit=False. This delays saving the model
# 			# until we're ready to avoid integrity problems.
# 			profile = profile_form.save(commit =False)
# 			profile.user = user
# 			# Did the user provide a profile picture?
# 			# If so, we need to get it from the input form and
# 			#put it in the UserProfile model.

# 			if 'picture' in request.FILES:
# 				profile.picture = request.FILES['picture']

# 				#Now we save the UserProfile model instance.
# 			profile.save()

# 			registered = True
# 			return HttpResponseRedirect(reverse('login'))
# 		else:
# 			# Invalid form or forms - mistakes or something else?
# 			# Print problems to the terminal.
# 			print user_form.errors, profile_form.errors
# 	else:
# 		# Not a HTTP POST, so we render our form using two ModelForm instances.
# 		# These forms will be blank, ready for user input.
# 		user_form = UserForm()
# 		profile_form =UserProfileForm()
# 	return render(request, 'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered,'categories':category_list})



#@login_required
# def user_logout(request):
# 	logout(request)
# 	return HttpResponseRedirect(reverse('index'))

