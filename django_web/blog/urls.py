
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views
from .views import prace_view
from .views import item_list, item_create, item_update, item_delete

#trasy widoków stron:

urlpatterns = [
    #strona główna
    path('', PostListView.as_view(), name='DPM'),
    #about
    path('about/', views.about, name='About'),
    path('skrypty/', views.skrypty, name='skrypty'),


#TRASY WIDOKÓW DLA POSTÓW:
    
# Trasa do widoku szczegółowego posta, gdzie <int:pk> to identyfikator liczbowy posta
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Trasa do widoku tworzenia nowego posta
    path('post/new/', PostCreateView.as_view(), name='post-create'),

    # Trasa do widoku aktualizacji posta, gdzie <int:pk> to identyfikator liczbowy posta
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    # Trasa do widoku usuwania posta, gdzie <int:pk> to identyfikator liczbowy posta
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('prace/', prace_view, name='prace-it'),


    path('item/', item_list, name='item_list'),
    path('item/create/', item_create, name='item_create'),
    path('item/<int:pk>/update/', item_update, name='item_update'),
    path('item/<int:pk>/delete/', item_delete, name='item_delete'),

]