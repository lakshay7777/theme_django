# views.py

import random
import string
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from .models import Post, Comment, Category, Tag, Contact
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

def home(request):
    return render(request, 'home.html')

def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    category = Category.objects.all()
    tags = Tag.objects.all()
    context = {'posts': posts, 'category': category, 'tags': tags}
    return render(request, 'blog.html', context)

def about(request):
    return render(request, 'about.html')

def blog_detail(request, slug):
    post = Post.objects.filter(slug=slug).first()
    if request.method == "POST":
        parent_id = request.POST.get('commentid', None)
        comment = Comment.objects.filter(id=parent_id).first()
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        text = request.POST.get('text', None)
        if parent_id:
            parent_comment = Comment.objects.filter(id=int(parent_id)).first()
            Comment.objects.create(text=text, post=post, parent=parent_comment, name=name)
        else:
            Comment.objects.create(name=name, email=email, text=text, post=post)
        return redirect(reverse('blog_details', kwargs={'slug': post.slug}))
    else:
        comment = Comment.objects.filter(post=post, parent__isnull=True)
        category = Category.objects.all()
        tags = Tag.objects.all()
        context = {'category': category, 'tags': tags, 'post': post, 'comment': comment}
        return render(request, 'blog-details.html', context)

def home_detail(request):
    return render(request, 'home_detail.html')

def category_blog_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {'posts': posts, 'category': category}
    return render(request, 'category_post_list.html', context)

def tag_blog_list(request, slug):
    tags = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tags)
    context = {'posts': posts, 'tags': tags}
    return render(request, 'tag_post_list.html', context)

def generate_captcha(request):
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    captcha_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    cache.set(captcha_key, captcha_text, 300)  # expires in 5 minutes
    return JsonResponse({
        'captcha_key': captcha_key,
        'captcha_text': captcha_text
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        captcha_answer = request.POST.get('captcha-answer')
        captcha_key = request.POST.get('captcha-key')
        
        # Verify CAPTCHA
        stored_captcha = cache.get(captcha_key)
        if not stored_captcha or stored_captcha.lower() != captcha_answer.lower():
            return JsonResponse({'success': False, 'error': 'Invalid CAPTCHA'})
        
        if name and email and subject and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
    
    return render(request, 'contact.html')
