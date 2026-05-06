from django.shortcuts import render,redirect
from .forms import ImageCompressForm
from .models import ImageCompress
from PIL import Image
import io
from django.http import HttpResponse
from django.core.files.base import ContentFile

# Create your views here.
def compress(request):
    if request.method == 'POST':
        form=ImageCompressForm(request.POST,request.FILES)

        if form.is_valid():
            original_img=form.cleaned_data['original_img']
            quality=form.cleaned_data['quality']

            compressed_image=form.save(commit=False)

            compressed_image.user=request.user

            img=Image.open(original_img)
            buffer=io.BytesIO()
        
            output_format=img.format
            img.save(buffer, format=output_format,quality=quality)
       
            buffer.seek(0)
            

            compressed_image.compressed_img.save(
                f'compressed_img_{original_img.name}',ContentFile(buffer.getvalue()),save=False)
            compressed_image.save()
            
            response=HttpResponse(buffer.getvalue(),content_type='image/{output_format.lower()}')
            response['Content-Disposition']=f'attachment;filename=compressed_img_{original_img.name}'
            return response

    else:
        form=ImageCompressForm()
        context={'form':form}
        return render(request, 'image_compression/compress.html',context)