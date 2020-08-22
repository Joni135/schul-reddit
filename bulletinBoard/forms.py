#from .models import Post
from django import forms
from .models import Post

class PostForm(forms.Form):
    text = forms.CharField(max_length=40, widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter Post!',
            'aria-label' : 'Post',
            'aria-describedby' : 'add-btn', 
        }
    ))    

class newPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter Title!',
            'aria-label' : 'Post',
            'aria-describedby' : 'add-btn', 
        }
            ), 
            'content' : forms.TextInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter Post!',
            'aria-label' : 'Post',
            'aria-describedby' : 'add-btn', 
        }
            )
        }