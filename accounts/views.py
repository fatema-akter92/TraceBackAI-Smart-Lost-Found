from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileUpdateForm
from items.models import ItemReport, ClaimRequest
from matching.models import MatchRecord, MatchNotification


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to TraceBack BD, {user.username}! Your account is now active.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors in the registration form.")
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    my_lost_reports = ItemReport.objects.filter(user=user, report_type='lost').order_by('-created_at')
    my_found_reports = ItemReport.objects.filter(user=user, report_type='found').order_by('-created_at')
    my_claims = ClaimRequest.objects.filter(claimant=user).order_by('-created_at')
    
    # Matches related to user's lost items
    my_lost_ids = my_lost_reports.values_list('id', flat=True)
    potential_matches = MatchRecord.objects.filter(
        lost_item_id__in=my_lost_ids,
        similarity_score__gte=40.0
    ).select_related('lost_item', 'found_item').order_by('-similarity_score')[:8]

    # Desk staff info if applicable
    desk_count = 0
    if user.is_desk_staff:
        from custody.models import CustodyRecord
        desk_count = CustodyRecord.objects.filter(desk__manager=user).count()

    context = {
        'my_lost_reports': my_lost_reports,
        'my_found_reports': my_found_reports,
        'my_claims': my_claims,
        'potential_matches': potential_matches,
        'desk_count': desk_count,
    }
    return render(request, 'accounts/dashboard.html', context)
