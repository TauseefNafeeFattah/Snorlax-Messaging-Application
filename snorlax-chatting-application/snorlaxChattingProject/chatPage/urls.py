from django.urls import path
from chatPage import views
app_name = "chatPage"
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('chat/<int:chatID>/', views.home, name='chat'),
    path('chat/search/<str:chat_user_name>/', views.chat_from_search, name='chatSearch'), #noqa
    path('search/', views.search_result, name='search')
]
