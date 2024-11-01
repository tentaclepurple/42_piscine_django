# ex02/views.py
import os
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import TextInputForm
from django.conf import settings


def ex02_view(request):
    # Crear instancia del formulario
    form = TextInputForm()
    history = []

    # Verificar si el archivo de logs existe y cargar el historial
    if os.path.exists(settings.LOGS_FILE_PATH):
        with open(settings.LOGS_FILE_PATH, 'r') as file:
            for line in file:
                history.append(line.strip())

    # Procesar el formulario al enviar una entrada
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            entry = f"{timestamp} - {text}"
            
            # Guardar la entrada en el archivo de logs
            with open(settings.LOGS_FILE_PATH, 'a') as file:
                file.write(entry + '\n')

            # Agregar la entrada al historial
            history.append(entry)

            # Redirigir para evitar reenvío de formularios
            return redirect('ex02:ex02_view')

    # Renderizar la página con el formulario y el historial
    return render(request, 'form.html', {'form': form, 'history': history})
