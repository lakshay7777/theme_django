from django.shortcuts import render,get_object_or_404 
from .models import Post, Comment,Category,Tag,Contact
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect

from django.shortcuts import render
from django.http import JsonResponse
from .models import Contact


def home(request):
    return render(request, 'home.html')

def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    category = Category.objects.all()
    tags = Tag.objects.all()
    context = {'posts': posts,'category':category,'tags':tags}
    return render(request, 'blog.html', context)    

def about(request):
    return render(request,'about.html')

def blog_detail(request,slug):
    post = Post.objects.filter(slug=slug).first()
    if request.method == "POST":
        parent_id = request.POST.get('commentid',None)
        # parent = request.POST.get('comment',None)
        comment = Comment.objects.filter(id=parent_id).first()
        name = request.POST.get('name', None)
       
        email = request.POST.get('email', None)
       
        text = request.POST.get('text', None)
      
        if parent_id:
            parent_comment = Comment.objects.filter(id=int(parent_id)).first()
            Comment.objects.create(text=text,post=post,parent=parent_comment,name=name)
        else:
            Comment.objects.create(name=name,email=email,text=text,post=post)
        return redirect(reverse('blog-details.html', kwargs={'slug': post.slug}))    
    else:
        comment = Comment.objects.filter(post=post,parent__isnull=True)
        
        category = Category.objects.all()
        tags = Tag.objects.all()
        context =  {'category':category,'tags':tags,'post':post,'comment':comment}
        return render(request, 'blog-details.html',context)

def home_detail(request):
    return render(request,'home_detail.html')

def category_blog_list(request,slug):
    category = get_object_or_404(Category,slug=slug)
    posts = Post.objects.filter(category=category)
    context = {'posts':posts,'category':category}
    return render(request,'category_post_list.html',context)

def tag_blog_list(request,slug):
    tags = get_object_or_404(Tag,slug=slug)
    posts = Post.objects.filter(tags=tags)
    context = {'posts':posts,'tags':tags}
    return render(request,'tag_post_list.html',context)


# def contact(request):
    # error_message = None
    # if request.method == 'POST':
    #     name = request.POST.get('name',None)
     
    #     email = request.POST.get('email',None)
      
    #     phone = request.POST.get('phone',None)
       
    #     subject = request.POST.get('subject',None)
     
    #     message = request.POST.get('message',None)
    
    #     if name and email and subject and message:
      
    #         Contact.objects.create(name=name, email=email,phone=phone,subject=subject, message=message)
    #         return render(request, 'contact.html', {'success': True})
    #     else:
    #         error_message = "Please fill all the required fields."
    # return render(request, 'contact.html', {'error_message':error_message})  




from django.shortcuts import render
from django.http import JsonResponse
from .models import Contact

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    
    return render(request, 'contact.html')
