from django.shortcuts import render

def file_selector(request):
    return render(request, 'file_selector.html', {})


