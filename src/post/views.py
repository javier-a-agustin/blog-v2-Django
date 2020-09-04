from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .models import Post, Author, PostView
from .forms import CommentForm, PostForm

from django.contrib.admin.views.decorators import staff_member_required


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    query = request.GET.get('q')
    queryset = Post.objects.all()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    return render(request, 'search_post.html', {
        'queryset': queryset,
    })

def get_categories_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    context = {
        'object_list': featured,
        'latest': latest,
    }

    return render(request, 'index.html', context)

def blog(request):
    categories_count = get_categories_count()
    
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    
    
    context = {
        'post_list': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'categories_count': categories_count,
    }
    return render(request, 'blog.html', context)

def post(request, id):
    categories_count = get_categories_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    #PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': post.pk}))
    return render(request, 'post.html', {
        'post': post,
        'most_recent': most_recent,
        'categories_count': categories_count,
        'form': form,
    })


@staff_member_required
def post_create(request):
    title = "Crear articulo"
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form': form,
        'title': title,
    }
    return render(request, "post_create.html", context)

@staff_member_required
def post_update(request, id):
    title = 'Editar articulo'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None, 
        request.FILES or None,
        instance=post
    )
    
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))

    context = {
        'form': form,
        'title': title,
    }
    return render(request, "post_create.html", context)

@staff_member_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post-list'))

def profile(request):
    return redirect(reverse('blog'))

def about(request):
    return render(request, 'contact.html')