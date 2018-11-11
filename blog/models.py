from django.db import models
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE) # the author can only be authorised user i.e. superuser
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)	

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
		
    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})
# above after create post take me to the blog post we just created via the detail view and the id/pk of that post
		

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)	
	
    def approve(self):
        self.approved_comment = True
        self.save()
		
    def get_absolute_url(self):
        return reverse('post_list') 	
    
    def __str__(self):
        return self.text	