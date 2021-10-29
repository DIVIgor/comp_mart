from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import CMUserBase


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First name', min_length=4,
        max_length=100, help_text='Required'
    )
    last_name = forms.CharField(
        label='Last name', min_length=4,
        max_length=100, help_text='Required'
    )
    phone_num = forms.CharField(
        label='Phone number', min_length=10,
        max_length=15, help_text='Required'
    )
    email = forms.EmailField(
        label='Enter an Email', max_length=100,
        help_text='Required',
        error_messages={'required': 'You need to fill an email field'}
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    acc_password = forms.CharField(
        label='Confirm the password', widget=forms.PasswordInput
    )

    class Meta:
        model = CMUserBase
        fields = ('first_name', 'last_name', 'phone_num', 'email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        email_filter = CMUserBase.objects.filter(email=email)
        if email_filter.exists():
            raise forms.ValidationError(
                'A user with this email already registered'
            )
        return email

    def clean_phone_num(self):
        pn = self.cleaned_data['phone_num']
        if not pn.isdigit():
            raise forms.ValidationError(
                'Phone number should contain only digits'
            )
        return pn

    def clean_acc_password(self):
        pw = self.cleaned_data
        if pw['password'] != pw['acc_password']:
            raise forms.ValidationError("Passwords don't match.")
        return pw['acc_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'First name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Last name'
        })
        self.fields['phone_num'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Phone number'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Email', 'name': 'email',
            'id': 'id_email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Password'
        })
        self.fields['acc_password'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Confirm password'
        })

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Email',
        'id': 'login-email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Password',
        'id': 'login-pwd'
    }))

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email (can not be changed)', max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'email',
            'id': 'form-email', 'readonly': 'readonly'
            }),
    )

    first_name = forms.CharField(
        label='First name',
        min_length=4,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'First name',
            'id': 'form-firstname'
        })
    )

    last_name = forms.CharField(
        label='Last name',
        min_length=4,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Last name',
            'id': 'form-lastname'
        })
    )

    phone_num = forms.CharField(
        label='Phone number',
        min_length=10,
        max_length=15,
        widget=forms.NumberInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Phone number',
            'id': 'form-phone_num'
        })
    )

    class Meta:
        model = CMUserBase
        fields = ('email', 'first_name', 'last_name', 'phone_num')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Email',
            'id': 'form-email'
        })
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        usr = CMUserBase.objects.filter(email=email)
        if not usr:
            raise forms.ValidationError('Unknown Email')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New password',
                'id': 'form-new_password1'
            }
        )
    )
    new_password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Confirm new password',
                'id': 'form-new_password2'
            }
        )
    )