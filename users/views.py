from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib import messages
import random
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings



def SignUpView(request):

	if request.method == 'POST':
		get_otp = request.POST.get('otp')

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				messages.success(request, f'Account is Created For {usr.username}')
				return redirect('login')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'users/signup.html', {'otp': True, 'usr': usr})

		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			usr = User.objects.get(username=username)
			usr.is_active = False
			messages.success(request, f'{username}! OTP has been sent successfull. Check your Email')
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)

			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to ITScorer - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)

			return render(request, 'users/signup.html', {'otp': True, 'usr': usr})


	else:
		form = SignUpForm()

	return render(request, 'users/signup.html', {'form':form})