from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from .models import CMUserBase
from .forms import RegistrationForm, UserEditForm
from .token import acc_activation_token


def register(request):
    """Registration of a new user"""
    if request.method != 'POST':
        # A blank registration form
        form = RegistrationForm()
    else:
        # Empty form processing
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Setup an email
            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string(
                'account/registration/acc_activation.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': acc_activation_token.make_token(user),
                }
            )
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/activation_message_page.html')

    # Return an empty or invalid form
    context = {'form': form}
    return render(request, 'account/registration/register.html', context)

def acc_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CMUserBase.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user != None and acc_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        print(user, uidb64)
        return render(request, 'account/registration/activation_invalid.html')

@login_required
def dashboard(request):
    # orders = user_orders(request)
    # context = {'section': 'profile', 'orders': orders}
    return render(request, 'account/user/dashboard.html')#, context)

@login_required
def edit_info(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {'user_form': user_form}
    return render(request, 'account/user/edit_info.html', context)

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = CMUserBase.objects.get(email=request.user)
        user.is_active = False
        user.save()
        logout(request)
        return redirect('account:delete_confirmation')