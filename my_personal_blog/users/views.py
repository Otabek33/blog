from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from my_personal_blog.apps.blogs.models import Post, Category
from my_personal_blog.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class MainBlogView(TemplateView):
    template_name = "blog/1/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        category = Category.objects.all()
        months_years = posts.dates('created_at', 'month', order='DESC')
        context["posts"] = posts
        context["the_last_post_list"] = Post.objects.all().order_by('-created_at')[:3]
        context['months_years'] = months_years
        context['category_list'] = category

        return context


main_page = MainBlogView.as_view()


class AboutMeView(TemplateView):
    template_name = "blog/1/about.html"


about_me = AboutMeView.as_view()
