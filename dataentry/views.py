from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from dataentry.tasks import celery_import_data,celery_export_data
from dataentry.utils import check_csv_error,generate_csv_file

from django.core.management import call_command

# Create your views here.


def import_data(request):
    if request.method=='POST':
        model_name=request.POST.get('model_name')
        file=request.FILES.get('file_path')

        upload=Upload.objects.create(file=file,model_name=model_name)

        absolute_url=upload.file.url

        base_url=settings.BASE_DIR
        

        file_path=str(base_url)+str(absolute_url)

        # handle the csv's error

        try:
            check_csv_error(file_path,model_name)
        except Exception as e:
            messages.error(request,str(e))
            return redirect('import_data')


        # trigger celery  to import data
    
        celery_import_data.delay(file_path,model_name)
        messages.success(request,'Importing data. You will be notified once it is done.')
        
        
        return redirect('import_data')


    else:
        
        models=get_all_custom_models()


        context={
            'models':models,
        }


    return render(request,'dataentry/import_data.html',context)


def export_data(request):
    if request.method=='POST':
        model_name=request.POST.get('model_name')
    
        # trigger celery to export data
        
        celery_export_data.delay(model_name)

        messages.success(request,'Your Data is being exported.You will be notified once it is done.')
        return redirect('export_data')

        
    else:
        models=get_all_custom_models()

        context={
            'models':models,
        }

    return render(request,'dataentry/export_data.html',context)




    