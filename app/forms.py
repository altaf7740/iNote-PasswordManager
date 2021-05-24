from django import forms
from django.forms import fields
from .models import Registration, Credential

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'exampleInputEmail1'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['id'] = 'exampleInputPassword1'

class SignupForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = "__all__"
        widgets = {
        'password': forms.PasswordInput()
    }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs['class'] = 'form-control'
        self.fields['firstname'].widget.attrs['id'] = 'firstname'
        self.fields['lastname'].widget.attrs['class'] = 'form-control'
        self.fields['lastname'].widget.attrs['id'] = 'lastname'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'exampleInputEmail1'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['id'] = 'exampleInputPassword1'
        self.fields['password'].widget.attrs['pattern'] = """^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{7,15}$"""
        self.fields['password'].widget.attrs['title'] = "must contains number + Special symbol + Lowercase + Uppercase character and lenght >= 8"
        


class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        exclude = ('userid',) 
        widgets = {
        'password': forms.PasswordInput(),}

    def __init__(self, *args, **kwargs):
        super(CredentialForm, self).__init__(*args, **kwargs)
        self.fields['website'].widget.attrs['class'] = 'form-control'
        self.fields['website'].widget.attrs['id'] = 'websitefield'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'usernamefield'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['id'] = 'passwordfield'
            

class CredentialForm2(forms.ModelForm):
    class Meta:
        model = Credential
        exclude = ('userid',)
        

    def __init__(self, *args, **kwargs):
        super(CredentialForm2, self).__init__(*args, **kwargs)
        self.fields['website'].widget.attrs['class'] = 'form-control'
        self.fields['website'].widget.attrs['id'] = 'websitefield'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'usernamefield'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['id'] = 'passwordfield'
        
                        