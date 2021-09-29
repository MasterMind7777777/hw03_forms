from django.forms import ModelForm
from .models import Group, Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
    

