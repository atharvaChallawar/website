from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from website import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .forms import TemplateForm
from .models import template,product,contact
from django.contrib.auth.tokens import default_token_generator
#from django.contrib.auth import get_user_model

#User = get_user_model()


# Create your views here.
def home(request):
    allProducts = product.objects.all()
    context = {'products': allProducts}
    return render(request, "index.html",context)

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        # Create a new Contact object and save it to the database
        contact = Contact.objects.create(name=name, email=email, description=description)
        return render(request, 'success.html', {'name': name}) 
    return render(request, "contact.html")

def search(request):
    return render(request, "search.html")

def productView(request,myid):
    productna = product.objects.filter(productId = myid)
    context={'product':productna[0]}

    return render(request, "productView.html",context)

def checkout(request):
    return render(request, "checkout.html")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if User.objects.filter(username=email):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        
        if password != password2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        
        myuser = User.objects.create_user(username =email,password = password)
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email - Django Login!!"
        message2 = render_to_string('email.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.username],
        )
        email.fail_silently = True
        email.send()

        return render(request, "signin.html")

    
    return render(request, "signup.html")
        

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request,username=username, password=password)
        print(user)

        if user is None:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
        else:
            login(request, user)
            allProducts = product.objects.all()
            context = {'products': allProducts}
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "index.html",context)
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def upload_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            template = Template(name=name, pdf_file=request.FILES['pdf_file'])
            template.save()
            return redirect('home')  # Redirect to a success page
    else:
        form = TemplateForm()

    return render(request, 'upload_template.html', {'form': form})


def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(username=email).first()
        if user:
            current_site = get_current_site(request)
            email_subject = "Password Reset"
            message = render_to_string('forgetemail.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.username],
            )
            email.send()
            messages.success(request, "Password reset email sent successfully!")
            return redirect('signin')
        else:
            messages.error(request, "Email Not Registered!!")
            return redirect('signup')
    
    return render(request, "ForgotPassword.html")

def change(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and default_token_generator.check_token(myuser, token):
        if request.method == 'POST':
            password = request.POST.get('new_password')
            password2 = request.POST.get('confirm_password')
            if password != password2:
                messages.error(request, "Passwords don't match!")
                return redirect('reset_password')

            # Update password using set_password() method
            myuser.set_password(password)
            myuser.is_active = True
            myuser.save()

            # Log the user in after password change
            login(request, myuser)

            messages.success(request, "Your password has been changed successfully!")
            return redirect('signin')
        else:
            # Render password reset form
            return render(request, 'reset_password.html')
    else:
        # Invalid user or token, render failure page
        return render(request, 'reset_password_failure.html')