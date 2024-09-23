from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.category_blog_list, name='category_blog_list'),
    path('tag/<str:slug>/', views.tag_blog_list, name='tag_blog_list'),
    path('blogdetails/<str:slug>/', views.blog_detail, name='blog_details'),
    path('ContactUs/', views.contact, name='contact-us'),
    path('AboutUs/', views.about, name='about-us'),
    path('blog/', views.blog, name='blog'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('generate_captcha/', views.generate_captcha, name='generate_captcha'),
]