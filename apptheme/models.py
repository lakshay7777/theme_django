from django.conf import settings
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from ckeditor.fields import RichTextField

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive','Inactive'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def _str_(self):
        return self.name
    
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')


    def _str_(self):
        return self.name 
    

class Post(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    slug = AutoSlugField(populate_from='title')
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    feature_image = models.ImageField(upload_to='post/feature_image')
    published_date = models.DateTimeField()
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def _str_(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name="replies", on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    text = models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def _str_(self):
        return  self.text
       
# class Contact(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     subject = models.CharField(max_length=255)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     timestamp = models.DateTimeField(auto_now_add=True, editable=False)
#     utimestamp = models.DateTimeField(auto_now=True, editable=False)
#     track = models.TextField()
#     utrack = models.TextField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

#     def str(self):
#         return self.name


# from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"