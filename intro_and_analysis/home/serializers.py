# video_app/serializers.py
from rest_framework import serializers
from .models import VideoIntroduction

class VideoIntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoIntroduction
        fields = ['video_file', 'extracted_keywords', 'facial_expression_result', 'tab_switch_count', 'total_hidden_time', 'transcribed_text', 'generated_report']
