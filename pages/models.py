from django.conf import settings
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PentestRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('progress', 'In Progress'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    OPERATION_CHOICES = [
        ('ping', 'Ping'),
        ('port_scan', 'Port Scan'),
        ('dns_lookup', 'DNS Lookup'),
        ('http_headers', 'HTTP Headers'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pentest_records',
    )
    target = models.CharField(max_length=253, help_text='Domain or IP address')
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    success = models.BooleanField(default=False)
    
    latency_ms = models.FloatField(null=True, blank=True, help_text='For ping operation')
    result_data = models.JSONField(null=True, blank=True, help_text='Full result data')
    error_message = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pentest Record'
        verbose_name_plural = 'Pentest Records'

    def __str__(self):
        return f"{self.target} - {self.get_operation_display()} ({self.get_status_display()})"
    
    def get_result_summary(self):
        """Returns brief result description"""
        if self.operation == 'ping' and self.success and self.latency_ms:
            return f"{self.latency_ms:.2f} ms"
        elif self.operation == 'port_scan' and self.result_data:
            return "Scan completed"
        elif self.operation == 'dns_lookup' and self.result_data:
            return "DNS records retrieved"
        elif self.operation == 'http_headers' and self.result_data:
            return f"Status: {self.result_data.get('status', 'N/A')}"
        return self.error_message or 'No data'


class PingRecord(PentestRecord):
    class Meta:
        proxy = True
        verbose_name = 'Ping Record (Legacy)'