from django.shortcuts import render,get_list_or_404,redirect
from django.http import *
from .models import TestPost

# Create your views here.

class createTask(request):

    #TestPostオブジェクトの作成
    post = TestPost()