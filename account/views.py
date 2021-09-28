from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Registration of a new user"""
    if request.method != 'POST':
        # A blank registration form
        form = UserCreationForm()
    else:
        # Empty form processing
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            return redirect('account:login')

    # Return an empty or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
