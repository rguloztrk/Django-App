"""firstBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
#from article.views import (anasayfa, post_list, post_detail, create_post, createPostMF)
from article.views import anasayfa


urlpatterns = [   #liste; djangonun arayacagi url'lerin yollarini tutuyor
    path('admin/', admin.site.urls),
#    path('article/', include('article.url')), #article/ uzantisi gelince 'article.url' sayfaya bak diyoruz
    path('', anasayfa, name='anasayfa'),
    path('posts/', include('article.urls')),
    #path('post/<int:post_id>/',post_detail, name='post_detail'),
    #path('posts/', post_list,name='post_list'),
    #path('post/create/', createPostMF, name='create_post')
    
]

#django projesinde verilen portu parse edip 7000 portu dolu ise 7001 portundan porjeyi ayaga kaldiran scripti yazma