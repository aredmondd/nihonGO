from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

DEEPL_API_KEY = 'your-deepl-api-key'
DEEPL_API_URL = 'https://api-free.deepl.com/v2/translate'  # Adjust for pro users

def deepl_translate_view(request):
    translated_text = None
    if request.method == 'POST':
        input_text = request.POST.get('text')
        target_lang = request.POST.get('target_lang', 'EN')  # Default to English if no language is selected

        # Ensure only English and Japanese are allowed
        if target_lang not in ['EN', 'JA']:
            target_lang = 'EN'  # Fallback to English if an invalid option is passed

        # Prepare the DeepL API request
        data = {
            'auth_key': DEEPL_API_KEY,
            'text': input_text,
            'target_lang': target_lang
        }

        # Make the request to DeepL API
        response = requests.post(DEEPL_API_URL, data=data)

        # Parse the response from DeepL
        if response.status_code == 200:
            translated_text = response.json().get('translations')[0].get('text')

    return render(request, 'translate.html', {'translated_text': translated_text})