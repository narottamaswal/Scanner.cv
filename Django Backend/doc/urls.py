from django.contrib import admin
from django.urls import path
from django.urls import path, include
from . import views
urlpatterns = [
    path('posts/', views.PostView.as_view(),name='postapi'),
        path('pdf/', views.PDFView.as_view(),name='pdfapi'),

]