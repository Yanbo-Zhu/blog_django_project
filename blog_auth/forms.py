from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Please enter username!',
        "max_length": 'the length of username should be between 2 and 20!',
        "min_length": 'the length of username should be between 2 and 20!'
    })
    email = forms.EmailField(error_messages={"required": 'please enter email addresse', 'invalid': 'please enter a valid email address'})
    password = forms.CharField(max_length=20, min_length=8,  error_messages={
        'required': 'Please enter password!',
        "max_length": 'the length of username should be between 8 and 20!',
        "min_length": 'the length of username should be between 8 and 20!'
    })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('The email has been registered!')
        return email


class LoginForm(forms.Form):
    print(User)
    #email = forms.EmailField(error_messages={"required": 'please enter email addresse', 'invalid': 'please enter a valid email address'})
    username = forms.CharField(error_messages={"required": 'please enter username', 'invalid': 'please enter a valid username'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)