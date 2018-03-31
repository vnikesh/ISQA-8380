from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import wikipediaapi

def home(request):
   return render(request, 'worldmap/home.html',
                 {'worldmap': home})

def denverText (request):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page('Denver')
    return page_py.summary[0:60];

@login_required
def plannerGetStarted (request):
    return render(request, 'worldmap/planner.html')