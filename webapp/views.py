from email import message
from http.client import HTTPResponse
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.http.response import Http404, HttpResponse
from .models import Article, Category, Like
from .forms import CommentForm, AddArticleForm, ArticleUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages

# Create your views here.

def base_view(request):
    cat = Category.objects.all()
    context = {'cat':cat}
    return render(request, 'base_content/base.html', context)

def articlelist_view(request):
    try:
        article = Article.objects.all()
    except:
        raise Http404("Posts Does Not Exists...!")
    featured_post = Article.objects.order_by('-create')[:1]
    popular_post = Article.objects.order_by('-title')[:4]
    recent_post = Article.objects.order_by('-create')[:4]
    author_pick = Article.objects.order_by('-author')[:1]
    author_side = Article.objects.order_by('-author')[:4]
    trending1 = Article.objects.order_by('-title')[:1]
    trending2 = Article.objects.order_by('category')[:2]
    category = Category.objects.all()
    inspiration = Article.objects.order_by('-author')[:3]
    latest_posts = Article.objects.order_by('-create')[:4]

    context = {'article':article,
     'featured_post':featured_post, 
     'popular_post':popular_post, 
     'recent_post':recent_post,
     'author_pick':author_pick,
     'author_side': author_side,
     'trending1': trending1,
     'trending2': trending2,
     'cat':category,
     'inspiration':inspiration,
     'latest_posts':latest_posts
     } 
    return render(request, 'webapp/home.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug) 
    articles = category.articles.filter(status='published')
    context = {'category' : category,
    'articles' : articles
    }
    return render(request, 'webapp/category.html',context)

def articledetails_view(request, category_slug, slug):
    user = request.user
    article = get_object_or_404(Article, status='published', slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', category_slug=article.category.slug, slug=article.slug)
            #return redirect('article_detail', category=category_slug, slug=slug)
    else:
        form = CommentForm()

    if request.method == "POST":
        article_id = request.POST.get('article_id')
        article_obj = Article.objects.get(id=article_id)
        if user in article_obj.liked.all():
            article_obj.liked.remove(user)
        else:
            article_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, article_id = article_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    featured_post = Article.objects.order_by('-create')[:1]
    popular_post = Article.objects.order_by('-title')[:4]
    recent_post = Article.objects.order_by('-create')[:4]
    author_pick = Article.objects.order_by('-author')[:1]
    author_side = Article.objects.order_by('-author')[:4]
    trending1 = Article.objects.order_by('-title')[:1]
    trending2 = Article.objects.order_by('category')[:2]
    category = Category.objects.all()
    inspiration = Article.objects.order_by('-author')[:3]
    latest_posts = Article.objects.order_by('-create')[:4]
    context = {'article':article,
    'featured_post':featured_post, 
    'popular_post':popular_post, 
    'recent_post':recent_post,
    'author_pick':author_pick,
    'author_side': author_side,
    'trending1': trending1,
    'trending2': trending2,
    'cat':category,
    'inspiration':inspiration,
    'latest_posts':latest_posts,
    'form': form
    }
    return render(request, 'webapp/article_details.html', context)


#Dashboard
@login_required()
def dashboard_view(request):
    if request.user.is_authenticated:
        article = Article.objects.order_by('-create')
        pagecount = request.session.get('count', 0)
        newcount = pagecount + 1
        request.session['count'] = newcount

        fullname = request.user.get_full_name
        user = request.user
        ip = request.session.get('ip',0)
        grps = user.groups.all()
        ct = cache.get('count', version=user.pk)
        loginct = cache.get('count', version=user.pk)
        context = {'article':article,
            'pagecount' : pagecount,
            'user' : user,
            'fullname' : fullname,
            'ip' : ip,
            'ct' : ct,
            'logct' : loginct,
            'groups' : grps
        }
        return render(request, 'webapp/dashboard.html', context)
    else:
        return HttpResponseRedirect('/accounts/login/')


#Add Article
def addarticle(request):
    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Created Successfully')
            return HttpResponseRedirect('/accounts/dashboard/')
    else:
        form = AddArticleForm()
    return render(request, 'webapp/addarticle.html',{'form':form})


#Edit Article 
def articleupdate(request,id):
    if request.method == 'POST':
        arti = Article.objects.get(pk=id)
        form = ArticleUpdateForm(request.POST, request.FILES, instance=arti)
        if form.is_valid():
            form.save()
            messages.success(request, "Post Updated Successfully")
            return HttpResponseRedirect('/accounts/dashboard/')
    else:
        arti = Article.objects.get(pk=id)
        form = ArticleUpdateForm(instance=arti)
    context = {'form':form}
    return render(request, 'webapp/articleupdate.html', context)   


#Delete Article
def articledelete(request, id):
    if request.method == 'POST':
        art = Article.objects.get(pk=id)
        art.delete()
    return HttpResponseRedirect('/accounts/dashboard/')


#Search
def search(request):
    query = request.GET.get('query','')
    articles = Article.objects.filter(status='published').filter(Q(title__icontains = query) | Q(author__username__icontains = query) | Q(content__icontains = query))
    context = { 'articles' : articles,
                'query' : query
    }
    return render(request, 'webapp/search.html', context)



def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HTTPResponse("\n".join(text), content_type="text/plain")
