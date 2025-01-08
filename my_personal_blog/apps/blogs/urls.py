from django.urls import path

from my_personal_blog.apps.blogs.views import blog_list, blog_create, blog_detail, admin_upload_image, category_filter, \
    post_data_filter

app_name = "blogs"
urlpatterns = [
    path("", view=blog_list, name="list"),
    path('add/', blog_create, name='create'),
    path('<int:pk>/filter/', category_filter, name='category_filter'),
    path('date/', post_data_filter, name='month_filter'),

    path('admin/upload_image/', admin_upload_image, name='admin_upload_image'),
    path('<slug:slug>/', blog_detail, name='detail'),
]
