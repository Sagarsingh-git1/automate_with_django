from django import forms
from .models import ImageCompress

class ImageCompressForm(forms.ModelForm):
    class Meta:
        model=ImageCompress
        fields=('original_img','quality')
    original_img=forms.ImageField(label='Upload an Image')
