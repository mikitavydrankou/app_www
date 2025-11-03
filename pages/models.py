from django.conf import settings
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PingRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ping_records',
    )
    domain = models.CharField(max_length=253)
    success = models.BooleanField(default=False)
    latency_ms = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = 'success' if self.success else 'failed'
        return f"{self.domain} ({status})"