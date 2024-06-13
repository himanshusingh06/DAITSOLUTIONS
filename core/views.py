from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage 
from django.conf import settings
from .models import UserProfile, UserService, Service
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def home(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'landing.html', {'user': user})


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if username or email already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists!")
            return redirect('login')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('login')
        elif pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!")
            return redirect('login')
        else:
            # Create new user
            my_user = User(username=uname, email=email, first_name=first_name, last_name=last_name)
            my_user.set_password(pass1)  # Use set_password() to properly hash the password
            my_user.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check if user exists
        if user is None:
            messages.error(request, "Invalid UserName or Password.")
        else:
            # User exists, check password
            if user.check_password(password):
                # Password is correct, log in user
                auth.login(request, user)
                return redirect('home')
            else:
                # Incorrect password
                messages.error(request, "Invalid UserName or Password.")


    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')






def send_mail_to_admin(user_name, user_email, mobile_number,subject,user_message):
    
    message_body = f'Form filled by {user_name}--- with the email {user_email}.\n\nMobile number -- {mobile_number}\n\nThe Message provided is :\n {user_message}'
    message = EmailMessage(
        subject=f'New form filled by {user_name}--- with subject {subject}',
        body=message_body,
        from_email=settings.EMAIL_HOST_USER,
        to=['himanshusinghwork365@gmail.com']
    )
    message.send()

def contact_form_submission(request):
    if request.method== 'POST':
        user_name=request.POST.get('name')
        user_email=request.POST.get('email')
        mobile_number=request.POST.get('mobile_number')
        subject=request.POST.get('subject')
        user_message=request.POST.get('message')
        send_mail_to_admin(user_name, user_email, mobile_number,subject,user_message)
        return redirect('home')
    
@login_required(login_url='login')
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    services = UserService.objects.filter(user=request.user)
    if request.method == "POST":
        if 'service_name' in request.POST and 'customer_description' in request.POST:
            service_name = request.POST['service_name']
            customer_description = request.POST['customer_description']
            # Create or get the service
            service, created = Service.objects.get_or_create(name=service_name)
            # Create UserService
            UserService.objects.create(user=request.user, service=service, customer_description=customer_description)
            return redirect('dashboard')
        elif 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            profile.profile_picture.save(profile_picture.name, profile_picture)
            return redirect('dashboard')
    context = {'profile': profile, 'services': services}
    return render(request, 'dashboard.html', context)




# Check if the user is admin
def is_admin(user):
    return user.is_superuser
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    query = request.GET.get('q')
    if query:
        users = users.filter(username__icontains=query)
    return render(request, 'admin_dashboard.html', {'users': users})
@login_required(login_url='login')
@user_passes_test(is_admin)
def user_services(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    services = UserService.objects.filter(user=user)
    return render(request, 'user_services.html', {'user': user, 'services': services})
@login_required(login_url='login')
@user_passes_test(is_admin)
def update_service_status(request, service_id):
    service = get_object_or_404(UserService, id=service_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        details = request.POST.get('details')
        service.status = status
        service.details = details
        service.save()
        return redirect('user_services', user_id=service.user.id)
    return render(request, 'update_service_status.html', {'service': service})
