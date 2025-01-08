import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, View, ListView
from django.views.generic.detail import DetailView
from django.core.serializers import serialize
from my_personal_blog.apps.blogs.forms import PostForm
from my_personal_blog.apps.blogs.models import Post, Category
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _

from my_personal_blog.apps.utils.general_utils import is_ajax


# Create your views here.
class BlogListView(ListView):
    model = Post
    template_name = "blog/blog/blog_list.html"
    paginate_by = 10




blog_list = BlogListView.as_view()


class BlogDetailView(DetailView):
    model = Post
    template_name = "blog/blog/blog_detail.html"


blog_detail = BlogDetailView.as_view()


class BlogAddView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/2/blog_create.html"


blog_create = BlogAddView.as_view()


@csrf_exempt
def admin_upload_image(request):
    if request.method == 'POST':
        file = request.FILES.get('file')  # Get the uploaded file
        if file:
            file_name = default_storage.save(file.name, file)  # Save the file
            file_url = default_storage.url(file_name)  # Get the file URL
            return JsonResponse({'location': file_url})  # TinyMCE expects 'location'
    return JsonResponse({'error': 'Upload failed'}, status=400)


class CategoryFilterShowView(View):
    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            category = get_object_or_404(Category, pk=self.kwargs["pk"])
            posts = Post.objects.filter(category=category.id).values(
                'id', 'title', 'slug', 'content', 'created_at', 'category__name'
            )
            posts_list = list(posts)
            return JsonResponse({'posts': posts_list}, safe=False)
        return JsonResponse({"success": False, "error": "Not an AJAX request"})


category_filter = CategoryFilterShowView.as_view()


class DataFilterShowView(View):
    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            data = json.loads(request.body)
            date_string = data.get('month')
            date_object = datetime.strptime(date_string, "%b. %d, %Y")

            posts = Post.objects.filter(created_at__year=date_object.year,
                                        created_at__month=date_object.month).values(
                'id', 'title', 'slug', 'content', 'created_at', 'category__name'
            )
            posts_list = list(posts)
            return JsonResponse({'posts': posts_list}, safe=False)
        return JsonResponse({"success": False, "error": "Not an AJAX request"})


post_data_filter = DataFilterShowView.as_view()
