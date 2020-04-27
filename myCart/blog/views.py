from django.shortcuts import render
from django.http import HttpResponse
from.models import Blogpost
# Create your views here.


def index(request):
    blogs = Blogpost.objects.all()
    params = {'blogs': blogs}
    return render(request, 'blog/index.html', params)


def postView(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    return render(request, 'blog/blogpost.html',{'post':post})