from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ComplaintForm
from .models import Complaint


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            return render(request, 'complaints/register.html', {'error': 'Username and password are required.'})
        if password != confirm_password:
            return render(request, 'complaints/register.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'complaints/register.html', {'error': 'Username already exists.'})

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'complaints/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url or 'dashboard')

        return render(request, 'complaints/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'complaints/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    context = {
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='Pending').count(),
        'resolved_complaints': complaints.filter(status='Resolved').count(),
    }
    return render(request, 'complaints/dashboard.html', context)


@login_required
def report_issue(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Complaint submitted successfully.')
            return redirect('my_complaints')
    else:
        form = ComplaintForm()

    return render(request, 'complaints/report_issue.html', {'form': form})


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints})


@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    complaints = Complaint.objects.select_related('user').order_by('-created_at')
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(status='Pending').count(),
        'in_progress': complaints.filter(status='In Progress').count(),
        'resolved': complaints.filter(status='Resolved').count(),
    }
    return render(request, 'complaints/admin_dashboard.html', {'complaints': complaints, 'stats': stats})


@login_required
def admin_complaint_detail(request, complaint_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        complaint.status = request.POST.get('status', complaint.status)
        complaint.admin_update = request.POST.get('admin_update', '').strip()
        if request.FILES.get('resolved_image'):
            complaint.resolved_image = request.FILES['resolved_image']
        complaint.save()
        messages.success(request, 'Complaint updated successfully.')
        return redirect('admin_complaint_detail', complaint_id=complaint.id)

    return render(request, 'complaints/admin_complaint_detail.html', {'complaint': complaint})
