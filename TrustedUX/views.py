from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import translation
from django.shortcuts import redirect

def index(request):
    return render(request,'index_soft.html',{})

def resource(request):
    return render(request,'index_soft_resources.html',{})


def aboutus(request):
    return render(request,'index_soft_aboutus.html',{})



def changLang(request,lang_code):
    translation.activate(lang_code)
    print('Language changed')
    return redirect('home')

def publication(request):
    return render(request,'publication.html',{})
