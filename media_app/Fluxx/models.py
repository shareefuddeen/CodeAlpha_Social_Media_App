from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') 
    title = models.CharField(max_length=46,null=False,default="testing title")
    content = models.TextField(blank=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Profile(models.Model):

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio =models.CharField(max_length=150,default="my bio")
    avatar = models.ImageField( upload_to='avatars/', default="avatars/default.jpg")
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.avatar.path)
            if img.height >300 and img.width > 300:
                size = (300,300)
                img.thumbnail=size
                img.save(self.avatar.path)
        except Exception as e:
            print("Error resizing image:", e)
        

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length= 60)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    

   

