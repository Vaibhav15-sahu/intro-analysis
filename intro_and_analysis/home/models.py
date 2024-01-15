# video_app/models.py
from django.db import models
from django.contrib.auth.models import User

class VideoIntroduction(models.Model):
    video_file = models.FileField(upload_to='videos/')
    facial_expression_result = models.CharField(max_length=255, default='NULL')
    extracted_keywords = models.TextField(default='NULL')
    tab_switch_count = models.IntegerField(default=0)
    total_hidden_time = models.IntegerField(default=0)
    transcribed_text = models.TextField(blank=True, null=True)
    generated_report = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
