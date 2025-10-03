

# Create your views here.
# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect admin users to admin_dashboard
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')  # make sure this URL name exists
            else:
                return redirect('home')  # normal user redirected to home
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from .models import Contribution

@login_required
def profile(request):
    contributions = Contribution.objects.filter(user=request.user).order_by('-year', '-month')
    return render(request, 'profile.html', {'contributions': contributions})

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContributionForm

def admin_check(user):
    return user.is_staff

@login_required
@user_passes_test(admin_check)
def add_contribution(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contribution added successfully!")
            return redirect('add_contribution')
    else:
        form = ContributionForm()
    return render(request, 'add_contribution.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Contribution

def is_admin(user):
    return user.is_superuser  # or use user.is_staff if appropriate

from .forms import ContributionFilterForm

@user_passes_test(is_admin)
def admin_dashboard(request):
    form = ContributionFilterForm(request.GET or None)
    contributions = Contribution.objects.all().order_by('-year', '-month')

    if form.is_valid():
        user = form.cleaned_data.get('user')
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')

        if user:
            contributions = contributions.filter(user=user)
        if month:
            contributions = contributions.filter(month=month)
        if year:
            contributions = contributions.filter(year=year)

    members = User.objects.all()

    context = {
        'members': members,
        'contributions': contributions,
        'filter_form': form,
    }
    return render(request, 'admin_dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoanInquiryForm

@login_required
def loan_inquiry_view(request):
    if request.method == 'POST':
        form = LoanInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            return redirect('home')  # or a "thank you" page
    else:
        form = LoanInquiryForm()

    return render(request, 'loan_inquiry.html', {'form': form})
