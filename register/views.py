import os
from django.shortcuts import render
from .forms import RegisterForm
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import random
from django.utils.translation import gettext as _


from django.contrib.auth.hashers import check_password



from . import tokens as t
from django.core.mail import send_mail
from smtplib import SMTPException
from django.conf import settings

user_number = 1


def login(request):
    #messages.add_message(request, messages.INFO, 'Hello world.')
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                print('user exists:',user.username,' pwd:',pwd)
                if not user.is_active:
                    messages.warning(request, 'Your account is not activated.')
                    return redirect('login')

                user_login_status = authenticate(username=user.username,password=pwd)

                print(user_login_status)

                if user_login_status is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth_login(request,user)
                    messages.info(request, 'Successfully logged in!')
                    return redirect('project_home')
                else:
                    messages.error(request, 'Entered password is wrong.')
                    return redirect('login')
            except:
                messages.error(request, 'User does not exists.')
                return redirect('login')



        else:
            print('not valid')
            form = LoginForm()
    else:
        if request.user.is_authenticated:
            return redirect('project_home')
        else:
            form = LoginForm()
    return render(request, "sign_in.html", {"form":form,"title":'Login',"button":'Login'})

# Create your views here.
def register(request):
    if request.method == "POST":
        form=RegisterForm(request.POST)

        print(form)

        if form.is_valid():
            print('form is valid')
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.email.split('@')[0] +':' + str(random.randint(0,100000))
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain':  current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': t.account_activation_token.make_token(user),
                })

            print('Domain:',current_site.domain)
            print('user pk',user.pk)
            print('base64 code uid:',urlsafe_base64_encode(force_bytes(user.pk)))
            print(t.account_activation_token.make_token(user))

            try:
                send_mail(
                    subject='Activate your TrustedUX account.',
                    message=message,
                    from_email=settings.EMAIL_FROM_FULL,
                    recipient_list=[user.email]
                )
            except SMTPException:
                messages.error(request, 'An email with instructions to activate your account could not be sent! Please contact the administrator to resolve the issue and activate your account.')
            else:
                messages.info(request, 'An email with instructions to activate your account has been sent.')

            return redirect('login')


        else:
            print('Form is not valid')

    else:
        c = get_current_site(request)
        print(c.domain)
        form = RegisterForm()

    #return render(request, "register.html", {"form":form})
    return render(request, "sign_up.html", {"form":form})

# Create your views here.


def activate(request, uidb64, token):
    print(uidb64)
    print(force_str(urlsafe_base64_decode(uidb64)))
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print('user does not exists')
    print('Account activation status:')
    print(t.account_activation_token.check_token(user, token))

    if user is not None and t.account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()
        messages.success(request, 'Your account is activated successfully!.You can login now.')
        return redirect('login')
    else:
        return render(request,'base_page.html',{"title":'Expired link',"content":"The confirmation link is not valid."})


def account_activation_sent(request):
    return render(request,'base_page.html',{"title":'Confirmation email sent',"content":'A email with confirmation link has been sent.'})

def logout(request):
    auth_logout(request)
    return redirect('login')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            print('form is valid with email')
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                print('user exists')
                current_site = get_current_site(request)
                for user in associated_users:
                    message = render_to_string('password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http'
                        })
                    try:
                        send_mail(
                            subject='TrustedUX Password Reset',
                            message=message,
                            from_email=settings.EMAIL_FROM_FULL,
                            recipient_list=[user.email]
                        )
                    except SMTPException:
                        return HttpResponse('Error')
                    messages.info(request,'We have emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you do not receive an email, please make sure you have entered the address you registered with, and check your spam folder.')

                    return redirect('login')
    else:
        password_reset_form = PasswordResetForm()
        return render(request,'sign_pwd_reset.html',{'form':password_reset_form})
