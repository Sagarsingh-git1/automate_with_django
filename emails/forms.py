from .models import Email
from django.forms import ModelForm

class EmailForm(ModelForm):
    class Meta:
        model=Email
        fields=('__all__')
        

