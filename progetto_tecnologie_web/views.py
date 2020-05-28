from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache


@never_cache
def landingPage(request):
    return render(request, 'home.html')