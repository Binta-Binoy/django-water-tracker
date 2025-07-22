from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import SignUpForm, WaterIntakeForm, DateRangeForm
from .models import WaterIntake
from datetime import date

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('intake_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('intake_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def intake_list(request):
    intakes = WaterIntake.objects.filter(user=request.user)
    paginator = Paginator(intakes, 5)
    page = request.GET.get('page')
    intakes_page = paginator.get_page(page)
    return render(request, 'intake_list.html', {'intakes': intakes_page})

@login_required
def intake_create(request):
    today = date.today()
    if WaterIntake.objects.filter(user=request.user, date=today).exists():
        messages.error(request, "You've already added intake for today.")
        return redirect('intake_list')
    
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            intake = form.save(commit=False)
            intake.user = request.user
            intake.save()
            return redirect('intake_list')
    else:
        form = WaterIntakeForm()
    return render(request, 'intake_form.html', {'form': form})

@login_required
def intake_update(request, pk):
    intake = get_object_or_404(WaterIntake, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST, instance=intake)
        if form.is_valid():
            form.save()
            return redirect('intake_list')
    else:
        form = WaterIntakeForm(instance=intake)
    return render(request, 'intake_update.html', {'form': form})

@login_required
def intake_delete(request, pk):
    intake = get_object_or_404(WaterIntake, pk=pk, user=request.user)
    if request.method == 'POST':
        intake.delete()
        return redirect('intake_list')
    return render(request, 'intake_confirm_delete.html', {'intake': intake})

@login_required
def intake_difference(request):
    result = None
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            intakes = WaterIntake.objects.filter(user=request.user, date__range=(start, end))
            total = sum(i.quantity_ml for i in intakes)
            result = {'total': total, 'start': start, 'end': end}
    else:
        form = DateRangeForm()
    return render(request, 'difference.html', {'form': form, 'result': result})
