from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '???????',
        "max_length":'??????2~20???',
        "min_length": '??????2~20???'
    })
    email = forms.EmailField(error_messages={"required": '??????', 'invalid': '???????????'})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('????????')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": '??????', 'invalid': '???????????'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)