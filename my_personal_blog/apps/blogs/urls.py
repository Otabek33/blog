from django.urls import path

from my_personal_blog.apps.blogs.views import blog_list, blog_create, blog_detail, admin_upload_image

app_name = "blogs"
urlpatterns = [
    path("", view=blog_list, name="list"),
    path('add/', blog_create, name='create'),

    path('admin/upload_image/', admin_upload_image, name='admin_upload_image'),
    path('<slug:slug>/', blog_detail, name='detail'),
]
