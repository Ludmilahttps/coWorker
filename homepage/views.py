from django.shortcuts import render
from django.utils.translation import get_language

def home(request):
    context = {
        'country': 'Brazil',
        'language': 'Portuguese',
        'LANGUAGE_CODE': get_language(),  # Adiciona a variável LANGUAGE_CODE ao contexto
    }
    return render(request, 'homepage/home.html', context)
