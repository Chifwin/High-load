from django.contrib import admin
# from .models import Company, Comment, BlogSeries, Post
from .models import Post

# Register your models here.
# admin.site.register(Company)
# admin.site.register(Comment)
# admin.site.register(BlogSeries)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title',)