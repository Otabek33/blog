from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView
from django.views.generic.detail import DetailView

from my_personal_blog.apps.blogs.forms import PostForm
from my_personal_blog.apps.blogs.models import Post
from django.core.files.storage import default_storage


# Create your views here.
class BlogListView(TemplateView):
    template_name = "blog/2/blog_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()

        context["posts"] = posts

        return context


blog_list = BlogListView.as_view()


class BlogDetailView(DetailView):
    model = Post
    template_name = "blog/2/blog_detail.html"


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
