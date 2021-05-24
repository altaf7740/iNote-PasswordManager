from cryptography import fernet
from django.shortcuts import render, redirect
from . import email_sender
from .models import Registration, Credential
from .forms import LoginForm, SignupForm, CredentialForm, CredentialForm2
from django.views import generic

import json
import requests
import random
import hashlib
from .keyGenerator import key_generator
from cryptography.fernet import Fernet


# generating, storing in session and send the otp
def otp_generate(request,email):
    otp = random.randint(100000,999999)
    request.session["otp"]=otp
    data = f"your OTP : {otp}\nPlease provide this otp to login to your account.\nThis is system generated email, please do not reply to this mail id."
    email_sender.send(data,email)

def validate_otp(request):
    if request.POST:
        otp = request.POST.get('otp')
        if otp==str(request.session['otp']) and captcha_verify(request):
            user = Registration.objects.get(id=request.session.get('userid'))
            request.session['name'] = user.firstname + " " + user.lastname
            
            return redirect('../dashboard')

    return render(request, "app/otp.html") 

# captcha verify
def captcha_verify(request):
	CLIENT_KEY = request.POST["g-recaptcha-response"]
	SECRET_KEY = "your-secret-key"
	captcha_data = {'secret':SECRET_KEY, 'response':CLIENT_KEY}
	response = requests.post("https://www.google.com/recaptcha/api/siteverify",data=captcha_data)
	str_response = json.loads(response.text)
	return str_response["success"]



# Create your views here.
def home(request):
    return render(request, "app/homepage.html", {'name':request.session.get('name',None)})

def contact(request):
    return render(request, "app/contact.html", {'name':request.session.get('name',None)})

def about(request):
    return render(request, "app/about.html", {'name':request.session.get('name',None)})

def send_mail(request):
    if request.POST and captcha_verify(request):
        name, email, body, seo = request.POST.get("username"),request.POST.get("email"),request.POST.get("problem"),request.POST.get("curious")
        msg = f"""Name : {name}\nEmail : {email}\n \nMessage : {body}\n\nSeo : {seo}\n 
        """
        email_sender.send(msg)
    return render(request, "app/thankyou-for-contact.html")

def login(request):
    if request.session.get('name') is not None:
        return redirect('../')
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid() and captcha_verify(request):
            user = Registration.objects.get(email=form.cleaned_data['email'])
            if user.password  == hashlib.md5((form.cleaned_data['password']).encode()).hexdigest() :
                request.session['userid'] = user.id
                request.session['key'] =  key_generator(form.cleaned_data['password']).decode()
                otp_generate(request,form.cleaned_data['email'])
                return validate_otp(request)
            else:
                print('invalid')
    return render(request,'app/login.html',{'form':form})

def thankyou(request):
    return render(request, 'app/thankyou.html')

def logout(request):
    try:
        del request.session['name']
        del request.session['userid']
        del request.session['key']
        del request.session['otp']
    finally:
        return redirect('../')

class Signup(generic.CreateView):
    form_class = SignupForm
    template_name = "app/signup.html"
    success_url = '/thankyou'

    def get(self, request, *args, **kwargs):
        if request.session.get('name') is not None:
            return redirect('../')
        self.object = None
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if  captcha_verify(request):
            request.POST = request.POST.copy()
            request.POST['password'] = hashlib.md5(request.POST.get('password').encode()).hexdigest()
            return super().post(request, *args, **kwargs)
        return redirect('../')





class Dashboard(generic.View):
    def get(self,request):
        if request.session.get('name') is not None:
            form = CredentialForm()
            fernet = Fernet((request.session.get('key')).encode())
            credential = Credential.objects.filter(userid_id=request.session.get('userid'))
            for cred in credential:
                cred.password = (fernet.decrypt((cred.password).encode())).decode()
            return render(request, 'app/dashboard.html', {'name':request.session.get('name',None),  'credential':credential, 'form':form})
        return redirect('../login')
    
    def post(self,request):
        form = CredentialForm(request.POST)        
        if form.is_valid() and captcha_verify(request):
            fernet = Fernet((request.session.get('key')).encode())
            form.cleaned_data['userid_id'] = int(request.session.get('userid'))
            form.cleaned_data['password'] = (fernet.encrypt((form.cleaned_data['password']).encode())).decode()
            Credential.objects.create(**form.cleaned_data)
        return redirect('../dashboard')



def UpdateCredential(request,pk):
    creds = Credential.objects.get(id=pk)
    form = CredentialForm2(request.POST, instance=creds)  
    
    print(request.POST)      
    if form.is_valid():
        fernet = Fernet((request.session.get('key')).encode())
        creds.username, creds.password, creds.website = form.cleaned_data['username'], (fernet.encrypt((form.cleaned_data['password']).encode())).decode(), form.cleaned_data['website']
        creds.save()
    return redirect('../dashboard')
    
class DeleteCredential(generic.DeleteView):
    success_url='/dashboard'
    model=Credential

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def account(request):
    user_info = Registration.objects.get(id=request.session.get('userid'))
    if request.POST:
        user_info.firstname, user_info.lastname, user_info.email = request.POST.get('firstname'), request.POST.get('lastname'), request.POST.get('email')
        if request.POST.get('password') != "":
            fernet = Fernet((request.session.get('key')).encode())
            credential = Credential.objects.filter(userid_id=request.session.get('userid'))
            request.session['key'] =  key_generator(request.POST.get('password')).decode()
            new_fernet = Fernet((request.session.get('key')).encode())
            for cred in credential:
                temp_password = (fernet.decrypt((cred.password).encode())).decode()
                cred.password = (new_fernet.encrypt(temp_password.encode())).decode()
                cred.save()
            user_info.password = hashlib.md5(request.POST.get('password').encode()).hexdigest() 
        user_info.save()
    firstname,lastname,email = user_info.firstname,user_info.lastname,user_info.email
    return render(request, "app/account.html",{'firstname':firstname,'lastname':lastname,'email':email})

def accountDelete(request):
    user = Registration.objects.get(id=request.session.get('userid'))  
    user.delete()
    return redirect("/logout")
