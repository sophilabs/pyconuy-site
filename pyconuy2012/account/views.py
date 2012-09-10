from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as aviews
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def profile(request):
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.instance.username = form.cleaned_data['username']
            form.instance.first_name = form.cleaned_data['first_name']
            form.instance.last_name = form.cleaned_data['last_name']
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile updated successfully.')
            return HttpResponseRedirect('')
    else:
        form = forms.ProfileForm(instance=request.user)
    return render_to_response('profile.html', {
        'form' : form
    }, context_instance=RequestContext(request))

def sign(request, next_page=None):
    sign_up = forms.UserCreationForm()
    sign_in = forms.AuthenticationForm()
    if request.method == 'POST':
        if 'sign_in' in request.POST:
            sign_in = forms.AuthenticationForm(data=request.POST)
            if sign_in.is_valid():
                login(request, sign_in.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                return HttpResponseRedirect(next_page or reverse('account:profile'))
        else:
            sign_up = forms.UserCreationForm(data=request.POST)
            if sign_up.is_valid():
                sign_up.instance.email = sign_up.cleaned_data['username']
                sign_up.save()
                authenticate(username=sign_up.instance.username, password=sign_up.instance.password)
                return HttpResponseRedirect(next_page or reverse('account:profile'))
    request.session.set_test_cookie()
    return render_to_response('sign.html',{
        'sign_up' : sign_up,
        'sign_in': sign_in
    }, context_instance=RequestContext(request))

def sign_up(request, next_page=None):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.instance.email = form.cleaned_data['username']
            form.save()
            authenticate(username=form.instance.username, password=form.instance.password)
            return HttpResponseRedirect(next_page or reverse('account:profile'))
    else:
        form = forms.UserCreationForm()
    return render_to_response('sign_up.html',{
        'form' : form
        }, context_instance=RequestContext(request))

def sign_in(request):
    return aviews.login(request,
        template_name="sign_in.html",
        authentication_form=forms.AuthenticationForm,
        extra_context={})

def sign_out(request, next_page=None):
    return aviews.logout(request, next_page=next_page or reverse('main:index'))

def password_reset(request):
    return aviews.password_reset(request, is_admin_site=False,
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        password_reset_form=forms.PasswordResetForm,
        post_reset_redirect=reverse('account:password_reset_done'),
        extra_context={})

def password_reset_done(request):
    return aviews.password_reset_done(request,
        template_name='password_reset_done.html',
        extra_context={})

def password_reset_complete(request):
    return aviews.password_reset_complete(request,
        template_name='password_reset_complete.html',
        extra_context={})

def password_reset_confirm(request, uidb36, token, post_reset_redirect=None):
    return aviews.password_reset_confirm(request, uidb36, token,
        template_name='password_reset_confirm.html',
        set_password_form=forms.SetPasswordForm,
        post_reset_redirect=post_reset_redirect or reverse('account:password_reset_complete'),
        extra_context={})

def password_reset_complete(request):
    return aviews.password_reset_complete(request,
        template_name='password_reset_complete.html')

def password_change(request):
    return aviews.password_change(request,
        template_name='password_change_form.html',
        post_change_redirect=reverse('account:password_change_done'),
        password_change_form=forms.PasswordChangeForm,
        extra_context={})

def password_change_done(request):
    return aviews.password_change_done(request,
        template_name='password_change_done.html',
        extra_context={})