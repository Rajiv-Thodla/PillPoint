from django.shortcuts import render
from main.models import Medicine

def home(request):
    query = request.GET.get('q', '')
    results = Medicine.objects.filter(name__icontains=query) if query else []
    return render(request, 'home/home.html', {'results': results, 'query': query})

def contact(request):
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')
