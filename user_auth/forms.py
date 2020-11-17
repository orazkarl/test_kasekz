from allauth.account.forms import SignupForm, LoginForm
from django import forms


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    # last_name = forms.CharField(label='Last Name', max_length=50,
    #                             widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'remember':
                visible.field.widget.attrs['class'] = ''
            # visible.label = None