from django.urls import path
from blog import views

#app_name = 'blog'


urlpatterns = [
    path('about/',views.AboutView.as_view(), name='about'), 
    
    path('post/<int:pk>/', views.PostDetailView.as_view(), name = 'post_detail'),
    path('post/create/', views.PostCreateView.as_view(),name='post_create'),
    path('post/<int:pk>/edit', views.PostUpdateView.as_view(), name='post_update'),	
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('drafts/', views.DraftListView.as_view(), name='draft_list'),	
    path('post/<int:pk>/add_comment', views.add_comment_to_post, name='add_comment'),
    path('comment/approve/<int:pk>/', views.approve_comment, name='comment_approve'), # need pk as it goes into function so we can match it to post
    path('comment/remove/<int:pk>/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'),	
]
