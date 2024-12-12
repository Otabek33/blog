from django.urls import path

from .views import main_page, about_me
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("", view=main_page, name="main_blog"),
    path("~me/", view=about_me, name="about"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
