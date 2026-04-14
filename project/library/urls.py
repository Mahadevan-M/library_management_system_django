from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('books/', views.all_books, name='all_books'),
    # path('recent/', views.recent_books, name='recent_books'),
    path('toggle/<int:id>/', views.toggle_borrow, name='toggle_borrow'),
    path('wishlist/<int:id>/', views.add_wishlist, name='wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
    path('profile/', views.profile, name='profile'),
    path('delete/<int:id>/', views.delete_book, name='delete_book'),
]