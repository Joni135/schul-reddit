from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from bulletinBoard.models import User, Post
from .forms import PostForm, newPostForm
# Create your views here.

def index(request):
    
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    post = Post.objects.all()
    
    #form = PostForm()
    newform = newPostForm()

    context = {
        'num_posts': num_posts,
        'num_users': num_users,
        'post': post, 
        'form' : newform,
        
    }

    return render(request, 'index.html', context=context)

@require_POST
def addPost(request):
    #form = PostForm(request.POST)
    newform = newPostForm(request.POST)
    
    if newform.is_valid():
        new_post = newform.save()
        
        #new_post = Post(content=form.cleaned_data['title'])
        #new_post.save()

    return redirect('index')