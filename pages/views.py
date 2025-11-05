import time
from datetime import datetime

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import PentestForm
from .models import PentestRecord


PING_TIMEOUT_SECONDS = 4
MAX_WAIT_TIME = 30  # Maximum wait time for result in seconds
POLL_INTERVAL = 0.5  # Task status check interval in seconds

OPERATION_ENDPOINTS = {
    'ping': '/ping',
    'port_scan': '/port-scan',
    'dns_lookup': '/dns-lookup',
    'http_headers': '/http-headers',
}


def execute_pentest_operation(user, target, operation, ports=None):
    """
    Executes one pentest operation and returns the record
    """
    record = PentestRecord.objects.create(
        user=user,
        target=target,
        operation=operation,
        status='pending',
    )
    
    try:
        endpoint = OPERATION_ENDPOINTS[operation]
        api_url = f"{settings.PENTEST_API_BASE_URL}{endpoint}"
        
        if operation == 'ping':
            payload = {'target': target, 'timeout': PING_TIMEOUT_SECONDS}
        elif operation == 'port_scan':
            payload = {'target': target, 'ports': ports or '80,443,22,21,25'}
        elif operation == 'dns_lookup':
            payload = {'domain': target}
        elif operation == 'http_headers':
            url = target if target.startswith(('http://', 'https://')) else f'http://{target}'
            payload = {'url': url}
        else:
            raise ValueError(f'Unknown operation: {operation}')
        
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        task_data = response.json()
        task_id = task_data.get('task_id')
        
        if not task_id:
            raise ValueError('No task_id received from API')
        
        record.task_id = task_id
        record.status = 'progress'
        record.save()
        
        start_time = time.time()
        while time.time() - start_time < MAX_WAIT_TIME:
            result_response = requests.get(
                f"{settings.PENTEST_API_BASE_URL}/task/{task_id}",
                timeout=5,
            )
            result_response.raise_for_status()
            task_result = result_response.json()
            
            if task_result['status'] == 'SUCCESS':
                result = task_result.get('result', {})
                record.status = 'success'
                record.success = result.get('success', False)
                record.result_data = result
                
                if operation == 'ping':
                    record.latency_ms = result.get('latency_ms')
                
                record.error_message = result.get('error') or ''
                record.completed_at = timezone.now()
                record.save()
                return record, None  # Success
            
            elif task_result['status'] == 'FAILURE':
                record.status = 'failed'
                record.error_message = task_result.get('error', 'Task failed')
                record.completed_at = timezone.now()
                record.save()
                return record, record.error_message  # Error
            
            time.sleep(POLL_INTERVAL)
        
        record.status = 'failed'
        record.error_message = 'Timeout waiting for result'
        record.completed_at = timezone.now()
        record.save()
        return record, 'Timeout'
    
    except Exception as exc:
        record.status = 'failed'
        record.error_message = str(exc)
        record.completed_at = timezone.now()
        record.save()
        return record, str(exc)


def home(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PentestForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            operations = form.cleaned_data['operations']
            ports = form.cleaned_data.get('ports')
            
            success_count = 0
            error_count = 0
            
            for operation in operations:
                record, error = execute_pentest_operation(
                    user=request.user,
                    target=target,
                    operation=operation,
                    ports=ports,
                )
                
                if error:
                    error_count += 1
                else:
                    success_count += 1
            
            if success_count > 0 and error_count == 0:
                messages.success(
                    request,
                    f'All operations ({success_count}) for {target} completed successfully!',
                )
            elif success_count > 0 and error_count > 0:
                messages.warning(
                    request,
                    f'{success_count} operations completed, {error_count} failed for {target}',
                )
            else:
                messages.error(
                    request,
                    f'All operations ({error_count}) failed for {target}',
                )
            
            return redirect('home')
    else:
        form = PentestForm()

    pentest_history = None
    if request.user.is_authenticated:
        pentest_history = request.user.pentest_records.all()

    context = {
        'form': form,
        'pentest_history': pentest_history,
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