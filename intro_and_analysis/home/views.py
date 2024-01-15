from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import VideoIntroduction
from django.conf import settings

from rest_framework.decorators import api_view
from .serializers import VideoIntroductionSerializer

from fer import FER
import cv2
import base64
import numpy as np

import os
import spacy
import assemblyai as aai

aai.settings.api_key = "e00a5d651cd84a23bac5d49d25370d5b"
nlp = spacy.load("en_core_web_sm")
emotion_detector = FER(mtcnn=True)


def extract_information(transcribed_text):
    doc = nlp(transcribed_text)

    name = None
    college_name = None
    hobbies = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "ORG" and not college_name:
            college_name = ent.text
        elif ent.label_ == "HOBBY":
            hobbies.append(ent.text)

    extracted_keywords = f"Name: {name}, College: {college_name}, Hobbies: {', '.join(hobbies)}"

    return extracted_keywords

def transcribe_audio(audio_url):
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_url, config)

    return transcript.text

def handle_uploaded_video(video_file):
    filename = 'recorded-video.webm'

    media_path = os.path.join(settings.MEDIA_ROOT, 'videos', filename)

    with open(media_path, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)

    return media_path

def analyze_facial_expression(video_path):
    cap = cv2.VideoCapture(video_path)
    unique_emotions = set()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_rgb = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        emotions = emotion_detector.detect_emotions(gray_frame_rgb)

        if emotions:
            dominant_emotion, _ = emotion_detector.top_emotion(gray_frame_rgb)
            unique_emotions.add(dominant_emotion)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    detected_emotions_string = "Detected Emotions from the video - " + ", ".join(unique_emotions)

    return detected_emotions_string

def generate_report(extracted_keywords, tab_switch_count, total_hidden_time, facial_expression_data):
    report_components = [
        f"Keywords: {extracted_keywords}",
        f"Tab Switch Count: {tab_switch_count}",
        f"Total Hidden Time: {total_hidden_time}",
        f"Facial Expression: {facial_expression_data}",
    ]

    return "\n".join(report_components)

@api_view(['POST'])
def upload_video(request):
    video_file = request.FILES.get('video-file')
    tab_switch_count = request.data.get('tabSwitchCount', 0)
    total_hidden_time = request.data.get('totalHiddenTime', 0) 
    
    video_path = handle_uploaded_video(video_file)

    transcribed_text = transcribe_audio(video_path)

    extracted_keywords = extract_information(transcribed_text)

    facial_expression_data = analyze_facial_expression(video_path)

    report = generate_report(extracted_keywords, tab_switch_count, total_hidden_time, facial_expression_data)

    serializer = VideoIntroductionSerializer(data={
        'video_file': video_file,
        'extracted_keywords' : extracted_keywords,
        'facial_expression_result' : facial_expression_data,
        'tab_switch_count': tab_switch_count,
        'total_hidden_time': total_hidden_time,
        'transcribed_text' : transcribed_text,
        'generated_report' : report,
    })

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failure'})

def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

def all_videos(request):
    videos = VideoIntroduction.objects.all()
    return render(request, 'all_videos.html', {'videos': videos})