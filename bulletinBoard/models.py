from django.db import models

# Create your models here.

class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    ...

    # Metadata
    class Meta: 
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name

class User(models.Model):
    
    last_name = models.CharField(max_length = 666, help_text = "Last name of user")
    first_name = models.CharField(max_length = 1000, help_text = "First name of user")
    ordering = ['last_name', 'first_name']

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

class Post(models.Model):

    title = models.CharField(max_length = 80, help_text = "Title of post")
    content = models.TextField(max_length = 8000, help_text = "Content of post")
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.title, self.content, self.author)
        

class Comment(models.Model):
    post = models.ForeignKey('Post' ,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80, default='title')
    email = models.EmailField(default='email@example.com')
    body = models.TextField(default=str, help_text='comment!')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)