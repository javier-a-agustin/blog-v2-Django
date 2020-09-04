from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from post.views import (index, blog, post, search,
    post_delete, post_update, post_create, profile, about)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='blog'),
    path('blog/', blog, name='post-list'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('create/', post_create, name='post-create'),
    path('post/<id>', post, name='post-detail'),
    path('post/<id>/update/', post_update, name='post-update'),
    path('post/<id>/delete/', post_delete, name='post-delete'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name='profile-detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

