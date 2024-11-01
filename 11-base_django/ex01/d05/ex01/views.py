from django.shortcuts import render


def django_page(request):
    return render(request, 'django.html')


def display_process_page(request):
    return render(request, 'display.html')


def template_engine_page(request):
    return render(request, 'templates.html')
