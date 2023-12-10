from django.urls import path
from .views import PostsList, PostsDetail, PostCreate, PostUpdate, PostDelete, AppointmentView, \
    AddCategoryView, CategoryList, CategoryPost, subscribe_to_category


urlpatterns = [
    path('', PostsList.as_view(), name='postlist'),
    path('<int:pk>', PostsDetail.as_view(), name='post'),
    path('news/<int:pk>', PostsDetail.as_view(), name='post'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('appointment_created/', AppointmentView.as_view(), name='appointment_created'),
    path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),
    path('category/<int:pk>/', CategoryPost.as_view(), name='category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', subscribe_to_category, name='subscribe'),

]
