import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .forms import (PasswordResetForm, PasswordResetRequestForm)
from .models import UserProfile, ValidPasswordResetKey
from .forms import (AccountSettingsForm,
                    SignupForm, DeleteAccountForm)

from .utils import validate_activation_key
from django.conf import settings


# Copyright Videntity Systems Inc.

logger = logging.getLogger('verifymyidentity_.%s' % __name__)


def reset_password(request):

    name = _('Reset Password')
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.user.set_password(data['password1'])
                request.user.save()
                user = authenticate(request=request,
                                    username=request.user.username,
                                    password=data['password1'])
                login(request, user)
                messages.success(request, 'Your password was updated.')
                return HttpResponseRedirect(reverse('account_settings'))
            else:
                return render(request, 'generic/bootstrapform.html',
                              {'form': form, 'name': name})
        # this is a GET
        return render(request, 'generic/bootstrapform.html',
                      {'form': PasswordResetForm(), 'name': name})
    else:
        return HttpResponseRedirect(reverse('home'))


def mylogout(request):
    logout(request)
    messages.success(request, _('You have been logged out.'))
    return HttpResponseRedirect(reverse('home'))


@login_required
def delete_account(request):
    name = _('Delete Account Information')
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, _('Your account has been deleted.'))
            return HttpResponseRedirect(reverse('home'))
    # This is a GET
    messages.warning(request, _(
        'You are about to permanently delete your account. This action cannot be undone.'))
    return render(request,
                  'generic/bootstrapform.html',
                  {'name': name, 'form': DeleteAccountForm()})


@login_required
def account_settings(request, subject=None):
    if not subject:
        # Looking at your own record.
        user = request.user
        up = get_object_or_404(UserProfile, user=user)
        name = _('Edit Your Basic Profile Information')
    else:
        up = get_object_or_404(UserProfile, subject=subject)
        # Check permission that the user can view other profiles.
        if not request.user.has_perm('accounts.change_userprofile'):
            raise Http404()
        user = up.user
        name = _("Edit Basic Profile Information for %s" % (up))

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # update the user info
            user.username = data['username']
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            # update the user profile
            up.nickname = data['nickname']
            up.sex = data['sex']
            up.birth_date = data['birth_date']
            up.save()
            messages.success(request,
                             _('Pro settings have been updated.'))
            if subject:
                return HttpResponseRedirect(reverse('account_settings_subject', args=(subject,)))
            return HttpResponseRedirect(reverse('account_settings'))
        else:
            # the form had errors
            return render(request,
                          'account-settings.html',
                          {'form': form, 'name': name, 'up': up})

    # this is an HTTP GET
    form = AccountSettingsForm(
        initial={
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'email': user.email,
            'mobile_phone_number': up.mobile_phone_number,
            'sex': up.sex,
            'birth_date': up.birth_date,
            'nickname': up.nickname,
        }
    )
    return render(request,
                  'account-settings.html',
                  {'name': name, 'form': form, 'up': up})


def create_account(request, service_title=settings.APPLICATION_TITLE):
    name = _("Signup for %s") % (service_title)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # get the username and password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate user then login
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect_url = request.GET.get('next', reverse('home'))
            return HttpResponseRedirect(redirect_url)
        else:
            # return the bound form with errors
            return render(request,
                          'generic/bootstrapform.html',
                          {'name': name, 'form': form,
                           'service_title': service_title})
    else:
        # this is an HTTP  GET
        # Adding ability to pre-fill invitation_code and email
        # via GET paramters
        form_data = {'invitation_code': request.GET.get('invitation_code', ''),
                     'email': request.GET.get('email', '')}
        return render(request,
                      'generic/bootstrapform.html',
                      {'name': name, 'form': SignupForm(initial=form_data),
                       'service_title': service_title})


def password_reset_email_verify(request, reset_password_key=None):
    vprk = get_object_or_404(ValidPasswordResetKey,
                             reset_password_key=reset_password_key)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            vprk.user.set_password(form.cleaned_data['password1'])
            vprk.user.save()
            vprk.delete()
            logout(request)
            messages.success(request, _('Your password has been reset.'))
            return HttpResponseRedirect(reverse('mfa_login'))
        else:
            return render(request,
                          'generic/bootstrapform.html',
                          {'form': form,
                           'reset_password_key': reset_password_key})

    return render(request,
                  'generic/bootstrapform.html',
                  {'form': PasswordResetForm(),
                   'reset_password_key': reset_password_key})


def activation_verify(request, activation_key):
    if validate_activation_key(activation_key):
        messages.success(request,
                         'Your email has been verified.')
    else:
        messages.error(request,
                       'This key does not exist or has already been used.')
    return HttpResponseRedirect(reverse('mfa_login'))


def forgot_password(request):
    name = _('Forgot Password?')
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                u = User.objects.get(email=data['email'])
            except(User.DoesNotExist):
                try:
                    u = User.objects.get(username=data['email'])
                except(User.DoesNotExist):
                    messages.error(
                        request,
                        'A user with the email or username supplied '
                        'does not exist.')
                    return HttpResponseRedirect(reverse('forgot_password'))

            # success - user found so ask some question
            return HttpResponseRedirect(reverse('secret_question_challenge',
                                                args=(u.username,)))
        else:
            return render(request,
                          'generic/bootstrapform.html',
                          {'name': name, 'form': form})
    else:
        return render(request,
                      'generic/bootstrapform.html',
                      {'name': name, 'form': PasswordResetRequestForm()})
