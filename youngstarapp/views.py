from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def home_view(request):
    return render(request, 'home.html')
def rules(request):
    return render(request, 'rules.html')
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

from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Contribution

@login_required
def profile(request):
    # Total contributed by this user
    user_total = Contribution.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Total pool contributed by all members
    total_contributed = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Calculate share percentage
    percentage = (user_total / total_contributed * 100) if total_contributed > 0 else 0

    # Get all contributions of the user
    contributions = Contribution.objects.filter(user=request.user).order_by('-year', '-month')

    context = {
        'contributions': contributions,
        'total_contributed': user_total,  # match template variable
        'percentage': round(percentage, 2),
    }

    return render(request, 'profile.html', context)

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
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Contribution
from .forms import ContributionFilterForm


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    form = ContributionFilterForm(request.GET or None)
    contributions = Contribution.objects.all().order_by('-year', '-month')

    # APPLY FILTERS
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

    # TOTAL POOL
    total_contributed = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # MEMBER SHARES
    shares = []
    for member in User.objects.all():
        member_total = Contribution.objects.filter(
            user=member
        ).aggregate(total=Sum('amount'))['total'] or 0

        percentage = (
            (member_total / total_contributed) * 100
            if total_contributed > 0 else 0
        )

        shares.append({
            'user': member,
            'total_contributed': member_total,
            'percentage': round(percentage, 2),
        })

    context = {
        'contributions': contributions,
        'filter_form': form,
        'total_contributed': total_contributed,
        'shares': shares,
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

from django.db.models import Sum
from .models import Contribution
from django.contrib.auth.models import User

def calculate_member_shares():
    total_contributed = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    members = User.objects.all()
    shares = []

    for member in members:
        member_total = Contribution.objects.filter(
            user=member
        ).aggregate(total=Sum('amount'))['total'] or 0

        percentage = (
            (member_total / total_contributed) * 100
            if total_contributed > 0 else 0
        )

        shares.append({
            'user': member,
            'total_contributed': member_total,
            'percentage': round(percentage, 2),
        })

    return total_contributed, shares

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Contribution
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Contribution
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum

@login_required
@user_passes_test(lambda u: u.is_superuser)
def member_detail(request, user_id):
    member = get_object_or_404(User, id=user_id)
    contributions = Contribution.objects.filter(user=member).order_by('-year', '-month')
    total_contributed = contributions.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'member': member,
        'contributions': contributions,
        'total_contributed': total_contributed,
    }
    return render(request, 'member_detail.html', context)


from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')

        if 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Password updated successfully.')
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form
    }
    return render(request, 'edit_profile.html', context)
