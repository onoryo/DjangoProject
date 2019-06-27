from django.contrib import admin
from .models import Post

# Register your models here.

admin.site.register(Post)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('_meta', 'admin_og_image')
    
    def _meta(self, row):
        return ','.join([x.name for x in row.meta.all()])
