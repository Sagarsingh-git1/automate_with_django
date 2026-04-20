from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings

from django.core.management import call_command
from django.contrib import messages

# Create your views here.


def import_data(request):
    if request.method=='POST':
        model_name=request.POST.get('model_name')
        file=request.FILES.get('file_path')

        upload=Upload.objects.create(file=file,model_name=model_name)

        absolute_url=upload.file.url

        base_url=settings.BASE_DIR


        file_path=str(base_url)+str(absolute_url)


        try:
            call_command('importdata',file_path,upload.model_name)
            messages.success(request,'Data Imported Successfully!')



        except Exception as e:
            messages.error(request,str(e))
        

        return redirect('import_data')


    else:

        
        models=get_all_custom_models()


        context={
            'models':models,
        }




    return render(request,'dataentry/import_data.html',context)