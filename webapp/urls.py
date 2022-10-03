from django.urls import path, include, re_path
from webapp import views as v2

app_name = 'webapp'

urlpatterns = [
    path('addpost/', v2.addarticle, name='addarticle'),
    path('deletearticle/<int:id>', v2.articledelete, name='deletearticle'),
    path('like/', v2.articledetails_view, name='like-article'),
    path('search/', v2.search, name = 'search'),
    path('editpost/<int:id>/', v2.articleupdate, name="articleupdate"),
    path('', v2.articlelist_view, name='article_list'),
    path('<slug:category_slug>/<slug:slug>/', v2.articledetails_view, name='article_detail'),
    path('<slug:slug>/', v2.category_view, name='category_detail'),



]


