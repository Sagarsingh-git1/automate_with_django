from django.contrib import admin
from .models import ImageCompress

from django.utils.html import format_html

# Register your models here.
class ImageCompressAdmin(admin.ModelAdmin):
    def thumbnail(self,obj):
        return format_html('<img src="{}" height="40" width="40">',obj.compressed_img.url)
    
    def org_img_size(self,obj):
        return f'{obj.original_img.size /(1024*1024):.2f} MB'
    
    def comp_img_size(self,obj):
        compressed_size=obj.compressed_img.size /(1024*1024)
        if compressed_size >= 1:
            return f'{compressed_size:.2f} MB'
        else:
            size_in_kb=obj.compressed_img.size /1024
            return f'{size_in_kb:.2f} KB'
        
      

    list_display=['user','thumbnail','org_img_size','comp_img_size','compressed_at']






admin.site.register(ImageCompress,ImageCompressAdmin)
