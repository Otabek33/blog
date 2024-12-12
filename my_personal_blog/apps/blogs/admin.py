from django import forms
from django.contrib import admin
from .models import Post, Category, Tag
from django.db import models
from tinymce.widgets import TinyMCE


# Registering the Post model in the Django admin with custom settings
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Automatically generate a slug from the title
    prepopulated_fields = {"slug": ("title",)}

    # Define the columns that will be displayed in the post list view
    list_display = ("title", "category", "created_at")

    # Allow searching by title and content
    search_fields = ("title", "content")

    # Filter posts by category, tags, and creation date
    list_filter = ("category", "tags", "created_at")

    # Override the default widget for text fields to use TinyMCE
    formfield_overrides = {
        models.TextField: {
            'widget': TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={
                    'plugins': 'image',  # Enable image plugins
                    'toolbar': 'undo redo | bold italic | image',  # Basic toolbar options
                    'images_upload_url': '/admin/upload_image/',  # URL for handling image uploads
                    'automatic_uploads': True,  # Enable automatic uploads
                    'paste_data_images': True,  # Allow drag and drop for image pasting
                    'setup': '''
                        function(editor) {
                            editor.on('BeforeUpload', function(e) {
                                // Attach CSRF token to the image upload request
                                var xhr = e.xhr();
                                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                            });
                        }
                    '''
                }
            )
        },
    }


# Register other models
admin.site.register(Category)
admin.site.register(Tag)
