from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    parent = TreeForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,related_name='children')

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return "{} - {}".format(self.user, self.post)



