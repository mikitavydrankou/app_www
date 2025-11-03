from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from ping3 import ping

from .forms import PingForm
from .models import PingRecord


PING_TIMEOUT_SECONDS = 4


def home(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PingForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            try:
                latency_ms = ping(
                    domain,
                    timeout=PING_TIMEOUT_SECONDS,
                    unit='ms',
                )
            except Exception as exc:  
                PingRecord.objects.create(
                    user=request.user,
                    domain=domain,
                    success=False,
                    error_message=str(exc) or 'Error.',
                )
                messages.error(request, f'Cant check {domain}: {exc or "error"}')
            else:
                if latency_ms is None or latency_ms is False:
                    PingRecord.objects.create(
                        user=request.user,
                        domain=domain,
                        success=False,
                        error_message='No response from host.',
                    )
                    messages.warning(request, f'Host {domain} did not respond.')
                else:
                    PingRecord.objects.create(
                        user=request.user,
                        domain=domain,
                        success=True,
                        latency_ms=float(latency_ms),
                    )
                    messages.success(
                        request,
                        f'Ping {domain} took {float(latency_ms):.2f} ms.',
                    )
            return redirect('home')
    else:
        form = PingForm()

    ping_history = None
    if request.user.is_authenticated:
        ping_history = request.user.ping_records.all()

    context = {
        'form': form,
        'ping_history': ping_history,
    }
    return render(request, 'pages/home.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})