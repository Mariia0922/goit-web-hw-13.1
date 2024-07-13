from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
import uuid
from django.core.mail import send_mail
from .models import EmailVerification
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
import cloudinary
from cloudinary import CloudinaryImage



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'quotes_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quotes_app/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(...)  # додайте ваш код
        token = str(uuid.uuid4())
        EmailVerification.objects.create(user=user, token=token)
        send_mail(
            'Verify your email',
            f'Use this token to verify your email: {token}',
            'from@example.com',
            [user.email],
        )
        return redirect('email-verification-sent')

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        verification.is_verified = True
        verification.save()
        return redirect('verification-success')
    except EmailVerification.DoesNotExist:
        return redirect('verification-failed')

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'quotes_app/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.added_by = request.user
            quote.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'quotes_app/add_quote.html', {'form': form})

    
@ratelimit(key='user', rate='5/m', method='POST', block=True)
def create_contact(request):
    pass

@login_required
def update_avatar(request):
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        upload_result = cloudinary.uploader.upload(avatar_file)
        request.user.profile.avatar_url = upload_result['secure_url']
        request.user.profile.save()
        return redirect('avatar-update-success')