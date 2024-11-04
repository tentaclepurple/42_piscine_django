# ex02/views.py
import os
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import TextInputForm
from django.conf import settings


def ex02_view(request):
    form = TextInputForm()
    history = []

    if os.path.exists(settings.LOGS_FILE_PATH):
        with open(settings.LOGS_FILE_PATH, 'r') as file:
            for line in file:
                history.append(line.strip())

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            entry = f"{timestamp} - {text}"
            
            with open(settings.LOGS_FILE_PATH, 'a') as file:
                file.write(entry + '\n')

            history.append(entry)

            return redirect('ex02:ex02_view')

    return render(request, 'form.html', {'form': form, 'history': history})
