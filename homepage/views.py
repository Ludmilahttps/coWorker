from django.shortcuts import render

def home(request):
    country = "Brazil"
    language = "Portuguese"
    
    context = {
        'country': country,
        'language': language,
    }
    
    return render(request, "homepage/home.html", context)
