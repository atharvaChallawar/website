from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('search', views.search, name="search"),
    path('productView', views.productView, name="productView"),
    path('checkout', views.checkout, name="checkout"),
    path('upload/', views.upload_template, name='upload_template'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("ForgotPassword/", views.ForgotPassword, name="ForgotPassword")
]