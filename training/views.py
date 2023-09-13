from django.shortcuts import render


def home(request):
    return render(request, 'training/pages/home.html')
