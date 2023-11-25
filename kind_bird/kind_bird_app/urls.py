from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('bite_like/<int:pk>', views.bite_like, name='bite_like'),
    path('bite_show/<int:pk>', views.bite_show, name='bite_show'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('delete_bite/<int:pk>', views.delete_bite, name='delete_bite'),
    path('edit_bite/<int:pk>', views.edit_bite, name='edit_bite'),
    path('search/', views.search, name='search'),
    path('search_user/', views.search_user, name='search_user'),
]